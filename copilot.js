/* Read-only snapshot assistant; no model or network calls. */
function answerMAC(s,question){
 const unavailable={answer:"Snapshot unavailable or unsupported.",evidence:[],action:"Load a valid synthetic snapshot."};
 if(!s||s.schema_version!==1||s.synthetic!==true||!s.monitoring||!s.reconciliation||!s.summary)return unavailable;
 const q=String(question).trim().toLowerCase(),m=s.summary,z=s.monitoring,f=s.reconciliation;
 if(![f.invoices,f.stock,f.exceptions,z.rejections,z.batches,z.sources].every(Array.isArray)||![f.outstanding_cents,f.overpaid_cents,m.accepted,m.rejected,m.order_value_cents].every(Number.isSafeInteger)||!m.entity_counts)return unavailable;
 const euro=n=>new Intl.NumberFormat("en-IE",{style:"currency",currency:"EUR"}).format(n/100);
 const out=(answer,evidence,action)=>({answer,evidence,action});
 if(/\b(send|delete|update|execute|transfer|pay|approve|modify|ignore|password|secret)\b/.test(q))return out("MAC is read-only and cannot perform actions or disclose secrets.",[],"Review records manually.");
 if(/invoice|finance|outstanding|payment/.test(q))return out("Outstanding invoices: "+euro(f.outstanding_cents)+". Overpayments: "+euro(f.overpaid_cents)+".",f.invoices.map(x=>x.invoice_id+": balance "+euro(x.balance_cents)),"Review nonzero invoice balances before contacting customers.");
 if(/stock|inventory|warehouse/.test(q))return out("Recorded stock counts: "+f.stock.length+".",f.stock.map(x=>x.product_id+" / "+x.warehouse_id+": expected "+x.expected+", observed "+x.observed+", variance "+x.delta),"Recount discrepant stock and compare movement records.");
 if(/quality|reject|invalid/.test(q))return out(m.accepted+" accepted; "+m.rejected+" rejected.",z.rejections.map(x=>x.batch_id+" / "+x.entity+" #"+x.ordinal+": "+x.reason),"Correct source records and submit a new validated batch.");
 if(/pipeline|batch|audit/.test(q))return out("Recorded batches: "+z.batches.length+".",z.batches.map(x=>x.id+": "+x.status+" at "+(x.finished||x.started)),"Review failed batches if present; this is not continuous monitoring.");
 if(/source|connector|health/.test(q))return out(z.sources.filter(x=>x.status==="healthy").length+" of "+z.sources.length+" recorded source reads healthy.",z.sources.map(x=>x.id+": "+x.status+" ("+(x.checked_at||"unchecked")+")"),"Investigate failed reads and verify source freshness.");
 if(/exception|risk/.test(q))return out(f.exceptions.length+" business exceptions; "+m.rejected+" rejected records.",f.exceptions.map(x=>x.code+": "+String(x.key)+" ("+x.delta+")"),"Review reconciliation exceptions and quarantined records.");
 if(/order|sales|overview|summary/.test(q))return out("Order value: "+euro(m.order_value_cents)+". This is not recognized revenue.",["Batch "+m.batch_id,"Orders: "+(m.entity_counts.orders||0)],"Review sales orders and outstanding invoices.");
 return out("I cannot answer that from the supported snapshot topics.",[],"Ask about orders, invoices, stock, quality, sources, batches or exceptions.");
}
if(typeof module!=="undefined")module.exports=answerMAC;
