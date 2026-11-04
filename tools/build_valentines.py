"""Make Victoria's Sweetheart Showdown (Valentine's Day) from the Night of Frights game source.

python3 tools/build_valentines.py night-of-frights.html valentines/sweetheart-showdown.html

Game logic stays identical. Internal ids (special "cat"/"witch", wand1/wand2, CSS class names) are kept;
everything a player sees or hears is replaced: name, texts, narrator lines, questions, art, colours, font, music.
Surprises: "cat" = Cupid's Arrow, "witch" = Box of Chocolates. Final: The Love Letter.
"""
import re, sys

S = "."
src, out = sys.argv[1], sys.argv[2]
h = open(src, encoding="utf-8").read()


def rep(old, new, count=1):
    global h
    n = h.count(old)
    assert n == count, f"expected {count}x, found {n}x: {old[:90]!r}"
    h = h.replace(old, new)


def rep_re(pattern, new, count=1, flags=re.S):
    global h
    h, n = re.subn(pattern, lambda m: new, h, flags=flags)
    assert n == count, f"regex expected {count}, found {n}: {pattern[:80]}"


# ---------- Name, fonts, colours ----------
rep("<title>Viktoriia’s Night of Frights</title>", "<title>Viktoriia’s Sweetheart Showdown</title>")
rep("&family=Pirata+One&display=swap", "&family=Yeseva+One&display=swap")
rep("Single dark theme by design (Halloween night).", "Single dark theme by design (a candlelit Valentine's evening).")
rep("one candlelit game table", "one cosy candlelit game table")
for old, new in [("--night:#15111d", "--night:#1a0f17"), ("--dusk:#1f1929", "--dusk:#251520"), ("--cell:#2b2239", "--cell:#33192a"),
                 ("--cell-hi:#3a2e4c", "--cell-hi:#45223a"), ("--line:#41355a", "--line:#4a2a3c"), ("--bone:#f2e9d8", "--bone:#fbeff2"),
                 ("--ash:#ab9fbd", "--ash:#c7a9b6"), ("--candle:#f2a24c", "--candle:#ef7d9a"), ("--ember:#ffd58a", "--ember:#ffd6e0"),
                 ("--good:#84bd7c", "--good:#7fc4a0"), ("--bad:#e66a5e", "--bad:#e8485f"), ("--witch:#a98be0", "--witch:#d4935f")]:
    rep(old, new)
rep('--f-display:"Pirata One","Old English Text MT","Times New Roman",serif;',
    '--f-display:"Yeseva One","Georgia","Times New Roman",serif;')

# Soft rose-coloured sparkles drifting up behind everything (off with reduced motion)
SNOW = """
/* ---------- Sparkles: two slow layers of rosy specks behind the game ---------- */
body::before,body::after{content:"";position:fixed;inset:-20vh 0 0;pointer-events:none;z-index:0;
  background-image:radial-gradient(2px 2px at 20px 30px,rgba(255,170,195,.5),transparent 60%),radial-gradient(1.5px 1.5px at 120px 80px,rgba(255,214,224,.4),transparent 60%),
  radial-gradient(2.5px 2.5px at 200px 160px,rgba(239,125,154,.35),transparent 60%),radial-gradient(1.5px 1.5px at 60px 210px,rgba(255,190,210,.45),transparent 60%),
  radial-gradient(2px 2px at 260px 250px,rgba(255,230,238,.3),transparent 60%);
  background-size:300px 300px;animation:snow 46s linear infinite;opacity:.45}
body::after{background-size:420px 420px;animation-duration:60s;opacity:.35;filter:blur(.6px)}
@keyframes snow{from{transform:translateY(20vh)}to{transform:translateY(0)}}
#app{position:relative;z-index:1}
.title,.round-name,.slide-title,.big-cat,.cat-ask,.cat-team,.reel-face,.special h3{letter-spacing:.01em}
"""
rep("@media (prefers-reduced-motion:reduce){\n  *,*::before,*::after{animation:none!important;transition:none!important}\n}",
    SNOW + "@media (prefers-reduced-motion:reduce){\n  *,*::before,*::after{animation:none!important;transition:none!important}\n  body::before,body::after{display:none}\n}")

