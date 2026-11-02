"""Preview images (1200x630) for the content pages, in the same style as the main one."""
import json, re, glob
S = "."
src = open(f"{S}/night-of-frights.html", encoding="utf-8").read()
svg = lambda n: re.search(n + r" = `(.*?)`;", src, re.S).group(1)
F = f"{S}/fontpkgs"
font = lambda slug, w, st: glob.glob(f"{F}/fontsource-{slug}-[0-9]*/package/files/{slug}-latin-{w}-{st}.woff2")[0]
faces = "".join(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};src:url(file://{font(slug,w,st)})}}"
  for fam, slug, w, st in [("Pirata One","pirata-one",400,"normal"),("Alegreya","alegreya",500,"italic"),("Alegreya Sans","alegreya-sans",800,"normal"),("Alegreya Sans","alegreya-sans",500,"normal")])
VARS = "--night:#15111d;--line:#41355a;--bone:#f2e9d8;--ash:#ab9fbd;--candle:#f2a24c;--ember:#ffd58a;--good:#84bd7c;--witch:#a98be0;"
art = {"halloween-trivia-questions": "PUMPKIN_SVG", "virtual-halloween-games-for-work": "GHOST_SVG", "how-to-host-a-halloween-game-night": "CANDLE_SVG", "faq": "CAT_SVG"}
for p in json.load(open(f"{S}/pages-og.json")):
    eyebrow, title, sub = p["og"]
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>{faces}:root{{{VARS}}}
*{{box-sizing:border-box}}html,body{{margin:0}}
body{{width:1200px;height:630px;overflow:hidden;background:#15111d;color:var(--bone);font-family:'Alegreya Sans';position:relative;
 background-image:radial-gradient(ellipse 55% 60% at 92% -10%, rgba(242,162,76,.28), transparent 70%),radial-gradient(ellipse 60% 55% at 0% 115%, rgba(169,139,224,.22), transparent 70%)}}
.frame{{position:absolute;inset:28px;border:1px solid var(--line);border-radius:22px}}
.t{{position:absolute;left:84px;top:84px;width:720px}}
.eyebrow{{font-weight:800;text-transform:uppercase;letter-spacing:.16em;font-size:22px;color:var(--ash)}}
h1{{font-family:'Pirata One';font-weight:400;font-size:112px;line-height:.92;margin:22px 0 0;color:var(--ember);text-shadow:0 0 40px rgba(242,162,76,.45)}}
.sub{{margin-top:26px;font-size:30px;font-weight:500;color:var(--bone)}}
.url{{position:absolute;left:84px;bottom:56px;font-size:24px;font-weight:800;letter-spacing:.06em;color:var(--candle)}}
.art{{position:absolute;right:80px;top:150px;width:290px;filter:drop-shadow(0 0 50px rgba(242,162,76,.35))}}.art svg{{width:290px;height:auto}}
</style></head><body><div class="frame"></div><div class="t"><div class="eyebrow">{eyebrow}</div><h1>{title}</h1><div class="sub">{sub}</div></div>
<div class="art">{svg(art[p['slug']])}</div><div class="url">NIGHTOFFRIGHTS.MONSTER · VICTORIA’S NIGHT OF FRIGHTS</div></body></html>"""
    open(f"{S}/seo/og-{p['slug']}.html", "w", encoding="utf-8").write(page)
