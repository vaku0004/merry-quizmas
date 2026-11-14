"""The home page of Victoria's Game Nights (/) and the privacy page (/privacy/).

From Python: home_page(published_games, today) and privacy_page().

Design D (her choice, Nov 14): made from her Google Stitch design on the Claude Design canvas: near-black ground,
Plus Jakarta Sans, one bright tile per game with the game's own art on a dark disc, real names, dates and texts.
"""
import datetime, html, json
from site_common import GA_HEAD, PAGE_EVENTS_JS, URL, BRAND, CONTACT_HREF
import games as G
import share as SH

e = lambda s: html.escape(s, quote=True)
# night = page ground, dusk = boxes, line = borders, bone = text, ash = muted text, ember = accent (lime). The share menu uses these too.
HUB = dict(night="#0c0c0e", dusk="#1b1b20", line="#27272e", line2="#3a3a44", bone="#ffffff", ash="#9898a4", dim="#2c2c34",
           ember="#cbff38", coral="#f45837", cyan="#25d5f2")
# The site's preview image and icons (tools/make_og.py) keep the original navy palette, so the published images stay as they are.
OG_HUB = dict(night="#111526", dusk="#1a1f36", cell="#232a47", line="#363f66", bone="#f4efe6", ash="#a9aec8",
              candle="#f0b44c", ember="#ffe2a3", good="#7cc39a", witch="#e77a95")
# Tile per game (Nov 14, her request: muted tones, a visible but soft gradient): a soft light patch top right over a
# gradient from a muted colour to one 30% darker, white text (each start colour
# checked for 4.6:1 or more), the game's bright colour as an accent (the "New" tag), a tag and one short line.
TILES = {
    "christmas":  ("#2b7f88", "#1e595f", "#25d5f2", "Christmas",         "Naughty or Nice, Krampus’s Bargain and a Christmas Eve wager."),
    "movies":     ("#ad5340", "#793a2d", "#f45837", "Any day",           "A plot twist, a popcorn bucket and a Final Cut wager."),
    "halloween":  ("#5e7a22", "#425518", "#cbff38", "Halloween",         "A black cat, a witch’s deal and a midnight wager."),
    "newyear":    ("#6a4cb0", "#4a357b", "#b18cff", "New Year’s Eve",    "A party popper, a fortune cookie and a Midnight Countdown wager."),
    "trivia":     ("#8c6a14", "#624a0e", "#ffd000", "Any day",           "A wild card, a mystery box and an all-in wager."),
    "decades":    ("#a63c55", "#742a3b", "#ff7a93", "’80s · ’90s · 2000s", "A tangled tape, a time machine and a time-capsule wager."),
    "valentines": ("#4f4aab", "#373478", "#9d98ff", "Valentine’s Day",   "Cupid’s Arrow, a box of chocolates and a love-letter wager."),
    "stpatricks": ("#22805f", "#185a42", "#3fe0a8", "St. Patrick’s Day", "A leprechaun’s trick, a rainbow and a pot-of-gold wager."),
}
# The game in season goes first, MM-DD to MM-DD (may wrap the year end).
FEATURE = {"halloween": ("10-01", "10-31"), "christmas": ("11-15", "12-25"), "newyear": ("12-26", "01-01"),
           "valentines": ("01-20", "02-14"), "stpatricks": ("02-10", "03-17")}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
HEART = ('<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 56 C14 43 6 33 6 22 C6 13 13 7 21 7 C26 7 30 10 32 14 '
         'C34 10 38 7 43 7 C51 7 58 13 58 22 C58 33 50 43 32 56 Z" fill="#e77a95"/></svg>')
ARROW = ('<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true">'
         '<path d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"/></svg>')
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800'
         + "".join(f"&family={g['gfont']}" for g in G.GAMES if "gfont" in g) + '&display=swap">')   # every tile's title font