# ---------- Storage keys (separate from the Halloween game) ----------
rep('const KEY_S = "nof-state-v1", KEY_Q = "nof-questions-v1";', 'const KEY_S = "ss-state-v1", KEY_Q = "ss-questions-v1";')
rep('const KEY_V = "nof-voice-v1";', 'const KEY_V = "ss-voice-v1";')
rep('const TEAM_NAMES = ["Team Pumpkins","Team Bats","Team Ghosts","Team Witches"];',
    'const TEAM_NAMES = ["Team Lovebirds","Team Sweethearts","Team Roses","Team Truffles"];')

# ---------- Questions ----------
qs = open(f"{S}/valentines/questions.js", encoding="utf-8").read().strip()
rep_re(r"const DEFAULT_Q = \{.*?\n\};\n", qs + "\n")
# The Halloween game's migration of old saved questions does not apply here
rep_re(r"\(function migrateQ\(\)\{.*?\n\}\)\(\);\n", "")

# ---------- Art: same constant names, new pictures ----------
art = open(f"{S}/valentines/art.js", encoding="utf-8").read()
grab = lambda name: re.search(rf"^const {name} = `.*?`;$", art, re.M).group(0)
for old, new in [("CAT_SVG", "ARROW_SVG"), ("HAT_SVG", "CHOCOLATES_SVG"), ("MOON_SVG", "LETTER_SVG"), ("PUMPKIN_SVG", "HEART_SVG"),
                 ("GHOST_SVG", "ROSE_SVG"), ("WAND_SVG", "BONBON_SVG")]:
    rep_re(rf"^const {old} = `.*?`;$", grab(new).replace(f"const {new} =", f"const {old} =", 1), flags=re.M)

# ---------- Narrator ----------
LINES = '''const LINES = {
  test: "Welcome to Victoria's Sweetheart Showdown. Pick a question, and play from the heart!",
  welcome: "Welcome to Victoria's Sweetheart Showdown! Tonight, our teams compete for glory, and for chocolate. Here is how it works.",
  ready: "Ready? The first team, pick a question. Good luck, and may the sweetest team win.",
  rules: "Rules of the game. Pick a question from the board. Watch out for Cupid's arrow, and for the box of chocolates. Play two rounds and the Love Letter finale.",
  cat: "Cupid's arrow! You've been struck. The team that found it must give this question to another team.",
  catWho: "Who gets Cupid's arrow?",
  witchTitle: "A box of chocolates!",
  witch: "Let's open a box of chocolates! The first chocolate picks the price. The second chocolate picks the team that must answer. Answer right, and win it. Answer wrong, and lose it.",
  tie: "It's a tie! Time for a tiebreaker."
};'''
rep_re(r"const LINES = \{.*?\n\};", LINES)
rep('const midnightLine = () => "Midnight has come. The final category is: "', 'const midnightLine = () => "The Love Letter has arrived. The final category is: "')
rep('const winnerLine = name => name + " survive the night!";', 'const winnerLine = name => name + " won our hearts!";')
rep('const dealLine = name => name + ", the deal is yours!";', 'const dealLine = name => name + ", this chocolate is yours!";')
TTS = '''    [LINES.test]: "[warmly] Welcome to Victoria's Sweetheart Showdown. Pick a question... and play from the heart!",
    [LINES.welcome]: "[warmly] Welcome to Victoria's Sweetheart Showdown! Tonight, our teams compete for glory... and for chocolate. Here is how it works.",
    [LINES.ready]: "[cheerfully] Ready? The first team, pick a question. Good luck... and may the sweetest team win! [laughs]",
    [LINES.rules]: "[warmly] Rules of the game. Pick a question from the board. [playfully] Watch out for Cupid's arrow... and for the box of chocolates. [cheerfully] Play two rounds... and the Love Letter finale.",
    [LINES.cat]: "[gasps] Cupid's arrow! [playfully] You've been struck. The team that found it... must give this question to another team.",
    [LINES.catWho]: "[playfully] So... who gets Cupid's arrow?",
    [LINES.witchTitle]: "[whispers] A box... [playfully] of chocolates!",'''
