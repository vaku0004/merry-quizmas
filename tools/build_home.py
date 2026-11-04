"""The home page of Victoria's Game Nights (/) and the privacy page (/privacy/).

From Python: home_page(published_games, today) and privacy_page().
"""
import html, json
from site_common import GA_HEAD, PAGE_EVENTS_JS, URL, BRAND
import games as G

e = lambda s: html.escape(s, quote=True)
HUB = dict(night="#111526", dusk="#1a1f36", cell="#232a47", line="#363f66", bone="#f4efe6", ash="#a9aec8",
           candle="#f0b44c", ember="#ffe2a3", good="#7cc39a", witch="#e77a95")
HEART = ('<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 56 C14 43 6 33 6 22 C6 13 13 7 21 7 C26 7 30 10 32 14 '
         'C34 10 38 7 43 7 C51 7 58 13 58 22 C58 33 50 43 32 56 Z" fill="#e77a95"/><path d="M17 16 C13 18 12 22 13 26" '
         'stroke="#ffd1dc" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/></svg>')
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,400;0,700;0,800;1,400;1,700'
         '&family=Alegreya+Sans:wght@400;700;800&family=Pirata+One&family=Mountains+of+Christmas:wght@700&display=swap">')

CSS = """
:root{color-scheme:dark;--night:%(night)s;--dusk:%(dusk)s;--cell:%(cell)s;--line:%(line)s;--bone:%(bone)s;--ash:%(ash)s;
 --candle:%(candle)s;--ember:%(ember)s;--good:%(good)s;--heart:%(witch)s;
 --f-text:"Alegreya",Georgia,serif;--f-ui:"Alegreya Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--wrap:1120px}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--night);color:var(--bone);font-family:var(--f-text);font-size:1.125rem;line-height:1.6;
 background-image:radial-gradient(ellipse 55%% 45%% at 85%% -10%%,rgba(240,180,76,.16),transparent 70%%),
 radial-gradient(ellipse 60%% 45%% at 0%% 105%%,rgba(231,122,149,.12),transparent 70%%);background-attachment:fixed}
a{color:var(--ember);text-underline-offset:.18em}
a:hover{color:var(--candle)}
:focus-visible{outline:3px solid var(--ember);outline-offset:3px}
.wrap{max-width:var(--wrap);margin:0 auto;padding-inline:16px}
.site-head{border-bottom:1px solid var(--line)}
.site-head .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:64px;flex-wrap:wrap}
.brand{font-family:var(--f-text);font-weight:800;font-style:italic;font-size:1.35rem;color:var(--ember);text-decoration:none}
.site-nav{display:flex;gap:4px 18px;flex-wrap:wrap;font-family:var(--f-ui);font-weight:700;font-size:.98rem}
.site-nav a{color:var(--bone);text-decoration:none}
.site-nav a:hover{color:var(--ember)}
.hero{padding:64px 0 28px;max-width:46rem}
.eyebrow{font-family:var(--f-ui);font-weight:800;text-transform:uppercase;letter-spacing:.14em;font-size:.8rem;color:var(--ash);margin:0}
h1{font-weight:800;font-size:clamp(2.6rem,7vw,4.4rem);line-height:1;margin:.2em 0 .35em;color:var(--ember)}
h1 i{font-style:italic;color:var(--candle)}
.lede{font-size:1.3rem;margin:0 0 .6em}
.muted{color:var(--ash)}
h2{font-weight:800;font-size:clamp(1.8rem,4vw,2.4rem);line-height:1.1;margin:2em 0 .5em;color:var(--ember)}
.games{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%%,440px),1fr));gap:20px;margin:18px 0 0}
.game{position:relative;display:flex;flex-direction:column;border:1px solid var(--g-line);border-radius:20px;padding:26px 24px 24px;
 background:radial-gradient(ellipse 80%% 70%% at 100%% 0%%,rgba(var(--g-glow),.22),transparent 65%%),var(--g-night);color:var(--g-bone);overflow:hidden}
.game svg{width:96px;height:96px;position:absolute;right:20px;top:20px;filter:drop-shadow(0 0 24px rgba(var(--g-glow),.45))}
.game .when{font-family:var(--f-ui);font-weight:800;font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--g-ash);margin:0 120px 0 0}
.game h3{font-family:var(--g-font);font-weight:var(--g-w);font-size:2.4rem;line-height:1;margin:10px 120px 12px 0;color:var(--g-ember)}
.game p.blurb{margin:0 0 18px;flex:1}
.game .chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 20px;padding:0;list-style:none;font-family:var(--f-ui);font-size:.9rem}
.game .chips li{border:1px solid var(--g-line);border-radius:999px;padding:2px 10px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5em;font-family:var(--f-ui);font-weight:800;text-decoration:none;
 border:1px solid var(--line);background:var(--dusk);color:var(--bone);padding:.65em 1.2em;border-radius:999px;line-height:1.2}
.btn.primary{background:var(--g-candle,var(--candle));border-color:transparent;color:#17121c}
.btn.primary:hover{filter:brightness(1.08);color:#17121c}
.game .links{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:14px;font-family:var(--f-ui);font-size:.95rem}
.game .links a{color:var(--g-ash)}
.game.soon{border-style:dashed}
.soon-h{font-family:var(--f-ui);font-weight:800;text-transform:uppercase;letter-spacing:.14em;font-size:.85rem;color:var(--ash);margin:34px 0 12px}
.games.small{grid-template-columns:repeat(auto-fit,minmax(min(100%%,300px),1fr));margin-top:0}
.games.small .game h3{font-size:2rem}
.games.small .game svg{width:76px;height:76px}
.game.soon .btn{background:transparent;border:1px dashed var(--g-line);color:var(--g-ash);cursor:default}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%%,240px),1fr));gap:16px;padding:0;margin:0;list-style:none;counter-reset:s}
.steps li{border:1px solid var(--line);border-radius:16px;padding:18px 20px;background:rgba(26,31,54,.7);font-family:var(--f-ui);font-size:1rem;line-height:1.45}
.steps li::before{counter-increment:s;content:counter(s);display:block;font-family:var(--f-text);font-weight:800;font-size:2rem;color:var(--candle);line-height:1;margin-bottom:6px}
.steps b{display:block;font-size:1.1rem;margin-bottom:4px;color:var(--bone)}
.faq h3{font-family:var(--f-ui);font-size:1.1rem;margin:1.4em 0 .2em}
.faq p{margin:0;max-width:46rem}
.prose{max-width:46rem}
.site-foot{border-top:1px solid var(--line);margin-top:72px;padding:28px 0 40px;font-family:var(--f-ui);font-size:.95rem;color:var(--ash)}
.site-foot nav{display:flex;flex-wrap:wrap;gap:6px 18px;margin-bottom:10px}
.site-foot a{color:var(--ash)}
@media (max-width:520px){.game svg{width:72px;height:72px}.game h3{font-size:2rem;margin-right:84px}.game .when{margin-right:84px}}
""" % HUB


