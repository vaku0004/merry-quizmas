"""Season trailer: the first screen of the home page (her idea, Nov 14, from the "animated site with video" regulation).

A pinned scene about one and a half screens tall for the game in season: the game's own night colours and glow, its
"weather" drawn on a canvas (snow for Christmas, embers for Halloween, confetti for New Year...), its art glowing, and
its title in its own display font. Scrolling down drops the title letter by letter (and scrolling up brings them back:
the animation follows the scroll position, not time), then the facts come in at the corners. No video file: the scene
is drawn by code, so it weighs a few KB, works the same on phones and has no stock footage or foreign logos.

trailer(g) -> (html, css, js). Reduced motion: no falling letters or particles, everything shown at once.
"""
import html, json
import games as G

e = lambda s: html.escape(s, quote=True)

# Weather per game: particle colours, direction (1 = falls, -1 = rises), sizes in px, density (per 10,000 px²), speed.
FX = {
    "christmas":  dict(colors=["#ffffff", "#eaf4ff", "#ffe6a6"], dir=1,  size=[1.2, 3.4], density=1.1, speed=[18, 55], sway=22),
    "newyear":    dict(colors=["#f5cf6b", "#ff6b81", "#f4f3ff", "#7fd0ff"], dir=1, size=[2, 4.5], density=.55, speed=[30, 80], sway=30, confetti=True),
    "halloween":  dict(colors=["#f2a24c", "#ffd58a", "#a98be0"], dir=-1, size=[1, 2.6], density=.45, speed=[12, 36], sway=18),
    "movies":     dict(colors=["#f2c14e", "#ffe4a3", "#ffffff"], dir=-1, size=[.8, 2.2], density=.5, speed=[6, 18], sway=10, beam=True),
    "valentines": dict(colors=["#ef7d9a", "#ffd6e0", "#ffffff"], dir=-1, size=[1.2, 3], density=.5, speed=[12, 30], sway=16),
    "stpatricks": dict(colors=["#e8b84a", "#5fbf73", "#ffe7a3"], dir=-1, size=[1.2, 3], density=.5, speed=[12, 30], sway=16),
    "trivia":     dict(colors=["#ffd23f", "#b48cff", "#ffffff"], dir=-1, size=[1.2, 3], density=.45, speed=[12, 30], sway=14),
    "decades":    dict(colors=["#ff5aa8", "#3fd5ff", "#ffffff"], dir=-1, size=[1.2, 3], density=.45, speed=[12, 30], sway=14),
}
ARROW = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">'
         '<path d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"/></svg>')
DOWN = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">'
        '<path d="M12 4v16m0 0l-6-6m6 6l6-6"/></svg>')


def trailer(g, new=False):
    th, rgb = g["theme"], g["rgb"]
    fam, w = g["display"][3].replace('"', "'"), g["display"][1]
    art = G.art(g, g["page_art"].get("trivia-questions", g["icon"]))
    chips = "".join(f"<li>{e(t)}</li>" for _, t in g["chips"])
    fx = json.dumps(FX.get(g["slug"], FX["trivia"]))
    title = g["short"].upper() if g["display"][0] in ("Bungee", "Lilita One", "Righteous") else g["short"]
    label = ("New · " if new else "Now playing · ") + g["holiday"]
    style = (f"--tr-night:{th['night']};--tr-dusk:{th['dusk']};--tr-bone:{th['bone']};--tr-ash:{th['ash']};--tr-ember:{th['ember']};"
             f"--tr-candle:{th['candle']};--tr-glow:{rgb['glow']};--tr-glow2:{rgb['glow2']};--tr-font:{fam};--tr-w:{w}")
    html_ = f'''<section class="trailer" style="{style}" aria-labelledby="tr-title">
<div class="trailer__sticky">
  <canvas class="trailer__fx" data-fx='{fx}' aria-hidden="true"></canvas>
  <div class="trailer__art" aria-hidden="true">{art}</div>
  <div class="trailer__fade" aria-hidden="true"></div>
  <div class="trailer__hero">
    <p class="trailer__eyebrow">{e(label)}</p>
    <h2 class="trailer__title" id="tr-title" data-text="{e(title)}">{e(title)}</h2>
    <div class="trailer__cta"><a class="trailer__play" href="/{g['slug']}/" data-play>Play {e(g['short'])} {ARROW}</a>
      <a class="trailer__all" href="#games">All games {DOWN}</a></div>
  </div>
  <div class="trailer__orbit" aria-hidden="true">
    <p class="trailer__item trailer__item--tl"><span>Victoria’s Game Nights</span>{e(g['name'].replace("Victoria’s ", ""))}, a quiz for the whole office</p>
    <p class="trailer__item trailer__item--tr">A narrator reads every question.<br>Teams answer out loud.</p>
    <ul class="trailer__item trailer__item--bl">{chips}</ul>
    <p class="trailer__item trailer__item--br">2–4 teams · about an hour<br>free, no sign-up</p>
  </div>
</div>
</section>'''
    return html_, CSS, JS


