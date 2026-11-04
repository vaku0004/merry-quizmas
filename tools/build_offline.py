"""Build one self-contained HTML file: game + narrator audio + fonts, no network needed (a backup for the party).

python3 tools/build_offline.py <game> <out.html>    e.g. christmas build/merry-quizmas-offline.html
(run from the repo root; the game's source and audio folder come from tools/games.py, fonts from fontpkgs/)
"""
import base64, json, os, sys, glob, subprocess
S = "."
sys.path.insert(0, os.path.join(S, 'tools'))
import games as G
game = next(g for g in G.PLAYABLE if g['slug'] == sys.argv[1])
out = sys.argv[2]
A = f"{S}/{game['audio']}"
os.makedirs(f"{S}/build", exist_ok=True)
subprocess.run(["python3", f"{S}/tools/build_index.py", f"{S}/{game['src']}", f"{S}/build/_page.html", "--mobile"], check=True)
html = open(f"{S}/build/_page.html", encoding="utf-8").read()

# 1. fonts: replace Google Fonts links with embedded @font-face rules
def b64(p): return base64.b64encode(open(p, "rb").read()).decode()
F = f"{S}/fontpkgs"
faces = [(game["display"][0], game["display"][2], [(game["display"][1], "normal")]),
         ("Alegreya", "alegreya", [(400,"normal"),(500,"normal"),(700,"normal"),(400,"italic"),(500,"italic"),(700,"italic")]),
         ("Alegreya Sans", "alegreya-sans", [(400,"normal"),(500,"normal"),(700,"normal"),(800,"normal")]),
         ("Oswald", "oswald", [(400,"normal"),(500,"normal"),(600,"normal")])]
css = []
for fam, slug, styles in faces:
    for w, st in styles:
        p = glob.glob(f"{F}/fontsource-{slug}-[0-9]*/package/files/{slug}-latin-{w}-{st}.woff2")[0]
        css.append(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{b64(p)}) format('woff2')}}")
start = html.index('<link rel="preconnect" href="https://fonts.googleapis.com">')
end = html.index('display=swap">', start) + len('display=swap">')
html = html[:start] + "<style>" + "\n".join(css) + "</style>" + html[end:]
assert "fonts.googleapis.com" not in html and "fonts.gstatic.com" not in html

# 2. narrator audio: every line as a data URI, read by loadPack instead of fetching audio/manifest.json
if not os.path.isfile(f"{A}/manifest.json"):     # no narrator audio yet: the game uses the browser voice
    print("no audio yet in", A)
    m = {"lines": {}}
else:
    m = json.load(open(f"{A}/manifest.json", encoding="utf-8-sig"))
lines = {text: "data:audio/mpeg;base64," + b64(f"{A}/{f}") for text, f in m["lines"].items()}
pack = {"base": "", "voice": m.get("voice", ""), "model": m.get("model", ""), "lines": lines}
pack_js = "<script>window.__NOF_PACK = " + json.dumps(pack, ensure_ascii=False).replace("</", "<\\/") + ";</script>\n"
if lines:   # without recordings, keep the game's own "no narrator audio yet" message
    html = html.replace("<div id=\"app\"></div>", "<div id=\"app\"></div>\n" + pack_js, 1)
old = "function loadPack(){\n  try {"
assert old in html
html = html.replace(old, "function loadPack(){\n  if (window.__NOF_PACK){ PACK = window.__NOF_PACK; return; }   // offline build: audio is embedded\n  try {", 1)
assert "http://" not in html.replace("http://www.w3.org", "")
open(out, "w", encoding="utf-8").write(html)
os.remove(f"{S}/build/_page.html")
print("lines:", len(lines), "| fonts:", len(css), "| size MB:", round(os.path.getsize(out) / 1e6, 1))
