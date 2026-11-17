"""Printable trivia PDF for one game (her request, Nov 17: "50 Christmas Trivia Questions" to download and share).

python tools/make_pdf.py <slug> <questions.json> <out.pdf>     (build_site.py runs it for the games in PRINTABLE)

US Letter, light pages (it gets printed in offices), the game's colours and title font, its art on the cover.
Part 1: the 50 questions by round and category, then the final and the tiebreaker (no answers, for reading out or for a
quiz without a screen). Part 2: the answer key with the short notes. Every page ends with the address of the game.
The HTML is rendered to PDF by tools/html_to_pdf.js (Playwright/Chromium), fonts from fontpkgs/.
"""
import glob, html, io, json, os, pathlib, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import games as G
from site_common import URL

PRINTABLE = ["christmas"]          # games that get a PDF; add slugs here (and the link appears on their trivia page)
e = lambda s: html.escape(str(s), quote=True)
S = os.path.abspath(".")


def qr_svg(url):
    """QR code as inline SVG (segno: pip install segno), black modules, sized by CSS; the white box and quiet zone come from CSS."""
    import segno
    b = io.BytesIO()
    q = segno.make(url, error="m", micro=False)
    q.save(b, kind="svg", xmldecl=False, svgns=True, scale=1, border=0, dark="#000")
    n = q.symbol_size(scale=1, border=0)[0]
    return re.sub(r'width="\d+" height="\d+"', f'viewBox="0 0 {n} {n}" shape-rendering="crispEdges"', b.getvalue().decode(), count=1)


def pdf_name(g):
    return f"{g['holiday'].lower().replace('’', '').replace(chr(39), '').replace(' ', '-')}-trivia-questions.pdf"


def _font_faces():
    """@font-face rules from fontpkgs/ for the text fonts and every game's title font."""
    out = []
    for fam, slug in [("Alegreya", "alegreya"), ("Alegreya Sans", "alegreya-sans")] + [(g["display"][0], g["display"][2]) for g in G.GAMES]:
        for f in glob.glob(f"{S}/fontpkgs/fontsource-{slug}-[0-9]*/package/files/{slug}-latin-*-*.woff2"):
            parts = f.replace("\\", "/").rsplit("-latin-", 1)[1][:-6].split("-")
            if len(parts) == 2 and parts[0].isdigit():
                out.append(f"@font-face{{font-family:'{fam}';font-weight:{parts[0]};font-style:{parts[1]};"
                           f"src:url({pathlib.Path(f).resolve().as_uri()}) format('woff2')}}")
    return "".join(out)


