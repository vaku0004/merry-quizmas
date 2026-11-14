"""The home page of Victoria's Game Nights (/) and the privacy page (/privacy/).

From Python: home_page(published_games, today) and privacy_page().
"""
import datetime, html, json
from site_common import GA_HEAD, PAGE_EVENTS_JS, URL, BRAND, CONTACT_HREF
import games as G
import share as SH

e = lambda s: html.escape(s, quote=True)
# Light page (her choice, Nov 13: design A "Game Night" from the Claude Design canvas, soft grey ground); game cards keep each game's own colours.
# Names kept from the dark version: night = page ground, dusk = boxes, bone = text, ash = muted text, ember = headings, candle = accent.
HUB = dict(night="#f1f1ee", dusk="#ffffff", cell="#f7f7f4", line="#dedcd6", line2="#c9c6bd", bone="#222220", ash="#605e59",
           candle="#a9631a", ember="#26233a", link="#8a5512", good="#3f8a5a", witch="#c4486b")
# A game is featured (wide card at the top) while today falls in its season, MM-DD to MM-DD (may wrap the year end).
FEATURE = {"halloween": ("10-01", "10-31"), "christmas": ("11-15", "12-25"), "newyear": ("12-26", "01-01"),
           "valentines": ("01-20", "02-14"), "stpatricks": ("02-10", "03-17")}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
HEART = ('<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 56 C14 43 6 33 6 22 C6 13 13 7 21 7 C26 7 30 10 32 14 '
         'C34 10 38 7 43 7 C51 7 58 13 58 22 C58 33 50 43 32 56 Z" fill="#e77a95"/><path d="M17 16 C13 18 12 22 13 26" '
         'stroke="#ffd1dc" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/></svg>')
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,400;0,700;0,800;1,400;1,700'
         '&family=Alegreya+Sans:wght@400;700;800' + "".join(f"&family={g['gfont']}" for g in G.GAMES if "gfont" in g) + '&display=swap">')   # every card's title font

