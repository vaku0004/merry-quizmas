"""Every game on Victoria's Game Nights: names, colours, art, texts for the game page and the home-page card.

status: "live" (published), "scheduled" (published on `launch`; before that only a "coming" card), "soon" (card only).
Add a new game here, plus games/<slug>/ (theme.py, questions.js, art.js; see tools/build_game.py) and a pages_<slug>.py module with its content pages.
"""
import re

S = "."


def _svgs(path, pattern=r"^const (\w+_SVG) = `(.*?)`;$"):
    return dict(re.findall(pattern, open(f"{S}/{path}", encoding="utf-8").read(), re.M))


def art(game, name):
    """An SVG from the game's own source, with theme variables filled in (for pages outside the game)."""
    svg = _svgs(game["art_src"])[name]
    for k, v in game["theme"].items():
        if v.startswith("#"):
            svg = svg.replace(f"var(--{k})", v)
    return svg.replace(' class="glyph"', "")


HALLOWEEN = dict(
    slug="halloween", status="live", launch=None,
    name="Victoria’s Night of Frights", short="Night of Frights", holiday="Halloween",
    src="games/halloween/game.html", art_src="engine/game.html", audio="audio/halloween", state_key="nof-state-v1",
    icon="PUMPKIN_SVG", specials={"cat": "black_cat", "witch": "witch"},
    theme=dict(night="#15111d", dusk="#1f1929", cell="#2b2239", line="#41355a", bone="#f2e9d8", ash="#ab9fbd",
               candle="#f2a24c", ember="#ffd58a", good="#84bd7c", witch="#a98be0", bad="#e66a5e"),
    rgb=dict(night="21,17,29", dusk="31,25,41", glow="242,162,76", glow2="169,139,224"), tag2="var(--witch)",
    display=("Pirata One", 400, "pirata-one", '"Pirata One","Old English Text MT","Times New Roman",serif'),
    gfont="Pirata+One",
    title="Victoria’s Night of Frights · Halloween Office Quiz Game",
    desc="Free Halloween trivia game for office parties and team events: a spooky game-show board, a black cat, a witch’s deal and a midnight wager.",
    og_desc="A free Halloween quiz for the whole office: spooky trivia, a black cat, a witch’s deal and a midnight wager, with a narrator.",
    og_alt="a Halloween quiz for the whole office, with a glowing jack-o'-lantern",
    eyebrow="A Halloween quiz for the whole office",
    intro="A free Halloween trivia game for office parties and team events, made for a big screen. Teams pick spooky questions on a game-show board, think for 30 seconds and answer. A narrator reads every question aloud.",
    rules=[("Two rounds", "of five Halloween and Canadian categories, worth 100–500 and then 200–1,000 points."),
           ("Black Cat in the Bag:", "the team that finds the cat must hand the question to another team."),
           ("Deal with the Witch:", "two magic wands pick a random price and the team that must answer."),
           ("Midnight:", "one final question with secret wagers, then a podium for the winning team.")],
    chips=[("CAT_SVG", "Black cat"), ("HAT_SVG", "Witch’s deal"), ("MOON_SVG", "Midnight wager")],
    card="Spooky trivia, a black cat, a witch’s deal and a midnight wager, with a narrator who loves a good scare.",
    page_art={"trivia-questions": "PUMPKIN_SVG", "virtual-games-for-work": "GHOST_SVG", "how-to-host-a-game-night": "CANDLE_SVG", "faq": "CAT_SVG"},
    shots=["board", "question", "witch", "cat", "final", "podium"],
)

