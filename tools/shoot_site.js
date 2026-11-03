// node tools/shoot_site.js <repo_root> <game_page_with_local_fonts.html>
// Renders build/seo/*.html into preview images and icons, and takes the game screenshots used on the content pages
// (build/pageshots/*.png, 1366x768). tools/build_site.py calls this and converts the shots to WebP.
const {chromium} = require('playwright'); const fs = require('fs');
const [,, ROOT, GAME] = process.argv; const SEO = ROOT + '/build/seo', SHOTS = ROOT + '/build/pageshots';
fs.mkdirSync(SHOTS, {recursive: true});
const teams = [{name: "Team Elves", score: 1100}, {name: "Team Reindeer", score: -300}, {name: "Team Snowmen", score: 900}, {name: "Team Gingerbread", score: 400}];
const base = {screen: "board", teamCount: 4, teams, round: 0, used: {"0-0-0": 1, "0-1-0": 1, "0-2-1": 1, "0-3-0": 1, "0-4-0": 1}, turn: 1, q: null, final: null, sound: false};
const shots = [
  ["board", {...base}],
  ["question", {...base, q: {c: 3, i: 3, value: 400, special: null, picker: 1, team: 1, bid: null, judged: {}, stage: "ask"}}],
  ["coal", {...base, q: {c: 1, i: 2, value: 300, special: "cat", picker: 0, team: null, bid: null, judged: {}, stage: "intro", catAsk: true}}],
  ["krampus", {...base, q: {c: 4, i: 4, value: 500, special: "witch", picker: 0, team: null, bid: 300, w: {price: 300, team: 2}, judged: {}, stage: "intro", witchAsk: true}}],
  ["final", {...base, screen: "final", round: 1, used: {}, final: {stage: "category", wagers: [], judged: []}}],
  ["podium", {...base, screen: "podium", round: 1, used: {}, final: {stage: "done", wagers: [], judged: []},
    teams: [{name: "Team Elves", score: 3400}, {name: "Team Reindeer", score: 2100}, {name: "Team Snowmen", score: 2800}, {name: "Team Gingerbread", score: 900}]}],
];
(async () => {
  const b = await chromium.launch();
  let p = await b.newPage({viewport: {width: 1200, height: 630}});
  const ogs = ['og'].concat(JSON.parse(fs.readFileSync(ROOT + '/build/pages-og.json')).map(x => 'og-' + x.slug));
  for (const n of ogs) { await p.goto('file://' + SEO + '/' + n + '.html'); await p.waitForTimeout(500); await p.screenshot({path: SEO + '/' + n + '.png'}); }
  for (const [f, src, size] of [['icon-512.png', 'tile.html', 512], ['icon-192.png', 'tile.html', 192], ['favicon-48.png', 'tile.html', 48],
                                ['favicon-32.png', 'tile.html', 32], ['favicon-16.png', 'tile.html', 16], ['apple-touch-icon.png', 'tile-square.html', 180]]) {
    p = await b.newPage({viewport: {width: 512, height: 512}, deviceScaleFactor: size / 512}); await p.goto('file://' + SEO + '/' + src);
    await p.screenshot({path: SEO + '/' + f, omitBackground: true}); await p.close();
  }
  const errs = [];
  for (const [name, st] of shots) {
    const ctx = await b.newContext({viewport: {width: 1366, height: 768}}); p = await ctx.newPage(); p.on('pageerror', e => errs.push(name + ': ' + e.message));
    await p.goto('file://' + GAME); await p.evaluate(s => { localStorage.clear(); localStorage.setItem("mq-state-v1", JSON.stringify(s)); }, st);
    await p.reload(); await p.waitForTimeout(900);
    await p.screenshot({path: SHOTS + '/' + name + '.png'}); await ctx.close();
  }
  console.log('shots:', shots.length, '| errors:', errs.length ? errs : 'none');
  await b.close();
})();
