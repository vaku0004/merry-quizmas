const {chromium}=require('playwright');const OUT=process.argv[2];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1366,height:768}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/');await p.waitForTimeout(800);
const vis=()=>p.evaluate(()=>!document.querySelector('.nof-links').hidden);
console.log('setup links visible:',await vis());

await p.click('text=Start the game');await p.waitForTimeout(500);console.log('rules screen links visible:',await vis());
await p.evaluate(()=>{localStorage.setItem('mq-state-v1',JSON.stringify({screen:"board",teamCount:3,teams:[{name:"A",score:0},{name:"B",score:0},{name:"C",score:0},{name:"D",score:0}],round:0,used:{},turn:0,q:null,final:null,sound:false}))});
await p.reload();await p.waitForTimeout(500);console.log('board links visible:',await vis(),'fits screen:',await p.evaluate(()=>document.documentElement.scrollHeight<=innerHeight+1));
const pages=['/','/christmas-trivia-questions/','/virtual-christmas-games-for-work/','/how-to-host-a-christmas-game-night/','/faq/'];const bad=[];const seen=new Set();
for(const u of pages){await p.goto('http://localhost:8765'+u);const hrefs=await p.$$eval('a[href^="/"],img[src^="/"],link[href^="/"]',as=>as.map(a=>a.getAttribute('href')||a.getAttribute('src')));
 const ids=await p.$$eval('[id]',e=>e.map(x=>x.id));const anchors=await p.$$eval('a[href^="#"]',as=>as.map(a=>a.getAttribute('href').slice(1)));
 anchors.forEach(a=>{if(a&&!ids.includes(a))bad.push(u+' missing #'+a)});
 for(const h of hrefs){const path=h.split('#')[0];if(seen.has(path))continue;seen.add(path);const r=await p.request.get('http://localhost:8765'+path);if(r.status()!==200)bad.push(u+' -> '+h+' '+r.status());}}
console.log('checked',seen.size,'internal URLs; broken:',bad,'errors:',errs);await b.close();})();
