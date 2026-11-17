"""Pinterest pins for a game (her request, Nov 17: promote the free printable PDF and the game on Pinterest).

python tools/make_pins.py christmas pins/christmas        (needs build/<slug>-q.json and build/site-win/assets/<slug>/printable.webp,
                                                           i.e. run tools/build_site.py build/site-win first)

Five vertical pins, 1000x1500 PNG (Pinterest's 2:3), in the game's colours and title font, rendered by tools/render_pins.js
(Playwright). Each pin gets a title, description, alt text and link in pins.json next to the images: that file is what
goes into Pinterest. Links carry utm_source=pinterest so GA shows the visits per pin.
"""
import html, json, os, pathlib, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import games as G
from make_pdf import _font_faces, pdf_name
from site_common import URL

e = lambda s: html.escape(str(s), quote=True)
S = os.path.abspath(".")
uri = lambda p: pathlib.Path(p).resolve().as_uri()


def css(g, light=False):
    th, fam, w = g["theme"], g["display"][0], g["display"][1]
    bg, fg, title, sub = (("#f6f1e6", "#1d2a24", "#1f5a43", "#4a5a52") if light else (th["night"], th["bone"], th["ember"], th["ash"]))
    glow = "rgba(230,179,76,.16)" if not light else "rgba(201,72,79,.10)"
    return f"""{_font_faces()}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1000px;height:1500px;overflow:hidden}}
body{{font-family:'Alegreya Sans',sans-serif;color:{fg};
  background:radial-gradient(circle at 85% 8%,{glow},transparent 45%),radial-gradient(circle at 10% 95%,{glow},transparent 40%),{bg};
  display:flex;flex-direction:column;padding:70px 70px 0;position:relative}}
body:before{{content:"";position:absolute;inset:26px;border:2px solid {th['line'] if not light else '#d8cfba'};border-radius:30px;pointer-events:none}}
.snow{{position:absolute;inset:0;pointer-events:none;opacity:{.0 if light else .55};
  background-image:radial-gradient(circle,#fff 1.3px,transparent 2px),radial-gradient(circle,#fff 1px,transparent 1.6px);
  background-size:120px 130px,77px 83px;background-position:13px 21px,51px 7px}}
.pill{{align-self:flex-start;font-weight:800;font-size:27px;letter-spacing:.14em;text-transform:uppercase;padding:12px 24px;border-radius:999px;
  background:{th['witch']};color:#fff;position:relative}}
h1{{font-family:'{fam}',serif;font-weight:{w};color:{title};font-size:132px;line-height:.98;margin:26px 0 18px;position:relative}}
.sub{{font-family:'Alegreya',serif;font-size:40px;line-height:1.25;color:{sub};position:relative}}
.grow{{flex:1;display:flex;align-items:center;justify-content:center;position:relative;min-height:0}}
.cta{{position:relative;margin:0 -70px;padding:34px 70px 58px;display:flex;align-items:center;justify-content:space-between;gap:20px}}
.btn{{background:{th['candle']};color:#14100a;font-weight:800;font-size:38px;padding:22px 34px;border-radius:18px}}
.url{{font-weight:800;font-size:34px;color:{th['candle'] if not light else th['witch']}}}
.brand{{font-size:24px;letter-spacing:.12em;text-transform:uppercase;font-weight:800;color:{sub};margin-bottom:6px}}
"""


def page(g, body, light=False):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{css(g, light)}{body[1]}</style></head><body><div class="snow"></div>{body[0]}</body></html>'


def footer(btn, url):
    return (f'<div class="cta"><div><div class="brand">Victoria’s Game Nights</div><div class="url">{e(url)}</div></div>'
            f'<div class="btn">{e(btn)}</div></div>')


