"""Write the HTML sources for preview images (1200x630) and icons into build/seo/. tools/shoot_site.js renders them.

From Python: make_all(games_out) (called by build_site.py). Art comes from each game's source, fonts from fontpkgs/.
"""
import glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_common import HOST, BRAND
import games as G
import build_home as H

S = "."
OUT = f"{S}/build/seo"
F = f"{S}/fontpkgs"
font = lambda slug, w, st: os.path.abspath(glob.glob(f"{F}/fontsource-{slug}-[0-9]*/package/files/{slug}-latin-{w}-{st}.woff2")[0])
FACES = "".join(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};src:url(file://{font(slug, w, st)})}}"
                for fam, slug, w, st in [("Mountains of Christmas", "mountains-of-christmas", 700, "normal"), ("Pirata One", "pirata-one", 400, "normal"), ("Yeseva One", "yeseva-one", 400, "normal"), ("Eagle Lake", "eagle-lake", 400, "normal"), ("Righteous", "righteous", 400, "normal"),
                                         ("Alegreya", "alegreya", 500, "italic"), ("Alegreya", "alegreya", 800, "normal"), ("Alegreya", "alegreya", 800, "italic"),
                                         ("Alegreya Sans", "alegreya-sans", 500, "normal"), ("Alegreya Sans", "alegreya-sans", 800, "normal")])
SNOW = "".join(f'<i style="left:{(i * 137) % 1200}px;top:{(i * 89) % 630}px;width:{2 + i % 4}px;height:{2 + i % 4}px;opacity:{0.15 + (i % 5) / 12:.2f}"></i>'
               for i in range(1, 70))
# The site icon: a game board with one golden cell
BOARD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">' +
         "".join(f'<rect x="{6 + c * 18}" y="{6 + r * 18}" width="16" height="16" rx="3.5" fill="{"#f0b44c" if (r, c) == (1, 1) else "#3d4775"}"/>'
                 for r in range(3) for c in range(3)) + "</svg>")


def base_css(th, glow, glow2, snow):
    return f"""{FACES}
*{{box-sizing:border-box}} html,body{{margin:0}}
body{{width:1200px;height:630px;overflow:hidden;background:{th['night']};color:{th['bone']};font-family:'Alegreya Sans';position:relative;
 background-image:radial-gradient(ellipse 55% 60% at 92% -10%, rgba({glow},.26), transparent 70%),
 radial-gradient(ellipse 60% 55% at 0% 115%, rgba({glow2},.24), transparent 70%)}}
.snow i{{position:absolute;border-radius:50%;background:#fff;{'' if snow else 'display:none'}}}
.frame{{position:absolute;inset:28px;border:1px solid {th['line']};border-radius:22px}}
.eyebrow{{font-weight:800;text-transform:uppercase;letter-spacing:.16em;font-size:22px;color:{th['ash']}}}
.url{{position:absolute;left:84px;bottom:56px;font-size:24px;font-weight:800;letter-spacing:.06em;color:{th['candle']}}}
.art{{position:absolute;filter:drop-shadow(0 0 50px rgba({glow},.35))}}
.art svg{{width:100%;height:auto;display:block}}"""


def game_sources(g, page_ogs):
    th, rgb = g["theme"], g["rgb"]
    fam, w = g["display"][0], g["display"][1]
    css = base_css(th, rgb["glow"], rgb["glow2"], g["slug"] == "christmas")
    chips = "".join(f'<span class="chip">{G.art(g, a)}{t}</span>' for a, t in g["chips"])
    og = f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}
