// node tools/render_pins.js '<json [{src, out}]>'  — renders 1000x1500 pin pages to PNG (used by tools/make_pins.py).
const {chromium} = require('playwright');
const {pathToFileURL} = require('url');
const jobs = JSON.parse(process.argv[2]);
(async () => {
  const b = await chromium.launch();
  for (const j of jobs) {
    const p = await b.newPage({viewport: {width: 1000, height: 1500}});
    await p.goto(pathToFileURL(j.src).href, {waitUntil: 'load'});
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(200);
    await p.screenshot({path: j.out});
    await p.close();
  }
  await b.close();
})();