def pins(g, Q):
    slug, art = g["slug"], G.art(g, g["icon"])
    site = URL.replace("https://", "").rstrip("/")
    cats = [c for r in Q["rounds"] for c in r["categories"]]
    n_q = sum(len(c["qs"]) for c in cats)
    prev = uri(f"{S}/build/site-win/assets/{slug}/printable.webp")
    board = uri(f"{S}/games/{slug}/shots/board.webp")
    find = lambda start: next(q for c in cats for q in c["qs"] if q["q"].startswith(start))
    teaser = [find("Under which plant"), find("In Home Alone"), find("How many sides")]
    link = lambda path, pin: f"{URL}{path}?utm_source=pinterest&utm_medium=social&utm_campaign={slug}-{pin}"
    out = []

    # 1. the free printable PDF
    out.append(dict(
        file="01-free-printable.png",
        html=page(g, (f"""<div class="pill">Free printable PDF</div>
<h1>{n_q} Christmas Trivia Questions</h1>
<p class="sub">with answers, for office parties, team events and family quiz nights</p>
<div class="grow"><img src="{prev}" style="width:1010px;margin:0 -60px"></div>
<p class="sub" style="text-align:center;font-family:'Alegreya Sans';font-weight:700;color:inherit;font-size:34px">10 categories · a final with wagers · answer key</p>
{footer("Download free", f"{site}/{slug}/")}""", "")),
        title=f"{n_q} Christmas Trivia Questions with Answers (Free Printable PDF)",
        description=(f"Free printable Christmas trivia: {n_q} questions in 10 categories, a final with wagers, a tiebreaker and an answer key "
                     "with fun facts. Great for office holiday parties, team events, classrooms and family quiz nights. "
                     "Print it, read it aloud, or play it as a game on the big screen."),
        alt=f"Two pages of a printable PDF with {n_q} Christmas trivia questions and an answer key",
        link=link(f"{slug}/trivia-questions/", "printable"), board="Christmas Trivia Questions"))

    # 2. teaser questions
    cards = "".join(f'<div class="q"><span class="n">{i + 1}</span><span>{e(q["q"])}</span></div>' for i, q in enumerate(teaser))
    out.append(dict(
        file="02-can-you-answer.png",
        html=page(g, (f"""<div class="pill">Christmas trivia</div>
<h1>Can you answer these?</h1>
<p class="sub">Three questions from our holiday quiz. Answers are in the free printable.</p>
<div class="grow" style="flex-direction:column;gap:26px;align-items:stretch">{cards}</div>
<p class="sub" style="text-align:center;margin-bottom:6px">+ {n_q - 3} more questions and an answer key</p>
{footer("Get the answers", f"{site}/{slug}/")}""",
            f""".q{{display:flex;gap:26px;align-items:flex-start;background:{g['theme']['dusk']};border:2px solid {g['theme']['line']};border-radius:24px;padding:30px 34px;
  font-family:'Alegreya',serif;font-size:42px;line-height:1.22}}
.q .n{{flex:none;width:66px;height:66px;border-radius:50%;background:{g['theme']['candle']};color:#14100a;font-family:'Alegreya Sans';font-weight:800;
  font-size:38px;display:flex;align-items:center;justify-content:center;margin-top:2px}}""")),
        title="Can You Answer These Christmas Trivia Questions?",
        description=("Test your holiday knowledge: mistletoe, Home Alone and snowflakes. Get the answers plus 47 more Christmas trivia "
                     "questions in a free printable PDF, perfect for office parties, Zoom calls and family game night."),
        alt="Three Christmas trivia questions on a dark green card: mistletoe, Home Alone and snowflakes",
        link=link(f"{slug}/trivia-questions/", "teaser"), board="Christmas Trivia Questions"))

    # 3. the game on the big screen
    chips = "".join(f"<li>{e(t)}</li>" for _, t in g["chips"])
    out.append(dict(
        file="03-office-party-game.png",
        html=page(g, (f"""<div class="pill">Free · no sign-up</div>
<h1 style="font-size:122px">Office Christmas Party Game</h1>
<p class="sub">Trivia on the big screen: teams, scores, a narrator who reads every question and a Christmas Eve final.</p>
<div class="grow"><img class="tv" src="{board}"></div>
<ul class="chips">{chips}</ul>
{footer("Play free", f"{site}/{slug}/")}""",
            f""".tv{{width:880px;border-radius:18px;border:10px solid #050807;box-shadow:0 30px 60px rgba(0,0,0,.55),0 0 0 2px {g['theme']['line']};transform:rotate(-2deg)}}
.chips{{list-style:none;display:flex;flex-wrap:wrap;gap:14px;justify-content:center;position:relative;margin-bottom:4px}}
.chips li{{border:2px solid {g['theme']['candle']};color:{g['theme']['ember']};border-radius:999px;padding:10px 22px;font-size:30px;font-weight:700}}""")),
        title="Office Christmas Party Game: Free Trivia on the Big Screen",
        description=(f"{g['name']} is a free Christmas trivia game for work: 2 to 4 teams, a game-show board, a narrator, "
                     "surprises like Naughty or Nice and Krampus's Bargain, and a Christmas Eve final with secret wagers. "
                     "One laptop and a TV, no sign-up. Works for hybrid teams on Zoom or Teams too."),
        alt=f"The {g['name']} game board on a TV screen with Christmas trivia categories and point values",
        link=link(f"{slug}/", "game"), board="Christmas Party Games for Work"))

    # 4. categories, light pin
    cat_list = "".join(f"<li>{e(c['name'])}</li>" for c in cats)
    out.append(dict(
        file="04-categories.png",
        html=page(g, (f"""<div class="pill">{n_q} questions · answers included</div>
<h1>Christmas Trivia Questions &amp; Answers</h1>
<div class="grow" style="gap:40px"><div class="art">{art}</div><ol class="cats">{cat_list}</ol></div>
{footer("Free printable", f"{site}/{slug}/")}""",
            f""".art svg{{width:300px;height:300px}}
.cats{{list-style:none;counter-reset:c;columns:1;font-size:50px;font-weight:700;line-height:1.45}}
.cats li{{counter-increment:c}}
.cats li:before{{content:counter(c) ". ";color:{g['theme']['witch']};font-weight:800}}
.cta .btn{{background:#1f5a43;color:#fff}}""", ), light=True),
        title="Christmas Trivia Questions and Answers in 10 Categories",
        description=("Christmas trivia for adults and kids alike: Deck the Halls, Christmas movies, Santa's workshop, holiday hits, "
                     "Christmas around the world, winter folklore and Canadian traditions. 50 questions with answers as a free printable PDF."),
        alt="List of ten Christmas trivia categories next to a decorated Christmas tree",
        link=link(f"{slug}/trivia-questions/", "categories"), board="Christmas Trivia Questions"))

    # 5. host guide
    steps = [("What you need", "a laptop, a TV or projector and speakers"), ("Teams", "2 to 4 teams of 3 to 5 people, mixed departments"),
             ("One hour", "two rounds, two surprises and a Christmas Eve final"), ("Make it yours", "swap in questions about your office"),
             ("Prizes", "small, funny and under $25")]
    st = "".join(f'<li><b>{e(a)}</b>{e(b)}</li>' for a, b in steps)
    out.append(dict(
        file="05-host-guide.png",
        html=page(g, (f"""<div class="pill">Step-by-step guide</div>
<h1 style="font-size:120px">How to Host a Christmas Game Night at Work</h1>
<div class="grow"><ol class="steps">{st}</ol></div>
{footer("Read the guide", f"{site}/{slug}/")}""",
            f""".steps{{list-style:none;counter-reset:s;display:flex;flex-direction:column;gap:22px;width:100%}}
.steps li{{counter-increment:s;display:grid;grid-template-columns:76px 1fr;column-gap:24px;font-size:36px;line-height:1.25;font-family:'Alegreya',serif}}
.steps li:before{{content:counter(s);grid-row:span 2;width:76px;height:76px;border-radius:50%;border:3px solid {g['theme']['candle']};color:{g['theme']['ember']};
  font-family:'Alegreya Sans';font-weight:800;font-size:40px;display:flex;align-items:center;justify-content:center}}
.steps b{{font-family:'Alegreya Sans';font-size:40px;color:{g['theme']['ember']}}}""")),
        title="How to Host a Christmas Game Night at Work (Step-by-Step)",
        description=("Planning the office holiday party? A simple guide to hosting a Christmas trivia game night: equipment, teams, "
                     "a one-hour timeline, office questions and prize ideas under $25. The game itself is free to play on a big screen."),
        alt="Five steps for hosting a Christmas game night at work: equipment, teams, one hour, office questions, prizes",
        link=link(f"{slug}/how-to-host-a-game-night/", "host"), board="Christmas Party Games for Work"))
    return out


def make(slug, out_dir):
    g = next(x for x in G.GAMES if x["slug"] == slug)
    Q = json.load(open(f"{S}/build/{slug}-q.json", encoding="utf-8"))
    os.makedirs(out_dir, exist_ok=True)
    jobs, meta = [], []
    for p in pins(g, Q):
        src = os.path.join(out_dir, p["file"].replace(".png", ".html"))
        open(src, "w", encoding="utf-8").write(p.pop("html"))
        jobs.append({"src": os.path.abspath(src), "out": os.path.abspath(os.path.join(out_dir, p["file"]))})
        meta.append(p)
    subprocess.run(["node", f"{S}/tools/render_pins.js", json.dumps(jobs)], check=True)
    for j in jobs:
        os.remove(j["src"])
    json.dump(meta, open(os.path.join(out_dir, "pins.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    make(sys.argv[1], sys.argv[2])
