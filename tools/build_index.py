"""Wrap a game (artifact source) into a full HTML page.

python3 tools/build_index.py <src> <out> [--mobile]   plain page (used by the offline build)
From Python: game_page(game, src_html) gives the page for /<slug>/ on Victoria's Game Nights.
"""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_common import GA_HEAD, MOBILE_CSS, URL, BRAND, game_events_js
import games as G
import share as SH

BASE_CSS = "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>"


def _split(src):
    src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    i = src.index('<div id="app"></div>')
    return src[:i], src[i:]


def _doc(meta, head, body, mobile):
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{meta}
{BASE_CSS}
{head.strip()}
</head>
<body>
{body.strip()}
</body>
</html>
'''
    if mobile and 'id="nof-mobile"' not in page:
        page = page.replace("</head>", MOBILE_CSS + "\n</head>", 1)
    return page


def plain_page(src, mobile=False):
    head, body = _split(src)
    t = re.search(r"<title>(.*?)</title>", head, re.S).group(1)
    return _doc(f'<meta name="description" content="{html.escape(t)}: a quiz game for office parties, with a narrator.">', head, body, mobile)


def game_page(g, src):
    head, body = _split(src)
    e = lambda s: html.escape(s, quote=True)
    url = f"{URL}{g['slug']}/"
    og_img = f"{url}og-image.png"
    th = g["theme"]
    head = re.sub(r"<title>.*?</title>", f"<title>{g['title']}</title>", head, count=1, flags=re.S)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": URL + "#website", "url": URL, "name": BRAND, "inLanguage": "en"},
        {"@type": "WebApplication", "@id": url + "#game", "url": url, "name": g["name"], "alternateName": g["short"],
         "description": g["desc"], "image": og_img, "inLanguage": "en",
         "applicationCategory": "GameApplication", "genre": ["Trivia", "Quiz", "Party game"],
         "operatingSystem": "Any", "browserRequirements": "Requires JavaScript. Best in Chrome or Edge.",
         "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CAD"},
         "author": {"@type": "Person", "name": "Victoria"}, "isPartOf": {"@id": URL + "#website"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": BRAND, "item": URL},
            {"@type": "ListItem", "position": 2, "name": g["short"], "item": url}]},
    ]}
    meta = f'''{GA_HEAD}
<meta name="description" content="{e(g['desc'])}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Victoria">
<meta name="theme-color" content="{th['night']}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/{g['slug']}/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(BRAND)}">
<meta property="og:locale" content="en_CA">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(g['name'])}">
<meta property="og:description" content="{e(g['og_desc'])}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(g['name'])}: {e(g['og_alt'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(g['name'])}">
<meta name="twitter:description" content="{e(g['og_desc'])}">
<meta name="twitter:image" content="{og_img}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'''
    rules = "".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in g["rules"])
    # Readable without JavaScript (search engines, link previews). The game replaces it as soon as it starts.
    static = f'''<div id="app"><main class="nof-static" style="max-width:760px;margin:0 auto;padding:40px 16px;font-family:Georgia,serif;color:{th['bone']}">
<p style="font:700 .9rem system-ui,sans-serif"><a href="/" style="color:{th['ash']}">{BRAND}</a></p>
<p style="text-transform:uppercase;letter-spacing:.14em;font:800 .78rem system-ui,sans-serif;color:{th['ash']}">{g['eyebrow']}</p>
<h1 style="color:{th['ember']};font-size:3rem;line-height:1;margin:.2em 0">{g['name']}</h1>
<p>{g['intro']}</p>
<h2 style="color:{th['candle']}">How it plays</h2>
<ul>{rules}</ul>
<p>Works for 2–4 teams in the room and over a video call. No sign-up, no download.</p>
<noscript><p><strong>This game needs JavaScript.</strong> Please turn it on to play.</p></noscript>
</main></div>'''
    # Links to the content pages and the other games: on the start screen only, hidden while a game is on screen.
    links = "".join(f'<a href="/{g["slug"]}/{s}/">{g.get("trivia_label", "%s trivia questions" % g["holiday"]) if s == "trivia-questions" else t.replace("&", "&amp;")}</a>\n'
                    for s, t in G.PAGES)
    nav = f'''<nav class="nof-links" aria-label="More about the game">
{links}<a href="/">All games</a>
{SH.buttons(url, g["name"], g.get("og_desc") or g["desc"], url + "og-image.png", "Share this game", "Bookmark", g["slug"], "nof-sb")}
</nav>
<style>
.nof-links{{display:flex;flex-wrap:wrap;gap:6px 22px;justify-content:center;max-width:1400px;margin:0 auto;padding:8px 16px 36px;
  font-family:"Alegreya Sans",system-ui,sans-serif;font-weight:700;font-size:.95rem}}
.nof-links a{{color:{th['ash']};text-decoration:none}}
.nof-links a:hover,.nof-links a:focus-visible{{color:{th['ember']};text-decoration:underline}}
.nof-links[hidden]{{display:none!important}}
.nof-links .gn-share{{gap:6px 22px}}
.nof-sb{{display:inline-flex;align-items:center;gap:6px;background:none;border:0;padding:0;color:{th['ash']};font:inherit;cursor:pointer}}
.nof-sb:hover,.nof-sb:focus-visible{{color:{th['ember']};text-decoration:underline}}
</style>
<script>
(function(){{
  var nav = document.querySelector('.nof-links'), app = document.getElementById('app');
  var sync = function(){{ nav.hidden = !(app.querySelector('.setup') || app.querySelector('.nof-static')); }};
  new MutationObserver(sync).observe(app, {{ childList: true }}); sync();
}})();
</script>'''
    body = body.replace('<div id="app"></div>', static, 1)
    body = body.rstrip() + "\n" + nav + "\n" + SH.WIDGET + "\n" + game_events_js(g)
    return _doc(meta, head, body, True)


if __name__ == "__main__":
    src_path, out_path = sys.argv[1], sys.argv[2]
    open(out_path, "w", encoding="utf-8").write(plain_page(open(src_path, encoding="utf-8").read(), "--mobile" in sys.argv[3:]))