# Tile colours: "juicy" (her choice, Nov 14, from PALETTES), "muted" (published earlier that day), "original" (each game's own dark palette with its glow; she tried it and went
# back), or a set from PALETTES. Preview one with the environment variable GN_TILES=<name>.
import os
TILE_COLORS = os.environ.get("GN_TILES", "juicy")
# Other colour sets tried on Nov 14 (start, end of the gradient); "dusty" and "juicy" use dark text, the others white. Contrast checked:
# white text 4.6:1 or more at both ends, dark text 4.8:1 or more.
PALETTES = {
    "jewel": {"christmas": ("#1f7a4f", "#0d3b2a"), "movies": ("#a3222f", "#4a0f18"), "halloween": ("#7b3fb0", "#2e1650"),
              "newyear": ("#2f3f9e", "#141a4a"), "trivia": ("#0f7a8a", "#083b44"), "decades": ("#8a2fb0", "#3a1260"),
              "valentines": ("#b02a5c", "#4f1028"), "stpatricks": ("#198346", "#0b3f22")},
    "duotone": {"christmas": ("#1e7a50", "#8a2a2a"), "movies": ("#a3222f", "#5e2a8a"), "halloween": ("#6a3aa8", "#a8501f"),
                "newyear": ("#2a3a9e", "#8a2a6a"), "trivia": ("#0f7a8a", "#5a3aa8"), "decades": ("#a02a8a", "#2a5aa8"),
                "valentines": ("#b02a5c", "#6a2a9a"), "stpatricks": ("#198346", "#8a6a14")},
    "dusty": {"christmas": ("#b6dccb", "#86bba5"), "movies": ("#ebbdaf", "#d69584"), "halloween": ("#d3c0ea", "#ae95d4"),
              "newyear": ("#bcc5ec", "#95a2de"), "trivia": ("#b0e0e6", "#83c6d0"), "decades": ("#e2bdec", "#c696d8"),
              "valentines": ("#f3bfcf", "#e195ad"), "stpatricks": ("#bce2c3", "#8fca9d")},
    # brighter, more distinct, by theme: frosty teal, movie gold, pumpkin, party violet, brainy blue, neon pink, heart red, clover green
    "juicy": {"christmas": ("#8ff0e2", "#2fd3c2"), "movies": ("#ffe07a", "#ffb72e"), "halloween": ("#ffc07a", "#ff8a3d"),
              "newyear": ("#cdb4ff", "#a079ff"), "trivia": ("#a8d4ff", "#5aa2ff"), "decades": ("#ffa8e4", "#ff5cc8"),
              "valentines": ("#ffaaae", "#ff6470"), "stpatricks": ("#c4f080", "#7fd447")},
}
# Title size per display font: wide or tall faces are scaled so every title fits its tile.
FONT_SCALE = {"Bungee": .66, "Limelight": .8, "Righteous": .82, "Eagle Lake": .72, "Lilita One": .95, "Pirata One": 1.08,
              "Mountains of Christmas": 1.0, "Yeseva One": .86}