def _gvars(g):
    th = g["theme"]
    if g["status"] == "soon":
        return (f"--g-night:{th['night']};--g-line:{th['line']};--g-bone:#f6e8ee;--g-ash:#d6a9b8;--g-ember:{th['ember']};"
                f"--g-candle:{th['candle']};--g-glow:231,122,149;--g-font:var(--f-text);--g-w:800")
    return (f"--g-night:{th['night']};--g-line:{th['line']};--g-bone:{th['bone']};--g-ash:{th['ash']};--g-ember:{th['ember']};"
            f"--g-candle:{th['candle']};--g-glow:{g['rgb']['glow']};--g-font:{g['display'][3]};--g-w:{g['display'][1]}").replace('"', "'")


def _card(g, out):
    if g["status"] == "soon":
        return f'''<article class="game soon" style="{_gvars(g)}">{HEART}
<p class="when">{e(g['holiday'])} · {e(g['coming'])}</p>
<h3>Coming soon</h3>
<p class="blurb">{e(g['card'])}</p>
<span class="btn" aria-disabled="true">{e(g['coming'])}</span>
</article>'''
    if not out:
        d = g["launch"]
        month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][int(d[5:7]) - 1]
        return f'''<article class="game soon" style="{_gvars(g)}">{G.art(g, g['icon'])}
<p class="when">{e(g['holiday'])} · coming {month} {int(d[8:10])}</p>
<h3>{e(g['short'])}</h3>
<p class="blurb">{e(g['card'])}</p>
<span class="btn" aria-disabled="true">Opens {month} {int(d[8:10])}</span>
</article>'''
    chips = "".join(f"<li>{e(t)}</li>" for _, t in g["chips"])
    return f'''<article class="game" style="{_gvars(g)}">{G.art(g, g['icon'])}
<p class="when">{e(g['holiday'])} · free to play</p>
<h3>{e(g['short'])}</h3>
<p class="blurb">{e(g['card'])}</p>
<ul class="chips">{chips}</ul>
<div><a class="btn primary" href="/{g['slug']}/" data-play>Play {e(g['short'])}</a></div>
<div class="links"><a href="/{g['slug']}/trivia-questions/">{e(g['holiday'])} trivia questions</a><a href="/{g['slug']}/how-to-host-a-game-night/">Host guide</a><a href="/{g['slug']}/faq/">FAQ</a></div>
</article>'''


FAQ = [
    ("Are the games really free?", "Yes. Open a game, name your teams and play. No account, no download, no ads."),
    ("What do we need?", "A computer with Chrome or Edge, a big screen or projector and speakers. Players only need their voices, and paper and pens for the final round."),
    ("Can remote coworkers play?", "Yes. Share the game in Teams, Zoom or Google Meet with computer sound on, and mix remote players into teams with people in the room. Each game has a page on how to set it up."),
    ("How many people can play?", "2 to 4 teams, ideally 6 to 20 people. With a bigger group, make bigger teams."),
    ("Can I change the questions?", "Yes. Every game has a question editor, so you can add questions about your own office."),
]


