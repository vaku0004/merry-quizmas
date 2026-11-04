"""Build the whole Victoria's Game Nights website into one folder, ready for GitHub Pages.

python3 tools/build_site.py <site_dir> [--preview] [--today YYYY-MM-DD]
  --preview   include games that are not published yet (status "scheduled" before their launch date), for checking
  --today     pretend it is another day (to test a launch date)

Run from the repo root. Needs fontpkgs/ (see HANDOFF.md), Node with Playwright, and Pillow.
Games and their texts: tools/games.py and tools/pages_<game>.py. Domain and Analytics: tools/site_common.py.
Intermediate files go to build/ (not committed).
"""
import datetime, importlib, json, os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_common import URL, HOST, BRAND
import games as G, page_shell as P, build_index as I, build_home as H, make_og as O

S = os.path.abspath(".")
args = sys.argv[1:]
OUT = os.path.abspath(args[0])
PREVIEW = "--preview" in args
TODAY = args[args.index("--today") + 1] if "--today" in args else datetime.date.today().isoformat()
B = f"{S}/build"
os.makedirs(OUT, exist_ok=True); os.makedirs(f"{B}/seo", exist_ok=True)
run = lambda *cmd: subprocess.run(list(cmd), check=True)
write = lambda path, text: (os.makedirs(os.path.dirname(path), exist_ok=True), open(path, "w", encoding="utf-8").write(text))

out_games = [g for g in G.PLAYABLE if G.is_out(g, TODAY, PREVIEW)]
print(f"Building {OUT} for {TODAY}{' (preview)' if PREVIEW else ''}: games", [g["slug"] for g in out_games])

# Game screenshots for the content pages, made once and kept in games/<slug>/shots/ (delete the folder to redo them)
TEAMS = [{"name": "Team Elves", "score": 1100}, {"name": "Team Reindeer", "score": -300}, {"name": "Team Snowmen", "score": 900}, {"name": "Team Gingerbread", "score": 400}]
BASE = {"screen": "board", "teamCount": 4, "teams": TEAMS, "round": 0, "used": {"0-0-0": 1, "0-1-0": 1, "0-2-1": 1, "0-3-0": 1, "0-4-0": 1},
        "turn": 1, "q": None, "final": None, "sound": False}
VTEAMS = [{"name": "Team Lovebirds", "score": 1100}, {"name": "Team Sweethearts", "score": -300}, {"name": "Team Roses", "score": 900}, {"name": "Team Truffles", "score": 400}]
VBASE = {**BASE, "teams": VTEAMS}
SHOT_STATES = {"valentines": {
    "board": VBASE,
    "question": {**VBASE, "q": {"c": 4, "i": 3, "value": 400, "special": None, "picker": 1, "team": 1, "bid": None, "judged": {}, "stage": "ask"}},
    "arrow": {**VBASE, "q": {"c": 1, "i": 2, "value": 300, "special": "cat", "picker": 0, "team": None, "bid": None, "judged": {}, "stage": "intro", "catAsk": True}},
    "chocolates": {**VBASE, "q": {"c": 4, "i": 4, "value": 500, "special": "witch", "picker": 0, "team": None, "bid": 300, "w": {"price": 300, "team": 2},
                                  "judged": {}, "stage": "intro", "witchAsk": True}},
    "final": {**VBASE, "screen": "final", "round": 1, "used": {}, "final": {"stage": "category", "wagers": [], "judged": []}},
    "podium": {**VBASE, "screen": "podium", "round": 1, "used": {}, "final": {"stage": "done", "wagers": [], "judged": []},
               "teams": [{"name": "Team Lovebirds", "score": 3400}, {"name": "Team Sweethearts", "score": 2100}, {"name": "Team Roses", "score": 2800}, {"name": "Team Truffles", "score": 900}]},
}, "christmas": {
    "board": BASE,
    "question": {**BASE, "q": {"c": 3, "i": 3, "value": 400, "special": None, "picker": 1, "team": 1, "bid": None, "judged": {}, "stage": "ask"}},
    "coal": {**BASE, "q": {"c": 1, "i": 2, "value": 300, "special": "cat", "picker": 0, "team": None, "bid": None, "judged": {}, "stage": "intro", "catAsk": True}},
    "krampus": {**BASE, "q": {"c": 4, "i": 4, "value": 500, "special": "witch", "picker": 0, "team": None, "bid": 300, "w": {"price": 300, "team": 2},
                              "judged": {}, "stage": "intro", "witchAsk": True}},
    "final": {**BASE, "screen": "final", "round": 1, "used": {}, "final": {"stage": "category", "wagers": [], "judged": []}},
    "podium": {**BASE, "screen": "podium", "round": 1, "used": {}, "final": {"stage": "done", "wagers": [], "judged": []},
               "teams": [{"name": "Team Elves", "score": 3400}, {"name": "Team Reindeer", "score": 2100}, {"name": "Team Snowmen", "score": 2800}, {"name": "Team Gingerbread", "score": 900}]},
}}

