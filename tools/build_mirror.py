"""Copy the main site (night-of-frights repo) into the night-of-frights-game repo, which GitHub Pages serves at
https://vaku0004.github.io/night-of-frights-game/ with no redirect to the custom domain.

python3 build_mirror.py <main_repo_dir> <mirror_repo_dir>

What differs from the main site:
- no CNAME (that file is what makes GitHub redirect), no Search Console / IndexNow files, no sitemap or robots.txt;
- root links ("/faq/", "/assets/...") get the /night-of-frights-game prefix, because the copy lives in a subfolder;
- every page says noindex and keeps its canonical URL on nightoffrights.monster, so search engines see one site, not two.
"""
import os, re, shutil, sys

MAIN, MIRROR = sys.argv[1], sys.argv[2]
BASE = "/night-of-frights-game"
SKIP = {"CNAME", "sitemap.xml", "robots.txt", ".git"}
SKIP_RE = re.compile(r"^(google[0-9a-f]+\.html|[0-9a-f]{32}\.txt)$")

# Start clean (keep .git) so files deleted from the main site disappear from the copy too
for name in os.listdir(MIRROR):
    if name == ".git":
        continue
    p = os.path.join(MIRROR, name)
    shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

for name in os.listdir(MAIN):
    if name in SKIP or SKIP_RE.match(name):
        continue
    src, dst = os.path.join(MAIN, name), os.path.join(MIRROR, name)
    shutil.copytree(src, dst) if os.path.isdir(src) else shutil.copy2(src, dst)


def fix_html(text):
    text = re.sub(r'(href|src)="/(?!/)', rf'\1="{BASE}/', text)
    text = text.replace('content="index, follow, max-image-preview:large"', 'content="noindex, follow"')
    # page-events script: links into the game and the page label
    text = text.replace("a[href=\"/\"]", f"a[href=\"{BASE}/\"]")
    text = text.replace("location.pathname.replace(/\\//g, '')", f"location.pathname.replace('{BASE}', '').replace(/\\//g, '')")
    return text


changed = 0
for root, dirs, files in os.walk(MIRROR):
    if ".git" in root.split(os.sep):
        continue
    for f in files:
        p = os.path.join(root, f)
        if f.endswith(".html"):
            t = open(p, encoding="utf-8").read()
            n = fix_html(t)
            assert 'href="/' not in n.replace(f'href="{BASE}/', "") and 'src="/' not in n.replace(f'src="{BASE}/', ""), p
            if n != t:
                open(p, "w", encoding="utf-8").write(n); changed += 1
        elif f == "site.webmanifest":
            t = open(p, encoding="utf-8").read()
            t = t.replace('"start_url": "/"', f'"start_url": "{BASE}/"').replace('"src": "/', f'"src": "{BASE}/')
            open(p, "w", encoding="utf-8").write(t)

readme = os.path.join(MIRROR, "README.md")
t = open(readme, encoding="utf-8").read()
t = t.replace("# Viktoriia's Night of Frights 🎃\n",
              "# Viktoriia's Night of Frights 🎃\n\n"
              "> A copy of [nightoffrights.monster](https://nightoffrights.monster/) that opens on GitHub Pages without "
              "redirecting: **https://vaku0004.github.io/night-of-frights-game/**. "
              "The main project lives in [vaku0004/night-of-frights](https://github.com/vaku0004/night-of-frights); "
              "this repository is updated from it.\n", 1)
open(readme, "w", encoding="utf-8").write(t)
print("html files adjusted:", changed)
