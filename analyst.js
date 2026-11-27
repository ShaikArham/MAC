/* Deterministic analyst; no model, credentials or external calls. */
let analystContext={};

/* Explicit historical date parsing; no inference of live dates. */
function macOrderDates(q,context){
 const names='january february march april may june july august september october november december'.split(' ');
 const dates=[];let invalid=false;
 const add=(y,m,d)=>{const v=String(y)+'-'+String(m).padStart(2,'0')+'-'+String(d).padStart(2,'0');const t=new Date(v+'T00:00:00Z');if(y!==2025||!Number.isFinite(+t)||t.toISOString().slice(0,10)!==v)invalid=true;else dates.push(v)};
 const pattern=/\b(\d{4})-(\d{2})-(\d{2})\b|\b(\d{1,2})(?:st|nd|rd|th)?\s+(january|february|march|april|may|june|july|august|september|october|november|december)(?:\s+(\d{4}))?\b/g;
 for(const m of q.matchAll(pattern)){if(m[1])add(+m[1],+m[2],+m[3]);else add(+(m[6]||2025),names.indexOf(m[5])+1,+m[4])}
 const short=q.match(/\b(?:between|from)\s+(\d{1,2})\s+(?:and|to|-)\s+(\d{1,2})\s+(january|february|march|april|may|june|july|august|september|october|november|december)(?:\s+(\d{4}))?\b/);
 if(short){dates.length=0;add(+(short[4]||2025),names.indexOf(short[3])+1,+short[1]);add(+(short[4]||2025),names.indexOf(short[3])+1,+short[2])}
 if(invalid||dates.length>2||dates.length===2&&dates[0]>dates[1])return {error:'Use a valid date or ascending date range within historical 2025 data.'};
 if(dates.length)return {start:dates[0],end:dates[1]||dates[0]};
 if(/\b(today|yesterday|tomorrow|these days|this week)\b/.test(q))return {error:'MAC contains historical 2025 data only. Please specify a date or range in 2025.'};
 if(/\b(next day|previous day)\b/.test(q)&&context.start===context.end&&context.start){const t=new Date(context.start+'T00:00:00Z');t.setUTCDate(t.getUTCDate()+(/previous day/.test(q)?-1:1));const v=t.toISOString().slice(0,10);return v.startsWith('2025-')?{start:v,end:v}:{error:'That date is outside historical 2025 data.'}}
 return null;
}

