# Victoria's Game Nights (Merry Quizmas, Night of Frights): handoff

Start here. This file carries everything decided so far, so a new session can continue without the original chat.

## Who and how

- Owner: Victoria (legal spelling Viktoriia; she wants **"Victoria" everywhere** in the games and on the site), web designer in Regina, Saskatchewan. GitHub: `vaku0004`.
- **Reply in Russian.** She writes in English or Russian. Thorough, structured answers. Use code (Python) for any arithmetic.
- She hosts office game nights. Coworkers play in teams in the room, and one or two join by video call.
- Never ask her to paste an ElevenLabs API key into chat. She types it only into the PowerShell generator on her PC.

## The project

A Christmas version of her Halloween game **Victoria's Night of Frights** (live at https://nightoffrights.monster/, repo `vaku0004/night-of-frights`, copy `vaku0004/night-of-frights-game`). Same engine, re-themed.

Decisions she made (November 2, 2026):

| Topic | Decision |
|---|---|
| Name | **Victoria's Merry Quizmas** (on Nov 4 she asked for "Victoria" everywhere: games, site, files; "Viktoriia" is gone) |
| Surprise 1 (was Black Cat) | **Naughty or Nice**: the team that finds a lump of coal must give the question to another team |
| Surprise 2 (was Deal with the Witch) | **Krampus's Bargain**: Krampus draws twice from his sack: first the price, then the team |
| Final (was Midnight) | **Christmas Eve**, secret wagers (up to half the score, or 500) |
| Winner line | "Team X saved Christmas!" |
| Party date | Shortly before the holidays, about **December 20–23, 2026** |
| Hosting | ~~Own domain~~ → replaced on Nov 3 by one brand site, **Victoria's Game Nights** (see below) |

Done so far:

- `quizmas/merry-quizmas.html`: the playable game, published as a private artifact: https://claude.ai/artifact/KXfY7qEGBmecmHLwb7pvCk
- 50 questions + final + tiebreaker in `quizmas/questions.js` (fact-checked; no song lyrics). Categories: Round One: Deck the Halls, Oh Canada!, Sweet Treats, Christmas at the Movies, Snow & Ice. Round Two: Santa's Workshop, Around the World, Christmas Creatures, Holiday Hits, Christmas History. Final: "A Christmas Miracle" (the 1914 Christmas Truce).
- Original SVG art in `quizmas/art.js`: tree, coal stocking, Krampus, star, gift, sack.
- Palette: evergreen night, gold, berry red; snowfall; display font Mountains of Christmas (700); text fonts Alegreya / Alegreya Sans / Oswald.
- Final-round music: warm music box with sleigh bells. Phone layout is built in.
- Narrator lines exported to `quizmas/voice-lines.json` and `voice-kit/voice-lines.json` (136 lines, about 13,250 characters, about 13k credits on Eleven v4).

## How the build works (engine + themes, since November 4, 2026)

**Paths moved on Nov 4:** `night-of-frights.html` → `engine/game.html`, `quizmas/*` → `games/christmas/*` (`merry-quizmas.html` → `game.html`), `valentines/*` → `games/valentines/*` (`sweetheart-showdown.html` → `game.html`), `voice-kit/` → `games/christmas/voice-kit/`. Older notes below may still use the old paths.

```
python3 tools/build_game.py --all          # or: christmas valentines halloween
```

- `engine/game.html` is the complete game, and its own content is the Halloween game. **Fix or improve the game here, once, for all games.**
- `engine/slots.py` lists the 86 places a game can change (texts, colours, font link, atmosphere CSS, storage keys, team names, questions, the 6 art SVGs, narrator name, lines and moods, sounds, music, rules slides, start screen, surprise screens, final, podium, editor). Each slot has the exact engine text (or a regex) and how often it must appear.
- `games/<slug>/theme.py` gives one game's values for those slots (`VALUES = {slot: value}`); slots left out keep the engine's value. Helpers inside theme.py: `file("questions.js")`, `art("COAL_SVG", "CAT_SVG")` (an SVG from the game's art.js under the engine's constant name), `MOBILE_CSS`.
- `tools/build_game.py` applies the slots in order, stops if any slot is not found exactly as expected, and warns if Halloween words show up in another game's visible text.
- **Checked on Nov 4:** the new builds of all three games are byte-identical to the old ones (so the narrator audio still matches 136/136 per game). The old `build_quizmas.py` / `build_valentines.py` are deleted (in git history).
- **Game test:** `node tools/e2e_game.js <game.html or http URL> ...` plays a short game headless (rules, a normal question, both surprises, undo, Round Two, final with wagers, podium, reload, editor, voice settings) and reports errors and narrator lines without a recording. Run it on the offline files (`build/<slug>-offline.html`) or on the served site; a raw `games/<slug>/game.html` over file:// cannot load its audio (fetch), which is expected. Full check after the refactor (Nov 4): all three games pass with no errors, final wagers add up, 0 lines without a recording; site builds for Nov 4 / Nov 15 / Jan 20 show the right games; 45 site URLs OK; screenshots regenerate; mirror and redirect tools work.
- If an engine change breaks a slot (its text changed), update `find` in `engine/slots.py` and the theme values that depend on it, then rebuild all games.
- **New game:** copy `games/valentines/` to `games/<slug>/`, rewrite `theme.py`, `questions.js`, `art.js`; add the game to `tools/games.py` and a `tools/pages_<slug>.py`; build; export lines with `node tools/export_lines.js games/<slug>/game.html games/<slug>/voice-lines.json`; make a voice kit (copy `games/valentines/voice-kit/`, change the default voice ID and the name).
- Internal ids stay Halloween-named on purpose (`special: "cat"` = the pass-the-question surprise, `"witch"` = the random price/team surprise, `wand1/wand2`, `--witch` colour). Storage keys per game: `nof-`, `mq-`, `ss-` (`-state-v1`, `-questions-v1`, `-voice-v1`); never change them for a published game.
- Run tools from the repo root. Local screenshots need the fonts: `cd fontpkgs && npm pack @fontsource/<font>@5` for pirata-one, alegreya, alegreya-sans, oswald, mountains-of-christmas and yeseva-one, then unpack each into `fontpkgs/fontsource-<name>-<version>/` (see `tools/fontify.py`). Playwright and Chromium are preinstalled in cloud sessions.
- `node tools/export_lines.js <game.html> <out.json>` lists every narrator line (file name = `l-<fnv32 of text>.mp3`).
- Website build: see "Victoria's Game Nights" below (it runs `build_game.py --all` first).

