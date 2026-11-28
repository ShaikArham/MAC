const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const base=process.env.MAC_BASE_URL||'http://127.0.0.1:8000';
const euro=n=>new Intl.NumberFormat('en-IE',{style:'currency',currency:'EUR'}).format(n/100);
(async()=>{
 const browser=await chromium.launch({headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1440,height:900}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base,{waitUntil:'domcontentloaded'});
  await page.getByLabel('Shared reporting period').waitFor();
  const go=async name=>{await page.locator('#nav').getByRole('button',{name,exact:true}).click();await page.locator('#view table').first().waitFor();};
  await go('Finance');
  const ledger=await page.evaluate(async()=>{
   const [invoices,payments]=await Promise.all([macRows('invoices'),macRows('payments')]);
   const sums=new Map();for(const p of payments)sums.set(p.invoice_id,(sums.get(p.invoice_id)||0)+p.amount_cents);
   let fully=0,partial=0,unpaid=0,overpaid=0;
   for(const i of invoices){const p=sums.get(i.invoice_id)||0;if(p===0)unpaid++;else if(p===i.amount_cents)fully++;else if(p<i.amount_cents)partial++;else overpaid++;}
   const amount=invoices.reduce((n,x)=>n+x.amount_cents,0),paid=payments.reduce((n,x)=>n+x.amount_cents,0);
   return {invoices:invoices.length,payments:payments.length,fully,partial,unpaid,overpaid,amount,paid,expected:currentSnapshot.finance};
  });
  assert.equal(ledger.invoices,47008);assert.equal(ledger.payments,44631);
  assert(ledger.fully>0&&ledger.partial>0&&ledger.unpaid>0,'All three invoice states must exist');
  assert.equal(ledger.overpaid,0,'Synthetic dataset must not overpay individual invoices');
  assert.equal(ledger.amount,ledger.expected.invoiced_cents);
  assert.equal(ledger.paid,ledger.expected.paid_cents);
  assert.equal(ledger.amount-ledger.paid,ledger.expected.outstanding_cents);
  console.log('PASS LEDGER_RECONCILIATION',JSON.stringify(ledger));
  const list=page.locator('#view');
  await list.getByLabel('Filter Invoice ID').fill('I000027');
  await list.getByRole('button',{name:'Find',exact:true}).click();
  const target=list.locator('tbody tr').first();
  await target.getByRole('button',{name:'I000027'}).waitFor();
  const targetText=await target.innerText();
  for(const value of ['I000027','O000027',euro(19220),euro(9610),'Partially paid'])
   assert(targetText.includes(value),'Missing target invoice table value '+value+': '+targetText);
  await target.getByRole('button',{name:'I000027'}).click();
  await page.getByRole('heading',{name:'I000027 · Partially paid'}).waitFor();
  const payment=page.locator('#view').getByText('Invoice '+euro(19220)+' · Collected '+euro(9610)+' · Outstanding '+euro(9610),{exact:true});
  await payment.waitFor();
  await page.getByRole('heading',{name:'Payment history'}).waitFor();
  await page.getByText('PAY000027',{exact:true}).waitFor();
  await page.getByRole('heading',{name:'Connected sales order'}).waitFor();
  const viewText=await page.locator('#view').innerText();
  for(const value of ['O000027','C0453','Maplerock Roofing Ireland','P1841','P0512',
    'General purpose cement 25kg / range 93','PVC drainage pipe 3m / range 26',
    'D000027','delivered','PAY000027'])
    assert(viewText.includes(value),'Missing connected invoice evidence '+value);
  console.log('PASS INVOICE_I000027_AND_CONNECTED_RECORDS');
  await page.getByRole('button',{name:'Open order O000027'}).click();
  await page.getByRole('heading',{name:'Order lines'}).waitFor();
  await page.getByRole('heading',{name:'Invoices'}).waitFor();
  await page.getByRole('heading',{name:'Payments'}).waitFor();
  assert((await page.locator('#view').innerText()).includes('I000027'));
  console.log('PASS INVOICE_TO_ORDER');
  await go('Finance');await page.getByLabel('Filter Invoice ID').fill('I000027');
  await page.locator('#view tbody').getByRole('button',{name:'I000027'}).click();
  await page.getByRole('heading',{name:'Connected sales order'}).waitFor();
  await page.locator('#view table tbody').getByRole('button',{name:'P1841'}).click();
  await page.locator('#heading').getByText('Products',{exact:true}).waitFor();
  await page.getByText('General purpose cement 25kg / range 93').first().waitFor();
  console.log('PASS INVOICE_TO_PRODUCT');
  await go('Finance');await page.getByLabel('Filter Invoice ID').fill('I000027');
  await page.locator('#view tbody').getByRole('button',{name:'I000027'}).click();
  await page.getByRole('heading',{name:'Connected sales order'}).waitFor();
  await page.getByRole('button',{name:/Maplerock Roofing Ireland · C0453/}).click();
  await page.locator('#heading').getByText('Customers',{exact:true}).waitFor();
  await page.getByText('Maplerock Roofing Ireland').first().waitFor();
  console.log('PASS INVOICE_TO_CUSTOMER');
  for(const [state,expected] of [['Fully paid','Outstanding '+euro(0)],['Partially paid','Collected'],['Unpaid','Collected '+euro(0)]]){
   await go('Finance');
   await page.getByLabel('Filter Payment status').selectOption(state);
   const first=page.locator('#view table tbody tr').first();
   await first.waitFor();
   assert((await first.innerText()).includes(state),'Incorrect filtered state '+state);
   const id=await first.locator('button').first().innerText();
   await first.locator('button').first().click();
   await page.getByRole('heading',{name:id+' · '+state}).waitFor();
   assert((await page.locator('#view').innerText()).includes(expected),'Wrong payment reconciliation for '+state);
   console.log('PASS PAYMENT_STATE',state,id);
  }
  await go('Finance');await page.getByRole('button',{name:'Clear filters',exact:true}).click();
  assert((await page.locator('#view tbody tr').count())>0);
  assert.deepEqual(errors,[]);
  console.log('PASS DESKTOP_FINANCE_NO_PAGEERROR');
  await page.close();
  for(const width of [375,320]){
   const mobile=await browser.newPage({viewport:{width,height:812},isMobile:true,hasTouch:true});
   const mobileErrors=[];mobile.on('pageerror',e=>mobileErrors.push(e.message));
   await mobile.goto(base,{waitUntil:'domcontentloaded'});
   await mobile.getByLabel('Shared reporting period').waitFor();
   await mobile.locator('#menu').click();
   await mobile.locator('#nav').getByRole('button',{name:'Finance',exact:true}).click();
   await mobile.locator('#view table').first().waitFor();
   await mobile.getByLabel('Filter Invoice ID').fill('I000027');
   await mobile.locator('#view tbody').getByRole('button',{name:'I000027'}).click();
   await mobile.getByRole('heading',{name:'I000027 · Partially paid'}).waitFor();
   await mobile.getByRole('heading',{name:'Connected sales order'}).waitFor();
   const text=await mobile.locator('#view').innerText();
   assert(text.includes(euro(19220))&&text.includes(euro(9610)));
   assert(text.includes('PAY000027')&&text.includes('Maplerock Roofing Ireland')&&text.includes('D000027'));
   const geom=await mobile.evaluate(()=>({innerWidth,documentWidth:document.documentElement.scrollWidth,viewWidth:document.querySelector('#view').getBoundingClientRect().width}));
   assert(geom.documentWidth<=geom.innerWidth+3,'Horizontal page overflow: '+JSON.stringify(geom));
   assert.deepEqual(mobileErrors,[]);
   console.log('PASS MOBILE_FINANCE',width,JSON.stringify(geom));
   await mobile.close();
  }
  console.log('FINANCE_ACCEPTANCE_PASSED');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
