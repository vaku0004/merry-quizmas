"""Every game on Victoria's Game Nights: names, colours, art, texts for the game page and the home-page card.

status: "live" (published), "scheduled" (published on `launch`; before that only a "coming" card), "soon" (card only).
Add a new game here, plus a pages_<slug>.py module with its content pages.
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
    src="night-of-frights.html", art_src="night-of-frights.html", audio="audio/halloween", state_key="nof-state-v1",
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
    src="quizmas/merry-quizmas.html", art_src="quizmas/art.js", audio="audio/christmas", state_key="mq-state-v1",
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
    slug="valentines", status="soon", launch=None, name="A Valentine’s Day game", short="Valentine’s Day", holiday="Valentine’s Day",
    theme=dict(night="#1a0f17", ember="#ffd1dc", candle="#e77a95", line="#4a2a3c"),
    card="A sweet (and slightly cheeky) quiz for teams, just in time for February 14.", coming="Coming in February",
)

GAMES = [HALLOWEEN, CHRISTMAS, VALENTINES]
PLAYABLE = [g for g in GAMES if g["status"] in ("live", "scheduled")]

# Content pages every playable game has (slug, nav label). Content: tools/pages_<game>.py
PAGES = [("trivia-questions", "Trivia questions"), ("virtual-games-for-work", "Remote & hybrid teams"),
         ("how-to-host-a-game-night", "Host guide"), ("faq", "FAQ")]


def is_out(game, today, preview=False):
    """Is the game published on this build?"""
    return game["status"] == "live" or (game["status"] == "scheduled" and (preview or today >= game["launch"]))
