/* Snapshot-driven dashboard enhancement */
function renderOverview(s){
 const root=document.querySelector("#view"),r=s.records,m=s.summary,z=s.monitoring,q=s.reconciliation;
 const el=(tag,txt,cls)=>{const n=document.createElement(tag);if(txt!==undefined)n.textContent=txt;if(cls)n.className=cls;return n};
 const panel=(title,parent)=>{const n=el("article");n.append(el("h3",title));parent.append(n);return n};
 const money=n=>new Intl.NumberFormat("en-IE",{style:"currency",currency:"EUR"}).format(n/100);
 const bar=(parent,label,n,total,value)=>{const line=el("div",undefined,"chart-label");line.append(el("span",label),el("strong",value));parent.append(line);const track=el("div",undefined,"bar");const fill=el("span");fill.style.width=(total?Math.max(0,Math.min(100,n/total*100)):0)+"%";track.append(fill);parent.append(track)};
 root.replaceChildren();
 const cards=el("div",undefined,"cards");root.append(cards);
 for(const [label,value] of [["Order value",money(m.order_value_cents)],["Orders",r.orders.length],["Products",r.products.length],["Customers",r.customers.length]]){const a=el("article");a.append(el("small",label),el("div",value,"metric"),el("small","Validated snapshot"));cards.append(a)}
 const split=el("div",undefined,"split");root.append(split);
 const sales=panel("Order value by order",split),max=Math.max(0,...r.orders.map(x=>x.amount_cents));for(const x of r.orders)bar(sales,x.order_id,x.amount_cents,max,money(x.amount_cents));
 const status=panel("Order status",split),counts={};for(const x of r.orders)counts[x.status]=(counts[x.status]||0)+1;
 const donut=el("div",undefined,"donut");const fulfilled=counts.fulfilled||0;donut.style.background="conic-gradient(#2dd4bf "+(r.orders.length?fulfilled/r.orders.length*100:0)+"%, #4389e8 0)";donut.append(el("span",r.orders.length+" orders"));status.append(donut);for(const [k,v] of Object.entries(counts))status.append(el("p",k+" · "+v));
 const pipe=panel("Data pipeline health",root),steps=el("div",undefined,"pipeline");pipe.append(steps);for(const [label,value] of [["Ingest",z.sources.length+" sources"],["Bronze",z.counts.bronze+" records"],["Validate",z.counts.quarantine+" rejected"],["Silver",z.counts.silver+" records"]]){const n=el("div",undefined,"stage");n.append(el("strong",label),el("small",value));steps.append(n)}
 pipe.append(el("p","Latest recorded batch: "+(z.batches.at(-1)?.status||"Unavailable"),"muted"));
 const bottom=el("div",undefined,"split");root.append(bottom);const quality=panel("Data quality by entity",bottom);for(const x of z.sources){const accepted=m.entity_counts[x.id]||0;bar(quality,x.id,accepted,x.rows,accepted+" / "+x.rows)}
 const ex=panel("Business exceptions",bottom);for(const x of q.exceptions)ex.append(el("p",x.code+" · "+String(x.key)+" · "+x.delta,"warning"));ex.append(el("p","Outstanding invoices: "+money(q.outstanding_cents)));const b=el("button","Review exceptions");b.onclick=()=>show("Exceptions");ex.append(b);
 const insights=document.querySelector("#insights");insights.replaceChildren();insights.append(el("h3","Insights"),el("p",money(q.outstanding_cents)+" outstanding invoices"),el("p",m.rejected+" rejected records"),el("p",q.exceptions.length+" business exceptions"));for(const name of ["Finance","Data quality","Exceptions"]){const b=el("button","Review "+name);b.onclick=()=>show(name);insights.append(b)}
}
