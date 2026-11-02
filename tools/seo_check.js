const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
 // 1) without JavaScript: what crawlers / link previews see
 let ctx=await b.newContext({javaScriptEnabled:false});let p=await ctx.newPage();await p.goto('file://'+process.argv[2]);
 console.log('NO-JS:',JSON.stringify({h1:await p.$$eval('h1',e=>e.map(x=>x.innerText)),words:(await p.innerText('body')).split(/\s+/).length}));
 // 2) with JavaScript: the game replaces the static text
 ctx=await b.newContext({viewport:{width:1366,height:768}});p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file://'+process.argv[2]);await p.waitForTimeout(1200);
 console.log('JS:',JSON.stringify({h1:await p.$$eval('h1',e=>e.map(x=>x.innerText)),static:await p.$$eval('.nof-static',e=>e.length),start:await p.$$eval('button',e=>e.some(x=>/Start the game/.test(x.innerText))),errs}));
 await p.screenshot({path:process.argv[3]});await b.close();})();