CSS = """
:root{color-scheme:dark;--night:%(night)s;--dusk:%(dusk)s;--line:%(line)s;--line2:%(line2)s;--bone:%(bone)s;--ash:%(ash)s;--dim:%(dim)s;
 --ember:%(ember)s;--candle:%(ember)s;--coral:%(coral)s;--cyan:%(cyan)s;
 --f-ui:"Plus Jakarta Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--wrap:1200px}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--night);color:var(--bone);font-family:var(--f-ui);font-size:1rem;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:var(--ember);text-underline-offset:.18em}
a:hover{color:var(--bone)}
:focus-visible{outline:3px solid var(--ember);outline-offset:3px}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.wrap{max-width:var(--wrap);margin:0 auto;padding-inline:20px}
.up{text-transform:uppercase}
.site-head{border-bottom:1px solid #1c1c22}
.site-head .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding-block:14px}
.brand{display:flex;align-items:center;gap:8px;color:var(--bone);text-decoration:none;font-weight:800;font-size:.95rem;letter-spacing:-.01em;text-transform:uppercase}
.brand span{color:var(--ash)}
.dot{width:10px;height:10px;border-radius:50%%;background:var(--ember);flex:none}
.site-nav{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.site-nav a{color:#e4e4ea;text-decoration:none;font-size:.75rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;border:1px solid var(--dim);border-radius:8px;padding:8px 12px}
.site-nav a:hover{border-color:#55555f;color:var(--bone)}
.site-nav a.cta{background:var(--ember);border-color:var(--ember);color:var(--night);font-weight:800}
.site-nav a.cta:hover{filter:brightness(1.05)}
.hero{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:16px 48px;padding:40px 0 28px}
.hero h1{margin:0;flex:1 1 700px;font-weight:800;font-size:clamp(2.75rem,8vw,6rem);line-height:.9;letter-spacing:-.045em;text-transform:uppercase}
.hero h1 span,.big span{color:#64646f}
.hero p{margin:0;flex:1 1 320px;max-width:440px;font-weight:500;color:var(--ash)}
.hero.prose{display:block;max-width:46rem}
.hero.prose h1{font-size:clamp(2.5rem,6vw,4rem);margin:.1em 0 .4em}
.prose p{color:#c9c9d1;font-weight:500}
.eyebrow{font-weight:800;text-transform:uppercase;letter-spacing:.14em;font-size:.75rem;color:var(--ash);margin:0}
.bar{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:14px}
.bar h2{margin:0;font-size:.8rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase}
.bar span{font-size:.75rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ash)}
/* 2-3-3 on a computer: the first two tiles (the game in season and the next one) are wide, then rows of three */
.tiles{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:16px}
.tile{grid-column:span 2;--h:2rem;display:flex;flex-direction:column;gap:12px;padding:20px;border-radius:20px;
 background:radial-gradient(120%% 90%% at 100%% 0%%,rgba(255,255,255,.2),transparent 60%%),linear-gradient(200deg,var(--t-a),var(--t-b));color:#ffffff;--t-soft:rgba(0,0,0,.24);--t-rule:color-mix(in srgb,currentColor 24%%,transparent)}
.tile.ink-dark{color:#16141a;--t-soft:rgba(0,0,0,.12)}
.tile.ink-dark .play{background:#16141a;color:#ffffff}
.tile.ink-dark .play:hover{color:#ffffff}
.tile:nth-child(-n+2){grid-column:span 3;--h:2.7rem}
.tile:nth-child(-n+2) .disc{width:104px;height:104px}
.tile:nth-child(-n+2) .disc svg{width:74px;height:74px}
.tile .top{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}
.tile .disc{width:86px;height:86px;border-radius:50%%;background:rgba(12,12,14,.82);display:grid;place-items:center;flex:none}
.tile .disc svg{width:60px;height:60px}
.tile .tag{font-size:.68rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;padding:3px 8px;border-radius:6px;background:var(--t-soft);text-align:right}
.tile .tag.new{background:#0c0c0e;color:var(--t-acc)}
.tile h3{margin:6px 0 0;font-family:var(--t-font);font-weight:var(--t-w);font-size:calc(var(--h) * var(--t-fs));line-height:1.05}
.tile .blurb{margin:0;font-size:.92rem;font-weight:500;line-height:1.5;flex:1}
.tile .chips{display:flex;flex-wrap:wrap;gap:6px;margin:2px 0 0;padding:0;list-style:none}
.tile .chips li{border:1px solid color-mix(in srgb,currentColor 40%%,transparent);border-radius:999px;padding:2px 10px;font-size:.75rem;font-weight:600}
.tile .foot{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px 16px;border-top:1px solid var(--t-rule);padding-top:12px;margin-top:4px}
.tile .play{display:inline-flex;align-items:center;gap:8px;background:var(--t-acc);color:#0c0c0e;text-decoration:none;font-size:.8rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;border-radius:10px;padding:10px 14px}
.tile .play:hover{filter:brightness(1.08);color:#0c0c0e}
.tile .when{font-size:.75rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase}
.tile .links{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:.8rem;font-weight:600}
.tile .links a{color:inherit}
.tile .links a:hover{opacity:.8}
@media (max-width:900px){.tiles{grid-template-columns:repeat(2,minmax(0,1fr))}.tile,.tile:nth-child(-n+2){grid-column:auto;--h:2rem}
 .tile:nth-child(-n+2) .disc{width:86px;height:86px}.tile:nth-child(-n+2) .disc svg{width:60px;height:60px}}
@media (max-width:640px){.tiles{grid-template-columns:minmax(0,1fr)}}
.stats{margin-top:40px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;border-block:1px solid #1c1c22;padding:26px 0}
.stats b{display:block;font-size:clamp(1.9rem,5vw,3.25rem);font-weight:800;letter-spacing:-.03em;line-height:1}
.stats span{display:block;margin-top:8px;font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--ash)}
.split{margin-top:56px;display:flex;flex-wrap:wrap;gap:24px 56px;align-items:flex-start}
.split>div{flex:1 1 440px}
.split>:last-child{flex:999 1 560px;min-width:0}
.big{margin:0;font-weight:800;font-size:clamp(2.5rem,5vw,3.6rem);line-height:.92;letter-spacing:-.045em;text-transform:uppercase}
.split p.lead{margin:16px 0 0;max-width:420px;color:var(--ash);font-weight:500}
.steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}
.steps li{display:flex;gap:18px;align-items:flex-start;background:var(--dusk);border:1px solid var(--line);border-radius:20px;padding:18px 20px}
.steps .n{font-size:2.1rem;font-weight:800;line-height:1;flex:none}
.steps b{display:block;font-size:.95rem;font-weight:800;text-transform:uppercase;letter-spacing:-.01em}
.steps li span span{font-size:.9rem;color:var(--ash)}
.faq-h{margin:0;font-size:1.4rem;font-weight:800;text-transform:uppercase;letter-spacing:-.01em}
.faq-list{display:flex;flex-direction:column;gap:10px}
.faq-list details{background:var(--dusk);border:1px solid var(--line);border-radius:16px;padding:14px 16px}
.faq-list summary{cursor:pointer;font-size:.82rem;font-weight:800;text-transform:uppercase;letter-spacing:.02em}
.faq-list p{margin:8px 0 0;font-size:.9rem;color:var(--ash)}
.reach{margin-top:48px;display:flex;flex-wrap:wrap;gap:16px}
.reach .lime{flex:2 1 420px;background:var(--ember);color:var(--night);border-radius:22px;padding:26px;display:flex;flex-direction:column;gap:10px}
.reach .lime .pill{align-self:flex-start;font-size:.68rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;background:rgba(0,0,0,.1);border-radius:6px;padding:3px 8px}
.reach .lime h3{margin:0;font-size:1.5rem;font-weight:800;text-transform:uppercase;letter-spacing:-.02em;line-height:1.1}
.reach .lime p{margin:0;font-weight:500}
.reach .lime a{align-self:flex-start;margin-top:6px;background:var(--night);color:var(--bone);text-decoration:none;font-size:.82rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;border-radius:12px;padding:14px 22px}
.reach .lime a:hover{color:var(--ember)}
.reach .box{flex:1 1 300px;background:var(--dusk);border:1px solid var(--line);border-radius:22px;padding:26px;display:flex;flex-direction:column;gap:10px}
.reach .box h3{margin:0;font-size:1.1rem;font-weight:800;text-transform:uppercase;letter-spacing:-.01em}
.reach .box p{margin:0 0 6px;font-size:.9rem;color:var(--ash)}
.sbtn{display:inline-flex;align-items:center;gap:8px;background:transparent;color:var(--bone);border:1px solid var(--line2);border-radius:12px;padding:11px 16px;
 font:800 .8rem var(--f-ui);letter-spacing:.06em;text-transform:uppercase;cursor:pointer}
.sbtn:hover{border-color:var(--ember);color:var(--ember)}
.site-foot{margin-top:56px;border-top:1px solid #1c1c22;font-size:.82rem;color:var(--ash)}
.site-foot .wrap{display:flex;flex-wrap:wrap;gap:12px 24px;justify-content:space-between;align-items:center;padding-block:28px 40px}
.site-foot .brand span{color:var(--bone)}
.site-foot .dot{background:var(--coral)}
.site-foot nav{display:flex;flex-wrap:wrap;gap:8px 20px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.site-foot a{color:var(--ash);text-decoration:none}
.site-foot a:hover{color:var(--bone)}
.tile.orig{background:radial-gradient(90%% 80%% at 100%% 0%%,rgba(var(--o-glow),.32),transparent 70%%),var(--o-night);
 border:1px solid var(--o-line);color:var(--o-bone);box-shadow:0 0 0 1px rgba(var(--o-glow),.06),0 18px 40px rgba(0,0,0,.35)}
.tile.orig .disc{background:transparent;filter:drop-shadow(0 0 22px rgba(var(--o-glow),.5))}
.tile.orig .tag{background:rgba(255,255,255,.07);color:var(--o-ash)}
.tile.orig .tag.new{background:var(--o-candle);color:#0c0c0e}
.tile.orig h3{color:var(--o-ember)}
.tile.orig .blurb{color:var(--o-bone)}
.tile.orig .chips li{border-color:var(--o-line);color:var(--o-bone)}
.tile.orig .foot{border-top-color:var(--o-line)}
.tile.orig .play{background:var(--o-candle)}
.tile.orig .when,.tile.orig .links a{color:var(--o-ash)}
.tile.orig .links a:hover{color:var(--o-ember)}
@media (max-width:420px){.tile,.tile:nth-child(-n+2){padding:16px}.tile .disc,.tile:nth-child(-n+2) .disc{width:72px;height:72px}.tile .disc svg,.tile:nth-child(-n+2) .disc svg{width:50px;height:50px}}
""" % HUB