def _shell(title, desc, canonical, body, ld=None, og_img=None):
    og_img = og_img or URL + "og-image.png"
    ld_tag = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace("</", "<\\/")}</script>' if ld else ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{GA_HEAD}
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="{HUB['night']}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(BRAND)}">
<meta property="og:locale" content="en_CA">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_img}">
{FONTS}
<style>{CSS}</style>
{ld_tag}
</head>
<body>
<header class="site-head"><div class="wrap">
  <a class="brand" href="/">{e(BRAND)}</a>
  <nav class="site-nav" aria-label="Main"><a href="/#games">Games</a><a href="/#how">How it works</a><a href="/#faq">FAQ</a></nav>
</div></header>
<main id="main" class="wrap">
{body}
</main>
<footer class="site-foot"><div class="wrap">
  <nav aria-label="Footer"><a href="/">All games</a><a href="/privacy/">Privacy</a></nav>
  <span>{e(BRAND)} · free quiz games for office parties and team events, made in Regina, Saskatchewan.</span>
</div></footer>
{PAGE_EVENTS_JS}
</body>
</html>
'''


def home_page(out_slugs, today):
    playable = [g for g in G.GAMES if g["slug"] in out_slugs]
    upcoming = [g for g in G.GAMES if g["slug"] not in out_slugs]
    cards = "\n".join(_card(g, True) for g in playable)
    soon = "\n".join(_card(g, False) for g in upcoming)
    soon_block = f'''<h3 class="soon-h">Coming soon</h3>
<div class="games small">
{soon}
</div>''' if upcoming else ""
    live = [g for g in G.GAMES if g["slug"] in out_slugs]
    faq = "".join(f"<h3>{e(q)}</h3><p>{a}</p>" for q, a in FAQ)
    body = f'''<section class="hero">
<p class="eyebrow">Free team games for the big screen</p>
<h1>Victoria’s <i>Game Nights</i></h1>
<p class="lede">Holiday quiz games for office parties and team events. One laptop, one big screen, a narrator who reads every question, and teams playing in the room and on the video call.</p>
<p class="muted">No sign-up, no download, nothing for players to install.</p>
</section>

<section id="games" aria-labelledby="games-h"><h2 id="games-h" style="margin-top:.6em">Pick a game</h2>
<div class="games">
{cards}
</div>
{soon_block}</section>

<section id="how" aria-labelledby="how-h"><h2 id="how-h">How a game night works</h2>
<ol class="steps">
<li><b>Open a game on the big screen</b>Chrome or Edge on the laptop connected to the TV or projector. Press F11 for full screen.</li>
<li><b>Name 2 to 4 teams</b>Mix departments, and put remote coworkers on teams with people in the room.</li>
<li><b>Let the narrator host</b>Teams pick questions on a game-show board, think for 30 seconds and answer out loud. The game keeps score.</li>
<li><b>Finish with a wager</b>One final question with secret bets, then a podium for the winning team. About an hour in total.</li>
</ol></section>

<section id="faq" aria-labelledby="faq-h" class="faq"><h2 id="faq-h">Questions</h2>
{faq}
</section>'''
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": URL + "#website", "url": URL, "name": BRAND, "inLanguage": "en"},
        {"@type": "ItemList", "name": "Games", "itemListElement": [
            {"@type": "ListItem", "position": k + 1, "url": f"{URL}{g['slug']}/", "name": g["name"]} for k, g in enumerate(live)]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]}
    return _shell(f"{BRAND} · Free Holiday Quiz Games for Office Parties",
                  "Free holiday trivia games for office parties and hybrid teams: a game-show board on the big screen, a narrator and teams in the room and on the call.",
                  URL, body, ld)


def privacy_page():
    body = '''<section class="hero prose">
<p class="eyebrow">Privacy</p>
<h1>Privacy</h1>
<p>This site uses Google Analytics to count visits and to see which parts of the games are used, for example how many games are started and finished. It does not collect team names, answers or anything typed into the question editor, and it does not use advertising cookies.</p>
<p>For visitors in the European Economic Area, the UK, Switzerland and Quebec, analytics cookies are turned off and Google receives only cookieless signals. You can also block analytics with any browser privacy setting or extension; the games work the same.</p>
<p>Each game saves its progress, your edited questions and voice settings in your own browser (local storage) so you can continue after closing the tab. That information never leaves your computer.</p>
<p>The games have no accounts and no sign-up, and nothing is sold or shared.</p>
</section>'''
    return _shell(f"Privacy · {BRAND}", "How Victoria’s Game Nights handles data: anonymous analytics only, no ads, no accounts.", URL + "privacy/", body)


def not_found_page():
    body = '''<section class="hero prose">
<p class="eyebrow">Page not found</p>
<h1>This page has wandered off</h1>
<p>The address may have changed. All the games are on the <a href="/">home page</a>.</p>
</section>'''
    return _shell(f"Page not found · {BRAND}", "This page does not exist.", URL, body).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
