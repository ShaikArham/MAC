/* MAC enterprise-mode UI: generated aggregates, bounded labeled samples, no external calls. */
const enterpriseMoney=n=>new Intl.NumberFormat('en-IE',{style:'currency',currency:'EUR',minimumFractionDigits:2,maximumFractionDigits:2}).format(n/100);
const enterpriseNumber=n=>new Intl.NumberFormat('en-IE').format(n);
function validateEnterprise(s){
 if(!s||s.schema_version!==2||s.synthetic!==true||s.mode!=='enterprise_aggregate'||!s.summary||!s.finance||!s.operations||!s.samples||!Array.isArray(s.monthly)||s.monthly.length!==12||!Array.isArray(s.quality))throw Error('Unsupported enterprise snapshot');
 const m=s.summary;if(!Number.isSafeInteger(m.order_value_cents)||!Number.isSafeInteger(m.accepted_rows)||!Number.isSafeInteger(m.rejected_rows)||!Number.isSafeInteger(s.finance.outstanding_cents)||!Number.isSafeInteger(s.operations.fulfilled)||!Number.isSafeInteger(s.operations.pending)||!Array.isArray(s.operations.warehouse_stats))throw Error('Invalid enterprise figures');
 if(s.monthly.reduce((n,x)=>n+x.orders,0)!==m.entity_counts.orders||s.monthly.reduce((n,x)=>n+x.order_value_cents,0)!==m.order_value_cents||s.finance.invoiced_cents-s.finance.paid_cents!==s.finance.outstanding_cents)throw Error('Unreconciled enterprise snapshot');
 return true;
}
function enterpriseViews(s){
 validateEnterprise(s);const v=s.samples,m=s.summary,f=s.finance,o=s.operations;
 const w=(columns,rows,metrics,total=rows.length)=>({columns,rows:rows.map(x=>x.map(String)),metrics:metrics.map(x=>x.map(String)),total});
 const summaryCount=k=>m.entity_counts[k];
 const sources=Object.entries(m.entity_counts).map(([k,n])=>[k,'Synthetic CSV',n,'Validated locally']);
 const warehouse=o.warehouse_stats.map(x=>[x.warehouse,enterpriseNumber(x.expected_units),enterpriseNumber(x.observed_units),x.variance_units,x.exceptions]);
 return {
  'Business overview':w(['Measure','Synthetic historical result'],[['Business','Horizon Supplies'],['Reporting period','Jan–Dec 2025'],['Warehouses',3],['Orders',summaryCount('orders')],['Order value',enterpriseMoney(m.order_value_cents)]],[['Customers',summaryCount('customers')],['Products',summaryCount('products')],['Suppliers',summaryCount('suppliers')]]),
  'Process mapping':w(['Stage','Input','Output'],[['Sales','Trade orders','Validated order lines'],['Warehouse','Stock movements','Inventory variance checks'],['Dispatch','Fulfilled orders','Delivery records'],['Finance','Invoices and payments','Outstanding balances']],[['Process stages',4]]),
  'System mapping':w(['System representation','Mode'],[['Sales','Synthetic CSV'],['Warehouse','Synthetic CSV'],['Finance','Synthetic CSV'],['Customers','Synthetic CSV']],[['Live integrations',0]]),
  'Sales orders':w(['Order','Date','Customer','Amount','Status'],v.orders.map(x=>[x.order_id,x.order_date,x.customer_id,enterpriseMoney(x.amount_cents),x.status]),[['Total orders',summaryCount('orders')],['Order value',enterpriseMoney(m.order_value_cents)],['Fulfilled',o.fulfilled]],summaryCount('orders')),
  'Inventory':w(['Warehouse','Expected units','Observed units','Variance','Exceptions'],warehouse,[['Warehouses',warehouse.length],['Stock discrepancies',o.stock_exception_count]]),
  'Finance':w(['Invoice','Order','Amount','Balance'],v.invoices.map(x=>[x.invoice_id,x.order_id,enterpriseMoney(x.amount_cents),enterpriseMoney(x.balance_cents)]),[['Invoiced',enterpriseMoney(f.invoiced_cents)],['Paid',enterpriseMoney(f.paid_cents)],['Outstanding',enterpriseMoney(f.outstanding_cents)]],summaryCount('invoices')),
  'Customers':w(['Customer','Name'],v.customers.map(x=>[x.customer_id,x.name]),[['Total customers',summaryCount('customers')]],summaryCount('customers')),
  'Suppliers':w(['Supplier','Name'],v.suppliers.map(x=>[x.supplier_id,x.name]),[['Total suppliers',summaryCount('suppliers')]],summaryCount('suppliers')),
  'Exceptions':w(['Code','Product','Warehouse','Variance'],v.exceptions.map(x=>[x.code,x.product_id,x.warehouse_id,x.delta]),[['Total stock discrepancies',o.stock_exception_count],['Rejected records',m.rejected_rows]],o.stock_exception_count),
  'Connected systems':w(['Source entity','Mode','Accepted records','Status'],sources,[['Synthetic source files',sources.length],['Live integrations',0]]),
  'ETL pipelines':w(['Stage','Evidence'],[['CSV ingestion',m.source_rows+' source records'],['Validation',m.accepted_rows+' accepted / '+m.rejected_rows+' rejected'],['Relational SQLite','Foreign key validation'],['Aggregation','12 verified monthly periods']],[['Accepted',m.accepted_rows],['Rejected',m.rejected_rows]]),
  'Data quality':w(['Entity','Source','Accepted','Rejected'],s.quality.map(x=>[x.entity,x.source,x.accepted,x.source-x.accepted]),[['Accepted',m.accepted_rows],['Rejected',m.rejected_rows],['Acceptance rate',(100*m.accepted_rows/m.source_rows).toFixed(3)+'%']]),
  'Reconciliation':w(['Control','Result'],[['Order line totals','Matched'],['Invoices vs orders','Matched'],['Payments outstanding',enterpriseMoney(f.outstanding_cents)],['Stock exceptions',o.stock_exception_count]],[['Outstanding',enterpriseMoney(f.outstanding_cents)],['Stock exceptions',o.stock_exception_count]]),
  'Audit logs':w(['Evidence','Status'],[['Local generated validation batch','Accepted with quarantined rows'],['Historical dataset','2025 snapshot'],['Continuous execution monitoring','Not enabled']],[['Rejected rows',m.rejected_rows]]),
  'Business insights':w(['Insight','Historical figure'],[['Unpaid invoice balance',enterpriseMoney(f.outstanding_cents)],['Pending orders',o.pending],['Warehouse discrepancies',o.stock_exception_count],['Rejected source rows',m.rejected_rows]],[['Order value',enterpriseMoney(m.order_value_cents)],['Fulfilled',o.fulfilled]]),
  'Reports':w(['Period','Orders','Order value','Fulfilled'],s.monthly.map(x=>[x.month,x.orders,enterpriseMoney(x.order_value_cents),x.fulfilled]),[['Months',12],['Orders',summaryCount('orders')],['Order value',enterpriseMoney(m.order_value_cents)]])
 };
}
function renderEnterpriseOverview(s){
 validateEnterprise(s);const root=document.querySelector('#view');root.replaceChildren();
 const el=(tag,txt,cls)=>{const a=document.createElement(tag);if(txt!==undefined)a.textContent=txt;if(cls)a.className=cls;return a};
 const panel=(name,where)=>{const p=el('article');p.append(el('h3',name));where.append(p);return p};
 const bar=(where,label,count,max,value)=>{const line=el('div',undefined,'chart-label');line.append(el('span',label),el('strong',value));where.append(line);const track=el('div',undefined,'bar'),fill=el('span');fill.style.width=(max?Math.min(100,count/max*100):0)+'%';track.append(fill);where.append(track)};
 const m=s.summary,o=s.operations,f=s.finance;const cards=el('div',undefined,'cards');root.append(cards);
 for(const [label,value] of [['Annual order value',enterpriseMoney(m.order_value_cents)],['Sales orders',enterpriseNumber(m.entity_counts.orders)],['Customers',enterpriseNumber(m.entity_counts.customers)],['Products',enterpriseNumber(m.entity_counts.products)]]){const card=el('article');card.append(el('small',label),el('div',value,'metric'),el('small','Synthetic 2025 · validated'));cards.append(card)}
 const split=el('div',undefined,'split');root.append(split);const month=panel('2025 monthly order value',split);const max=Math.max(...s.monthly.map(x=>x.order_value_cents));for(const x of s.monthly)bar(month,x.month,x.order_value_cents,max,enterpriseMoney(x.order_value_cents));
 const status=panel('Order fulfilment',split);const donut=el('div',undefined,'donut');donut.style.background='conic-gradient(#2dd4bf '+(100*o.fulfilled/m.entity_counts.orders)+'%,#4389e8 0)';donut.append(el('span',enterpriseNumber(m.entity_counts.orders)+' orders'));status.append(donut);status.append(el('p','Fulfilled · '+enterpriseNumber(o.fulfilled)),el('p','Pending · '+enterpriseNumber(o.pending)));
 const pipeline=panel('Validated data pipeline',root),stages=el('div',undefined,'pipeline');pipeline.append(stages);for(const [title,number] of [['Source CSV',enterpriseNumber(m.source_rows)],['Validate',enterpriseNumber(m.accepted_rows)],['Quarantine',enterpriseNumber(m.rejected_rows)],['SQLite',enterpriseNumber(m.accepted_rows)]]){const stage=el('div',undefined,'stage');stage.append(el('strong',title),el('small',number+' rows'));stages.append(stage)}pipeline.append(el('p','Local validated batch · not continuous monitoring','muted'));
 const bottom=el('div',undefined,'split');root.append(bottom);const warehouse=panel('Warehouse reconciliation',bottom);for(const x of o.warehouse_stats)bar(warehouse,x.warehouse,x.observed_units,x.expected_units,enterpriseNumber(x.observed_units)+' / '+enterpriseNumber(x.expected_units));warehouse.append(el('p',enterpriseNumber(o.stock_exception_count)+' product-location stock exceptions','warning'));
 const financial=panel('Financial intelligence',bottom);financial.append(el('p','Invoiced: '+enterpriseMoney(f.invoiced_cents)),el('p','Paid: '+enterpriseMoney(f.paid_cents)),el('p','Outstanding: '+enterpriseMoney(f.outstanding_cents),'warning'));
 const detail=el('button','Review finance');detail.onclick=()=>show('Finance');financial.append(detail);
 const insights=document.querySelector('#insights');insights.replaceChildren();insights.append(el('h3','Business insights'),el('p',enterpriseMoney(f.outstanding_cents)+' outstanding invoices'),el('p',enterpriseNumber(o.pending)+' pending orders'),el('p',enterpriseNumber(o.stock_exception_count)+' stock discrepancies'));for(const name of ['Finance','Inventory','Reports']){const b=el('button','Review '+name);b.onclick=()=>show(name);insights.append(b)}
}
function answerEnterprise(s,q){
 try{validateEnterprise(s)}catch{return {answer:'Enterprise snapshot unavailable or invalid.',evidence:[],action:'Review the generated snapshot.'}};
 const m=s.summary,f=s.finance,o=s.operations,p=String(q||'').toLowerCase();const out=(answer,evidence,action)=>({answer,evidence,action});
 if(/\b(send|delete|update|execute|transfer|pay|approve|modify|ignore|password|secret)\b/.test(p))return out('MAC is read-only and cannot perform actions or disclose secrets.',[],'Review records manually.');
 if(/invoice|finance|outstanding|payment/.test(p))return out('Outstanding invoices: '+enterpriseMoney(f.outstanding_cents)+'.',[enterpriseNumber(m.entity_counts.invoices)+' validated invoices',enterpriseNumber(m.entity_counts.payments)+' payment records'],'Review overdue balances in the finance workspace; no collections have been initiated.');
 if(/stock|inventory|warehouse/.test(p))return out(enterpriseNumber(o.stock_exception_count)+' recorded stock discrepancies.',o.warehouse_stats.map(x=>x.warehouse+': '+x.variance_units+' units variance'),'Recount flagged product-location pairs.');
 if(/quality|reject|invalid/.test(p))return out(enterpriseNumber(m.accepted_rows)+' accepted; '+m.rejected_rows+' rejected.',s.quality.filter(x=>x.source>x.accepted).map(x=>x.entity+': '+(x.source-x.accepted)+' rejected'),'Review quarantined source rows before a new batch.');
 if(/pipeline|batch|audit|source|connector/.test(p))return out('The historical synthetic CSV batch was validated and loaded into SQLite.',[m.source_rows+' source records','2025-01 through 2025-12'],'This is not live monitoring or a production connector.');
 if(/exception|risk/.test(p))return out(o.stock_exception_count+' stock exceptions and '+m.rejected_rows+' rejected source records.',o.warehouse_stats.map(x=>x.warehouse+': '+x.exceptions+' exceptions'),'Review stock counts and source validation.');
 if(/order|sales|overview|summary|month|revenue/.test(p))return out('Recorded order value: '+enterpriseMoney(m.order_value_cents)+'. This is not recognized revenue.',[enterpriseNumber(m.entity_counts.orders)+' orders','2025 synthetic period'],'Review monthly reports for seasonal variation.');
 return out('I cannot answer that from the synthetic enterprise snapshot.',[],'Ask about orders, invoices, stock, quality, sources or pipelines.');
}
if(typeof module!=='undefined')module.exports={enterpriseViews,validateEnterprise,answerEnterprise};