CHRISTMAS = dict(
    slug="christmas", status="scheduled", launch="2026-11-15",
    name="Victoria’s Merry Quizmas", short="Merry Quizmas", holiday="Christmas",
    src="games/christmas/game.html", art_src="games/christmas/art.js", audio="audio/christmas", state_key="mq-state-v1",
    icon="TREE_SVG", specials={"cat": "naughty_or_nice", "witch": "krampus"},
    theme=dict(night="#0d1714", dusk="#15231e", cell="#1c3029", line="#33544a", bone="#f6f1e6", ash="#a8c0b6",
               candle="#e6b34c", ember="#ffe6a6", good="#5fae6e", witch="#c9484f", bad="#e2554f"),
    rgb=dict(night="13,23,20", dusk="21,35,30", glow="230,179,76", glow2="201,72,79"), tag2="#f08a85",
    display=("Mountains of Christmas", 700, "mountains-of-christmas", '"Mountains of Christmas",Georgia,"Times New Roman",serif'),
    gfont="Mountains+of+Christmas:wght@700",
    title="Victoria’s Merry Quizmas · Christmas Office Quiz Game",
    desc="Free Christmas trivia game for office parties and team events: a festive game-show board, Naughty or Nice, Krampus’s Bargain and a Christmas Eve wager.",
    og_desc="A free Christmas quiz for the whole office: holiday trivia, Naughty or Nice, Krampus’s Bargain and a Christmas Eve wager, with a narrator.",
    og_alt="a Christmas quiz for the whole office, with a glowing Christmas tree",
    eyebrow="A Christmas quiz for the whole office",
    intro="A free Christmas trivia game for office parties and team events, made for a big screen. Teams pick holiday questions on a game-show board, think for 30 seconds and answer. A warm narrator reads every question aloud.",
    rules=[("Two rounds", "of five Christmas and Canadian categories, worth 100–500 and then 200–1,000 points."),
           ("Naughty or Nice:", "the team that finds a lump of coal must hand the question to another team."),
           ("Krampus’s Bargain:", "Krampus draws twice from his sack: first the price, then the team that must answer."),
           ("Christmas Eve:", "one final question with secret wagers, then a podium for the team that saved Christmas.")],
    chips=[("COAL_SVG", "Naughty or Nice"), ("KRAMPUS_SVG", "Krampus’s Bargain"), ("STAR_SVG", "Christmas Eve wager")],
    card="Holiday trivia, Naughty or Nice, Krampus’s Bargain and a Christmas Eve wager, read by a jolly storyteller.",
    page_art={"trivia-questions": "TREE_SVG", "virtual-games-for-work": "GIFT_SVG", "how-to-host-a-game-night": "STAR_SVG", "faq": "KRAMPUS_SVG"},
    shots=["board", "question", "krampus", "coal", "final", "podium"],
)

VALENTINES = dict(
    slug="valentines", status="scheduled", launch="2027-01-20",
    name="Victoria’s Sweetheart Showdown", short="Sweetheart Showdown", holiday="Valentine’s Day",
    src="games/valentines/game.html", art_src="games/valentines/art.js", audio="audio/valentines", state_key="ss-state-v1",
    icon="HEART_SVG", specials={"cat": "cupids_arrow", "witch": "box_of_chocolates"},
    theme=dict(night="#1a0f17", dusk="#251520", cell="#33192a", line="#4a2a3c", bone="#fbeff2", ash="#c7a9b6",
               candle="#ef7d9a", ember="#ffd6e0", good="#7fc4a0", witch="#d4935f", bad="#e8485f"),
    rgb=dict(night="26,15,23", dusk="37,21,32", glow="239,125,154", glow2="212,147,95"), tag2="var(--witch)",
    display=("Yeseva One", 400, "yeseva-one", '"Yeseva One",Georgia,"Times New Roman",serif'),
    gfont="Yeseva+One",
    title="Victoria’s Sweetheart Showdown · Valentine’s Day Office Quiz Game",
    desc="Free Valentine’s Day trivia game for office parties and team events: a game-show board, Cupid’s Arrow, a box of chocolates and a love-letter wager.",
    og_desc="A free Valentine’s Day quiz for the whole office: sweet trivia, Cupid’s Arrow, a box of chocolates and a love-letter wager, with a narrator.",
    og_alt="a Valentine’s Day quiz for the whole office, with a glowing heart",
    eyebrow="A Valentine’s Day quiz for the whole office",
    intro="A free Valentine’s Day trivia game for office parties and team events, made for a big screen. Teams pick sweet questions on a game-show board, think for 30 seconds and answer. A narrator reads every question aloud. Love of every kind, and nothing awkward for the office.",
    rules=[("Two rounds", "of five categories about love, chocolate, flowers, movies, songs and more, worth 100–500 and then 200–1,000 points."),
           ("Cupid’s Arrow:", "the team that gets hit by the arrow must hand the question to another team."),
           ("Box of Chocolates:", "two chocolates pick a random price and the team that must answer."),
           ("The Love Letter:", "one final question with secret wagers, then a podium for the team that won our hearts.")],
    chips=[("ARROW_SVG", "Cupid’s Arrow"), ("CHOCOLATES_SVG", "Box of Chocolates"), ("LETTER_SVG", "Love Letter wager")],
    card="Sweet trivia about love of every kind, Cupid’s Arrow, a box of chocolates and a love-letter wager. Nothing awkward for the office.",
    page_art={"trivia-questions": "HEART_SVG", "virtual-games-for-work": "LETTER_SVG", "how-to-host-a-game-night": "ROSE_SVG", "faq": "CHOCOLATES_SVG"},
    shots=["board", "question", "chocolates", "arrow", "final", "podium"],
)