CSS = """
:root{color-scheme:light;--night:%(night)s;--dusk:%(dusk)s;--cell:%(cell)s;--line:%(line)s;--line2:%(line2)s;--bone:%(bone)s;--ash:%(ash)s;
 --candle:%(candle)s;--ember:%(ember)s;--link:%(link)s;--good:%(good)s;--heart:%(witch)s;
 --f-text:"Alegreya",Georgia,serif;--f-ui:"Alegreya Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--wrap:1120px}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--night);color:var(--bone);font-family:var(--f-text);font-size:1.125rem;line-height:1.6}
a{color:var(--link);text-underline-offset:.18em}
a:hover{color:var(--ember)}
:focus-visible{outline:3px solid var(--candle);outline-offset:3px}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.wrap{max-width:var(--wrap);margin:0 auto;padding-inline:16px}
.site-head{border-bottom:1px solid var(--line);background:var(--night)}
.site-head .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px 16px;min-height:64px;flex-wrap:wrap;padding-block:10px}
.brand{font-family:var(--f-text);font-weight:800;font-style:italic;font-size:1.4rem;color:var(--ember);text-decoration:none}
.site-nav{display:flex;align-items:center;gap:6px 22px;flex-wrap:wrap;font-family:var(--f-ui);font-weight:700;font-size:1rem}
.site-nav a{color:var(--bone);text-decoration:none}
.site-nav a:hover{color:var(--candle)}
.site-nav a.pill{border:1px solid var(--line2);border-radius:999px;padding:.4em 1em;background:var(--dusk)}
.hero{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px 40px;padding:40px 0 28px}
.hero>div{flex:1 1 560px;min-width:0}
.hero.prose{display:block;max-width:46rem}
.eyebrow{font-family:var(--f-ui);font-weight:800;text-transform:uppercase;letter-spacing:.14em;font-size:.8rem;color:var(--ash);margin:0}
h1{font-weight:800;font-size:clamp(2.5rem,6vw,4rem);line-height:1;margin:.15em 0 .3em;color:var(--ember)}
h1 i{font-style:italic;color:var(--candle)}
.lede{font-size:1.25rem;margin:0;max-width:40rem}
.note{font-family:var(--f-ui);font-size:.95rem;margin:0}
.muted{color:var(--ash)}
h2{font-weight:800;font-size:clamp(1.8rem,4vw,2.4rem);line-height:1.1;margin:2em 0 .5em;color:var(--ember)}
.games{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%%,320px),1fr));gap:20px;margin:20px 0 0}
.game{position:relative;display:flex;flex-direction:column;border:1px solid var(--g-line);border-radius:20px;padding:24px;
 background:radial-gradient(ellipse 80%% 70%% at 100%% 0%%,rgba(var(--g-glow),.22),transparent 65%%),var(--g-night);color:var(--g-bone);overflow:hidden}
.game a{color:var(--g-ember)}
.game>svg{width:72px;height:72px;position:absolute;right:20px;top:18px;filter:drop-shadow(0 0 20px rgba(var(--g-glow),.45))}
.game .when{font-family:var(--f-ui);font-weight:800;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--g-ash);margin:0 90px 0 0}
.game h3{font-family:var(--g-font);font-weight:var(--g-w);font-size:2.2rem;line-height:1.05;margin:12px 90px 10px 0;color:var(--g-ember)}
.game p.blurb{margin:0 0 18px;flex:1;font-size:1.05rem}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5em;font-family:var(--f-ui);font-weight:800;text-decoration:none;
 border:1px solid var(--line2);background:var(--dusk);color:var(--bone);padding:.65em 1.2em;border-radius:999px;line-height:1.2;font-size:1rem}
.btn:hover{border-color:var(--candle);color:var(--ember)}
.btn.primary{background:var(--g-candle,var(--candle));border-color:transparent;color:#17121c}
.btn.primary:hover{filter:brightness(1.08);color:#17121c}
.btn.big{font-size:1.15rem;padding:.8em 1.6em}
.game .links{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:14px;font-family:var(--f-ui);font-size:.95rem}
.game .links a{color:var(--g-ash)}
.game.soon{border-style:dashed}
.game.soon .btn{background:transparent;border:1px dashed var(--g-line);color:var(--g-ash);cursor:default;align-self:flex-start}
.game.feature{grid-column:1/-1;flex-direction:row;flex-wrap:wrap;align-items:center;gap:20px 36px;padding:32px}
.game.feature>svg{position:static;flex:0 0 170px;width:170px;height:170px}
.game.feature .body{flex:1 1 480px;min-width:0;display:flex;flex-direction:column}
.game.feature .when{margin:0}
.game.feature h3{font-size:clamp(2.6rem,5vw,3.8rem);margin:10px 0 12px}
.game.feature p.blurb{font-size:1.2rem;max-width:40rem;flex:none}
.game.feature .actions{display:flex;flex-wrap:wrap;align-items:center;gap:12px 20px;font-family:var(--f-ui);font-weight:700}
.game.feature .actions a:not(.btn){color:var(--g-ember)}
.badge{display:inline-block;background:var(--g-candle);color:#17121c;border-radius:999px;padding:2px 10px;margin-right:10px;letter-spacing:.08em}
.soon-h{font-family:var(--f-ui);font-weight:800;text-transform:uppercase;letter-spacing:.14em;font-size:.8rem;color:var(--ash);margin:34px 0 12px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%%,240px),1fr));gap:14px}
.tile{display:flex;align-items:center;gap:14px;border:1px solid var(--g-line);border-radius:16px;padding:14px 16px;background:var(--g-night)}
.tile svg{flex:none;width:44px;height:44px}
.tile b{display:block;font-family:var(--g-font);font-weight:var(--g-w);font-size:1.2rem;line-height:1.15;color:var(--g-ember)}
.tile span{font-family:var(--f-ui);font-size:.88rem;color:var(--g-ash)}
.reach{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%%,340px),1fr));gap:16px;margin:48px 0 0}
.reach>div{border:1px solid var(--line);border-radius:20px;padding:22px 24px;background:var(--dusk)}
.reach-h{font-weight:800;font-size:1.35rem;color:var(--ember);margin:0 0 4px;line-height:1.2}
.reach .muted{font-family:var(--f-ui);font-size:1rem;margin:0 0 16px}
.reach-btns{display:flex;flex-wrap:wrap;gap:10px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%%,240px),1fr));gap:16px;padding:0;margin:0;list-style:none;counter-reset:s}
.steps li{border:1px solid var(--line);border-radius:16px;padding:20px;background:var(--dusk);font-family:var(--f-ui);font-size:1rem;line-height:1.45}
.steps li::before{counter-increment:s;content:counter(s);display:block;font-family:var(--f-text);font-weight:800;font-size:2rem;color:var(--candle);line-height:1;margin-bottom:6px}
.steps b{display:block;font-size:1.1rem;margin-bottom:4px;color:var(--bone)}
.faq-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%%,420px),1fr));gap:4px 48px}
.faq h3{font-family:var(--f-ui);font-size:1.1rem;margin:1.2em 0 .2em}
.faq p{margin:0}
.prose{max-width:46rem}
.site-foot{border-top:1px solid var(--line);margin-top:72px;padding:28px 0 40px;font-family:var(--f-ui);font-size:.95rem;color:var(--ash)}
.site-foot nav{display:flex;flex-wrap:wrap;gap:6px 18px;margin-bottom:10px}
.site-foot a{color:var(--ash)}
@media (max-width:520px){.game>svg{width:60px;height:60px}.game h3{font-size:1.9rem;margin-right:70px}.game .when{margin-right:70px}
 .game.feature{padding:24px}.game.feature>svg{flex-basis:110px;width:110px;height:110px}}
""" % HUB