def _date_words(d):
    return f"{MONTHS[int(d[5:7]) - 1]} {int(d[8:10])}"


def _in_season(slug, today):
    if slug not in FEATURE:
        return False
    start, end = FEATURE[slug]; md = today[5:10]
    return start <= md <= end if start <= end else (md >= start or md <= end)


def _art(g):
    return G.art(g, g["icon"]) if "art_src" in g else HEART


def _tile(g, state, today):
    """state: "play" (on the site), "scheduled" (opens on its launch date), "soon"."""
    c1, c2, acc, tag, _ = TILES.get(g["slug"], ("#3a3a44", "#292930", "#cbff38", g["holiday"], g["card"]))
    fam, w = g["display"][3].replace('"', "'"), g["display"][1]
    style = f"--t-a:{c1};--t-b:{c2};--t-acc:{acc};--t-font:{fam};--t-w:{w};--t-fs:{FONT_SCALE.get(g['display'][0], 1)}"
    cls = "tile"
    if TILE_COLORS in PALETTES and g["slug"] in PALETTES[TILE_COLORS]:
        c1, c2 = PALETTES[TILE_COLORS][g["slug"]]
        style = style.replace(f"--t-a:{TILES[g['slug']][0]};--t-b:{TILES[g['slug']][1]}", f"--t-a:{c1};--t-b:{c2}")
        if TILE_COLORS in ("dusty", "juicy"):
            cls = "tile ink-dark"
    if TILE_COLORS == "original" and "rgb" in g:
        th = g["theme"]
        style += (f";--o-night:{th['night']};--o-line:{th['line']};--o-bone:{th['bone']};--o-ash:{th['ash']};--o-ember:{th['ember']};"
                  f"--o-candle:{th['candle']};--o-glow:{g['rgb']['glow']}")
        cls = "tile orig"
    new = state == "play" and g.get("launch") and 0 <= (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(g["launch"])).days <= 45
    tag_html = f'<span class="tag new">New · {e(tag)}</span>' if new else f'<span class="tag">{e(tag)}</span>'
    chips = "".join(f"<li>{e(t)}</li>" for _, t in g["chips"])
    head = (f'<div class="top"><span class="disc">{_art(g)}</span>{tag_html}</div>'
            f'<h3>{e(g["short"])}</h3><p class="blurb">{e(g["card"])}</p><ul class="chips">{chips}</ul>')
    if state == "play":
        slug, label = g["slug"], e(g.get("trivia_label", g["holiday"] + " trivia questions"))
        return (f'<article class="{cls}" style="{style}">{head}<div class="foot">'
                f'<a class="play" href="/{slug}/" data-play>Play {e(g["short"])} {ARROW}</a>'
                f'<span class="links"><a href="/{slug}/trivia-questions/">{label}</a><a href="/{slug}/how-to-host-a-game-night/">Host guide</a>'
                f'<a href="/{slug}/faq/">FAQ</a></span></div></article>')
    label = f"Opens {_date_words(g['launch'])}" if state == "scheduled" else "Coming soon"
    return f'<article class="{cls}" style="{style}">{head}<div class="foot"><span class="when">{label}</span></div></article>'


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
  <a class="brand" href="/"><i class="dot"></i>Victoria’s <span>Game Nights</span></a>
  <nav class="site-nav" aria-label="Main"><a href="/#how">How it works</a><a href="/#faq">FAQ</a><a class="cta" href="{CONTACT_HREF}" data-contact>Write to Victoria</a></nav>