CSS = """
.trailer{position:relative;height:190vh;background:var(--tr-night);color:var(--tr-bone)}
body:has(.trailer) .site-head{position:absolute;top:0;left:0;right:0;z-index:5;background:transparent;border-bottom-color:transparent}
.trailer__sticky{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden;--tr-pad:max(clamp(16px,4vw,56px),calc((100% - 1200px) / 2 + 20px));
 background:radial-gradient(70% 60% at 78% 62%,rgba(var(--tr-glow),.20),transparent 70%),radial-gradient(60% 50% at 10% 10%,rgba(var(--tr-glow2),.12),transparent 70%),var(--tr-night)}
.trailer__fx{position:absolute;inset:0;width:100%;height:100%;display:block}
.trailer__art{position:absolute;right:calc(var(--tr-pad) + 2%);top:clamp(72px,11vh,120px);width:min(30vw,44vh,440px);aspect-ratio:1;filter:drop-shadow(0 0 60px rgba(var(--tr-glow),.55));
 transform-origin:50% 50%;will-change:transform}
.trailer__art svg{width:100%;height:100%}
.trailer__fade{position:absolute;inset:0;pointer-events:none;background:linear-gradient(to bottom,transparent 62%,rgba(12,12,14,.55) 84%,#0c0c0e 100%)}
.trailer__hero{position:absolute;inset:0;padding:0 var(--tr-pad) clamp(28px,6vh,64px);display:flex;flex-direction:column;justify-content:flex-end;gap:10px}
.trailer__eyebrow{margin:0;font-family:var(--f-ui);font-weight:800;font-size:.8rem;letter-spacing:.16em;text-transform:uppercase;color:var(--tr-candle)}
.trailer__title{margin:0;font-family:var(--tr-font);font-weight:var(--tr-w);line-height:.9;letter-spacing:-.01em;white-space:nowrap;
 display:inline-flex;align-self:flex-start;width:max-content;font-size:14vw;color:var(--tr-ember);text-shadow:0 0 50px rgba(var(--tr-glow),.45)}
.trailer__title .ch{display:inline-block;transform-origin:50% 100%;white-space:pre}
.trailer__cta{display:flex;flex-wrap:wrap;gap:12px 22px;align-items:center;margin-top:6px;font-family:var(--f-ui)}
.trailer__play{display:inline-flex;align-items:center;gap:8px;background:var(--tr-candle);color:#0c0c0e;text-decoration:none;font-weight:800;font-size:.9rem;
 letter-spacing:.06em;text-transform:uppercase;border-radius:12px;padding:14px 20px}
.trailer__play:hover{filter:brightness(1.08);color:#0c0c0e}
.trailer__all{display:inline-flex;align-items:center;gap:6px;color:var(--tr-bone);font-weight:700;font-size:.9rem;text-decoration:none;opacity:.85}
.trailer__all:hover{opacity:1;color:var(--tr-ember)}
.trailer__orbit{position:absolute;inset:0;opacity:0;pointer-events:none;font-family:var(--f-ui)}
.trailer__item{position:absolute;margin:0;max-width:30ch;font-size:clamp(.95rem,1.4vw,1.15rem);line-height:1.45;font-weight:600;color:var(--tr-bone)}
.trailer__item span{display:block;margin-bottom:6px;font-size:.72rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--tr-ash)}
.trailer__item--tl{top:clamp(88px,12vh,120px);left:var(--tr-pad)}
.trailer__item--tr{top:clamp(88px,12vh,120px);right:var(--tr-pad);text-align:right}
.trailer__item--bl{bottom:clamp(120px,22vh,220px);left:var(--tr-pad);list-style:none;padding:0;display:flex;flex-direction:column;gap:6px;
 font-family:var(--tr-font);font-weight:var(--tr-w);font-size:clamp(1.4rem,3.2vw,2.6rem);line-height:1.1;color:var(--tr-ember);max-width:none}
.trailer__item--br{bottom:clamp(120px,22vh,220px);right:var(--tr-pad);text-align:right}
@media (max-width:760px){
 .trailer{height:170vh}
 .trailer__art{right:-4%;top:84px;width:min(60vw,40vh)}
 .trailer__item--bl{left:var(--tr-pad)}
 .trailer__item--tr,.trailer__item--br{display:none}
 .trailer__item--bl{bottom:auto;top:clamp(110px,20vh,180px)}
}
@media (prefers-reduced-motion:reduce){.trailer{height:auto}.trailer__sticky{position:relative}.trailer__orbit{opacity:1}}
"""

