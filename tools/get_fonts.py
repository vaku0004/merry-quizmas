"""Download the font files the build needs into fontpkgs/ (not kept in git). Run once on a new computer, from the repo root:

    python tools/get_fonts.py

Takes each font package from the npm registry (Fontsource, open fonts) and unpacks it to fontpkgs/fontsource-<name>-<version>/package/.
Works on Windows, macOS and Linux; needs only Python.
"""
import io, os, sys, tarfile, urllib.request

VERSION = "5.3.0"
FONTS = ["alegreya", "alegreya-sans", "oswald",                      # site and game text
         "pirata-one", "mountains-of-christmas", "yeseva-one", "eagle-lake",
         "righteous", "lilita-one", "limelight", "bungee"]           # each game's title font (see tools/games.py)
OUT = "fontpkgs"


def main():
    os.makedirs(OUT, exist_ok=True)
    for name in FONTS:
        dest = os.path.join(OUT, f"fontsource-{name}-{VERSION}")
        if os.path.isdir(os.path.join(dest, "package", "files")):
            print("have", name)
            continue
        url = f"https://registry.npmjs.org/@fontsource/{name}/-/{name}-{VERSION}.tgz"
        data = urllib.request.urlopen(url, timeout=60).read()
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as t:
            members = [m for m in t.getmembers() if m.name.startswith("package/") and ".." not in m.name and (m.isfile() or m.isdir())]
            t.extractall(dest, members=members)
        print("got ", name, f"({len(data) // 1024} KB)")
    print("done: fonts are in", OUT)


if __name__ == "__main__":
    sys.exit(main())
