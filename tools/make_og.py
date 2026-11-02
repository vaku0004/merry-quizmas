"""Render the social preview image (1200x630) and site icons from the game's own art and fonts."""
import re, glob, subprocess, sys
S = "."
src = open(f"{S}/night-of-frights.html", encoding="utf-8").read()
def svg(name): return re.search(name + r" = `(.*?)`;", src, re.S).group(1)
F = f"{S}/fontpkgs"
def font(slug, w, st): return glob.glob(f"{F}/fontsource-{slug}-[0-9]*/package/files/{slug}-latin-{w}-{st}.woff2")[0]
faces = "".join(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};src:url(file://{font(slug,w,st)})}}"
  for fam, slug, w, st in [("Pirata One","pirata-one",400,"normal"),("Alegreya","alegreya",500,"italic"),
                           ("Alegreya Sans","alegreya-sans",500,"normal"),("Alegreya Sans","alegreya-sans",800,"normal")])
VARS = "--night:#15111d;--dusk:#1f1929;--line:#41355a;--bone:#f2e9d8;--ash:#ab9fbd;--candle:#f2a24c;--ember:#ffd58a;--good:#84bd7c;--witch:#a98be0;"
og = f"""<!doctype html><html><head><meta charset="utf-8"><style>{faces}
:root{{{VARS}}}
*{{box-sizing:border-box}} html,body{{margin:0}}
body{{width:1200px;height:630px;overflow:hidden;background:var(--night);
 background-image:radial-gradient(ellipse 55% 60% at 92% -10%, rgba(242,162,76,.28), transparent 70%),
 radial-gradient(ellipse 60% 55% at 0% 115%, rgba(169,139,224,.22), transparent 70%);
 color:var(--bone);font-family:'Alegreya Sans';position:relative}}
.frame{{position:absolute;inset:28px;border:1px solid var(--line);border-radius:22px}}
.text{{position:absolute;left:84px;top:66px;width:690px}}
.eyebrow{{font-weight:800;text-transform:uppercase;letter-spacing:.16em;font-size:22px;color:var(--ash)}}
.byline{{font-family:'Alegreya';font-style:italic;font-weight:500;font-size:50px;color:var(--candle);margin-top:26px;line-height:1}}
h1{{font-family:'Pirata One';font-weight:400;font-size:150px;line-height:.86;margin:6px 0 0;color:var(--ember);text-shadow:0 0 40px rgba(242,162,76,.45)}}
.chips{{display:flex;gap:12px;margin-top:28px;flex-wrap:wrap}}
.chip{{display:flex;align-items:center;gap:10px;border:1px solid var(--line);background:rgba(31,25,41,.85);border-radius:999px;padding:9px 18px 9px 12px;font-size:23px;font-weight:500}}
.chip svg{{width:30px;height:30px}}
.url{{position:absolute;left:84px;bottom:56px;font-size:24px;font-weight:800;letter-spacing:.06em;color:var(--candle)}}
.art{{position:absolute;right:70px;top:120px;width:340px;filter:drop-shadow(0 0 50px rgba(242,162,76,.35))}}
.art svg{{width:340px;height:auto}}
</style></head><body><div class="frame"></div>
<div class="text"><div class="eyebrow">A Halloween quiz for the whole office</div>
<div class="byline">Victoria’s</div><h1>Night of Frights</h1>
<div class="chips"><span class="chip">{svg('CAT_SVG')}Black cat</span><span class="chip">{svg('HAT_SVG')}Witch’s deal</span><span class="chip">{svg('MOON_SVG')}Midnight wager</span></div></div>
<div class="art">{svg('PUMPKIN_SVG')}</div>
<div class="url">NIGHTOFFRIGHTS.MONSTER · FREE TO PLAY</div>
</body></html>"""
open(f"{S}/seo/og.html","w",encoding="utf-8").write(og)
# Icon: the pumpkin on a dark rounded square (readable on light and dark tabs)
pump = svg('PUMPKIN_SVG').replace(' class="glyph"','').replace('var(--good)','#84bd7c').replace('var(--candle)','#f2a24c').replace('var(--night)','#15111d')
icon = pump.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true"','')
open(f"{S}/seo/favicon.svg","w",encoding="utf-8").write(icon)
tile = f"""<!doctype html><html><head><style>html,body{{margin:0;background:transparent}}
.t{{width:512px;height:512px;background:#15111d;border-radius:{{R}}px;display:grid;place-items:center;
 background-image:radial-gradient(circle at 50% 60%, rgba(242,162,76,.25), transparent 65%)}}.t svg{{width:400px;height:400px}}</style></head>
<body><div class="t">{pump}</div></body></html>"""
open(f"{S}/seo/tile.html","w",encoding="utf-8").write(tile.replace("{R}","96"))
open(f"{S}/seo/tile-square.html","w",encoding="utf-8").write(tile.replace("{R}","0"))