jobs = {"renders": [], "shots": []}
page_ogs, sitemap = {}, [URL]
for g in out_games:
    slug = g["slug"]
    print(f"- {slug}")
    src = open(f"{S}/{g['src']}", encoding="utf-8").read()
    write(f"{OUT}/{slug}/index.html", I.game_page(g, src))
    sitemap.append(f"{URL}{slug}/")
    if os.path.isfile(f"{S}/{g['audio']}/manifest.json"):
        shutil.copytree(f"{S}/{g['audio']}", f"{OUT}/{slug}/audio", dirs_exist_ok=True)
    else:
        print(f"   no {g['audio']}/ yet: this game falls back to the browser voice")
    run("node", f"{S}/tools/dump_q.js", f"{S}/{g['src']}", f"{B}/{slug}-q.json")
    shots = f"{S}/games/{slug}/shots"
    if not os.path.isdir(shots):
        run("python3", f"{S}/tools/fontify.py", f"{OUT}/{slug}/index.html", f"{B}/{slug}-local.html")
        os.makedirs(f"{B}/{slug}-shots", exist_ok=True)
        for n, st in SHOT_STATES[slug].items():
            jobs["shots"].append({"page": f"{B}/{slug}-local.html", "key": g["state_key"], "state": st, "out": f"{B}/{slug}-shots/{n}.png"})
    # content pages
    mod = importlib.import_module(f"pages_{slug}")
    mod.NAME = g["name"]
    mod.Q = json.load(open(f"{B}/{slug}-q.json", encoding="utf-8"))
    page_ogs[slug] = [(p["slug"], p["og"]) for p in mod.PAGES]
    P.use(g)
    for p in mod.PAGES:
        html = P.page(p["slug"], p["title"], p["desc"], p["og_title"], p["h1"], p["eyebrow"], p["body"](),
                      extra_ld=p.get("ld", lambda: None)(), crumb=p.get("crumb"), scripts=p.get("scripts", ""), today=TODAY)
        write(f"{OUT}/{slug}/{p['slug']}/index.html", html)
        sitemap.append(f"{URL}{slug}/{p['slug']}/")
        jobs["renders"].append({"src": f"{B}/seo/{slug}-og-{p['slug']}.html", "out": f"{OUT}/assets/{slug}/og/{p['slug']}.png", "w": 1200, "h": 630})
    write(f"{OUT}/assets/{slug}/pages.css", P.theme_css(g))
    jobs["renders"].append({"src": f"{B}/seo/{slug}-og.html", "out": f"{OUT}/{slug}/og-image.png", "w": 1200, "h": 630})
    os.makedirs(f"{OUT}/assets/{slug}/og", exist_ok=True)

print("- preview images, icons, screenshots")
O.make_all(out_games, page_ogs)
jobs["renders"].append({"src": f"{B}/seo/og.html", "out": f"{OUT}/og-image.png", "w": 1200, "h": 630})
for f, src, size in [("icon-512.png", "tile.html", 512), ("icon-192.png", "tile.html", 192), ("favicon-48.png", "tile.html", 48),
                     ("apple-touch-icon.png", "tile-square.html", 180)]:
    jobs["renders"].append({"src": f"{B}/seo/{src}", "out": f"{B}/seo/{f}", "w": 512, "h": 512, "scale": size / 512, "transparent": True})
json.dump(jobs, open(f"{B}/shoot-jobs.json", "w"))
run("node", f"{S}/tools/shoot_site.js", f"{B}/shoot-jobs.json")
from PIL import Image
for g in out_games:
    slug, shots = g["slug"], f"{S}/games/{g['slug']}/shots"
    if not os.path.isdir(shots):
        os.makedirs(shots)
        for n in SHOT_STATES[slug]:
            Image.open(f"{B}/{slug}-shots/{n}.png").convert("RGB").save(f"{shots}/{n}.webp", "WEBP", quality=82, method=6)
        print(f"   new screenshots in games/{slug}/shots/ (commit them)")
    shutil.copytree(shots, f"{OUT}/assets/{slug}/shots", dirs_exist_ok=True)
    shutil.copy(f"{B}/seo/{slug}-favicon.svg", f"{OUT}/assets/{slug}/favicon.svg")

print("- home page, privacy, site files")
write(f"{OUT}/index.html", H.home_page({g["slug"] for g in out_games}, TODAY))
write(f"{OUT}/privacy/index.html", H.privacy_page())
sitemap.append(f"{URL}privacy/")
for f in ["icon-192.png", "icon-512.png", "apple-touch-icon.png", "favicon.svg"]:
    shutil.copy(f"{B}/seo/{f}", f"{OUT}/{f}")
Image.open(f"{B}/seo/favicon-48.png").save(f"{OUT}/favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
json.dump({"name": BRAND, "short_name": "Game Nights", "start_url": "/", "display": "standalone",
           "background_color": H.HUB["night"], "theme_color": H.HUB["night"],
           "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]},
          open(f"{OUT}/site.webmanifest", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
write(f"{OUT}/robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {URL}sitemap.xml\n")
write(f"{OUT}/sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in sitemap) + "</urlset>\n")
write(f"{OUT}/CNAME", HOST + "\n")
write(f"{OUT}/404.html", H.not_found_page())
print("done:", OUT, "|", len(sitemap), "pages in the sitemap")