rep_re(r'    \[LINES\.test\]: .*?\n    \[LINES\.witchTitle\]: [^\n]*\n', TTS + "\n")
rep('    [LINES.witch]: "[whispers] And now... [mischievously] with one of you... I shall make a deal! [laughs] My first wand picks the price. My second wand picks the team that must answer. Answer right... and win it. Answer wrong... [whispers] and lose it.",', '    [LINES.witch]: "[playfully] Let\'s open a box of chocolates! [laughs] The first chocolate picks the price. The second chocolate picks the team that must answer. Answer right... and win it. Answer wrong... [whispers] and lose it.",')
rep('if (/ survive the night!$/.test(t)) return "[excited] " + t + " [applause]";', 'if (/ won our hearts!$/.test(t)) return "[excited] " + t + " [applause]";')

# ---------- Final-round music: a slow music-box ballad with soft sparkles instead of the midnight lament ----------
rep("/* ===================== Midnight thinking music =====================\n   An original music-box tune over a descending \"lament\" bass, a low drone and a clock tick.",
    "/* ===================== Love Letter thinking music =====================\n   An original music-box ballad over a warm I-iii-IV-V bass, with soft sparkles.")
rep("const M_CHORDS = [[69,72,76],[68,71,76],[67,72,76],[66,69,74],[65,69,74],[64,68,71],[65,69,74],[64,68,74]];",
    "const M_CHORDS = [[72,76,79],[71,76,79],[69,72,77],[67,71,74],[72,76,79],[71,74,79],[69,72,77],[67,71,74]];")
rep("const M_BASS = [45,44,43,42,41,40,41,40];", "const M_BASS = [48,52,53,55,48,52,53,43];")
rep("const M_STEP = 60 / 104 / 2;   // eighth notes at 104 bpm", "const M_STEP = 60 / 84 / 2;    // eighth notes at 84 bpm")
rep('o1.type = o2.type = "sawtooth"; o1.frequency.value = 55; o2.frequency.value = 55.4;',
    'o1.type = o2.type = "sine"; o1.frequency.value = 65.4; o2.frequency.value = 65.7;')
rep('f.type = "lowpass"; f.frequency.value = 320; g.gain.value = 0.045;', 'f.type = "lowpass"; f.frequency.value = 400; g.gain.value = 0.02;')
rep('    if (pos % 2 === 0) this.note(pos % 4 === 0 ? 1900 : 1500, t, 0.03, "square", 0.01);   // tick, tock',
    '    if (pos % 8 === 0) this.note(pos % 16 === 0 ? 2093 : 2637, t, 0.5, "sine", 0.012);   // a soft sparkle every bar')

# ---------- Sound effects for the surprises ----------
rep('cat(){ tone(820,.45,"sine",.12,0,520); tone(700,.35,"sine",.08,.35,460); },',
    'cat(){ tone(500,.18,"sine",.1,0,1400); tone(1568,.35,"triangle",.09,.2); },')
rep('witch(){ [392,370,349,330].forEach((f,i)=>tone(f,.35,"sawtooth",.04,i*.13)); },',
    'witch(){ [523,659,784,1047].forEach((f,i)=>tone(f,.3,"triangle",.07,i*.11)); },')

# ---------- Rules slides ----------
rep('{ eyebrow: "Welcome to", title: "Viktoriia’s Night of Frights", art: hero(PUMPKIN_SVG),',
    '{ eyebrow: "Welcome to", title: "Viktoriia’s Sweetheart Showdown", art: hero(PUMPKIN_SVG),')
rep("Two rounds of spooky trivia, two cursed surprises and one last wager at midnight.",
    "Two rounds of sweet trivia, two surprises from Cupid and one last wager in a love letter.")
rep('bullets: ["Pick a question from the board.", "Beware the black cat and the witch.", "Survive two rounds and the midnight finale."],',
    'bullets: ["Pick a question from the board.", "Watch out for Cupid’s arrow and the box of chocolates.", "Play two rounds and the Love Letter finale."],')