## Random surprises (November 4, 2026)

Surprises are no longer fixed in the question files. At **Start the game** the engine deals them to random cells (`dealSpecials()` in `engine/game.html`, stored in `S.specials`, kept on reload, part of undo history): per round 2 × `"cat"` and 1 × `"witch"`, never on the two cheapest rows, never two of the same kind in one category. A question with `special` set in the editor ("Surprise in this cell") is pinned and always keeps it; the default option is "Random (the game decides)". `special:` was removed from every `questions.js` and from the engine's Halloween defaults, so the trivia pages no longer show surprise tags. Checked: 2,000 simulated deals (always 6, all 30 allowed cells used, rules hold), pinning works, each start gives a new layout, all 7 games' narrator lines unchanged, game test passes (it now reads the layout from `S.specials`), 97 site URLs OK. Hosts with edited questions saved in the browser from before keep their old specials as pins.

## Victoria's Game Nights (decided November 3, 2026)

Not one site per game any more: **one brand site, Victoria's Game Nights**, with every game on it. Decisions:

- **Halloween moves** from nightoffrights.monster to `/halloween/` on the new site. The old domain then forwards every page (tool ready, see below). Run it only after the new site is live.
- **Christmas** goes on the site on **November 15, 2026** (`launch` in `tools/games.py`). Before that date the home page shows a "coming November 15" card and no Christmas pages are built.
- **Valentine's Day**: a "Coming in February" card only (`status: "soon"`). Game not started.
- **New repo** for the site: `vaku0004/game-nights` (she creates it; it did not exist yet on November 3). This repo (merry-quizmas) holds all the sources for now; move them there once it exists.
- Long term she may sell games. Ideas discussed: free + paid full version, office editions on order, Etsy printables, annual pass; merchant-of-record payments (Lemon Squeezy, Paddle); GitHub Pages forbids sites mainly for selling, so move to Cloudflare Pages or Netlify then; ElevenLabs audio needs a paid plan for commercial use; GST small-supplier threshold $30k. Nothing decided yet.

### Site layout

```
/                          home: brand, game cards, how it works, FAQ        (tools/build_home.py)
/privacy/  /404.html
/<game>/                   the game (tools/build_index.py game_page) + /<game>/audio/ + /<game>/og-image.png
/<game>/trivia-questions/  /<game>/virtual-games-for-work/  /<game>/how-to-host-a-game-night/  /<game>/faq/
/assets/<game>/pages.css   theme colours per game; also shots/*.webp, og/*.png, favicon.svg
```

### Build

```
python3 tools/build_site.py <site_dir>                 # what is published today
python3 tools/build_site.py <site_dir> --preview       # also games not launched yet
python3 tools/build_site.py <site_dir> --today 2026-11-15
```

Needs `fontpkgs/` (see above), Node with Playwright, and Pillow. Intermediate files go to `build/` (ignored by git).

