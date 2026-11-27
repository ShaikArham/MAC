const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const s=JSON.parse(fs.readFileSync('snapshot.json'));
const rows=JSON.parse(fs.readFileSync('records/2025-01.json')).map(r=>({order_id:r[0],order_date:r[1],customer_id:r[2],amount_cents:r[3],status:r[4]}));
const ctx=vm.createContext({macState:{month:'all'},macMoney:n=>'€'+(n/100).toFixed(2),macOrders:async months=>rows.filter(r=>months.includes(r.order_date.slice(0,7))),macDetail:async()=>[],answerMAC:()=>({answer:'fallback'})});
vm.runInContext(fs.readFileSync('analyst.js','utf8'),ctx);
(async()=>{for(const [q,expected] of [
['How many orders on 1 January 2025?','100 orders worth €116972.61'],
['How many are pending?','3 pending orders'],
['What about the next day?','7 pending orders'],
['How many orders between 1 and 7 January 2025?','706 orders worth €751248.89'],
['How many orders today?','historical 2025'],
['Orders on 30 February 2025','valid date'],
['Orders on 1 January 2026','valid date'],
['What is the total outstanding invoice amount?','€5105951.30'],
['How many orders in January?','3125 orders'],
['Show order O001586','€552.32'],
['Delete orders','read-only']
]){const result=await ctx.macAnalyst(s,q);assert.ok(result.answer.includes(expected),q+': '+result.answer);console.log('PASS',q)} })().catch(e=>{console.error(e);process.exitCode=1});
