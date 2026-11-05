"""Write the fonts from fontpkgs/ as base64 @font-face rules, for tools/check_site.js (served in place of Google Fonts). From the repo root:

    python tools/fonts_css.py build/fonts.css
"""
import base64, glob, sys

FAMS = {"Pirata One": "pirata-one", "Mountains of Christmas": "mountains-of-christmas", "Yeseva One": "yeseva-one",
        "Eagle Lake": "eagle-lake", "Righteous": "righteous", "Lilita One": "lilita-one", "Limelight": "limelight",
        "Bungee": "bungee", "Alegreya": "alegreya", "Alegreya Sans": "alegreya-sans", "Oswald": "oswald"}

out = []
for fam, slug in FAMS.items():
    for f in sorted(glob.glob(f"fontpkgs/fontsource-{slug}-[0-9]*/package/files/{slug}-latin-*-*.woff2")):
        parts = f.rsplit("-latin-", 1)[1][:-6].split("-")      # "400-normal"; skips latin-ext
        if len(parts) != 2 or not parts[0].isdigit():
            continue
        w, st = parts
        data = base64.b64encode(open(f, "rb").read()).decode()
        out.append(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};src:url(data:font/woff2;base64,{data})}}")
if not out:
    sys.exit("no fonts found: run python tools/get_fonts.py first")
open(sys.argv[1], "w", encoding="utf-8").write("".join(out))
print(len(out), "font faces ->", sys.argv[1])
