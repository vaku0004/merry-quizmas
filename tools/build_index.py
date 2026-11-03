"""Wrap the game (artifact source) into a full HTML page.

python3 build_index.py <src> <out>          plain page (used by the offline build)
python3 build_index.py <src> <out> --site   the public website: site name, search and social tags, icons
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_common import GA_HEAD, GAME_EVENTS_JS, MOBILE_CSS, URL, NAME, SHORT

src_path, out_path = sys.argv[1], sys.argv[2]
SITE = "--site" in sys.argv[3:]
MOBILE = SITE or "--mobile" in sys.argv[3:]   # phone layout: part of every website build

src = open(src_path, encoding="utf-8").read().replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
i = src.index('<div id="app"></div>')
head, body = src[:i], src[i:]

# Favicon for the plain page: the tree from quizmas/art.js with the theme colours filled in
_COLS = {"var(--good)": "#5fae6e", "var(--bone)": "#f6f1e6", "var(--candle)": "#e6b34c", "var(--bad)": "#e2554f"}
_tree = re.search(r"^const TREE_SVG = `(.*?)`;$", open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "quizmas", "art.js"),
                  encoding="utf-8").read(), re.M).group(1)
for _k, _v in _COLS.items():
    _tree = _tree.replace(_k, _v)
_tree = _tree.replace(' class="glyph"', '').replace(' aria-hidden="true"', '').replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
fav = "data:image/svg+xml," + _tree.replace("%", "%25").replace("#", "%23").replace('"', "'").replace("<", "%3C").replace(">", "%3E")
base_css = "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>"

if not SITE:
    meta = f'''<meta name="description" content="A Christmas quiz game for office parties: two rounds, Naughty or Nice, Krampus’s Bargain and a Christmas Eve wager, with a narrator.">
<link rel="icon" href="{fav}">'''
else:
    TITLE = NAME + " · Christmas Office Quiz Game"
    DESC = "Free Christmas trivia game for office parties and team events: a festive game-show board, Naughty or Nice, Krampus\u2019s Bargain and a Christmas Eve wager."
    OG_DESC = "A free Christmas quiz for the whole office: holiday trivia, Naughty or Nice, Krampus’s Bargain and a Christmas Eve wager, with a narrator."
    OG_IMG = URL + "og-image.png"
    head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, count=1, flags=re.S)
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": URL + "#website", "url": URL, "name": NAME,
             "alternateName": SHORT, "inLanguage": "en"},
            {"@type": "WebApplication", "@id": URL + "#game", "url": URL, "name": NAME,
             "description": DESC, "image": OG_IMG, "inLanguage": "en",
             "applicationCategory": "GameApplication", "genre": ["Trivia", "Quiz", "Party game"],
             "operatingSystem": "Any", "browserRequirements": "Requires JavaScript. Best in Chrome or Edge.",
             "isAccessibleForFree": True,
             "offers": {"@type": "Offer", "price": "0", "priceCurrency": "CAD"},
             "author": {"@type": "Person", "name": "Victoria"},
             "isPartOf": {"@id": URL + "#website"}},
        ],
    }
    meta = f'''{GA_HEAD}
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Victoria">
<meta name="theme-color" content="#0d1714">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:locale" content="en_CA">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="{NAME}">
<meta property="og:description" content="{OG_DESC}">
<meta property="og:image" content="{OG_IMG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{NAME}: a Christmas quiz for the whole office, with a glowing Christmas tree">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{NAME}">
<meta name="twitter:description" content="{OG_DESC}">
<meta name="twitter:image" content="{OG_IMG}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'''
    # Readable without JavaScript (search engines, link previews). The game replaces it as soon as it starts.
    static = '''<div id="app"><main class="nof-static" style="max-width:760px;margin:0 auto;padding:40px 16px;font-family:Georgia,serif;color:#f6f1e6">
<p style="text-transform:uppercase;letter-spacing:.14em;font:800 .78rem system-ui,sans-serif;color:#a8c0b6">A Christmas quiz for the whole office</p>
<h1 style="color:#ffe6a6;font-size:3rem;line-height:1;margin:.2em 0">Victoria’s Merry Quizmas</h1>
<p>A free Christmas trivia game for office parties and team events, made for a big screen. Teams pick holiday questions on a game-show board, think for 30 seconds and answer. A warm narrator reads every question aloud.</p>
<h2 style="color:#e6b34c">How it plays</h2>
<ul>
<li><strong>Two rounds</strong> of five Christmas and Canadian categories, worth 100–500 and then 200–1,000 points.</li>
<li><strong>Naughty or Nice:</strong> the team that finds a lump of coal must hand the question to another team.</li>
<li><strong>Krampus’s Bargain:</strong> Krampus draws twice from his sack: first the price, then the team that must answer.</li>
<li><strong>Christmas Eve:</strong> one final question with secret wagers, then a podium for the team that saved Christmas.</li>
</ul>
<p>Works for 2–4 teams in the room and over a video call. No sign-up, no download.</p>
<noscript><p><strong>This game needs JavaScript.</strong> Please turn it on to play.</p></noscript>
</main></div>'''
    # Links to the content pages: visible on the start screen only, hidden while a game is on screen.
    links = '''<nav class="nof-links" aria-label="More about the game">
<a href="/christmas-trivia-questions/">Christmas trivia questions</a>
<a href="/virtual-christmas-games-for-work/">Remote &amp; hybrid teams</a>
<a href="/how-to-host-a-christmas-game-night/">Host guide</a>
<a href="/faq/">FAQ</a>
</nav>
<style>
.nof-links{display:flex;flex-wrap:wrap;gap:6px 22px;justify-content:center;max-width:1400px;margin:0 auto;padding:8px 16px 36px;
  font-family:"Alegreya Sans",system-ui,sans-serif;font-weight:700;font-size:.95rem}
.nof-links a{color:#a8c0b6;text-decoration:none}
.nof-links a:hover,.nof-links a:focus-visible{color:#ffe6a6;text-decoration:underline}
.nof-links[hidden]{display:none!important}
</style>
<script>
(function(){
  var nav = document.querySelector('.nof-links'), app = document.getElementById('app');
  var sync = function(){ nav.hidden = !(app.querySelector('.setup') || app.querySelector('.nof-static')); };
  new MutationObserver(sync).observe(app, { childList: true }); sync();
})();
</script>'''
    body = body.replace('<div id="app"></div>', static, 1)
    body = body.rstrip() + "\n" + links + "\n" + GAME_EVENTS_JS

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{meta}
{base_css}
{head.strip()}
</head>
<body>
{body.strip()}
</body>
</html>
'''
if MOBILE and 'id="nof-mobile"' not in page:
    page = page.replace("</head>", MOBILE_CSS + "\n</head>", 1)
if SITE:
    # On the website the game screens use the site's name too (the artifact and offline file keep "Viktoriia’s").
    page = page.replace("Viktoriia’s", "Victoria’s")
open(out_path, "w", encoding="utf-8").write(page)
