"""Write the HTML sources for the social preview images (1200x630) and the site icons into build/seo/.
tools/shoot_site.js turns them into PNGs. Art comes from quizmas/art.js, fonts from fontpkgs/ (see tools/fontify.py).

python3 tools/make_og.py        (run from the repo root, after build/pages-og.json exists)
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_common import HOST, NAME, SHORT

S = "."
OUT = f"{S}/build/seo"
os.makedirs(OUT, exist_ok=True)
art = open(f"{S}/quizmas/art.js", encoding="utf-8").read()
svg = lambda name: re.search(rf"^const {name} = `(.*?)`;$", art, re.M).group(1)
F = f"{S}/fontpkgs"
font = lambda slug, w, st: glob.glob(f"{F}/fontsource-{slug}-[0-9]*/package/files/{slug}-latin-{w}-{st}.woff2")[0]
faces = "".join(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};src:url(file://{os.path.abspath(font(slug, w, st))})}}"
                for fam, slug, w, st in [("Mountains of Christmas", "mountains-of-christmas", 700, "normal"),
                                         ("Alegreya", "alegreya", 500, "italic"),
                                         ("Alegreya Sans", "alegreya-sans", 500, "normal"),
                                         ("Alegreya Sans", "alegreya-sans", 800, "normal")])
COLS = {"--night": "#0d1714", "--dusk": "#15231e", "--line": "#33544a", "--bone": "#f6f1e6", "--ash": "#a8c0b6",
        "--candle": "#e6b34c", "--ember": "#ffe6a6", "--good": "#5fae6e", "--bad": "#e2554f", "--witch": "#c9484f"}
VARS = "".join(f"{k}:{v};" for k, v in COLS.items())

# Snow: fixed dots so every build gives the same picture
SNOW = "".join(f'<i style="left:{(i * 137) % 1200}px;top:{(i * 89) % 630}px;width:{2 + i % 4}px;height:{2 + i % 4}px;opacity:{0.15 + (i % 5) / 12:.2f}"></i>'
               for i in range(1, 70))
BASE_CSS = f"""{faces}
:root{{{VARS}}}
*{{box-sizing:border-box}} html,body{{margin:0}}
body{{width:1200px;height:630px;overflow:hidden;background:var(--night);color:var(--bone);font-family:'Alegreya Sans';position:relative;
 background-image:radial-gradient(ellipse 55% 60% at 92% -10%, rgba(230,179,76,.26), transparent 70%),
 radial-gradient(ellipse 60% 55% at 0% 115%, rgba(201,72,79,.24), transparent 70%)}}
.snow i{{position:absolute;border-radius:50%;background:#fff}}
.frame{{position:absolute;inset:28px;border:1px solid var(--line);border-radius:22px}}
.eyebrow{{font-weight:800;text-transform:uppercase;letter-spacing:.16em;font-size:22px;color:var(--ash)}}
.url{{position:absolute;left:84px;bottom:56px;font-size:24px;font-weight:800;letter-spacing:.06em;color:var(--candle)}}
.art{{position:absolute;filter:drop-shadow(0 0 50px rgba(230,179,76,.35))}}
.art svg{{width:100%;height:auto;display:block}}"""

og = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
.text{{position:absolute;left:84px;top:66px;width:760px}}
.byline{{font-family:'Alegreya';font-style:italic;font-weight:500;font-size:50px;color:var(--candle);margin-top:26px;line-height:1}}
h1{{font-family:'Mountains of Christmas';font-weight:700;font-size:136px;line-height:.9;margin:4px 0 0;color:var(--ember);text-shadow:0 0 40px rgba(230,179,76,.45)}}
.chips{{display:flex;gap:10px;margin-top:30px;flex-wrap:nowrap}}
.chip{{display:flex;align-items:center;gap:10px;border:1px solid var(--line);background:rgba(21,35,30,.88);border-radius:999px;padding:8px 16px 8px 10px;font-size:21px;font-weight:500;white-space:nowrap}}
.chip svg{{width:28px;height:28px}}
.art{{right:70px;top:110px;width:340px}}
</style></head><body><div class="snow">{SNOW}</div><div class="frame"></div>
<div class="text"><div class="eyebrow">A Christmas quiz for the whole office</div>
<div class="byline">Victoria’s</div><h1>{SHORT}</h1>
<div class="chips"><span class="chip">{svg('COAL_SVG')}Naughty or Nice</span><span class="chip">{svg('KRAMPUS_SVG')}Krampus’s Bargain</span><span class="chip">{svg('STAR_SVG')}Christmas Eve wager</span></div></div>
<div class="art">{svg('TREE_SVG')}</div>
<div class="url">{HOST.upper()} · FREE TO PLAY</div>
</body></html>"""
open(f"{OUT}/og.html", "w", encoding="utf-8").write(og)

# Content pages
for p in json.load(open(f"{S}/build/pages-og.json")):
    eyebrow, title, sub = p["og"]
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}
.t{{position:absolute;left:84px;top:84px;width:740px}}
h1{{font-family:'Mountains of Christmas';font-weight:700;font-size:104px;line-height:.95;margin:22px 0 0;color:var(--ember);text-shadow:0 0 40px rgba(230,179,76,.45)}}
.sub{{margin-top:26px;font-size:30px;font-weight:500;color:var(--bone)}}
.art{{right:80px;top:150px;width:290px}}
</style></head><body><div class="snow">{SNOW}</div><div class="frame"></div>
<div class="t"><div class="eyebrow">{eyebrow}</div><h1>{title}</h1><div class="sub">{sub}</div></div>
<div class="art">{svg(p['art'])}</div><div class="url">{HOST.upper()} · {NAME.upper()}</div></body></html>"""
    open(f"{OUT}/og-{p['slug']}.html", "w", encoding="utf-8").write(page)

# Icons: the tree on a dark rounded square (readable on light and dark tabs)
tree = svg("TREE_SVG").replace(' class="glyph"', "").replace(' aria-hidden="true"', "")
for k, v in COLS.items():
    tree = tree.replace(f"var({k})", v)
icon = tree.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
open(f"{OUT}/favicon.svg", "w", encoding="utf-8").write(icon)
tile = f"""<!doctype html><html><head><style>html,body{{margin:0;background:transparent}}
.t{{width:512px;height:512px;background:#0d1714;border-radius:{{R}}px;display:grid;place-items:center;
 background-image:radial-gradient(circle at 50% 55%, rgba(230,179,76,.22), transparent 65%)}}.t svg{{width:420px;height:420px}}</style></head>
<body><div class="t">{tree}</div></body></html>"""
open(f"{OUT}/tile.html", "w", encoding="utf-8").write(tile.replace("{R}", "96"))
open(f"{OUT}/tile-square.html", "w", encoding="utf-8").write(tile.replace("{R}", "0"))
print("og sources in", OUT)