rep('{ eyebrow: "Surprise", title: "Black Cat in the Bag", art: hero(CAT_SVG),\n      bullets: ["Find the black cat and you must give the question away.", "You choose which team gets it.", "That team answers for the full value, right or wrong."] },',
    '{ eyebrow: "Surprise", title: "Cupid’s Arrow", art: hero(CAT_SVG),\n      bullets: ["Get hit by Cupid’s arrow and you must give the question away.", "You choose which team gets it.", "That team answers for the full value, right or wrong."] },')
rep('{ eyebrow: "Surprise", title: "Deal with the Witch", art: hero(HAT_SVG),\n      bullets: ["The witch waves two magic wands.", `The first wand picks the price:',
    '{ eyebrow: "Surprise", title: "Box of Chocolates", art: hero(HAT_SVG),\n      bullets: ["Open the box of chocolates.", `The first chocolate picks the price:')
rep('"The second wand picks t', '"The second chocolate picks t')
rep('{ eyebrow: "The finale", title: "Midnight", art: hero(MOON_SVG),', '{ eyebrow: "The finale", title: "The Love Letter", art: hero(MOON_SVG),')
rep('"Only one team survives the night and wins."', '"Only one team wins our hearts."')
rep('if (deck === "midnight") return list.filter(sl => sl.title === "Midnight");', 'if (deck === "midnight") return list.filter(sl => sl.title === "The Love Letter");')
rep('return list.filter(sl => !["Black Cat in the Bag", "Deal with the Witch", "Double trouble", "Midnight"].includes(sl.title));',
    'return list.filter(sl => !["Cupid’s Arrow", "Box of Chocolates", "Double the love", "The Love Letter"].includes(sl.title));')

rep('{ eyebrow: "Round Two", title: "Double trouble", art: ladder,', '{ eyebrow: "Round Two", title: "Double the love", art: ladder,')
rep('if (deck === "round2") return list.filter(sl => sl.title === "Double trouble");', 'if (deck === "round2") return list.filter(sl => sl.title === "Double the love");')

# ---------- Start screen ----------
rep('<div class="eyebrow">A Halloween quiz for the whole office</div>', '<div class="eyebrow">A Valentine’s Day quiz for the whole office</div>')
rep('<h1 class="title"><span class="byline">Viktoriia’s</span>Night of Frights</h1>', '<h1 class="title"><span class="byline">Viktoriia’s</span>Sweetheart Showdown</h1>')
rep("Two rounds of spooky trivia, two cursed surprises on the board, and one last wager at midnight.",
    "Two rounds of sweet trivia, two surprises from Cupid on the board, and one last wager in a love letter.")
rep("<li>${CAT_SVG}<div><b>Black Cat in the Bag</b><p>The team that finds the black cat must hand the question to another team.",
    "<li>${CAT_SVG}<div><b>Cupid’s Arrow</b><p>The team that gets hit by Cupid’s arrow must hand the question to another team.")
rep("<li>${HAT_SVG}<div><b>Deal with the Witch</b><p>The witch waves two wands. The first picks a random price, the second picks the team that must answer.",
    "<li>${HAT_SVG}<div><b>Box of Chocolates</b><p>Two chocolates come out of the box. The first picks a random price, the second picks the team that must answer.")
rep("<li>${MOON_SVG}<div><b>Midnight</b><p>Round Two doubles every value.", "<li>${MOON_SVG}<div><b>The Love Letter</b><p>Round Two doubles every value.")

# ---------- Board, question cards, final, podium, editor ----------
rep('const nextLabel = finalDone ? "Back to the standings" : isLast ? "Go to Midnight"', 'const nextLabel = finalDone ? "Back to the standings" : isLast ? "Go to the Love Letter"')
rep('<div class="eyebrow">Viktoriia’s Night of Frights</div>', '<div class="eyebrow">Viktoriia’s Sweetheart Showdown</div>')
rep('<div class="special blackcat">${CAT_SVG}<div><h3>Black Cat in the Bag</h3>\n      <p>${esc(T[q.picker].name)} found the black cat and must hand this question to another team.',
    '<div class="special blackcat">${CAT_SVG}<div><h3>Cupid’s Arrow</h3>\n      <p>${esc(T[q.picker].name)} got hit by Cupid’s arrow and must hand this question to another team.')
