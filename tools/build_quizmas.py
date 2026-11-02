"""Make Victoria's Merry Quizmas from the Night of Frights game source.

python3 build_quizmas.py <night-of-frights.html> <out.html>

Game logic stays identical. Internal ids (special "cat"/"witch", wand1/wand2, CSS class names) are kept;
everything a player sees or hears is replaced: name, texts, narrator lines, questions, art, colours, font, music.
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
rep("<title>Viktoriia’s Night of Frights</title>", "<title>Viktoriia’s Merry Quizmas</title>")
rep("&family=Pirata+One&display=swap", "&family=Mountains+of+Christmas:wght@700&display=swap")
rep("Single dark theme by design (Halloween night).", "Single dark theme by design (a snowy Christmas night).")
rep("one candlelit game table", "one cosy game table by the tree")
for old, new in [("--night:#15111d", "--night:#0d1714"), ("--dusk:#1f1929", "--dusk:#15231e"), ("--cell:#2b2239", "--cell:#1c3029"),
                 ("--cell-hi:#3a2e4c", "--cell-hi:#28443a"), ("--line:#41355a", "--line:#33544a"), ("--bone:#f2e9d8", "--bone:#f6f1e6"),
                 ("--ash:#ab9fbd", "--ash:#a8c0b6"), ("--candle:#f2a24c", "--candle:#e6b34c"), ("--ember:#ffd58a", "--ember:#ffe6a6"),
                 ("--good:#84bd7c", "--good:#5fae6e"), ("--bad:#e66a5e", "--bad:#e2554f"), ("--witch:#a98be0", "--witch:#c9484f")]:
    rep(old, new)
rep('--f-display:"Pirata One","Old English Text MT","Times New Roman",serif;',
    '--f-display:"Mountains of Christmas","Georgia","Times New Roman",serif;')

# Gentle snowfall behind everything (off with reduced motion)
SNOW = """
/* ---------- Snow: two slow layers of flakes behind the game ---------- */
body::before,body::after{content:"";position:fixed;inset:-20vh 0 0;pointer-events:none;z-index:0;
  background-image:radial-gradient(2px 2px at 20px 30px,rgba(255,255,255,.55),transparent 60%),radial-gradient(1.5px 1.5px at 120px 80px,rgba(255,255,255,.45),transparent 60%),
  radial-gradient(2.5px 2.5px at 200px 160px,rgba(255,255,255,.35),transparent 60%),radial-gradient(1.5px 1.5px at 60px 210px,rgba(255,255,255,.5),transparent 60%),
  radial-gradient(2px 2px at 260px 250px,rgba(255,255,255,.3),transparent 60%);
  background-size:300px 300px;animation:snow 38s linear infinite;opacity:.55}