STPATRICKS = dict(
    slug="stpatricks", status="scheduled", launch="2027-02-10",
    name="Victoria’s Pot o’ Gold", short="Pot o’ Gold", holiday="St. Patrick’s Day",
    src="games/stpatricks/game.html", art_src="games/stpatricks/art.js", audio="audio/stpatricks", state_key="pg-state-v1",
    icon="SHAMROCK_SVG", specials={"cat": "leprechauns_trick", "witch": "over_the_rainbow"},
    theme=dict(night="#0c1a12", dusk="#13261b", cell="#1a3324", line="#2f5a3e", bone="#f4f1e4", ash="#a9c2ae",
               candle="#e8b84a", ember="#ffe7a3", good="#5fbf73", witch="#7fb8e8", bad="#e2604f"),
    rgb=dict(night="12,26,18", dusk="19,38,27", glow="232,184,74", glow2="95,191,115"), tag2="var(--witch)",
    display=("Eagle Lake", 400, "eagle-lake", '"Eagle Lake",Georgia,"Times New Roman",serif'),
    gfont="Eagle+Lake",
    title="Victoria’s Pot o’ Gold · St. Patrick’s Day Office Quiz Game",
    desc="Free St. Patrick’s Day trivia game for office parties and team events: a game-show board, a leprechaun’s trick, a rainbow and a pot-of-gold wager.",
    og_desc="A free St. Patrick’s Day quiz for the whole office: Irish trivia, a leprechaun’s trick, a rainbow and a pot-of-gold wager, with a narrator.",
    og_alt="a St. Patrick’s Day quiz for the whole office, with a glowing shamrock",
    eyebrow="A St. Patrick’s Day quiz for the whole office",
    intro="A free St. Patrick’s Day trivia game for office parties and team events, made for a big screen. Teams pick lucky questions on a game-show board, think for 30 seconds and answer. A narrator reads every question aloud.",
    rules=[("Two rounds", "of five categories about Ireland, luck, legends, words, music, food and St. Patrick himself, worth 100–500 and then 200–1,000 points."),
           ("Leprechaun’s Trick:", "the team that finds the leprechaun must hand the question to another team."),
           ("Over the Rainbow:", "the rainbow appears twice and picks a random price and the team that must answer."),
           ("End of the Rainbow:", "one final question with secret wagers, then a podium for the team that found the pot of gold.")],
    chips=[("LEPRECHAUN_SVG", "Leprechaun’s Trick"), ("RAINBOW_SVG", "Over the Rainbow"), ("POT_SVG", "Pot-of-gold wager")],
    card="Irish trivia, myths and legends, a leprechaun’s trick, a rainbow and a pot-of-gold wager, for the luckiest team in the office.",
    page_art={"trivia-questions": "SHAMROCK_SVG", "virtual-games-for-work": "RAINBOW_SVG", "how-to-host-a-game-night": "POT_SVG", "faq": "LEPRECHAUN_SVG"},
    shots=["board", "question", "rainbow", "leprechaun", "final", "podium"],
)