- **Settings:** `tools/site_common.py`. `URL` is a placeholder (`https://victoriasgamenights.com/`) until she buys the domain. `GA_ID` = the Night of Frights property `G-JL1KBEZPQX`, reused for the whole site (rename the property in GA to "Victoria's Game Nights"). Games are told apart by page path.
- **Games:** `tools/games.py` (names, colours, fonts, art, texts for the game page and the home card, launch status). Content pages: `tools/pages_halloween.py`, `tools/pages_christmas.py`. In content, `href="/"` means "play this game"; `href="/" data-home` means the home page. Page frame and theme CSS: `tools/page_shell.py` + `pages-src/pages.css`. Preview images and icons: `tools/make_og.py`, rendered by `tools/shoot_site.js`.
- **Sources per game:** Halloween = `night-of-frights.html` (identical to the live game), audio `audio/halloween/` (copied from the night-of-frights repo, voice "Spooky Narrator" `K2A5xiNNI7XXY6YGaeGW`), shots `games/halloween/shots/`. Christmas = `quizmas/merry-quizmas.html` (built by `tools/build_quizmas.py`), audio `audio/christmas/` (voice "Santa" `eFPFwIAgneOfhQZArsFc`), shots `games/christmas/shots/` (delete the folder to retake them).
- **GA events:** `game_start`, `round_two`, `final_round`, `tiebreaker`, `game_complete`, `question_open` (special = black_cat / witch / naughty_or_nice / krampus / none), `open_question_editor`, `open_voice_settings`, `questions_edited`; on pages `play_click` (links with `data-play`), `print_questions`, `show_all_answers`, `copy_invite`, `show_answer`. The Halloween final used to be `midnight`, now `final_round`.
- **Check:** serve the site folder (`python3 -m http.server 8765`), then `node tools/check_site.js <shots_dir> <fonts.css> http://localhost:8765` (fonts.css = base64 @font-face rules from fontpkgs, served in place of Google Fonts). Last run (preview build, Nov 3): 32 URLs, nothing broken, no JS errors, no horizontal scroll at 390px, both games load their 136 audio lines.
- **Old domain:** `python3 tools/build_redirects.py <night-of-frights repo>` replaces that repo's site with forwarding pages (canonical + meta refresh + JS) and keeps CNAME and the Search Console / IndexNow files. Tested on a copy only; the real repo is untouched.
- **Mirror** (no-redirect copy on github.io): `python3 tools/build_mirror.py <site_dir> <mirror_repo>`; `MIRROR_BASE = /game-nights-play` (repo not created).
- **Offline single file:** `python3 tools/build_offline.py christmas <out.html>` (or `halloween`): game + audio + fonts, about 24 MB, no network.

## Sweetheart Showdown (Valentine's Day game, started November 4, 2026)

Decisions she made: name **Victoria's Sweetheart Showdown** (spelled "Victoria" everywhere); surprise 1 **Cupid's Arrow** (`special: "cat"`: the team that gets hit gives the question away); surprise 2 **Box of Chocolates** (`"witch"`: the first chocolate picks the price, the second the team); final **The Love Letter** (secret wagers); winner line "Team X won our hearts!"; Round Two slide "Double the love". Audience: **the whole English-speaking world, US first**, US spelling, no country category; love of every kind (friendship, chocolate, flowers, famous couples, movies, songs, animals, science, world traditions), nothing about dating coworkers. On the site from **January 20, 2027** (`launch` in `tools/games.py`).