body::after{background-size:420px 420px;animation-duration:60s;opacity:.35;filter:blur(.6px)}
@keyframes snow{from{transform:translateY(0)}to{transform:translateY(20vh)}}
#app{position:relative;z-index:1}
.title,.round-name,.slide-title,.big-cat,.cat-ask,.cat-team,.reel-face,.special h3{letter-spacing:.01em}
"""
rep("@media (prefers-reduced-motion:reduce){\n  *,*::before,*::after{animation:none!important;transition:none!important}\n}",
    SNOW + "@media (prefers-reduced-motion:reduce){\n  *,*::before,*::after{animation:none!important;transition:none!important}\n  body::before,body::after{display:none}\n}")

# ---------- Storage keys (separate from the Halloween game) ----------
rep('const KEY_S = "nof-state-v1", KEY_Q = "nof-questions-v1";', 'const KEY_S = "mq-state-v1", KEY_Q = "mq-questions-v1";')
rep('const KEY_V = "nof-voice-v1";', 'const KEY_V = "mq-voice-v1";')
rep('const TEAM_NAMES = ["Team Pumpkins","Team Bats","Team Ghosts","Team Witches"];',
    'const TEAM_NAMES = ["Team Elves","Team Reindeer","Team Snowmen","Team Gingerbread"];')

# ---------- Questions ----------
qs = open(f"{S}/quizmas/questions.js", encoding="utf-8").read().strip()
rep_re(r"const DEFAULT_Q = \{.*?\n\};\n", qs + "\n")
# The Halloween game's migration of old saved questions does not apply here
rep_re(r"\(function migrateQ\(\)\{.*?\n\}\)\(\);\n", "")

# ---------- Art: same constant names, new pictures ----------
art = open(f"{S}/quizmas/art.js", encoding="utf-8").read()
grab = lambda name: re.search(rf"^const {name} = `.*?`;$", art, re.M).group(0)
for old, new in [("CAT_SVG", "COAL_SVG"), ("HAT_SVG", "KRAMPUS_SVG"), ("MOON_SVG", "STAR_SVG"), ("PUMPKIN_SVG", "TREE_SVG"),
                 ("GHOST_SVG", "GIFT_SVG"), ("WAND_SVG", "SACK_SVG")]:
    rep_re(rf"^const {old} = `.*?`;$", grab(new).replace(f"const {new} =", f"const {old} =", 1), flags=re.M)

# ---------- Narrator ----------
LINES = '''const LINES = {
  test: "Welcome to Victoria's Merry Quizmas. Pick a question, and make it merry!",
  welcome: "Welcome to Victoria's Merry Quizmas! Tonight, our teams compete for glory, and for prizes. Here is how it works.",
  ready: "Ready? The first team, pick a question. Good luck, and may the merriest team win.",
  rules: "Rules of the game. Pick a question from the board. Watch out for the naughty list, and for Krampus. Survive two rounds and the Christmas Eve finale.",
  cat: "Naughty or nice? You found a lump of coal! The team that found it must give this question to another team.",
  catWho: "Who gets the coal?",
  witchTitle: "A bargain with Krampus!",
  witch: "And now, with one of you, I shall strike a bargain! My first draw picks the price. My second draw picks the team that must answer. Answer right, and win it. Answer wrong, and lose it.",
  tie: "It's a tie! Time for a tiebreaker."
};'''
rep_re(r"const LINES = \{.*?\n\};", LINES)
rep('const midnightLine = () => "Midnight has come. The final category is: "', 'const midnightLine = () => "Christmas Eve has come. The final category is: "')
rep('const winnerLine = name => name + " survive the night!";', 'const winnerLine = name => name + " saved Christmas!";')
rep('const dealLine = name => name + ", the deal is yours!";', 'const dealLine = name => name + ", the bargain is yours!";')
TTS = '''    [LINES.test]: "[cheerfully] Welcome to Victoria's Merry Quizmas. Pick a question... and make it merry!",
    [LINES.welcome]: "[warmly] Welcome to Victoria's Merry Quizmas! Tonight, our teams compete for glory... and for prizes. Here is how it works.",
    [LINES.ready]: "[cheerfully] Ready? The first team, pick a question. Good luck... and may the merriest team win! [laughs]",
    [LINES.rules]: "[warmly] Rules of the game. Pick a question from the board. [mischievously] Watch out for the naughty list... and for Krampus. [cheerfully] Survive two rounds... and the Christmas Eve finale.",
    [LINES.cat]: "[mischievously] Naughty or nice? You found a lump of coal! The team that found it... must give this question to another team.",
    [LINES.catWho]: "[mischievously] So... who gets the coal?",
    [LINES.witchTitle]: "[whispers] A bargain... [mischievously] with Krampus!",'''
rep_re(r'    \[LINES\.test\]: .*?\n    \[LINES\.witchTitle\]: [^\n]*\n', TTS + "\n")
rep('    [LINES.witch]: "[whispers] And now... [mischievously] with one of you... I shall make a deal! [laughs] My first wand picks the price. My second wand picks the team that must answer. Answer right... and win it. Answer wrong... [whispers] and lose it.",', '    [LINES.witch]: "[whispers] And now... [mischievously] with one of you... I shall strike a bargain! [laughs] My first draw picks the price. My second draw picks the team that must answer. Answer right... and win it. Answer wrong... [whispers] and lose it.",')
rep('if (/ survive the night!$/.test(t)) return "[excited] " + t + " [applause]";', 'if (/ saved Christmas!$/.test(t)) return "[excited] " + t + " [applause]";')

# ---------- Final-round music: a warm music box with sleigh bells instead of the midnight lament ----------
rep("/* ===================== Midnight thinking music =====================\n   An original music-box tune over a descending \"lament\" bass, a low drone and a clock tick.",
    "/* ===================== Christmas Eve thinking music =====================\n   An original music-box tune over a warm I-vi-IV-V bass, with soft sleigh bells.")
rep("const M_CHORDS = [[69,72,76],[68,71,76],[67,72,76],[66,69,74],[65,69,74],[64,68,71],[65,69,74],[64,68,74]];",
    "const M_CHORDS = [[72,76,79],[69,72,76],[65,69,72],[67,71,74],[72,76,79],[69,72,76],[65,69,74],[67,71,77]];")
rep("const M_BASS = [45,44,43,42,41,40,41,40];", "const M_BASS = [48,45,41,43,48,45,41,43];")
rep("const M_STEP = 60 / 104 / 2;   // eighth notes at 104 bpm", "const M_STEP = 60 / 96 / 2;    // eighth notes at 96 bpm")
rep('o1.type = o2.type = "sawtooth"; o1.frequency.value = 55; o2.frequency.value = 55.4;',
    'o1.type = o2.type = "sine"; o1.frequency.value = 65.4; o2.frequency.value = 65.7;')
rep('f.type = "lowpass"; f.frequency.value = 320; g.gain.value = 0.045;', 'f.type = "lowpass"; f.frequency.value = 400; g.gain.value = 0.02;')
rep('    if (pos % 2 === 0) this.note(pos % 4 === 0 ? 1900 : 1500, t, 0.03, "square", 0.01);   // tick, tock',
    '    if (pos % 2 === 0){ this.note(pos % 4 === 0 ? 5200 : 6100, t, 0.06, "square", 0.006); this.note(pos % 4 === 0 ? 6700 : 7400, t + 0.02, 0.05, "square", 0.004); }   // sleigh bells')

# ---------- Sound effects for the surprises ----------
rep('cat(){ tone(820,.45,"sine",.12,0,520); tone(700,.35,"sine",.08,.35,460); },',
    'cat(){ tone(330,.35,"triangle",.12,0,250); tone(262,.5,"triangle",.1,.3,196); },')
rep('witch(){ [392,370,349,330].forEach((f,i)=>tone(f,.35,"sawtooth",.04,i*.13)); },',
    'witch(){ [196,185,175,165].forEach((f,i)=>tone(f,.4,"sawtooth",.05,i*.14)); },')

# ---------- Rules slides ----------
rep('{ eyebrow: "Welcome to", title: "Viktoriia’s Night of Frights", art: hero(PUMPKIN_SVG),',
    '{ eyebrow: "Welcome to", title: "Viktoriia’s Merry Quizmas", art: hero(PUMPKIN_SVG),')
rep("Two rounds of spooky trivia, two cursed surprises and one last wager at midnight.",
    "Two rounds of festive trivia, two naughty surprises and one last wager on Christmas Eve.")
rep('bullets: ["Pick a question from the board.", "Beware the black cat and the witch.", "Survive two rounds and the midnight finale."],',
    'bullets: ["Pick a question from the board.", "Watch out for the naughty list and for Krampus.", "Survive two rounds and the Christmas Eve finale."],')
rep('{ eyebrow: "Surprise", title: "Black Cat in the Bag", art: hero(CAT_SVG),\n      bullets: ["Find the black cat and you must give the question away.", "You choose which team gets it.", "That team answers for the full value, right or wrong."] },',
    '{ eyebrow: "Surprise", title: "Naughty or Nice", art: hero(CAT_SVG),\n      bullets: ["Find a lump of coal and you must give the question away.", "You choose which team gets it.", "That team answers for the full value, right or wrong."] },')
rep('{ eyebrow: "Surprise", title: "Deal with the Witch", art: hero(HAT_SVG),\n      bullets: ["The witch waves two magic wands.", `The first wand picks the price:',
    '{ eyebrow: "Surprise", title: "Krampus’s Bargain", art: hero(HAT_SVG),\n      bullets: ["Krampus reaches into his sack twice.", `The first draw picks the price:')
rep('"The second wand picks t', '"The second draw picks t')
rep('{ eyebrow: "The finale", title: "Midnight", art: hero(MOON_SVG),', '{ eyebrow: "The finale", title: "Christmas Eve", art: hero(MOON_SVG),')
rep('"Only one team survives the night and wins."', '"Only one team saves Christmas and wins."')
rep('if (deck === "midnight") return list.filter(sl => sl.title === "Midnight");', 'if (deck === "midnight") return list.filter(sl => sl.title === "Christmas Eve");')
rep('return list.filter(sl => !["Black Cat in the Bag", "Deal with the Witch", "Double trouble", "Midnight"].includes(sl.title));',
    'return list.filter(sl => !["Naughty or Nice", "Krampus’s Bargain", "Double trouble", "Christmas Eve"].includes(sl.title));')

# ---------- Start screen ----------
rep('<div class="eyebrow">A Halloween quiz for the whole office</div>', '<div class="eyebrow">A Christmas quiz for the whole office</div>')
rep('<h1 class="title"><span class="byline">Viktoriia’s</span>Night of Frights</h1>', '<h1 class="title"><span class="byline">Viktoriia’s</span>Merry Quizmas</h1>')
rep("Two rounds of spooky trivia, two cursed surprises on the board, and one last wager at midnight.",
    "Two rounds of festive trivia, two naughty surprises on the board, and one last wager on Christmas Eve.")
rep("<li>${CAT_SVG}<div><b>Black Cat in the Bag</b><p>The team that finds the black cat must hand the question to another team.",
    "<li>${CAT_SVG}<div><b>Naughty or Nice</b><p>The team that finds a lump of coal must hand the question to another team.")
rep("<li>${HAT_SVG}<div><b>Deal with the Witch</b><p>The witch waves two wands. The first picks a random price, the second picks the team that must answer.",
    "<li>${HAT_SVG}<div><b>Krampus’s Bargain</b><p>Krampus draws twice from his sack. The first draw picks a random price, the second picks the team that must answer.")
rep("<li>${MOON_SVG}<div><b>Midnight</b><p>Round Two doubles every value.", "<li>${MOON_SVG}<div><b>Christmas Eve</b><p>Round Two doubles every value.")

# ---------- Board, question cards, final, podium, editor ----------
rep('const nextLabel = finalDone ? "Back to the standings" : isLast ? "Go to Midnight"', 'const nextLabel = finalDone ? "Back to the standings" : isLast ? "Go to Christmas Eve"')
rep('<div class="eyebrow">Viktoriia’s Night of Frights</div>', '<div class="eyebrow">Viktoriia’s Merry Quizmas</div>')
rep('<div class="special blackcat">${CAT_SVG}<div><h3>Black Cat in the Bag</h3>\n      <p>${esc(T[q.picker].name)} found the black cat and must hand this question to another team.',
    '<div class="special blackcat">${CAT_SVG}<div><h3>Naughty or Nice</h3>\n      <p>${esc(T[q.picker].name)} found a lump of coal and must hand this question to another team.')
rep('<h3 class="cat-ask">Who gets the cat?</h3>', '<h3 class="cat-ask">Who gets the coal?</h3>')
rep('<div class="special witch">${HAT_SVG}<div><h3>Deal with the Witch</h3>\n      ${q.witchAsk ? `<p class="witch-quote" style="animation:rise-in .5s ease both">“And now, with one of you, I shall make a deal!”</p>` : ""}',
    '<div class="special witch">${HAT_SVG}<div><h3>Krampus’s Bargain</h3>\n      ${q.witchAsk ? `<p class="witch-quote" style="animation:rise-in .5s ease both">“And now, with one of you, I shall strike a bargain!”</p>` : ""}')
rep("<span><b>First wand</b> picks the price:", "<span><b>First draw</b> picks the price:")
rep("<span><b>Second wand</b> picks the team that must answer.", "<span><b>Second draw</b> picks the team that must answer.")
rep('<div class="reel-label">First wand · The price</div>', '<div class="reel-label">First draw · The price</div>')
rep("${WAND_SVG} Wave the first wand</button>", "${WAND_SVG} Draw from the sack</button>")
rep('<div class="reel-label">Second wand · The team</div>', '<div class="reel-label">Second draw · The team</div>')
rep("${WAND_SVG} Wave the second wand</button>", "${WAND_SVG} Draw again</button>")
rep('${q.special==="cat"?`<div class="special blackcat">${CAT_SVG}<div><h3>Black Cat in the Bag</h3></div></div>`:""}',
    '${q.special==="cat"?`<div class="special blackcat">${CAT_SVG}<div><h3>Naughty or Nice</h3></div></div>`:""}')
rep('${q.special==="witch"?`<div class="special witch">${HAT_SVG}<div><h3>Deal with the Witch</h3></div></div>`:""}',
    '${q.special==="witch"?`<div class="special witch">${HAT_SVG}<div><h3>Krampus’s Bargain</h3></div></div>`:""}')
rep('<div class="eyebrow">Midnight · final category</div>', '<div class="eyebrow">Christmas Eve · final category</div>')
rep('<div class="eyebrow">Midnight · ${esc(F.category)}</div>', '<div class="eyebrow">Christmas Eve · ${esc(F.category)}</div>', 2)
rep('const headline = winners.length === 1 ? esc(winners[0].name) + " survive the night"', 'const headline = winners.length === 1 ? esc(winners[0].name) + " saved Christmas"')
rep('<div class="eyebrow">Viktoriia’s Night of Frights · final standings</div>', '<div class="eyebrow">Viktoriia’s Merry Quizmas · final standings</div>')
rep('<option value="cat" ${q.special==="cat"?"selected":""}>Black Cat in the Bag</option>', '<option value="cat" ${q.special==="cat"?"selected":""}>Naughty or Nice</option>')
rep('<option value="witch" ${q.special==="witch"?"selected":""}>Deal with the Witch</option>', '<option value="witch" ${q.special==="witch"?"selected":""}>Krampus’s Bargain</option>')
rep('data-t="final" aria-selected="${tab==="final"}">Midnight</button>', 'data-t="final" aria-selected="${tab==="final"}">Christmas Eve</button>')

rep('<button class="btn" data-act="vpreset" data-p="spooky">Spooky voice</button>', '<button class="btn" data-act="vpreset" data-p="spooky">Storyteller voice</button>')

# Phone layout (same rules as the Halloween website) built into the game itself
sys.path.insert(0, f"{S}/tools")
from site_common import MOBILE_CSS
rep("</style>\n\n<div id=\"app\"></div>", "</style>\n" + MOBILE_CSS + "\n\n<div id=\"app\"></div>")

open(out, "w", encoding="utf-8").write(h)

left = [w for w in ["Halloween", "Night of Frights", "Black Cat", "black cat", "Witch", "witch'", "Midnight", "midnight", "spooky", "Spooky",
                    "pumpkin", "Pumpkin", "Dracula", "scream", "survive the night", "wand"] if w.lower() in h.lower()]
print("built", out, "| words still present (check):", left)
