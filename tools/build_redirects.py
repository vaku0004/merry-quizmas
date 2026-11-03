"""Turn the old nightoffrights.monster site (repo vaku0004/night-of-frights) into redirects to Victoria's Game Nights.

python3 tools/build_redirects.py <night_of_frights_repo_dir>

Run it only after the new site is live on its domain. Every old address gets a small page that sends the visitor
(and search engines: canonical + instant meta refresh) to the same page on the new site. The CNAME, the Search
Console and IndexNow verification files and .git are kept; everything else is replaced.
"""
import html, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_common import URL, BRAND

OLD = sys.argv[1]
MAP = {"": "halloween/", "halloween-trivia-questions/": "halloween/trivia-questions/",
       "virtual-halloween-games-for-work/": "halloween/virtual-games-for-work/",
       "how-to-host-a-halloween-game-night/": "halloween/how-to-host-a-game-night/", "faq/": "halloween/faq/"}
KEEP = re.compile(r"^(\.git|CNAME|google[0-9a-f]+\.html|[0-9a-f]{32}\.txt)$")

for name in os.listdir(OLD):
    if KEEP.match(name):
        continue
    p = os.path.join(OLD, name)
    shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)


def redirect(target):
    t = html.escape(target, quote=True)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Victoria’s Night of Frights has moved</title>
<link rel="canonical" href="{t}">
<meta http-equiv="refresh" content="0; url={t}">
<script>location.replace({target!r} + location.hash);</script>
</head>
<body style="font-family:Georgia,serif;background:#15111d;color:#f2e9d8;padding:40px 16px">
<p>Victoria’s Night of Frights is now part of {html.escape(BRAND)}: <a style="color:#ffd58a" href="{t}">{t}</a></p>
</body>
</html>
'''


for old, new in MAP.items():
    os.makedirs(os.path.join(OLD, old), exist_ok=True)
    open(os.path.join(OLD, old, "index.html"), "w", encoding="utf-8").write(redirect(URL + new))
open(os.path.join(OLD, "404.html"), "w", encoding="utf-8").write(redirect(URL + "halloween/"))
open(os.path.join(OLD, "robots.txt"), "w").write("User-agent: *\nAllow: /\n")
open(os.path.join(OLD, "README.md"), "w", encoding="utf-8").write(
    f"# Viktoriia's Night of Frights 🎃\n\nThe game has moved to **{BRAND}**: {URL}halloween/\n\n"
    "This repository only keeps nightoffrights.monster working: every old page forwards to the same page on the new site. "
    "The source lives in [vaku0004/merry-quizmas](https://github.com/vaku0004/merry-quizmas) (later vaku0004/game-nights).\n")
print("redirect pages:", len(MAP) + 1)