DECADES = dict(
    slug="decades", status="live", launch=None,
    name="Victoria’s Decades Showdown", short="Decades Showdown", holiday="Retro",
    src="games/decades/game.html", art_src="games/decades/art.js", audio="audio/decades", state_key="ds-state-v1",
    icon="CASSETTE_SVG", specials={"cat": "tangled_tape", "witch": "time_machine"},
    theme=dict(night="#120d24", dusk="#1c1533", cell="#281d47", line="#43356e", bone="#f5f0ff", ash="#b3a8d6",
               candle="#ff5aa8", ember="#ffd1ec", good="#3be8b0", witch="#3fd5ff", bad="#ff6b5a"),
    rgb=dict(night="18,13,36", dusk="28,21,51", glow="255,90,168", glow2="63,213,255"), tag2="var(--witch)",
    display=("Righteous", 400, "righteous", '"Righteous","Arial Rounded MT Bold",Helvetica,sans-serif'),
    gfont="Righteous",
    title="Victoria’s Decades Showdown · ’80s, ’90s and 2000s Office Quiz Game",
    desc="Free retro trivia game for office parties and team events: ’80s, ’90s and 2000s questions on a game-show board, a tangled tape, a time machine and a final wager.",
    og_desc="A free retro quiz for the whole office: ’80s, ’90s and 2000s trivia, a tangled tape, a time machine and a time-capsule wager, with a narrator.",
    og_alt="a retro quiz for the whole office, with a neon cassette tape",
    eyebrow="A retro quiz for the whole office",
    intro="A free trivia game about the ’80s, ’90s and 2000s for office parties and team events, made for a big screen. Teams pick retro questions on a game-show board, think for 30 seconds and answer. A narrator reads every question aloud. Every generation in the office gets its moment.",
    rules=[("Two rounds", "of five categories about toys, TV, movies, music, tech, fads and headlines from three decades, worth 100–500 and then 200–1,000 points."),
           ("Tangled Tape:", "the team that finds the tangled tape must hand the question to another team."),
           ("Time Machine:", "the time machine makes two trips and picks a random price and the team that must answer."),
           ("The Time Capsule:", "one final question with secret wagers, then a podium for the team that rocked the decades.")],
    chips=[("TANGLED_SVG", "Tangled Tape"), ("TIMEMACHINE_SVG", "Time Machine"), ("CAPSULE_SVG", "Time-capsule wager")],
    card="’80s, ’90s and 2000s trivia: toys, TV, movies, music, tech and fads, with a tangled tape, a time machine and a time-capsule wager. Fun any time of year.",
    page_art={"trivia-questions": "CASSETTE_SVG", "virtual-games-for-work": "BOOMBOX_SVG", "how-to-host-a-game-night": "TIMEMACHINE_SVG", "faq": "CAPSULE_SVG"},
    shots=["board", "question", "timemachine", "tape", "final", "podium"],
)

GAMES = [DECADES, HALLOWEEN, CHRISTMAS, VALENTINES, STPATRICKS]
PLAYABLE = [g for g in GAMES if g["status"] in ("live", "scheduled")]

# Content pages every playable game has (slug, nav label). Content: tools/pages_<game>.py
PAGES = [("trivia-questions", "Trivia questions"), ("virtual-games-for-work", "Remote & hybrid teams"),
         ("how-to-host-a-game-night", "Host guide"), ("faq", "FAQ")]


def is_out(game, today, preview=False):
    """Is the game published on this build?"""
    return game["status"] == "live" or (game["status"] == "scheduled" and (preview or today >= game["launch"]))
