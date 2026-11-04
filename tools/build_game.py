"""Build a game from the engine and its theme.

python3 tools/build_game.py <slug> [<slug> ...]     e.g. christmas valentines    (or --all)
Writes games/<slug>/game.html. Run from the repo root.

The engine (engine/game.html) is the complete Halloween game. engine/slots.py lists every piece of it that a game can
change (texts, colours, font, art, narrator lines, sounds, music); games/<slug>/theme.py gives that game's values.
Every slot a theme changes must be found in the engine exactly as often as slots.py says, or the build stops.
To make a new game: copy a games/<slug>/ folder, edit theme.py, questions.js and art.js, add it to tools/games.py.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from site_common import MOBILE_CSS
from slots import SLOTS

S = "."
ENGINE = f"{S}/engine/game.html"
# Words that must not appear in a non-Halloween game's visible text (internal ids like "cat"/"witch" are fine)
HALLOWEEN_WORDS = ["Halloween", "Night of Frights", "Black Cat", "black cat", "Midnight", "spooky", "Spooky", "pumpkin", "Pumpkin",
                   "Dracula", "survive the night", "Deal with the Witch", "magic wand"]


def load_theme(slug):
    folder = f"{S}/games/{slug}"
    art_src = open(f"{folder}/art.js", encoding="utf-8").read() if os.path.isfile(f"{folder}/art.js") else ""

    def file(name):
        return open(f"{folder}/{name}", encoding="utf-8").read()

    def art(name, as_name):
        line = re.search(rf"^const {name} = `.*?`;$", art_src, re.M).group(0)
        return line.replace(f"const {name} =", f"const {as_name} =", 1)

    g = {"file": file, "art": art, "MOBILE_CSS": MOBILE_CSS}
    exec(open(f"{folder}/theme.py", encoding="utf-8").read(), g)
    return g["VALUES"]


def build(slug):
    values = load_theme(slug)
    unknown = set(values) - {s["key"] for s in SLOTS}
    assert not unknown, f"{slug}: theme values for slots that do not exist: {sorted(unknown)}"
    h = open(ENGINE, encoding="utf-8").read()
    for s in SLOTS:
        if s["key"] not in values:
            continue
        new, count = values[s["key"]], s.get("count", 1)
        if s["kind"] == "text":
            n = h.count(s["find"])
            assert n == count, f"{slug}: slot {s['key']}: expected {count}x, found {n}x: {s['find'][:80]!r}"
            h = h.replace(s["find"], new)
        else:
            h, n = re.subn(s["find"], lambda m: new, h, flags=s.get("flags", re.S))
            assert n == count, f"{slug}: slot {s['key']}: regex expected {count}, found {n}"
    out = f"{S}/games/{slug}/game.html"
    open(out, "w", encoding="utf-8").write(h)
    visible = re.sub(r"/\*.*?\*/", "", h, flags=re.S).replace('data-p="spooky"', "").replace('=== "spooky"', "")   # skip comments and ids
    left = [w for w in HALLOWEEN_WORDS if w in visible] if values else []
    print(f"built {out}: {len(values)} slots changed" + (f" | check these words: {left}" if left else ""))


if __name__ == "__main__":
    slugs = sys.argv[1:]
    if slugs == ["--all"]:
        slugs = sorted(d for d in os.listdir(f"{S}/games") if os.path.isfile(f"{S}/games/{d}/theme.py"))
    for slug in slugs:
        build(slug)
