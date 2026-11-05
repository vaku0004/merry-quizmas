// node tools/e2e_game.js <game.html> [<game.html> ...]
// Plays a short game in a headless browser: setup, rules, a normal question, both surprises, undo, Round Two,
// the final with wagers, the podium, reload (saved progress), the question editor and voice settings.
// Reports page errors, scores at each step, and narrator lines that had no recording (browser-voice fallback).
const {chromium} = require('playwright');
const files = process.argv.slice(2);

(async () => {
  const b = await chromium.launch({args: ['--autoplay-policy=no-user-gesture-required']});
  let failed = 0;
  for (const file of files) {
    const ctx = await b.newContext({viewport: {width: 1366, height: 768}});
    const p = await ctx.newPage();
    const errs = [], log = []; let played0 = 0; const fb0 = [];
    p.on('pageerror', e => errs.push(e.message));
    p.on('console', m => { if (m.type() === 'error' && !/Fetch API cannot load file:|ERR_TUNNEL_CONNECTION_FAILED/.test(m.text())) errs.push('console: ' + m.text()); });   // no audio over file://, no outside fonts in the sandbox
    await p.addInitScript(() => {
      window.__fallback = []; window.__played = 0;
      const sp = window.speechSynthesis && window.speechSynthesis.speak.bind(window.speechSynthesis);
      if (window.speechSynthesis) window.speechSynthesis.speak = u => { window.__fallback.push(u.text); };
      const A = window.Audio;
      window.Audio = function(src){ const a = new A(src); window.__played++;
        a.play = () => { setTimeout(() => a.dispatchEvent(new Event('ended')), 60); return Promise.resolve(); }; return a; };
    });
    await p.goto(/^https?:/.test(file) ? file : require('url').pathToFileURL(require('path').resolve(file)).href);
    await p.evaluate(() => localStorage.clear()); await p.reload(); await p.waitForTimeout(500);
    const has = async sel => (await p.$(sel)) !== null;
    const click = async (sel, wait = 250) => {
      const el = await p.waitForSelector(sel + ':not([disabled])', {timeout: 10000});
      await el.click(); await p.waitForTimeout(wait);
    };
    const scores = () => p.evaluate(() => S.teams.slice(0, S.teamCount).map(t => t.score));
    const step = async name => log.push(name + ' ' + JSON.stringify(await scores()) + ' screen=' + await p.evaluate(() => S.screen));
    const nextRound = async () => {
      await click('[data-act=next]', 300);
      if (await p.evaluate(() => S.screen === 'board')) await click('[data-act=next]', 400);   // second press confirms skipping the rest
      for (let k = 0; k < 6 && await p.evaluate(() => S.screen === 'rules'); k++)
        await click(await has('[data-act=sskip]:not([disabled])') ? '[data-act=sskip]' : '[data-act=snext]', 400);
    };
    const playCell = async (c, i, verdict) => {
      await click(`[data-act=open][data-c="${c}"][data-i="${i}"]`, 400);
      const sp = await p.evaluate(() => S.q && S.q.special);
      if (sp === 'cat') await click('[data-act=catto]');
      if (sp === 'witch') {
        await click('[data-act=wand1]', 2600); await click('[data-act=wand2]', 2600); await click('[data-act=witchgo]');
      }
      await click('[data-act=reveal]');
      const team = await p.evaluate(() => S.q.team);
      await click(`[data-act=judge][data-i="${team}"][data-v="${verdict}"]`);
      if (await has('[data-act=done]:not([disabled])')) await click('[data-act=done]');
      return sp || 'normal';
    };
    try {
      await click('[data-act=count][data-n="3"]');
      await click('[data-act=start]', 500);
      await step('rules');
      await click('[data-act=sskip]', 400);
      await step('board R1');
      // Surprises are dealt at random when the game starts: read the layout from the game itself
      const SP = await p.evaluate(() => S.specials || {});
      const find = (r, sp) => { for (let c = 0; c < 5; c++) for (let i = 0; i < 5; i++) if ((SP[r + '-' + c + '-' + i] || null) === sp) return [c, i]; };
      log.push('surprises this game: ' + Object.entries(SP).map(([k, v]) => k + '=' + v).join(' '));
      const [nc, ni] = find(0, null), [cc, ci] = find(0, 'cat'), [wc, wi] = find(0, 'witch');
      log.push('played ' + await playCell(nc, ni, 'ok')); await step('after right answer');
      log.push('played ' + await playCell(cc, ci, 'no')); await step('after surprise 1, wrong');
      log.push('played ' + await playCell(wc, wi, 'ok')); await step('after surprise 2, right');
      const before = await scores(); await click('[data-act=undo]'); const after = await scores();
      log.push('undo changes scores back: ' + (JSON.stringify(before) !== JSON.stringify(after)));
      await nextRound();
      await step('board R2');
      const [rc, ri] = find(1, null); log.push('played ' + await playCell(rc, ri, 'ok')); await step('after R2 question');
      await nextRound();
      await step('final');
      await click('[data-act=fask]', 400); await click('[data-act=freveal]', 300);
      await p.$$eval('[data-wager]', els => els.forEach((e, k) => { e.value = String(100 * (k + 1)); }));   // wagers 100, 200, 300
      const n = await p.evaluate(() => S.teamCount);
      for (let i = 0; i < n; i++) await click(`[data-act=fjudge][data-i="${i}"][data-v="${i % 2 ? 'no' : 'ok'}"]`, 150);   // right, wrong, right
      await click('[data-act=fdone]', 800);
      await step('after final');
      const headline = await p.evaluate(() => (document.querySelector('h1, .podium h2, .big') || {}).innerText || '');
      log.push('podium headline: ' + headline.replace(/\s+/g, ' ').slice(0, 60));
      const pre = await p.evaluate(() => [window.__played, window.__fallback.slice()]); played0 += pre[0]; fb0.push(...pre[1]);
      await p.reload(); await p.waitForTimeout(500); await step('after reload');
      await click('[data-act=new]', 300);
      if (await has('[data-act=cancel]')) await click('[data-act=cancel]', 200);
      await p.evaluate(() => { S.screen = 'setup'; render(); }); await p.waitForTimeout(200);
      if (await has('[data-act=edit]')) { await click('[data-act=edit]', 300); log.push('editor opened: ' + await has('.editor, [data-act=edone]')); await click('[data-act=edone]', 300); }
      await click('[data-act=voice]', 300);
      log.push('voice panel: ' + (await p.$$eval('.overlay .pick button', e => e.map(x => x.innerText.trim()))).join(' / ') + ' | ' +
        (await p.$eval('.overlay .vgrid .hint', e => e.innerText)));
      await click('[data-act=vdone]', 200);
    } catch (e) {
      errs.push('script: ' + e.message.split('\n')[0] + ' | state: ' + await p.evaluate(() => JSON.stringify({screen: S.screen, round: S.round, q: S.q, deck: S.deck})));
      await p.screenshot({path: '/tmp/e2e-fail.png'});
    }
    const fb = fb0.concat(await p.evaluate(() => window.__fallback)), played = played0 + await p.evaluate(() => window.__played);
    const bad = errs.length > 0;
    if (bad) failed++;
    console.log(`\n=== ${file}\n` + log.map(l => '  ' + l).join('\n') +
      `\n  narrator: ${played} recorded lines played, ${fb.length} without a recording${fb.length ? ': ' + fb.slice(0, 3).map(t => t.slice(0, 50)).join(' | ') : ''}` +
      `\n  errors: ${bad ? errs.join(' || ') : 'none'}`);
    await ctx.close();
  }
  await b.close();
  process.exit(failed ? 1 : 0);
})();
