const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+process.argv[2]);
const d=await p.evaluate(()=>JSON.stringify(DEFAULT_Q));require('fs').writeFileSync(process.argv[3],d);await b.close();})();