</div></header>
<main id="main" class="wrap">
{body}
</main>
<footer class="site-foot"><div class="wrap">
  <a class="brand" href="/"><i class="dot"></i><span>Victoria’s Game Nights</span></a>
  <nav aria-label="Footer"><a href="/#games">Games</a><a href="/#how">How it works</a><a href="{CONTACT_HREF}" data-contact>Write to Victoria</a><a href="/privacy/">Privacy</a></nav>
  <span>Quiz games for office parties and team events, made in Regina, Saskatchewan.</span>
</div></footer>
{SH.WIDGET if 'data-gn-' in body else ''}
{PAGE_EVENTS_JS}
</body>
</html>
'''


def home_page(out_slugs, today):
    playable = [g for g in G.GAMES if g["slug"] in out_slugs]
    playable.sort(key=lambda g: not _in_season(g["slug"], today))          # the game in season first, the rest keep games.py order
    scheduled = sorted((g for g in G.GAMES if g["slug"] not in out_slugs and g["status"] != "soon"), key=lambda g: g.get("launch") or "")
    soon = [g for g in G.GAMES if g["slug"] not in out_slugs and g["status"] == "soon"]
    tiles = "\n".join([_tile(g, "play", today) for g in playable] + [_tile(g, "scheduled", today) for g in scheduled]
                      + [_tile(g, "soon", today) for g in soon])
    faq = "".join(f'<details{" open" if k == 0 else ""}><summary>{e(q)}</summary><p>{a}</p></details>' for k, (q, a) in enumerate(FAQ))
    colors = ["var(--ember)", "var(--coral)", "var(--cyan)", "var(--bone)"]
    steps = [("Open a game on the big screen", "Chrome or Edge on the laptop connected to the TV or projector. Press F11 for full screen."),
             ("Name 2 to 4 teams", "Mix departments, and put remote coworkers on teams with people in the room."),
             ("Let the narrator host", "Teams pick questions on a game-show board, think for 30 seconds and answer out loud. The game keeps score."),
             ("Finish with a wager", "One final question with secret bets, then a podium for the winning team.")]
    steps_html = "".join(f'<li><span class="n" style="color:{colors[k]}">0{k + 1}</span><span><b>{e(t)}</b><span>{e(d)}</span></span></li>'
                         for k, (t, d) in enumerate(steps))
    share = SH.buttons(URL, BRAND, SH.SITE_TEXT, URL + "og-image.png", "Share", "Bookmark", "site", "sbtn")
    body = f'''<section class="hero">
