"""Make a local test copy of a built page with fonts loaded from the fontsource packages (no network)."""
import glob, sys
S = "."
src, out = sys.argv[1], sys.argv[2]
h = open(src, encoding="utf-8").read()
F = f"{S}/fontpkgs"
faces = [("Pirata One","pirata-one",[(400,"normal")]),("Mountains of Christmas","mountains-of-christmas",[(700,"normal")]),("Alegreya","alegreya",[(400,"normal"),(500,"normal"),(700,"normal"),(400,"italic"),(500,"italic"),(700,"italic")]),
("Alegreya Sans","alegreya-sans",[(400,"normal"),(500,"normal"),(700,"normal"),(800,"normal")]),("Oswald","oswald",[(400,"normal"),(500,"normal"),(600,"normal")])]
css = "".join(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};src:url(file://{glob.glob(f'{F}/fontsource-{slug}-[0-9]*/package/files/{slug}-latin-{w}-{st}.woff2')[0]})}}" for fam,slug,ss in faces for w,st in ss)
s = h.index('<link rel="preconnect" href="https://fonts.googleapis.com">'); e = h.index('display=swap">', s) + len('display=swap">')
h = h[:s] + "<style>" + css + "</style>" + h[e:]
h = h.replace('<script async src="https://www.googletagmanager.com', '<script async data-off src="about:blank#')
open(out, "w", encoding="utf-8").write(h)
