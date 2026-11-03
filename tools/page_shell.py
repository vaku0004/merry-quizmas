"""The frame of every content page on Victoria's Game Nights: head tags, header, footer, theme CSS.

The content itself lives in tools/pages_<game>.py. Those modules use e(), fig() and play_box() from here and the
globals NAME and Q, which build_site.py sets before rendering. Inside a game's content, href="/" means "play the game"
and is turned into the game's own address here.
"""
import html, json, re
from site_common import GA_HEAD, PAGE_EVENTS_JS, URL, BRAND
import games as G

S = "."
CUR = {}          # the game being rendered (set by use())
e = lambda s: html.escape(s, quote=True)


def use(game):
    CUR.clear(); CUR.update(game)


def theme_css(game):
    """pages.css with this game's colours and display font in the :root block."""
    css = open(f"{S}/pages-src/pages.css", encoding="utf-8").read()
    th, rgb = game["theme"], game["rgb"]
    fam, weight = game["display"][3], game["display"][1]
    root = (":root{\n  color-scheme: dark;\n  " + " ".join(f"--{k}:{v};" for k, v in th.items()) + "\n"
            f"  --night-rgb:{rgb['night']}; --dusk-rgb:{rgb['dusk']}; --glow:{rgb['glow']}; --glow2:{rgb['glow2']}; --tag2:{game['tag2']};\n"
            f"  --f-display:{fam}; --display-w:{weight};\n"
            '  --f-text:"Alegreya",Georgia,"Times New Roman",serif;\n'
            '  --f-ui:"Alegreya Sans",system-ui,-apple-system,"Segoe UI",sans-serif;\n'
            '  --f-num:"Oswald","Arial Narrow",sans-serif;\n'
            "  --wrap:1120px; --read:46rem;\n}")
    s = css.index(":root{"); t = css.index("}", s) + 1
    return css[:s] + root + css[t:]


def fig(name, alt, caption, w=1366, h=768):
    return (f'<figure><img src="/assets/{CUR["slug"]}/shots/{name}.webp" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{e(alt)}">'
            f'<figcaption>{caption}</figcaption></figure>')


def icon():
    return G.art(CUR, CUR["icon"])


def play_box(title="Play it free tonight", text="Open the game on the computer connected to your big screen, name your teams and press Start. No sign-up, no download, nothing for players to install."):
    return f'''<section class="play" aria-labelledby="play-h">
  <div><h2 id="play-h">{title}</h2><p>{text}</p>
  <div class="cta-row"><a class="btn primary big" href="/">Play {e(CUR["name"])}</a></div></div>
  {icon()}
</section>'''


def page(slug, title, desc, og_title, h1, eyebrow, body, extra_ld=None, crumb=None, scripts="", today=""):
    g = CUR
    home = f"{URL}{g['slug']}/"
    url = f"{home}{slug}/"
    og = f"{URL}assets/{g['slug']}/og/{slug}.png"
    graph = [
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc, "inLanguage": "en",
         "isPartOf": {"@id": URL + "#website"}, "primaryImageOfPage": og, "dateModified": today},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": BRAND, "item": URL},
            {"@type": "ListItem", "position": 2, "name": g["short"], "item": home},
            {"@type": "ListItem", "position": 3, "name": crumb or h1, "item": url}]},
    ] + (extra_ld or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    # Inside the content, "/" means the game itself
    body = re.sub(r'href="/"(?! data-home)', f'href="/{g["slug"]}/" data-play', body)
    nav = "".join(f'<a href="/{g["slug"]}/{s}/"{" aria-current=\"page\"" if s == slug else ""}>{t}</a>' for s, t in G.PAGES)
    foot = "".join(f'<a href="/{g["slug"]}/{s}/">{t}</a>' for s, t in G.PAGES)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{GA_HEAD}
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="{g['theme']['night']}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/{g['slug']}/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{e(BRAND)}">
<meta property="og:locale" content="en_CA">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(og_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(og_title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(og_title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,400;0,700;1,400&family=Alegreya+Sans:wght@400;700;800&family=Oswald:wght@400;500&family={g['gfont']}&display=swap">
<link rel="stylesheet" href="/assets/{g['slug']}/pages.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="btn" href="#main" style="position:absolute;left:-9999px" onfocus="this.style.left='12px';this.style.top='12px';this.style.zIndex=9">Skip to content</a>
<header class="site-head"><div class="wrap">
  <a class="brand" href="/{g['slug']}/">{icon()}<span>{e(g['short'])}</span></a>
  <nav class="site-nav" aria-label="Main">{nav}<a class="btn primary" href="/{g['slug']}/" data-play>Play free</a></nav>
</div></header>
<main id="main" class="wrap">
  <div class="hero">
    <p class="crumbs"><a href="/">{e(BRAND)}</a> › <a href="/{g['slug']}/">{e(g['short'])}</a> › {e(crumb or h1)}</p>
    <p class="eyebrow" style="margin-top:22px">{eyebrow}</p>
    <h1>{h1}</h1>
  </div>
{body}
</main>
<footer class="site-foot"><div class="wrap">
  <nav aria-label="Footer"><a href="/{g['slug']}/" data-play>Play the game</a>{foot}<a href="/">All games</a></nav>
  <span>{e(g['name'])} · a free {g['holiday']} quiz game for teams · part of <a href="/">{e(BRAND)}</a> · <a href="/privacy/">Privacy</a></span>
</div></footer>
{scripts}
{PAGE_EVENTS_JS}
</body>
</html>
'''


TRIVIA_JS = '''<script>
(function(){
  var all = function(open){ document.querySelectorAll('.qlist details').forEach(function(d){ d.open = open; }); };
  var t = document.querySelector('[data-toggle-all]');
  if (t) t.addEventListener('click', function(){ var open = t.getAttribute('aria-pressed') !== 'true'; all(open);
    t.setAttribute('aria-pressed', open); t.textContent = open ? 'Hide all answers' : 'Show all answers'; });
  document.querySelectorAll('[data-print]').forEach(function(b){ b.addEventListener('click', function(){
    var withAnswers = b.getAttribute('data-print') === 'answers';
    document.body.classList.toggle('print-no-answers', !withAnswers);
    var was = Array.prototype.map.call(document.querySelectorAll('.qlist details'), function(d){ return d.open; });
    all(withAnswers); window.print();
    document.querySelectorAll('.qlist details').forEach(function(d, i){ d.open = was[i]; });
    document.body.classList.remove('print-no-answers'); }); });
})();
</script>'''

COPY_JS = '''<script>
document.querySelectorAll('[data-copy]').forEach(function(b){ b.addEventListener('click', function(){
  var box = document.getElementById(b.getAttribute('data-copy')); var text = box.firstChild.textContent;
  var done = function(){ b.textContent = 'Copied'; setTimeout(function(){ b.textContent = 'Copy'; }, 1800); };
  if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function(){}); }); });
</script>'''


def faq_ld(faq):
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return [{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]}]


slugify = lambda s: re.sub(r"-+", "-", "".join(c.lower() if c.isalnum() else "-" for c in s.replace("'", ""))).strip("-")