def page_html(g, Q):
    th, fam, w = g["theme"], g["display"][0], g["display"][1]
    art = G.art(g, g["page_art"].get("trivia-questions", g["icon"]))
    link = f"{URL.replace('https://', '').rstrip('/')}/{g['slug']}"
    href = f"{URL.rstrip('/')}/{g['slug']}/?utm_source=printable&utm_medium=pdf"   # GA shows visits from the PDF
    qr = qr_svg(f"{URL.rstrip('/')}/{g['slug']}/?utm_source=printable&utm_medium=qr")
    n_q = sum(len(c["qs"]) for r in Q["rounds"] for c in r["categories"])
    # Part 1: questions
    num, qs_html = 0, []
    for ri, r in enumerate(Q["rounds"]):
        qs_html.append(f'<h2 class="round">Round {"One" if ri == 0 else "Two"}<span>{r["values"][0]}–{r["values"][-1]} points</span></h2>')
        for c in r["categories"]:
            items = []
            for k, q in enumerate(c["qs"]):
                num += 1
                items.append(f'<li><span class="n">{num}</span><span class="v">{r["values"][k]}</span><span class="q">{e(q["q"])}</span></li>')
            qs_html.append(f'<section class="cat"><h3>{e(c["name"])}</h3><ol>{"".join(items)}</ol></section>')
    fin, tb = Q["final"], Q.get("tiebreak")
    qs_html.append(f'<section class="cat final"><h3>Final question · {e(fin["category"])}</h3>'
                   f'<p class="hint">Each team secretly writes down a wager before hearing the question.</p><p class="big-q">{e(fin["q"])}</p></section>')
    if tb:
        qs_html.append(f'<section class="cat final"><h3>Tiebreaker · closest number wins</h3><p class="big-q">{e(tb["q"])}</p></section>')
    # Part 2: answer key
    num, ans = 0, []
    for ri, r in enumerate(Q["rounds"]):
        ans.append(f'<h2 class="round">Round {"One" if ri == 0 else "Two"}</h2>')
        for c in r["categories"]:
            items = []
            for q in c["qs"]:
                num += 1
                note = f'<span class="note">{e(q["note"])}</span>' if q.get("note") else ""
                items.append(f'<li><span class="n">{num}</span><span><b>{e(q["a"])}</b>{note}</span></li>')
            ans.append(f'<section class="cat"><h3>{e(c["name"])}</h3><ol class="ans">{"".join(items)}</ol></section>')
    ans.append(f'<section class="cat"><h3>Final · {e(fin["category"])}</h3><ol class="ans"><li><span class="n">F</span><span><b>{e(fin["a"])}</b>'
               f'{"<span class=note>" + e(fin["note"]) + "</span>" if fin.get("note") else ""}</span></li>'
               + (f'<li><span class="n">T</span><span><b>{e(tb["a"])}</b>{"<span class=note>" + e(tb["note"]) + "</span>" if tb.get("note") else ""}</span></li>' if tb else "")
               + '</ol></section>')
    css = f"""{_font_faces()}
@page{{size:Letter;margin:0.55in 0.6in 0.7in}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:'Alegreya',Georgia,serif;font-size:11.5pt;line-height:1.38;color:#1d1b1a}}
.cover{{display:flex;gap:22px;align-items:center;border-radius:16px;padding:22px 26px;background:{th['night']};color:{th['bone']};margin-bottom:16px}}
.cover svg{{width:118px;height:118px;flex:none}}
.cover .eyebrow{{font-family:'Alegreya Sans',sans-serif;font-weight:800;font-size:8.5pt;letter-spacing:.16em;text-transform:uppercase;color:{th['ash']}}}
.cover h1{{font-family:'{fam}',serif;font-weight:{w};font-size:40pt;line-height:1;margin:4px 0 6px;color:{th['ember']}}}
.cover p{{margin:0;font-size:12pt}}
.how{{display:flex;gap:16px;margin:0 0 6px;font-family:'Alegreya Sans',sans-serif;font-size:9.8pt;line-height:1.35}}
.how div{{flex:1;border:1px solid #d9d4c7;border-radius:10px;padding:9px 12px}}
.how b{{display:block;color:{th['line']};font-size:10.5pt;margin-bottom:2px}}
h2.round{{font-family:'{fam}',serif;font-weight:{w};font-size:21pt;color:{th['line']};margin:18px 0 4px;border-bottom:2px solid {th['candle']};padding-bottom:2px}}
h2.round span{{font-family:'Alegreya Sans',sans-serif;font-weight:700;font-size:9.5pt;color:#6b6457;margin-left:10px;letter-spacing:.04em}}
.cat{{break-inside:avoid;margin:10px 0 6px}}
.cat h3{{font-family:'Alegreya Sans',sans-serif;font-weight:800;font-size:10.5pt;letter-spacing:.1em;text-transform:uppercase;color:{th['witch']};margin:0 0 4px}}
ol{{list-style:none;margin:0;padding:0}}
li{{display:flex;gap:8px;padding:3px 0;border-bottom:1px dotted #d9d4c7;break-inside:avoid}}
li .n{{flex:none;width:20px;font-family:'Alegreya Sans',sans-serif;font-weight:800;color:#8a8273;text-align:right}}
li .v{{flex:none;width:30px;font-family:'Alegreya Sans',sans-serif;font-weight:700;font-size:9pt;color:{th['line']};padding-top:1.5px}}
.final{{border:1.5px solid {th['candle']};border-radius:10px;padding:10px 14px;margin-top:14px}}
.final .hint{{margin:0 0 4px;font-family:'Alegreya Sans',sans-serif;font-size:9.5pt;color:#6b6457}}
.big-q{{margin:0;font-size:12.5pt}}
.part{{break-before:page}}
.part h1{{font-family:'{fam}',serif;font-weight:{w};font-size:28pt;color:{th['line']};margin:0 0 2px}}
.part .sub{{font-family:'Alegreya Sans',sans-serif;font-size:10pt;color:#6b6457;margin:0 0 6px}}
ol.ans li b{{color:#1d1b1a}}
ol.ans .note{{display:block;font-size:9.6pt;color:#5d574c;line-height:1.3}}
.cta{{break-inside:avoid;margin-top:18px;border-radius:14px;padding:16px 20px;background:{th['night']};color:{th['bone']};display:flex;gap:18px;align-items:center}}
.cta svg{{width:64px;height:64px;flex:none}}
.cta b{{display:block;font-family:'{fam}',serif;font-weight:{w};font-size:18pt;color:{th['ember']};line-height:1.05}}
.cta span{{font-family:'Alegreya Sans',sans-serif;font-size:10.5pt}}
.qr{{flex:none;background:#fff;border-radius:10px;padding:12px 12px 6px;text-align:center;margin-left:auto}}
.qr svg{{display:block;width:92px;height:92px}}
.qr small{{display:block;font-family:'Alegreya Sans',sans-serif;font-weight:700;font-size:7pt;color:#3a362f;margin-top:3px;letter-spacing:.03em}}
.cta .qr svg{{width:84px;height:84px}}
a{{color:inherit;text-decoration:none}}
.how a{{font-weight:700;color:{th['line']}}}
.cta .url{{display:inline-block;margin-top:5px;font-weight:800;font-size:12.5pt;color:{th['candle']}}}
"""
    footer = (f'<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7.5pt;color:#7a7365;padding:0 0.6in;display:flex;justify-content:space-between">'
              f'<span>{e(g["name"])} · free to play on the big screen at <b>{e(link)}</b></span>'
              f'<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')
    body = f"""<div class="cover">{art}<div><div class="eyebrow">Victoria’s Game Nights · printable quiz</div>
<h1>{n_q} {e(g['holiday'])} Trivia Questions</h1>
<p>From {e(g['short'])}, a quiz game for the office: questions by category, a final with wagers, a tiebreaker and an answer key.</p></div>
<div class="qr">{qr}<small>Scan to play</small></div></div>
<div class="how"><div><b>Quiz without a screen</b>Read the questions aloud, teams write their answers, check them with the answer key at the end.</div>
<div><b>Or play it on the big screen</b>The free game has a narrator, a game-show board, surprises and the scores: <a href="{e(href)}">{e(link)}</a></div></div>
{''.join(qs_html)}
<div class="part"><h1>Answer key</h1><p class="sub">With a short note to read out after each answer.</p>
{''.join(ans)}
<div class="cta">{G.art(g, g['icon'])}<div><b>Play {e(g['short'])} on the big screen</b>
<span>One laptop, one TV, a narrator who reads every question and a board that keeps the score. Free, no sign-up.</span><br>
<a class="url" href="{e(href)}">{e(link)}</a></div><div class="qr">{qr}<small>Scan to play</small></div></div></div>"""
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{n_q} {e(g["holiday"])} Trivia Questions · {e(g["short"])}</title><style>{css}</style></head><body>{body}</body></html>', footer


def make(slug, qjson, out):
    g = next(x for x in G.GAMES if x["slug"] == slug)
    Q = json.load(open(qjson, encoding="utf-8"))
    doc, footer = page_html(g, Q)
    tmp = os.path.splitext(out)[0] + ".html"
    open(tmp, "w", encoding="utf-8").write(doc)
    subprocess.run(["node", f"{S}/tools/html_to_pdf.js", tmp, out, footer], check=True)
    os.remove(tmp)


if __name__ == "__main__":
    make(*sys.argv[1:4])
