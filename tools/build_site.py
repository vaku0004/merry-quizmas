"""Build the whole Merry Quizmas website into one folder, ready for GitHub Pages.

python3 tools/build_site.py <site_dir>        (run from the repo root; needs fontpkgs/, Playwright and Pillow)

What it does, in order:
1. index.html: the game as a full web page (tools/build_index.py --site)
2. build/pages-data-q.json: the questions, read from the game itself
3. preview images and icons (tools/make_og.py + tools/shoot_site.js), game screenshots for the content pages
4. the four content pages (tools/build_pages.py)
5. favicon.ico, site.webmanifest, robots.txt, sitemap.xml, CNAME, and audio/ if the narrator files are in the repo

Settings (domain, Analytics ID) are in tools/site_common.py. Intermediate files go to build/ (not committed).
"""
import json, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_common import URL, HOST, NAME, SHORT

S = "."
OUT = sys.argv[1]
B = f"{S}/build"
GAME = f"{S}/quizmas/merry-quizmas.html"
run = lambda *cmd: subprocess.run(list(cmd), check=True)
os.makedirs(OUT, exist_ok=True)
os.makedirs(B, exist_ok=True)

print("1. index.html")
run("python3", f"{S}/tools/build_index.py", GAME, f"{OUT}/index.html", "--site")

print("2. questions")
run("node", f"{S}/tools/dump_q.js", os.path.abspath(GAME), f"{B}/pages-data-q.json")

print("3. preview images, icons, screenshots")
import build_pages
build_pages.Q = json.load(open(f"{B}/pages-data-q.json", encoding="utf-8"))
build_pages.write_og_list()
run("python3", f"{S}/tools/make_og.py")
run("python3", f"{S}/tools/fontify.py", f"{OUT}/index.html", f"{B}/game-local.html")
run("node", f"{S}/tools/shoot_site.js", os.path.abspath(S), os.path.abspath(f"{B}/game-local.html"))
from PIL import Image
for n in build_pages.SHOTS:
    Image.open(f"{B}/pageshots/{n}.png").convert("RGB").save(f"{B}/pageshots/{n}.webp", "WEBP", quality=82, method=6)

print("4. content pages")
build_pages.build(OUT)

print("5. icons, manifest, robots, sitemap")
os.makedirs(f"{OUT}/assets/og", exist_ok=True)
shutil.copy(f"{B}/seo/og.png", f"{OUT}/og-image.png")
for p in build_pages.PAGES:
    shutil.copy(f"{B}/seo/og-{p['slug']}.png", f"{OUT}/assets/og/{p['slug']}.png")
for f in ["favicon.svg", "icon-192.png", "icon-512.png", "apple-touch-icon.png"]:
    shutil.copy(f"{B}/seo/{f}", f"{OUT}/{f}")
ico = Image.open(f"{B}/seo/favicon-48.png")
ico.save(f"{OUT}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
json.dump({"name": NAME, "short_name": SHORT, "start_url": "/", "display": "standalone",
           "background_color": "#0d1714", "theme_color": "#0d1714",
           "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                     {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]},
          open(f"{OUT}/site.webmanifest", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {URL}sitemap.xml\n")
urls = [URL] + [f"{URL}{p['slug']}/" for p in build_pages.PAGES]
open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"  <url><loc>{u}</loc><lastmod>{build_pages.TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
open(f"{OUT}/CNAME", "w").write(HOST + "\n")
if os.path.isfile(f"{S}/audio/manifest.json"):
    shutil.copytree(f"{S}/audio", f"{OUT}/audio", dirs_exist_ok=True)
    print("   audio copied:", len(os.listdir(f"{OUT}/audio")) - 1, "files")
else:
    print("   no audio/ yet: the game falls back to the browser voice")
print("done:", OUT)