rep('<h3 class="cat-ask">Who gets the cat?</h3>', '<h3 class="cat-ask">Who gets the arrow?</h3>')
rep('<div class="special witch">${HAT_SVG}<div><h3>Deal with the Witch</h3>\n      ${q.witchAsk ? `<p class="witch-quote" style="animation:rise-in .5s ease both">“And now, with one of you, I shall make a deal!”</p>` : ""}',
    '<div class="special witch">${HAT_SVG}<div><h3>Box of Chocolates</h3>\n      ${q.witchAsk ? `<p class="witch-quote" style="animation:rise-in .5s ease both">“Let’s see what’s inside this box…”</p>` : ""}')
rep("<span><b>First wand</b> picks the price:", "<span><b>First chocolate</b> picks the price:")
rep("<span><b>Second wand</b> picks the team that must answer.", "<span><b>Second chocolate</b> picks the team that must answer.")
rep('<div class="reel-label">First wand · The price</div>', '<div class="reel-label">First chocolate · The price</div>')
rep("${WAND_SVG} Wave the first wand</button>", "${WAND_SVG} Pick a chocolate</button>")
rep('<div class="reel-label">Second wand · The team</div>', '<div class="reel-label">Second chocolate · The team</div>')
rep("${WAND_SVG} Wave the second wand</button>", "${WAND_SVG} Pick another</button>")
rep('${q.special==="cat"?`<div class="special blackcat">${CAT_SVG}<div><h3>Black Cat in the Bag</h3></div></div>`:""}',
    '${q.special==="cat"?`<div class="special blackcat">${CAT_SVG}<div><h3>Cupid’s Arrow</h3></div></div>`:""}')
rep('${q.special==="witch"?`<div class="special witch">${HAT_SVG}<div><h3>Deal with the Witch</h3></div></div>`:""}',
    '${q.special==="witch"?`<div class="special witch">${HAT_SVG}<div><h3>Box of Chocolates</h3></div></div>`:""}')
rep('<div class="eyebrow">Midnight · final category</div>', '<div class="eyebrow">The Love Letter · final category</div>')
rep('<div class="eyebrow">Midnight · ${esc(F.category)}</div>', '<div class="eyebrow">The Love Letter · ${esc(F.category)}</div>', 2)
rep('const headline = winners.length === 1 ? esc(winners[0].name) + " survive the night"', 'const headline = winners.length === 1 ? esc(winners[0].name) + " won our hearts"')
rep('<div class="eyebrow">Viktoriia’s Night of Frights · final standings</div>', '<div class="eyebrow">Viktoriia’s Sweetheart Showdown · final standings</div>')
rep('<option value="cat" ${q.special==="cat"?"selected":""}>Black Cat in the Bag</option>', '<option value="cat" ${q.special==="cat"?"selected":""}>Cupid’s Arrow</option>')
rep('<option value="witch" ${q.special==="witch"?"selected":""}>Deal with the Witch</option>', '<option value="witch" ${q.special==="witch"?"selected":""}>Box of Chocolates</option>')
rep('data-t="final" aria-selected="${tab==="final"}">Midnight</button>', 'data-t="final" aria-selected="${tab==="final"}">Love Letter</button>')

rep('<button class="btn" data-act="vpreset" data-p="spooky">Spooky voice</button>', '<button class="btn" data-act="vpreset" data-p="spooky">Sweetheart voice</button>')

# Phone layout (same rules as the Halloween website) built into the game itself
sys.path.insert(0, f"{S}/tools")
from site_common import MOBILE_CSS
rep("</style>\n\n<div id=\"app\"></div>", "</style>\n" + MOBILE_CSS + "\n\n<div id=\"app\"></div>")

open(out, "w", encoding="utf-8").write(h)

left = [w for w in ["Halloween", "Night of Frights", "Black Cat", "black cat", "Witch", "witch'", "Midnight", "midnight", "spooky", "Spooky",
                    "pumpkin", "Pumpkin", "Dracula", "scream", "survive the night", "wand", "Christmas", "Krampus", "coal"] if w.lower() in h.lower()]
print("built", out, "| words still present (check):", left)