def _gvars(g):
    th = g["theme"]
    if "rgb" not in g:
        return (f"--g-night:{th['night']};--g-line:{th['line']};--g-bone:#f6e8ee;--g-ash:#d6a9b8;--g-ember:{th['ember']};"
                f"--g-candle:{th['candle']};--g-glow:231,122,149;--g-font:var(--f-text);--g-w:800")
    return (f"--g-night:{th['night']};--g-line:{th['line']};--g-bone:{th['bone']};--g-ash:{th['ash']};--g-ember:{th['ember']};"
            f"--g-candle:{th['candle']};--g-glow:{g['rgb']['glow']};--g-font:{g['display'][3]};--g-w:{g['display'][1]}").replace('"', "'")


def _date_words(d):
    return f"{MONTHS[int(d[5:7]) - 1]} {int(d[8:10])}"


def _in_season(slug, today):
    if slug not in FEATURE:
        return False
    start, end = FEATURE[slug]; md = today[5:10]
    return start <= md <= end if start <= end else (md >= start or md <= end)


def _links(g):
    slug, label = g["slug"], e(g.get("trivia_label", g["holiday"] + " trivia questions"))
    return (f'<a href="/{slug}/trivia-questions/">{label}</a>'
            f'<a href="/{slug}/how-to-host-a-game-night/">Host guide</a><a href="/{slug}/faq/">FAQ</a>')


def _art(g):
    return G.art(g, g["icon"]) if "art_src" in g else HEART


def _featured(g, today):
    new = ""
    if g.get("launch"):
        age = (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(g["launch"])).days
        new = '<span class="badge">New</span>' if 0 <= age <= 45 else ""
    return f'''<article class="game feature" style="{_gvars(g)}">{_art(g)}
<div class="body">
<p class="when">{new}{e(g['holiday'])} · free to play</p>
<h3>{e(g['short'])}</h3>
<p class="blurb">{e(g['card'])}</p>
<div class="actions"><a class="btn primary big" href="/{g['slug']}/" data-play>Play {e(g['short'])}</a>{_links(g)}</div>
</div>
</article>'''


def _card(g):
    return f'''<article class="game" style="{_gvars(g)}">{_art(g)}
<p class="when">{e(g['holiday'])} · free to play</p>
<h3>{e(g['short'])}</h3>
<p class="blurb">{e(g['card'])}</p>
<div><a class="btn primary" href="/{g['slug']}/" data-play>Play {e(g['short'])}</a></div>
<div class="links">{_links(g)}</div>
</article>'''


def _scheduled(g):
    return f'''<article class="game soon" style="{_gvars(g)}">{_art(g)}
<p class="when">{e(g['holiday'])} · opens {_date_words(g['launch'])}</p>
<h3>{e(g['short'])}</h3>
<p class="blurb">{e(g['card'])}</p>
<span class="btn" aria-disabled="true">Opens {_date_words(g['launch'])}</span>
</article>'''


def _tile(g):
    return f'''<div class="tile" style="{_gvars(g)}">{_art(g)}<div><b>{e(g['short'])}</b><span>{e(g['holiday'])}</span></div></div>'''