<h1>Game nights<br><span>for teams</span></h1>
<p>Quiz games for office parties and team events, for the holidays and any day of the year: one laptop, one big screen, a narrator who reads every question, and teams in the room and on the call. No sign-up, nothing to install.</p>
</section>

<section id="games" aria-labelledby="games-h">
<div class="bar"><h2 id="games-h">All quiz games</h2><span>{len(playable)} to play · {len(scheduled) + len(soon)} coming</span></div>
<div class="tiles">
{tiles}
</div>
</section>

<section class="stats" aria-label="At a glance">
<div><b>{len(G.GAMES)}</b><span>Games through the year</span></div>
<div><b>136</b><span>Narrated lines per game</span></div>
<div><b>0</b><span>Apps to install</span></div>
</section>

<section id="how" aria-labelledby="how-h" class="split">
<div><h2 id="how-h" class="big">Free to play<br><span>no sign-up</span></h2>
<p class="lead">Plug the laptop into the big screen, split the room into teams and let the narrator do the hosting. About an hour from start to podium.</p></div>
<ol class="steps">{steps_html}</ol>
</section>

<section id="faq" aria-labelledby="faq-h" class="split">
<div><h2 id="faq-h" class="faq-h">Frequently asked</h2><p class="lead" style="margin-top:4px">Everything about hosting one in your office.</p></div>
<div class="faq-list">{faq}</div>
</section>

<section class="reach" aria-label="Contact and share">
<div class="lime"><span class="pill">Custom games</span><h3>Want a quiz made for your office party?</h3>
<p>Questions, ideas or a game with your own office in it? Victoria reads every message.</p>
<a href="{CONTACT_HREF}" data-contact>Write to Victoria</a></div>
<div class="box"><h3>Planning a party later?</h3><p>Bookmark the site or send it to the person organizing it.</p>
<div>{share}</div></div>
</section>'''
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": URL + "#website", "url": URL, "name": BRAND, "inLanguage": "en"},
        {"@type": "ItemList", "name": "Games", "itemListElement": [
            {"@type": "ListItem", "position": k + 1, "url": f"{URL}{g['slug']}/", "name": g["name"]} for k, g in enumerate(playable)]},
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