async function macAnalyst(s,question){
 const q=String(question).trim().toLowerCase(),out=(answer,evidence=[],target='',id='',month='all',status='')=>({answer,evidence,links:target?[{label:'Open '+target+(id?' · '+id:''),target,id,month,status}]:[]});
 if(!s||s.schema_version!==2)return out('Validated snapshot is not ready.');
 if(/\b(send|delete|update|execute|transfer|approve|modify|password|secret)\b/.test(q))return out('MAC is read-only. No external actions or credentials are available.');
 const months=s.monthly.map(x=>x.month),names=['january','february','march','april','may','june','july','august','september','october','november','december'];
 const explicit=months.find((m,i)=>q.includes(m)||new RegExp('\\b'+names[i]+'\\b').test(q));
 const follow=/^(and |what about|how many|how much|what is|show me)/.test(q);
 const id=(q.match(/\b(?:c\d{4}|s\d{3}|p\d{4}|o\d{5,}|inv\d+)\b/i)||[])[0]?.toUpperCase()||(follow?analystContext.id:'');
 const month=explicit||(/annual|all year|full year/.test(q)?'all':follow&&analystContext.month?analystContext.month:macState.month);
 const period=month==='all'?months:[month],label=month==='all'?'2025':month;
 const sum=(rows,k)=>rows.reduce((n,x)=>n+x[k],0),money=macMoney;

 const dateScope=macOrderDates(q,analystContext);
 const orderIntent=/\b(orders?|pending|fulfilled|sales|order value|customers?)\b/.test(q);
 const dateFollow=analystContext.topic==='datedOrders'&&/^(and |what about|how many|how much|what is|show me|which|list)/.test(q)&&!explicit&&!/annual|all year|full year|invoice|payment|stock|supplier|product|finance/.test(q)&&!id;
 const scope=dateScope||(dateFollow?{start:analystContext.start,end:analystContext.end}:null);
 if(scope&&(orderIntent||dateFollow||dateScope?.error)&&!id&&!/invoice|payment|finance|stock|supplier|product/.test(q)){
  if(scope.error)return out(scope.error);
  const selected=months.filter(m=>m>=scope.start.slice(0,7)&&m<=scope.end.slice(0,7));
  const rows=(await macOrders(selected)).filter(x=>x.order_date>=scope.start&&x.order_date<=scope.end);
  const status=/\bpending\b/.test(q)?'pending':/\bfulfilled\b/.test(q)?'fulfilled':/next day|previous day/.test(q)?analystContext.status||'':'';
  const matching=status?rows.filter(x=>x.status===status):rows;
  const pending=rows.filter(x=>x.status==='pending').length;
  const title=scope.start===scope.end?scope.start:scope.start+' to '+scope.end;
  analystContext={topic:'datedOrders',start:scope.start,end:scope.end,month:selected.length===1?selected[0]:'all',status};
  const examples=matching.slice(0,5);
  const result=out(title+': '+matching.length+' '+(status?status+' ':'')+'orders worth '+money(sum(matching,'amount_cents'))+'. All orders in period: '+rows.length+'; '+pending+' pending, '+(rows.length-pending)+' fulfilled.',['Integrity-checked order partitions; inclusive order dates; historical status, not status as of that date.',...examples.map(x=>x.order_id+' · '+x.customer_id+' · '+x.status+' · '+money(x.amount_cents))]);
  result.links=examples.map(x=>({label:'Open Sales orders · '+x.order_id,target:'Sales orders',id:x.order_id,month:x.order_date.slice(0,7),status:x.status}));
  return result;
 }

 if(id&&/^C/.test(id)){const c=(await macDetail('customers')).find(x=>x.customer_id===id);if(!c)return out('No matching customer '+id);const rows=(await macOrders(period)).filter(x=>x.customer_id===id);analystContext={id,month,topic:'customer'};return out(c.name+' · '+label+': '+rows.length+' orders worth '+money(sum(rows,'amount_cents'))+'. '+rows.filter(x=>x.status==='pending').length+' pending.',['Customer '+id,'Validated order partitions; order value, not recognized revenue.'],'Customers',id)}
 if(id&&/^S/.test(id)){const c=(await macDetail('suppliers')).find(x=>x.supplier_id===id);if(!c)return out('No matching supplier '+id);const rows=(await macDetail('purchase_orders')).filter(x=>x.supplier_id===id);analystContext={id,month:'all',topic:'supplier'};return out(c.name+': '+rows.length+' historical purchase orders.',['Supplier '+id,...Object.entries(rows.reduce((a,x)=>(a[x.status]=(a[x.status]||0)+1,a),{})).map(([k,v])=>k+': '+v)],'Suppliers',id)}
 if(id&&/^P/.test(id)){const p=(await macDetail('products')).find(x=>x.product_id===id);if(!p)return out('No matching product '+id);const rows=(await macDetail('stock_counts')).filter(x=>x.product_id===id);analystContext={id,month:'all',topic:'product'};return out(p.name+' · '+money(p.price_cents)+' per '+p.unit+'. Counted stock '+sum(rows,'observed')+' units.',['Product '+id,...rows.map(x=>x.warehouse+': variance '+x.delta)],'Products',id)}
 if(id&&/^O/.test(id)){const row=(await macOrders(months)).find(x=>x.order_id===id);if(!row)return out('No matching order '+id);analystContext={id,month:row.order_date.slice(0,7),topic:'order'};return out(id+' · '+row.order_date+' · '+money(row.amount_cents)+' · '+row.status,['Customer '+row.customer_id,'Validated order record'],'Sales orders',id,row.order_date.slice(0,7))}
 if(/invoice|finance|outstanding|payment|collected/.test(q)){const f=s.finance;analystContext={month:'all',topic:'finance'};return out('2025 invoiced '+money(f.invoiced_cents)+', collected '+money(f.paid_cents)+', outstanding '+money(f.outstanding_cents)+'. Collection rate '+(100*f.paid_cents/f.invoiced_cents).toFixed(2)+'%.',['Validated annual invoice and payment aggregates; not a monthly figure.'],'Finance')}
 if(/stock|inventory|warehouse|discrepanc/.test(q)){const rows=await macDetail('stock_counts');const bad=rows.filter(x=>x.delta!==0);analystContext={month:'all',topic:'stock'};return out(bad.length+' stock discrepancies across '+rows.length+' product-warehouse counts.',['Net variance '+sum(rows,'delta')+' units',...s.operations.warehouse_stats.map(x=>JSON.stringify(x))],'Exceptions')}
 if(/sales|order|revenue|best month|top customer/.test(q)||explicit||follow&&analystContext.topic==='sales'){const rows=s.monthly.filter(x=>period.includes(x.month));analystContext={month,topic:'sales'};if(/top customer/.test(q)){const orders=await macOrders(period),totals=new Map();for(const o of orders)totals.set(o.customer_id,(totals.get(o.customer_id)||0)+o.amount_cents);const best=[...totals].sort((a,b)=>b[1]-a[1])[0],c=(await macDetail('customers')).find(x=>x.customer_id===best[0]);return out('Top customer by order value in '+label+': '+c.name+' · '+money(best[1]),['Grouped validated orders by customer ID'],'Customers',best[0])}if(/best month/.test(q)){const b=[...s.monthly].sort((a,b)=>b.order_value_cents-a.order_value_cents)[0];return out('Highest order value month: '+b.month+' · '+money(b.order_value_cents),['Compared all 12 months of 2025'],'Reports','',b.month)}const n=sum(rows,'orders'),f=sum(rows,'fulfilled');return out((month==='all'?'2025':'Selected period '+label)+': '+money(sum(rows,'order_value_cents'))+' order value across '+n+' orders. '+f+' fulfilled, '+(n-f)+' pending. Average order '+money(n?Math.round(sum(rows,'order_value_cents')/n):0)+'.',['Validated monthly aggregates; not recognized revenue.'],'Sales orders','',month,/pending/.test(q)?'pending':'')}
 analystContext={};const result=answerMAC(s,q);return {...result,links:[{label:'Open '+(/quality|reject/.test(q)?'Data quality':/pipeline/.test(q)?'ETL pipelines':'Connected systems'),target:/quality|reject/.test(q)?'Data quality':/pipeline/.test(q)?'ETL pipelines':'Connected systems'}]};
}
