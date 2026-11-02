const {chromium}=require('playwright');const S=process.argv[2],OUT=process.argv[3];
const slugs=JSON.parse(require('fs').readFileSync(S+'/pages-og.json')).map(p=>p.slug);
(async()=>{const b=await chromium.launch();for(const s of slugs){const p=await b.newPage({viewport:{width:1200,height:630}});
await p.goto('file://'+S+'/seo/og-'+s+'.html');await p.waitForTimeout(600);await p.screenshot({path:OUT+'/assets/og/'+s+'.png'});await p.close();}await b.close();})();