JS = """<script>
(function(){
  var st = document.querySelector('.trailer'); if (!st) return;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var clamp = function(v,a,b){ return Math.min(b===undefined?1:b, Math.max(a===undefined?0:a, v)); };
  var range = function(v,a,b){ return clamp((v-a)/(b-a)); };
  var smooth = function(p){ return p*p*(3-2*p); };
  var hero = st.querySelector('.trailer__hero'), title = st.querySelector('.trailer__title');
  var orbit = st.querySelector('.trailer__orbit'), items = [].slice.call(orbit.querySelectorAll('.trailer__item'));
  var art = st.querySelector('.trailer__art'), eyebrow = st.querySelector('.trailer__eyebrow'), cta = st.querySelector('.trailer__cta');
  // title letters
  var chars = [], text = title.getAttribute('data-text'); title.textContent = '';
  for (var i = 0; i < text.length; i++){ var s = document.createElement('span'); s.className = 'ch'; s.textContent = text[i]; title.appendChild(s); chars.push(s); }
  title.setAttribute('aria-label', text);
  function fit(){
    var cs = getComputedStyle(hero), avail = hero.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    if (avail <= 0) return; title.style.fontSize = '100px';
    var w = title.getBoundingClientRect().width; if (w > 0) title.style.fontSize = Math.min(100 * avail / w, innerHeight * 0.27) + 'px';
  }
  var progress = 0;
  function read(){ var travel = st.offsetHeight - innerHeight; progress = travel > 0 ? clamp(-st.getBoundingClientRect().top / travel) : 0; }
  function render(){
    if (reduce) return;
    var n = chars.length, STAG = 0.32 / Math.max(n, 1), SPAN = 0.16;
    for (var i = 0; i < n; i++){ var k = smooth(range(progress, 0.04 + i*STAG, 0.04 + i*STAG + SPAN));
      chars[i].style.transform = 'translateY(' + (k*130) + 'px) scaleY(' + (1 - k*0.22) + ')'; chars[i].style.opacity = String(1 - k); }
    var f = String(1 - range(progress, 0.05, 0.22)); eyebrow.style.opacity = f; cta.style.opacity = f; cta.style.pointerEvents = +f < .2 ? 'none' : '';
    art.style.transform = 'translateY(' + (-progress*6) + 'vh) scale(' + (1 + progress*0.18) + ')';
    var start = 0.36, out = range(progress, 0.9, 1);
    orbit.style.opacity = String(range(progress, start, start + 0.14) * (1 - out));
    items.forEach(function(it, j){ var k = smooth(range(progress, start + j*0.05, start + 0.22 + j*0.05));
      it.style.transform = 'translateY(' + ((1-k)*24) + 'px)'; it.style.opacity = String(k); });
  }
  // weather
  var cv = st.querySelector('.trailer__fx'), ctx = cv.getContext('2d'), fx = JSON.parse(cv.getAttribute('data-fx')), parts = [], W = 0, H = 0, dpr = 1;
  function rnd(a,b){ return a + Math.random()*(b-a); }
  function spawn(p, anywhere){ p.x = rnd(0, W); p.y = anywhere ? rnd(0, H) : (fx.dir > 0 ? -10 : H + 10); p.r = rnd(fx.size[0], fx.size[1]);
    p.v = rnd(fx.speed[0], fx.speed[1]); p.ph = rnd(0, 6.28); p.c = fx.colors[(Math.random()*fx.colors.length)|0]; p.a = rnd(.35, .95); p.rot = rnd(0, 6.28); return p; }
  function size(){ dpr = Math.min(devicePixelRatio || 1, 2); W = cv.clientWidth; H = cv.clientHeight; cv.width = W*dpr; cv.height = H*dpr;
    ctx.setTransform(dpr,0,0,dpr,0,0); var want = Math.round(W*H/10000*fx.density); while (parts.length < want) parts.push(spawn({}, true)); parts.length = want; }
  var visible = true, last = 0;
  function draw(t){
    var dt = Math.min(.05, (t - last)/1000 || 0); last = t; ctx.clearRect(0,0,W,H);
    if (fx.beam){ var gr = ctx.createLinearGradient(W*.85, 0, W*.35, H); gr.addColorStop(0,'rgba(255,228,163,.16)'); gr.addColorStop(1,'rgba(255,228,163,0)');
      ctx.fillStyle = gr; ctx.beginPath(); ctx.moveTo(W*.9, 0); ctx.lineTo(W*.2, H); ctx.lineTo(W*.6, H); ctx.lineTo(W*.98, 0); ctx.fill(); }
    for (var i = 0; i < parts.length; i++){ var p = parts[i];
      p.y += fx.dir * p.v * dt; p.ph += dt; var x = p.x + Math.sin(p.ph*0.8) * fx.sway * 0.3;
      if (p.y > H + 12 || p.y < -12) spawn(p, false);
      ctx.globalAlpha = p.a; ctx.fillStyle = p.c;
      if (fx.confetti){ p.rot += dt*2; ctx.save(); ctx.translate(x, p.y); ctx.rotate(p.rot); ctx.fillRect(-p.r, -p.r*.45, p.r*2, p.r*.9); ctx.restore(); }
      else { ctx.beginPath(); ctx.arc(x, p.y, p.r, 0, 6.283); ctx.fill(); } }
    ctx.globalAlpha = 1;
  }
  function frame(t){ render(); if (visible && !reduce) draw(t); requestAnimationFrame(frame); }
  new IntersectionObserver(function(es){ visible = es[0].isIntersecting; }).observe(st);
  addEventListener('scroll', read, { passive: true });
  addEventListener('resize', function(){ fit(); size(); read(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  fit(); size(); read();
  if (reduce) draw(0);   // one still frame of the weather
  requestAnimationFrame(frame);
})();
</script>"""
