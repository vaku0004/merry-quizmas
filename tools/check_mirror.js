const {chromium}=require('playwright');const B='http://localhost:8766/night-of-frights-game';
(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route(/googletagmanager|google-analytics|fonts\.g/,r=>r.abort());
const pages=['/','/halloween-trivia-questions/','/virtual-halloween-games-for-work/','/how-to-host-a-halloween-game-night/','/faq/'];const bad=[];const seen=new Set();
for(const u of pages){const r=await p.goto(B+u);if(r.status()!==200)bad.push(u+' '+r.status());
 const refs=await p.$$eval('a[href^="/"],img[src^="/"],link[href^="/"]',as=>as.map(a=>a.getAttribute('href')||a.getAttribute('src')));
 for(const h of refs){const path=h.split('#')[0];if(seen.has(path))continue;seen.add(path);const s=(await p.request.get('http://localhost:8766'+path)).status();if(s!==200)bad.push(u+' -> '+h+' '+s);}}
await p.goto(B+'/');await p.waitForTimeout(1200);
const voice=await p.evaluate(async()=>{const m=await fetch('audio/manifest.json').then(r=>r.json());return Object.keys(m.lines).length});
const links=await p.evaluate(()=>!document.querySelector('.nof-links').hidden);
console.log('checked',seen.size,'links; broken:',bad,'| narrator lines:',voice,'| start-screen links:',links,'| errors:',errs);await b.close();})();
