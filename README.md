# Victoria's Merry Quizmas 🎄

A Christmas quiz game for office parties: two rounds, Naughty or Nice, Krampus's Bargain and a Christmas Eve wager, with a narrator. Built from the engine of [Victoria's Night of Frights](https://github.com/vaku0004/night-of-frights).

- Engine: `engine/game.html` (the full game; Halloween is its own content) and `engine/slots.py`
- Games: `games/<slug>/` (theme.py, questions.js, art.js, built game.html), built by `python3 tools/build_game.py --all`
- Website (Victoria's Game Nights, all games): `tools/build_site.py`
- Plan and decisions: [HANDOFF.md](HANDOFF.md)

Game, questions and design by **Victoria**.