FAQ = [
    ("How much do the games cost?", "The games on this site can be played for free right now: open a game, name your teams and play, with no account and no ads. Some games, question packs or custom office editions may become paid later, and anything paid will be clearly marked."),
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
  <nav class="site-nav" aria-label="Main"><a href="/#games">Games</a><a href="/#how">How it works</a><a href="/#faq">FAQ</a><a class="pill" href="{CONTACT_HREF}" data-contact>Write to Victoria</a></nav>
</div></header>
<main id="main" class="wrap">
{body}
</main>
<footer class="site-foot"><div class="wrap">
  <nav aria-label="Footer"><a href="/">All games</a><a href="{CONTACT_HREF}" data-contact>Write to Victoria</a><a href="/privacy/">Privacy</a></nav>
  <span>{e(BRAND)} · quiz games for office parties and team events, made in Regina, Saskatchewan.</span>
</div></footer>
{SH.WIDGET if 'data-gn-' in body else ''}
{PAGE_EVENTS_JS}
</body>
</html>
'''


def home_page(out_slugs, today):
    playable = [g for g in G.GAMES if g["slug"] in out_slugs]
    featured = next((g for g in playable if _in_season(g["slug"], today)), None)
    regular = [g for g in playable if g is not featured]
    scheduled = sorted((g for g in G.GAMES if g["slug"] not in out_slugs and g["status"] != "soon"), key=lambda g: g.get("launch") or "")
    soon = [g for g in G.GAMES if g["slug"] not in out_slugs and g["status"] == "soon"]
    cards = "\n".join(([_featured(featured, today)] if featured else []) + [_card(g) for g in regular] + [_scheduled(g) for g in scheduled])
    soon_block = f'''<h3 class="soon-h">Coming soon</h3>
<div class="tiles">
{"".join(_tile(g) for g in soon)}
</div>''' if soon else ""
    live = playable
    faq = "".join(f"<div><h3>{e(q)}</h3><p>{a}</p></div>" for q, a in FAQ)
    body = f'''<section class="hero">
<div>
<p class="eyebrow">Team games for the big screen</p>
<h1>Victoria’s <i>Game Nights</i></h1>
<p class="lede">Quiz games for office parties and team events, for the holidays and any day of the year: one laptop, one big screen, a narrator who reads every question, and teams in the room and on the call.</p>
</div>
<p class="note muted">No sign-up · no download · nothing for players to install</p>
</section>

<section id="games" aria-labelledby="games-h"><h2 id="games-h" class="sr-only">Pick a game</h2>
<div class="games">
{cards}
</div>
{soon_block}</section>

<section class="reach" aria-label="Share and contact">
<div><p class="reach-h">Planning a party later?</p><p class="muted">Bookmark the site or send it to the person organizing it.</p>
<div class="reach-btns">{SH.buttons(URL, BRAND, SH.SITE_TEXT, URL + "og-image.png", "Share", "Bookmark")}</div></div>
<div><p class="reach-h">Questions or a custom game?</p><p class="muted">Ideas, or a game made for your office? Victoria reads every message.</p>
<div class="reach-btns"><a class="btn" href="{CONTACT_HREF}" data-contact>Write to Victoria</a></div></div>
</section>

<section id="how" aria-labelledby="how-h"><h2 id="how-h">How a game night works</h2>
<ol class="steps">
<li><b>Open a game on the big screen</b>Chrome or Edge on the laptop connected to the TV or projector. Press F11 for full screen.</li>
<li><b>Name 2 to 4 teams</b>Mix departments, and put remote coworkers on teams with people in the room.</li>
<li><b>Let the narrator host</b>Teams pick questions on a game-show board, think for 30 seconds and answer out loud. The game keeps score.</li>
<li><b>Finish with a wager</b>One final question with secret bets, then a podium for the winning team. About an hour in total.</li>
</ol></section>

<section id="faq" aria-labelledby="faq-h" class="faq"><h2 id="faq-h">Questions</h2>
<div class="faq-grid">{faq}</div>
</section>'''
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": URL + "#website", "url": URL, "name": BRAND, "inLanguage": "en"},
        {"@type": "ItemList", "name": "Games", "itemListElement": [
            {"@type": "ListItem", "position": k + 1, "url": f"{URL}{g['slug']}/", "name": g["name"]} for k, g in enumerate(live)]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]}
    return _shell(f"{BRAND} · Quiz Games for Office Parties and Teams",
                  "Trivia games for office parties and hybrid teams, for the holidays and any day of the year: a game-show board on the big screen, a narrator and teams in the room and on the call.",
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
