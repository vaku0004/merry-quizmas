// node tools/shoot_site.js <jobs.json>
// Renders HTML files into PNGs. Written by tools/build_site.py:
//   {"renders": [{"src": "/abs/file.html", "out": "/abs/file.png", "w": 1200, "h": 630, "scale": 1, "transparent": false}],
//    "shots":   [{"page": "/abs/game.html", "key": "mq-state-v1", "state": {...}, "out": "/abs/shot.png"}]}
// "shots" open a game with a saved state (screen, teams, question) and take a 1366x768 screenshot.
const {chromium} = require('playwright'); const fs = require('fs');
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const r of jobs.renders || []) {
    const p = await b.newPage({viewport: {width: r.w, height: r.h}, deviceScaleFactor: r.scale || 1});
    await p.goto(require('url').pathToFileURL(r.src).href); await p.waitForTimeout(400);
    await p.screenshot({path: r.out, omitBackground: !!r.transparent}); await p.close();
  }
  for (const s of jobs.shots || []) {
    const ctx = await b.newContext({viewport: {width: 1366, height: 768}}); const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(s.out + ': ' + e.message));
    await p.goto(require('url').pathToFileURL(s.page).href); await p.evaluate(([k, st]) => { localStorage.clear(); localStorage.setItem(k, JSON.stringify(st)); }, [s.key, s.state]);
    await p.reload(); await p.waitForTimeout(900);
    await p.screenshot({path: s.out}); await ctx.close();
  }
  console.log('   rendered:', (jobs.renders || []).length, '| shots:', (jobs.shots || []).length, '| errors:', errs.length ? errs : 'none');
  await b.close();
})();
