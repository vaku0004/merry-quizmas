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

GAMES = [HALLOWEEN, CHRISTMAS, VALENTINES]
PLAYABLE = [g for g in GAMES if g["status"] in ("live", "scheduled")]

# Content pages every playable game has (slug, nav label). Content: tools/pages_<game>.py
PAGES = [("trivia-questions", "Trivia questions"), ("virtual-games-for-work", "Remote & hybrid teams"),
         ("how-to-host-a-game-night", "Host guide"), ("faq", "FAQ")]


def is_out(game, today, preview=False):
    """Is the game published on this build?"""
    return game["status"] == "live" or (game["status"] == "scheduled" and (preview or today >= game["launch"]))
