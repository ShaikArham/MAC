const {chromium}=require('playwright');
(async()=>{const browser=await chromium.launch({headless:true});try{
const page=await browser.newPage({viewport:{width:375,height:812},isMobile:true,hasTouch:true});
page.on('console',m=>{if(m.text().startsWith('TOUCH_DIAG'))console.log(m.text())});
await page.goto('http://localhost:8000');await page.getByLabel('Shared reporting period').waitFor();
await page.evaluate(()=>{for(const t of ['touchstart','touchmove','touchend','touchcancel'])window.addEventListener(t,e=>console.log('TOUCH_DIAG '+JSON.stringify({type:t,target:e.target.tagName,cls:e.target.className,scroll:scrollY,y:e.touches[0]?.clientY,change:e.changedTouches[0]?.clientY,cancelable:e.cancelable,heading:document.querySelector('#heading').textContent})),{capture:true,passive:true})});
const c=await page.context().newCDPSession(page);
async function swipe(d){const box=await page.locator('.notice').boundingBox();const x=d>0?8:Math.round(box.x+box.width/2);const y=d>0?650:Math.round(box.y+box.height/2);await c.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y}]});for(let i=1;i<=5;i++)await c.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x,y:y-d*i*65}]});await c.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});console.log('END_GESTURE',d,await page.evaluate(()=>({h:document.querySelector('#heading').textContent,scroll:scrollY})))}
await page.locator('#menu').click();await page.locator('#nav').getByRole('button',{name:'System mapping',exact:true}).click();
await page.locator('#mac-next-workspace').evaluate(e=>e.scrollIntoView({block:'end'}));
await swipe(1);await page.waitForFunction(()=>document.querySelector('#heading').textContent==='Command Centre');
await page.waitForTimeout(1000);await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(120);
await swipe(-1);await page.waitForFunction(()=>document.querySelector('#heading').textContent==='System mapping',{timeout:5000});
console.log('MOBILE_EDGE_FOCUSED_PASSED');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
