const test=require('node:test'),assert=require('node:assert/strict'),answer=require('./copilot'),s=require('./snapshot.json');
for(const [q,expected] of [['invoice','€650.00'],['inventory','Recorded stock counts: 1'],['quality','17 accepted; 5 rejected'],['pipeline','Recorded batches: 1'],['sources','10 of 10'],['exceptions','1 business exceptions'],['sales','€2,100.00'],['delete invoices','read-only'],['weather','cannot answer']])test(q,()=>assert.ok(answer(s,q).answer.includes(expected)));
test('missing snapshot',()=>assert.match(answer(null,'invoice').answer,/unavailable/));
test('malformed reconciliation',()=>assert.match(answer({...s,reconciliation:{}},'invoice').answer,/unavailable/));
test('changed balance',()=>assert.match(answer({...s,reconciliation:{...s.reconciliation,outstanding_cents:12345}},'invoice').answer,/€123.45/));
test('no mutation',()=>{const before=JSON.stringify(s);answer(s,'inventory');assert.equal(JSON.stringify(s),before)});