.text{{position:absolute;left:84px;top:66px;width:760px}}
.byline{{font-family:'Alegreya';font-style:italic;font-weight:500;font-size:50px;color:{th['candle']};margin-top:26px;line-height:1}}
h1{{font-family:'{fam}';font-weight:{w};font-size:{int((136 if w == 700 else 150) * {'Righteous': 0.78, 'Eagle Lake': 0.85}.get(fam, 1))}px;line-height:.88;margin:4px 0 0;color:{th['ember']};text-shadow:0 0 40px rgba({rgb['glow']},.45)}}
.chips{{display:flex;gap:10px;margin-top:30px;flex-wrap:nowrap}}
.chip{{display:flex;align-items:center;gap:10px;border:1px solid {th['line']};background:rgba({rgb['dusk']},.88);border-radius:999px;padding:8px 16px 8px 10px;font-size:21px;font-weight:500;white-space:nowrap}}
.chip svg{{width:28px;height:28px}}
.art{{right:70px;top:110px;width:340px}}
</style></head><body><div class="snow">{SNOW}</div><div class="frame"></div>
<div class="text"><div class="eyebrow">{g['eyebrow']}</div><div class="byline">Victoria’s</div><h1>{g['short']}</h1><div class="chips">{chips}</div></div>
<div class="art">{G.art(g, g['icon'])}</div>
<div class="url">{HOST.upper()} · FREE TO PLAY</div></body></html>"""
    open(f"{OUT}/{g['slug']}-og.html", "w", encoding="utf-8").write(og)
    for slug, (eyebrow, title, sub) in page_ogs:
        page = f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}
.t{{position:absolute;left:84px;top:84px;width:740px}}
h1{{font-family:'{fam}';font-weight:{w};font-size:{int((104 if w == 700 else 112) * ({'Eagle Lake': 0.7, 'Righteous': 0.8}.get(fam, 1)))}px;line-height:.93;margin:22px 0 0;color:{th['ember']};text-shadow:0 0 40px rgba({rgb['glow']},.45)}}
.sub{{margin-top:26px;font-size:30px;font-weight:500}}
.art{{right:80px;top:150px;width:290px}}
</style></head><body><div class="snow">{SNOW}</div><div class="frame"></div>
<div class="t"><div class="eyebrow">{eyebrow}</div><h1>{title}</h1><div class="sub">{sub}</div></div>
<div class="art">{G.art(g, g['page_art'][slug])}</div><div class="url">{HOST.upper()} · {g['name'].upper()}</div></body></html>"""
        open(f"{OUT}/{g['slug']}-og-{slug}.html", "w", encoding="utf-8").write(page)
    icon = G.art(g, g["icon"]).replace(' aria-hidden="true"', "").replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    open(f"{OUT}/{g['slug']}-favicon.svg", "w", encoding="utf-8").write(icon)


def hub_sources(games_out):
    th = H.HUB
    css = base_css(th, "240,180,76", "231,122,149", False)
    arts = "".join(f'<div class="a">{G.art(g, g["icon"]) if g["status"] != "soon" else H.HEART}</div>' for g in G.GAMES)
    og = f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}
.text{{position:absolute;left:84px;top:80px;width:1040px}}
h1{{font-family:'Alegreya';font-weight:800;font-size:94px;line-height:1;margin:18px 0 0;white-space:nowrap;color:{th['ember']}}}
h1 i{{color:{th['candle']}}}
.sub{{margin-top:22px;font-size:32px;font-weight:500;max-width:760px}}
.row{{position:absolute;right:84px;bottom:56px;display:flex;gap:22px}}
.a svg{{width:92px;height:92px;filter:drop-shadow(0 0 22px rgba(240,180,76,.35))}}
</style></head><body><div class="frame"></div>
<div class="text"><div class="eyebrow">Free team games for the big screen</div><h1>Victoria’s <i>Game Nights</i></h1>
<div class="sub">Holiday quiz games for office parties, with a narrator, for teams in the room and on the call.</div></div>
<div class="row">{arts}</div><div class="url">{HOST.upper()}</div></body></html>"""
    open(f"{OUT}/og.html", "w", encoding="utf-8").write(og)
    open(f"{OUT}/favicon.svg", "w", encoding="utf-8").write(BOARD)
    tile = f"""<!doctype html><html><head><style>html,body{{margin:0;background:transparent}}
.t{{width:512px;height:512px;background:{th['night']};border-radius:{{R}}px;display:grid;place-items:center}}.t svg{{width:400px;height:400px}}</style></head>
<body><div class="t">{BOARD}</div></body></html>"""
    open(f"{OUT}/tile.html", "w", encoding="utf-8").write(tile.replace("{R}", "96"))
    open(f"{OUT}/tile-square.html", "w", encoding="utf-8").write(tile.replace("{R}", "0"))


def make_all(games_out, page_ogs):
    os.makedirs(OUT, exist_ok=True)
    hub_sources(games_out)
    for g in games_out:
        game_sources(g, page_ogs[g["slug"]])