- Game: `games/valentines/game.html`, built by `python3 tools/build_game.py valentines` from `games/valentines/theme.py`. Questions `valentines/questions.js` (50 + final "Royal Romance" = Edward VIII + tiebreaker Hershey's Kisses 1907; facts checked from memory, no song lyrics). Art `valentines/art.js`: heart, arrow-through-heart, heart box of chocolates, love letter, rose, bonbon. Palette: wine night `#1a0f17`, rose `#ef7d9a`, blush `#ffd6e0`, caramel `#d4935f`; display font **Yeseva One** (fontsource `yeseva-one`, added to `fontify.py`); rosy sparkles drifting up instead of snow; slow music-box ballad in the final. Storage keys `ss-state-v1`, `ss-questions-v1`, `ss-voice-v1`. Team names: Lovebirds, Sweethearts, Roses, Truffles.
- Site: `tools/pages_valentines.py` (four pages, made from the Christmas pages and rewritten), screenshots `games/valentines/shots/`. Preview build checked: 45 URLs, nothing broken, no JS errors.
- Narrator: 136 lines, 13,210 characters, in `valentines/voice-lines.json`. Voice made on Nov 4: ID `7elAVxKk0tXJT7YGjurH` (prompts in `valentines/voice-design-prompts.md`). Kit with this voice as default: `valentines/voice-kit/` (sent to her as SweetheartShowdown-voice.zip). **Audio done (Nov 4):** 136/136 lines (voice name in ElevenLabs "Valentine Vic", eleven_v4) checked and committed to `audio/valentines/`.
- Offline file for her review (browser voice, no audio): `python3 tools/build_offline.py valentines <out.html>` (works without audio now).

## Pot o' Gold (St. Patrick's Day game, made November 4, 2026, on the new engine)

Decisions she made: name **Victoria's Pot o' Gold**; surprise 1 **Leprechaun's Trick** (`"cat"`: the leprechaun snatches the question, the team gives it away); surprise 2 **Over the Rainbow** (`"witch"`: the rainbow appears twice, price then team); final **End of the Rainbow**; winner line "Team X found the pot of gold!"; Round Two slide "Double the luck". Audience: whole world, US first, US spelling. On the site from **February 10, 2027** (`launch` in `tools/games.py`).

- Files: `games/stpatricks/` (theme.py, questions.js, art.js, game.html, voice-lines.json, voice-design-prompts.md, shots/); site pages `tools/pages_stpatricks.py`. Storage keys `pg-state-v1`, `pg-questions-v1`, `pg-voice-v1`. Teams: Shamrocks, Leprechauns, Rainbows, Clovers. Narrator name "Lucky Liam".
- Look: emerald night `#0c1a12`, gold `#e8b84a`, green `#5fbf73`, sky blue `#7fb8e8` for the rainbow; display font **Eagle Lake** (fontsource `eagle-lake`; Uncial Antiqua was dropped on Nov 4 because its lowercase t looks like c, so "Victoria" read as "Viccoria"); gold and green specks drifting up; a lilting tune with soft bodhrán taps in the final. Art: shamrock, leprechaun hat, rainbow with clouds, pot of gold, four-leaf clover, coin.
- Questions: 50 + final "Irish in America" (John Barry) + tiebreaker (Ireland joined the EEC in 1973); checked from memory, worth a second look before launch. Categories R1: The Emerald Isle, Luck & Legends, Myths of Ireland, Going Green, Around the World; R2: The Real St. Patrick, Irish Words, Famous Irish, Music & Dance, A Taste of Ireland.
- Checks: game test (`tools/e2e_game.js`) passes; preview site 58 URLs OK; home page now shows the game cards 2 × 2.
- Voice made on Nov 4: ID `t6vJ4FT1TpF4LOWRQV9n` (prompts in `games/stpatricks/voice-design-prompts.md`). Kit with it as default: `games/stpatricks/voice-kit/` (sent as PotOGold-voice.zip). **Audio done (Nov 4):** 136/136 lines (voice name in ElevenLabs "Patrick", eleven_v4) checked and committed to `audio/stpatricks/`.

## Movie Night (all-year movie game, made November 4, 2026)

Decisions she made: name **Victoria's Movie Night**; surprise 1 **Plot Twist** (`"cat"`); surprise 2 **Popcorn Bucket** (`"witch"`: two tickets, price then team); final **The Final Cut**; winner line "Team X steal the show!"; Round Two slide "The sequel". **Status "live"** (any day). No "Oscar"/"Academy" in game or page names; facts about Oscars inside questions are fine.

- Files: `games/movies/` (theme.py, questions.js, art.js, game.html, voice-lines.json, voice-design-prompts.md, shots/); site pages `tools/pages_movies.py`. games.py: `holiday="Movies"`, `footer_kind="movie"`, `trivia_label="Movie trivia questions"`. Storage keys `mn-state-v1`, `mn-questions-v1`, `mn-voice-v1`. Teams: Popcorn, Blockbusters, Spotlight, Red Carpet. Narrator name "Marquee Max".
- Look: red-velvet night `#140b0d`, gold `#f2c14e`, butter orange `#ffa94d` for the popcorn bucket; display font **Limelight** (art-deco marquee; fontsource `limelight`); golden specks; a sweeping film-score tune with projector clatter. Art: clapperboard, plot-twist arrow with "?", striped popcorn bucket, film reel, 3D glasses, star.
- Questions: 50 + final "Hollywood Legends" (Katharine Hepburn, four Best Actress Oscars) + tiebreaker (first Star Wars, 1977). Categories R1: Animated Classics, Superheroes, Movie Food, Famous Lines, Sequels & Series; R2: Behind the Scenes, Directors, Movie Music, Hollywood History, World Cinema. Checked from memory (one fix: Miyazaki won again in 2024).
- Checks: game test passes; preview site (7 games) 97 URLs OK.
- Voice made on Nov 4: ID `MgsaOm0mZXCSwbjBKimg` (prompts in `games/movies/voice-design-prompts.md`; suggested ElevenLabs name "Marquee Max"). Kit with it as default: `games/movies/voice-kit/` (sent as MovieNight-voice.zip). 136 lines, 11,533 characters. **Audio done (Nov 4):** 136/136 lines (voice "Marquee Max", eleven_v4) checked and committed to `audio/movies/`.

## Countdown Quiz (New Year's game, made November 4, 2026)

Decisions she made: name **Victoria's Countdown Quiz**; surprise 1 **Party Popper** (`"cat"`); surprise 2 **Fortune Cookie** (`"witch"`: two fortunes, price then team); final **The Midnight Countdown** (thinking music with a ticking clock and a chime every other bar); winner line "Team X ring in the New Year!"; Round Two slide "The last hour". **Status "scheduled", launch December 1, 2026**, free.

- Files: `games/newyear/` (theme.py, questions.js, art.js, game.html, voice-lines.json, voice-design-prompts.md, shots/); site pages `tools/pages_newyear.py` (made from pages_movies, adds the FAQ item "Do we have to play it on New Year's Eve?"). games.py: `holiday="New Year’s Eve"`. Storage keys `ny-state-v1`, `ny-questions-v1`, `ny-voice-v1`. Teams: Confetti, Sparklers, Party Hats, Midnight. Narrator name "Midnight Mae".
- Look: midnight blue `#0d0f24`, gold `#f5cf6b`, pink `#ff6b81`, cookie orange `#f0a35e`; display font **Bungee** (fontsource `bungee`); falling confetti. Art: clock at midnight, party popper, fortune cookie, firework, party hat, sparkle.
- Questions: 50 + final "Midnight History" (Times Square named after The New York Times, first party 1904) + tiebreaker (first ball drop, 1907). R1: Traditions Around the World, Midnight Around the Globe, Party Food & Drink, New Year New You, Calendars & Time; R2: Lunar New Year, Fireworks & Bubbles, Songs for Midnight (no lyrics), New Year on Screen, Countdown Numbers. Checked from memory.
- Checks: game test passes; preview site 58 URLs OK, today's build 32 URLs OK.
- Voice made on Nov 4: ID `R5Ofd4ZMFC0vxt0QrdYU` (prompts in `games/newyear/voice-design-prompts.md`; suggested ElevenLabs name "Midnight Mae"). Kit with it as default: `games/newyear/voice-kit/` (sent as CountdownQuiz-voice.zip). 136 lines, 12,018 characters. **Audio done (Nov 4):** 136/136 lines (voice "Midnight Mae", eleven_v4) checked and committed to `audio/newyear/`; game test over http plays only recorded lines.

## Big Brain Battle (all-year general-knowledge game, made November 4, 2026)

Decisions she made: name **Victoria's Big Brain Battle**; surprise 1 **Wild Card** (`"cat"`); surprise 2 **Mystery Box** (`"witch"`: two tickets, price then team); final **All In**; winner line "Team X win the Big Brain Battle!"; Round Two slide "Brain boost". Made for **National Trivia Day (January 4, US)** as a hook, but it is an any-day game: **status "live"**. Publish the site by early December so search engines find it before January 4.

- Files: `games/trivia/` (theme.py, questions.js, art.js, game.html, voice-lines.json, voice-design-prompts.md, shots/); site pages `tools/pages_trivia.py` (FAQ has a National Trivia Day item). games.py: `holiday="Any day"`, `footer_kind`, `trivia_label="General knowledge questions"` (new optional fields, used by build_index, build_home and page_shell). Storage keys `bb-state-v1`, `bb-questions-v1`, `bb-voice-v1`. Teams: Brainiacs, Know-It-Alls, Smarty Pants, Quizzards. Narrator name "Quizmaster Quinn".
- Look: deep teal night `#0b1a22`, electric yellow `#ffd23f`, violet `#b48cff`; display font **Lilita One** (fontsource `lilita-one`); yellow and violet specks; bouncy game-show tune with the engine's ticking clock. Art: pink brain, wild card, mystery gift box, stack of poker chips (All In), light bulb, ticket.
- Questions: 50 + final "Wonders of the World" (Great Pyramid of Giza) + tiebreaker (Eiffel Tower height with antennas, 330 m). Categories R1: Planet Earth, Science Lab, Food & Drink, Animal Kingdom, Words & Wordplay; R2: History Mystery, Space, Numbers Game, Sports & Games, Art & Music. Checked from memory.
- Checks: game test passes; preview site (6 games) 84 URLs OK.
- Voice made on Nov 4: ID `6t3wUwKWAogfOUr44ltj` (prompts in `games/trivia/voice-design-prompts.md`; suggested ElevenLabs name "Quizmaster Quinn"). Kit with it as default: `games/trivia/voice-kit/` (sent as BigBrainBattle-voice.zip). 136 lines, 10,213 characters. **Audio done (Nov 4):** 136/136 lines (voice "Quizmaster Quinn", eleven_v4) checked and committed to `audio/trivia/`.

## Decades Showdown (all-year retro game, made November 4, 2026)

Decisions she made: name **Victoria's Decades Showdown**, decades **'80s, '90s and 2000s**; surprise 1 **Tangled Tape** (`"cat"`); surprise 2 **Time Machine** (`"witch"`: two trips, price then team); final **The Time Capsule**; winner line "Team X rocked the decades!"; Round Two slide "Fast forward". Audience: whole world, US first. **Status "live"** (no holiday, so it goes on the site at launch; set `status`/`launch` in `tools/games.py` to hold it back).

- Files: `games/decades/` (theme.py, questions.js, art.js, game.html, voice-lines.json, voice-design-prompts.md, shots/); site pages `tools/pages_decades.py`; `holiday="Retro"` in games.py (used in "Retro trivia questions" links). Storage keys `ds-state-v1`, `ds-questions-v1`, `ds-voice-v1`. Teams: Cassettes, Arcade, Neon, Dial-Up. Narrator name "DJ Rewind".
- Look: deep purple night `#120d24`, neon pink `#ff5aa8`, cyan `#3fd5ff`, mint `#3be8b0`; display font **Righteous** (fontsource `righteous`); a faint neon grid at the bottom and pink/cyan specks; synth arpeggio with off-beat hi-hats in the final. Art: cassette, tangled tape, time-machine clock, time capsule "2000", boombox, rewind icon.
- Questions: 50 + final "Inventions That Changed Everything" (World Wide Web) + tiebreaker (first SMS, 1992). Categories R1: Totally ’80s, All That ’90s, Y2K & the 2000s, Toys & Games, TV Time; R2: Movie Flashback, Chart Toppers, Tech Flashback, Fads & Fashion, Headlines. Checked from memory.
- Home page now: playable games 2 per row, then a "Coming soon" row of smaller cards. Preview images scale wide display fonts (Righteous, Eagle Lake) down.
- Checks: game test passes; preview site 71 URLs OK; today's build shows Decades + Halloween playable.
- Voice made on Nov 4: ID `dLA2DLXZxgLToYRsB6Bb` (prompts in `games/decades/voice-design-prompts.md`; suggested ElevenLabs name "DJ Rewind"). Kit with it as default: `games/decades/voice-kit/` (sent as DecadesShowdown-voice.zip). **Audio done (Nov 4):** 136/136 lines (voice "DJ Rewind", eleven_v4) checked and committed to `audio/decades/`.

## Fact check of all questions (November 4, 2026)

All 3 × 52 questions reviewed; doubtful facts checked online. Fixed: Halloween "Windsor Pumpkin Regatta" (the 2019 race was cancelled; now "for about twenty years from 1999", note says it ended when the lake was drained) and "Ganong" (first wrapped bar is the company's own claim: now "says it made the first wrapped chocolate bar in North America"; 1898 vs 1910 dates disputed, removed); Christmas tiebreaker note (Gene Autry's Rudolph: about 1.75 million copies in the first season, not "more than 2 million"); Valentine's "Colombia" question reworded (largest supplier of cut flowers to the US, not "most flowers sold").
**Re-voicing: done the same day** (she sent both `audio` folders; checked: 136/136 lines match `voice-lines.json`, old files for the changed lines removed). For later changes the method is: She puts the new `voice-lines.json` (`games/halloween/voice-lines.json` → her Halloween kit folder, `quizmas/voice-lines.json` → her Merry Quizmas kit folder) next to `generate-voice.ps1`, runs `start-voice.bat`; only changed lines are voiced. Then copy the new MP3s and `manifest.json` into `audio/halloween/` and `audio/christmas/`. Until then those lines fall back to the browser voice.

## Narrator names in Voice settings (November 4, 2026)

No "ElevenLabs" or model name on screen any more. The button is "Game narrator" / "Browser voice", and the line under it reads "Narrator: <name>. All 136 lines are recorded." Names: Halloween "The Spooky Narrator", Christmas "Grandpa Noel", Valentine's "Valentine Vic" (`const NARRATOR` in `night-of-frights.html`, replaced in `build_quizmas.py` / `build_valentines.py`). ElevenLabs is still mentioned only in code comments and the voice kit. The "Copy voice lines for the generator" button was removed (use `node tools/export_lines.js <game.html> <out.json>` instead).

## Contact and bug reports (November 4, 2026)

- Address: **vvakulenko.work@gmail.com** (`CONTACT_EMAIL` in `tools/site_common.py`; written as HTML entities in links, a little harder for harvesters).
- Home page: a **"Write to Victoria"** button under the intro ("Questions, ideas or a custom game for your office? Victoria reads every message."), plus "Write to Victoria" in the footer of the home page and of every game page. GA event `contact_click`.
- Every game: a small, semi-transparent **"Bug"** button in the bottom-left corner of every screen (`bugReport()` in `engine/game.html`, address in `BUG_TO`). It opens an e-mail "Bug report: <game>" with "What happened? / What did you expect?" and the game, screen, round, teams, open question, browser and window size filled in (a local file shows "file on this computer", not its path). Checked: no overlap with buttons at 1366×768 and 1920×1080; on a phone it floats over scrolling text in the editor and voice panel.
- The Ko-fi "Support" link and the "custom office edition, Contact us" text from the money plan below can now point to the same address.

## Money and growth plan (agreed November 3, 2026; do it when the site is published)

She liked this three-step test of demand and wants it built **together with the website**:

1. **Donations this winter.** Ko-fi page in the brand's name (she creates it and sends the link). Links: on the podium screen at the end of a game ("Enjoyed the game? Buy Victoria a hot chocolate"), small "Support the games" link on the home page and in every footer, an FAQ item "How can I support the games?". GA event `support_click`. Wording "Support"/"Tip", not "Donate" (only registered charities give donation receipts; tips are income).
2. **"Want a custom office edition? Contact us"** on every game page and the home page, to test the most expensive product. Needs a contact address or form from her (forms on a static site need a service such as Formspree, or just an email address shown as text).
3. **Paid full version** from Valentine's Day or St. Patrick's Day, once Analytics shows real traffic.

Pricing hypothesis (USD, to test): full game $19–29 one-time; office edition $99–249 (logo, company name, 5–10 office questions she writes, narrator says the company name); annual pass $49–99 once there are 4–5+ games; Etsy PDF packs $5–9. Revenue math at $19: 10,000 seasonal visitors × 1% ≈ $1,900; real income comes from many games per year plus office editions.

Payments: Stripe works for a Saskatchewan sole proprietor and is cheapest (~2.9% + 30¢), but she is then the seller of record for foreign taxes (EU/UK VAT on digital sales to consumers from the first sale; US states have high thresholds; Canada GST/HST only above $30k). Merchant-of-record services (Lemon Squeezy, owned by Stripe; Paddle; ~5% + 50¢) handle all of that; check whether Stripe's own merchant-of-record option (Managed Payments) is available in Canada. Plan: Stripe if selling mainly to Canada/US, a merchant of record if selling worldwide. She should see an accountant before paid sales start. When selling starts, move hosting from GitHub Pages to Cloudflare Pages or Netlify.

Direction: **the whole English-speaking world, US first**, neutral English for the rest. Ideas agreed in principle: swappable local category per country (Oh, Canada! / Stars & Stripes / Rule, Britannia / Down Under), dates in words, units in both systems, US spelling (decide; site is en_CA now), prices in USD. Holiday calendar for 2027 (launch 4–6 weeks ahead): Valentine's Day (~Jan 20), St. Patrick's Day (~Feb 10), all-year Team Trivia (spring, basis for the paid version), Canada Day / July 4, Thanksgiving (Canada October + US November), Halloween and Christmas with local packs; also International Women's Day and Employee Appreciation Day for HR buyers. Avoid trademarked names (Olympics, Super Bowl, Oscars, Eurovision, World Cup) and solemn days; cultural and religious holidays only with review by people from that culture. Before many new games: refactor to one engine + a theme file per game (questions, art, colours, narrator lines) instead of text replacement.

## Ideas for later (not started)

**Kids' party game** (discussed Nov 4, she wants to do it later). Needs a **kids mode in the engine** first (one time, then any kids theme can use it): no negative points (a wrong answer just scores nothing), answer options A/B/C on screen, a shorter board (20–25 questions, 25–30 minutes), a simple final (last question worth double for everyone, no wagers), a gentler or optional timer, a warm ending ("Everyone did amazing!", confetti), a slow, cheerful narrator. Theme ideas: **Pirate Treasure Quiz** (5–10 years; parrot steals the question, treasure map draws price and team, treasure chest final) as the first one; dinosaurs, space, fairy-tale castle (own magic, no Harry Potter references), under the sea / jungle; and **kids' question packs for the existing holiday games** for classroom parties (teachers with smartboards; Teachers Pay Teachers). Paid extra: the birthday child's name on screen. Buyers: parents ($5–15) and teachers (best fit). For a site aimed at under-13s, US COPPA applies: turn Analytics off on kids' pages and collect nothing. Open questions for her: age group, theme, home birthday vs classroom.

**More game ideas** (discussed Nov 4, not started). All-year: Team Trivia Night (general knowledge; launch for National Trivia Day, January 4), Around the World (geography), Foodie Quiz, Movie Night (no "Oscar"/"Academy" in names), Sports Day (no "Olympics"/"World Cup" in names), Science & Nature. Holidays: Spring Fling (Easter, March 28, 2027; launch about Feb 20), Canada Day / July 4 "Summer Cookout" (Hot Potato, Firework Finale), Thanksgiving "Great Gobble" (Canada October + US November; the Wishbone surprise), New Year "Countdown Quiz" (Party Popper, Fortune Cookie, Midnight Countdown), International Women's Day "Trailblazers", Employee Appreciation Day, Pi Day, Earth Day, Talk Like a Pirate Day (September 19), Boss's Day, Administrative Professionals Day, Back to School. Custom editions to sell ($99–249): farewell or retirement, new-hire onboarding, team year in review, wedding or bridal or baby shower, milestone birthdays, family reunions. New round types for the engine: picture round, sound round, higher or lower, true or false, emoji puzzles. Avoid: trademarked names, solemn days; cultural and religious holidays only with review by people from that culture.

**"Free" wording** (Nov 4): the brand-level texts no longer say "free" (home page title, description, eyebrow, footer, site preview image), because some games may become paid. The home FAQ now says the games can be played for free right now and that paid games or packs will be clearly marked. Per-game "free" wording is still there and must change when a game becomes paid: `title`/`desc`/`og_desc` in `tools/games.py`, the "free to play" line on home cards (`build_home.py`), "Play free" in the page header (`page_shell.py`), "FREE TO PLAY" on game preview images (`make_og.py`), and the "Is … free?" FAQ items and page titles in `tools/pages_<game>.py`.

**Free games and "coming soon" (decided Nov 4, replaces the earlier paid plan below):** the site opens with **four free games**: Night of Frights (Halloween, live), Movie Night (live), Merry Quizmas (opens November 15, 2026) and Countdown Quiz (New Year's, opens December 1, 2026). Big Brain Battle, Decades Showdown, Sweetheart Showdown and Pot o' Gold are `status="soon"`: the home page shows them as "Coming soon" cards with their art, and none of their pages are built. Their `launch` dates are kept in games.py for later. The home page loads every card's title font (from `gfont` in games.py).

**Paid games: postponed (Nov 5).** She decided: launch the site now with the four free games and the rest as "Coming soon"; connect paid games later. Notes from the Nov 5 discussion, for when we start:
- Payments: Lemon Squeezy still takes new sellers but is being folded into **Stripe Managed Payments** (merchant of record, GA April 2026, reportedly open to sellers in Canada, about 3.5% on top of Stripe fees ≈ 6.4% + 30¢; no license keys or storefront). Lemon Squeezy ≈ 5% + 50¢ with license keys, receipts and discount codes built in. Either works; build the unlock service so it can accept both, and keep a copy of every validated purchase so a later move does not lock out old buyers. Store activation needs the live site with prices, Terms of Sale, Refund Policy and a contact. Official pages (lemonsqueezy.com, docs.stripe.com) were not reachable from the cloud session; figures come from reviews.
- Design: public page = engine + Round One (questions, audio, editor); Round Two, final, tiebreaker and their audio live only in private storage; after Round One (and on the start screen: "Round One free · Full game $29 · Unlock now") an unlock screen sells the game; a small server checks the key with the payment service and returns the paid pack; the unlock is remembered in the browser; about 3 activations per key; optional "Download for offline play" after purchase. Trivia pages of paid games show only Round One.
- Where the check runs: Cloudflare Worker + R2 (free, no upkeep), or her **Hetzner server** (she has one; setup unknown, nothing about it in her GitHub repos). Recommended: keep the site static (Cloudflare Pages later, GitHub Pages discourages selling) and run only the unlock service on Hetzner or Cloudflare. If Hetzner: deploy through GitHub Actions with an SSH key in repo Secrets, or a one-command Docker install she runs; ask her what runs on the server, which OS, and set a subdomain such as api.<domain>. Never ask for server passwords or keys in chat.
- Before paid sales: one talk with an accountant (business-name registration with ISC in Saskatchewan if selling as "Victoria's Game Nights", income reporting, GST only above $30k), and check that the ElevenLabs plan used for the audio allows commercial use.

**Earlier paid plan (Nov 4, on hold):**  launch the site with **every game free**; switch on the paid part **with Valentine's Day (January 20, 2027)**. From then on: **fully free** = Night of Frights (Halloween) and Movie Night; **first round free, full game paid** = Big Brain Battle, Decades Showdown, Merry Quizmas (paid from next season), Sweetheart Showdown, Pot o' Gold and every new game unless decided otherwise. Technical design: in paid games the public page holds only Round One (questions, audio, editor); after Round One an "Unlock the full game" screen sells it via Lemon Squeezy (license key, about 3 activations per key); a Cloudflare Worker checks the key and returns Round Two, the final, the tiebreaker and their audio from Cloudflare R2; the unlock is remembered in the browser. Trivia pages of paid games show only Round One's 25 questions. Hosting moves to Cloudflare Pages (commercial use allowed). Needs from her: Lemon Squeezy store + products, a Cloudflare account, price ($29 per game? annual pass $79–99?), activations per key. Estimated 3–4 sessions + a test purchase in Lemon Squeezy test mode.

**Pricing to test** (Nov 4, after checking comparable products): full game $29 one-time; annual pass $79–99; custom office edition $149–249; Etsy PDF $5–9. Hosted trivia with a live host costs about $399 per group of 15, TeamBuilding.com about $40 per person, Kahoot business about $19–79 per host per month, so $29 is cheap for an office. Start at $29 with no discounts; add "Custom office edition from $149, Contact us"; adjust after one season.

## Next steps (in order)

1. **Domain for Victoria's Game Nights.** Suggestions: victoriasgamenights.com / .ca. She checks on Namecheap and buys it; then set `URL` in `tools/site_common.py`. DNS like Night of Frights: four A records `185.199.108.153` to `185.199.111.153`, CNAME `www` to `vaku0004.github.io.`, remove the Namecheap parking redirect, set the custom domain in GitHub Pages, **Enforce HTTPS** once the certificate is issued (about a day last time; removing and re-adding the domain helped).
2. **Repo `vaku0004/game-nights`:** she creates it (public, for free Pages) and adds it to the session. Move the sources there, or keep the sources here and publish only the built site there. Publish the `build_site.py` output (without Christmas until Nov 15).
3. **After the new site is live:** run `build_redirects.py` on the night-of-frights repo and push. Search Console: add the new domain (HTML-file verification, she can't give Namecheap passwords), submit the sitemap, use the Change of Address tool from nightoffrights.monster; IndexNow for Bing. Update or retire the night-of-frights-game mirror. In GA: rename the property, add the new domain.
4. **November 15:** rebuild (Christmas appears by date), push, request indexing for the Christmas pages.
5. **She reviews the Christmas game** (offline file sent on Nov 3) and sends changes in one list. Changed narrator text needs re-voicing of those lines only (`voice-kit/start-voice.bat` on her PC, same folder; ElevenLabs is not reachable from the cloud). She sends audio as .rar; `node-unrar-js` (npm, WASM) extracts it in the cloud.
6. **Valentine's Day game:** built on Nov 4 (see "Sweetheart Showdown"). Voice and audio done. Remaining: her review. Goes live by date on January 20, 2027.
7. **St. Patrick's Day game:** built on Nov 4 (see "Pot o' Gold"). Voice and audio done. Remaining: her review. Goes live by date on February 10, 2027.

## Things to keep in mind

- Her cloud-session bonus credit ends November 4, 2026, 11:59 PM PT; after that her weekly plan limits apply. Work efficiently and avoid repeated screenshots.
- Publishing, buying and account actions go through her own Chrome (Claude in Chrome). Ask before anything irreversible.
- Commit as `git -c user.name="Viktoriia" -c user.email="vaku0004@users.noreply.github.com"`.
