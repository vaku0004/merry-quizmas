// node tools/check_site.js <screenshot_dir> <fonts.css> http://localhost:8765   (serve the built site folder on that port first)
// Follows every internal link from the home page, reports broken links, missing #anchors and JS errors, and takes screenshots.
const {chromium}=require('playwright');const fs=require('fs');const [,,OUT,CSS,BASE]=process.argv;const css=fs.readFileSync(CSS,'utf8');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:900}});
await ctx.route('**/fonts.googleapis.com/**',r=>r.fulfill({contentType:'text/css',body:css}));
await ctx.route('**/googletagmanager.com/**',r=>r.fulfill({contentType:'text/javascript',body:''}));
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(p.url()+' '+e.message));
const todo=['/'],seen=new Set(),bad=[];
while(todo.length){const u=todo.shift();if(seen.has(u))continue;seen.add(u);const r=await p.goto(BASE+u);if(!r||r.status()!==200){bad.push(u+' '+(r&&r.status()));continue;}
 if(!/\.html?$|\/$/.test(u))continue;await p.waitForTimeout(150);
 const refs=await p.$$eval('a[href^="/"],img[src^="/"],link[href^="/"]',as=>as.map(a=>a.getAttribute('href')||a.getAttribute('src')));
 const ids=await p.$$eval('[id]',e=>e.map(x=>x.id));for(const a of await p.$$eval('a[href*="#"]',as=>as.map(a=>a.getAttribute('href'))))if(a.startsWith('#')&&a.length>1&&!ids.includes(a.slice(1)))bad.push(u+' missing '+a);
 for(const h of refs){const path=h.split('#')[0];if(!path||seen.has(path))continue;if(path.endsWith('/'))todo.push(path);else{seen.add(path);const rr=await p.request.get(BASE+path);if(rr.status()!==200)bad.push(u+' -> '+path+' '+rr.status());}}}
console.log('checked',seen.size,'URLs; broken:',bad,'js errors:',errs);
await p.goto(BASE+'/');await p.waitForTimeout(500);await p.screenshot({path:OUT+'/home.png',fullPage:true});
const m=await b.newContext({viewport:{width:390,height:844}});await m.route('**/fonts.googleapis.com/**',r=>r.fulfill({contentType:'text/css',body:css}));
const mp=await m.newPage();await mp.goto(BASE+'/');await mp.waitForTimeout(400);console.log('mobile overflow home:',await mp.evaluate(()=>document.documentElement.scrollWidth>innerWidth));
await mp.screenshot({path:OUT+'/home-m.png',fullPage:false});
await p.goto(BASE+'/halloween/how-to-host-a-game-night/');await p.waitForTimeout(400);await p.screenshot({path:OUT+'/hal.png'});
await b.close();})();
