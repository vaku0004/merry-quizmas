const {chromium}=require('playwright');const S=process.argv[2];
(async()=>{const b=await chromium.launch();
 let p=await b.newPage({viewport:{width:1200,height:630}});await p.goto('file://'+S+'/seo/og.html');await p.waitForTimeout(800);
 await p.screenshot({path:S+'/seo/og-image.png'});
 for (const [f,src,size] of [['icon-512.png','tile.html',512],['icon-192.png','tile.html',192],['favicon-48.png','tile.html',48],['apple-touch-icon.png','tile-square.html',180]]){
   p=await b.newPage({viewport:{width:512,height:512},deviceScaleFactor:size/512});await p.goto('file://'+S+'/seo/'+src);
   await p.screenshot({path:S+'/seo/'+f,omitBackground:true});}
 await b.close();})();
