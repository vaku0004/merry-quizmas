# Victoria's Merry Quizmas: handoff

Start here. This file carries everything decided so far, so a new session can continue without the original chat.

## Who and how

- Owner: Viktoriia (Victoria), web designer in Regina, Saskatchewan. GitHub: `vaku0004`.
- **Reply in Russian.** She writes in English or Russian. Thorough, structured answers. Use code (Python) for any arithmetic.
- She hosts office game nights. Coworkers play in teams in the room, and one or two join by video call.
- Never ask her to paste an ElevenLabs API key into chat. She types it only into the PowerShell generator on her PC.

## The project

A Christmas version of her Halloween game **Victoria's Night of Frights** (live at https://nightoffrights.monster/, repo `vaku0004/night-of-frights`, copy `vaku0004/night-of-frights-game`). Same engine, re-themed.

Decisions she made (November 2, 2026):

| Topic | Decision |
|---|---|
| Name | **Victoria's Merry Quizmas** (on screen: "Viktoriia's", like the Halloween game; the website name can be "Victoria's") |
| Surprise 1 (was Black Cat) | **Naughty or Nice**: the team that finds a lump of coal must give the question to another team |
| Surprise 2 (was Deal with the Witch) | **Krampus's Bargain**: Krampus draws twice from his sack: first the price, then the team |
| Final (was Midnight) | **Christmas Eve**, secret wagers (up to half the score, or 500) |
| Winner line | "Team X saved Christmas!" |
| Party date | Shortly before the holidays, about **December 20–23, 2026** |
| Hosting | **New domain + GitHub Pages**, plus a no-redirect copy on github.io (same as Night of Frights) |

Done so far:

- `quizmas/merry-quizmas.html`: the playable game, published as a private artifact: https://claude.ai/artifact/KXfY7qEGBmecmHLwb7pvCk
- 50 questions + final + tiebreaker in `quizmas/questions.js` (fact-checked; no song lyrics). Categories: Round One: Deck the Halls, Oh Canada!, Sweet Treats, Christmas at the Movies, Snow & Ice. Round Two: Santa's Workshop, Around the World, Christmas Creatures, Holiday Hits, Christmas History. Final: "A Christmas Miracle" (the 1914 Christmas Truce).
- Original SVG art in `quizmas/art.js`: tree, coal stocking, Krampus, star, gift, sack.
- Palette: evergreen night, gold, berry red; snowfall; display font Mountains of Christmas (700); text fonts Alegreya / Alegreya Sans / Oswald.
- Final-round music: warm music box with sleigh bells. Phone layout is built in.
- Narrator lines exported to `quizmas/voice-lines.json` and `voice-kit/voice-lines.json` (136 lines, about 13,250 characters, about 13k credits on Eleven v4).

## How the build works

`night-of-frights.html` is the Halloween game source (kept here as the base). `tools/build_quizmas.py` turns it into the Christmas game with exact, asserted text replacements:

```
python3 tools/build_quizmas.py night-of-frights.html quizmas/merry-quizmas.html
```

- Change questions in `quizmas/questions.js`, art in `quizmas/art.js`, everything else (texts, narrator lines, colours, music) in `tools/build_quizmas.py`. Then rebuild.
- Internal ids stay Halloween-named on purpose (`special: "cat"` = Naughty or Nice, `"witch"` = Krampus, `wand1/wand2`, `--witch` colour). Don't rename them; the logic is tested.
- Storage keys are `mq-state-v1`, `mq-questions-v1`, `mq-voice-v1`.
- Run tools from the repo root. Local screenshots need the fonts: `cd fontpkgs && npm pack @fontsource/<font>@5` for pirata-one, alegreya, alegreya-sans, oswald and mountains-of-christmas, then unpack each into `fontpkgs/fontsource-<name>-<version>/` (see `tools/fontify.py`). Playwright and Chromium are preinstalled in cloud sessions.
- `node tools/export_lines.js <built page> quizmas/voice-lines.json` lists every narrator line (file name = `l-<fnv32 of text>.mp3`).
- Website build: `python3 tools/build_index.py quizmas/merry-quizmas.html index.html --site` (full page, SEO tags, phone layout).

### Website build (ready since November 3, 2026)

The website tools are converted to Merry Quizmas. One command builds the whole site:

```
python3 tools/build_site.py <site_dir>
```

It makes `index.html` (game + SEO tags + no-JS text + phone layout), four content pages (`/christmas-trivia-questions/`, `/virtual-christmas-games-for-work/`, `/how-to-host-a-christmas-game-night/`, `/faq/`), preview images (`og-image.png`, `assets/og/*.png`), game screenshots (`assets/shots/*.webp`), icons, `favicon.ico`, `site.webmanifest`, `robots.txt`, `sitemap.xml`, `CNAME`, and copies `audio/` if the narrator files are in the repo. Intermediate files go to `build/` (ignored by git). Needs `fontpkgs/` (see above), Playwright and Pillow.

- **Settings in one place: `tools/site_common.py`.** `URL` is a placeholder (`https://merryquizmas.com/`) until she buys the domain; `GA_ID` is empty, and with an empty ID no Analytics code goes on the pages. Fill both in, then rebuild.
- Page texts, FAQ and category intros: `tools/build_pages.py`. Main page texts: `tools/build_index.py`. Page styles: `pages-src/pages.css`. Preview images: `tools/make_og.py`; screenshots: `tools/shoot_site.js`.
- GA events: `game_start`, `round_two`, `christmas_eve`, `tiebreaker`, `game_complete`, `question_open` (special = `naughty_or_nice` / `krampus` / `none`), plus the content-page events. Session key `mq-ga`.
- The FAQ links to nightoffrights.monster ("Is there a Halloween version?").
- Mirror (no-redirect copy): `python3 tools/build_mirror.py <site_dir> <mirror_repo_dir>`; path `MIRROR_BASE = /merry-quizmas-game` (a repo `vaku0004/merry-quizmas-game` still has to be created).
- Offline single file: `python3 tools/build_offline.py <out.html>` (needs `audio/manifest.json` + MP3s in the repo).
- Checks: serve the site folder on port 8765 (`python3 -m http.server 8765`), then `node tools/check_links.js <site_dir>`. Last run: 16 internal URLs, nothing broken, no JS errors, no horizontal scroll on a 390px phone.
- Open question: where the site is published. Simplest: build into `docs/` of this repo and set GitHub Pages to "main branch, /docs" (the repo must be public for free Pages), or a separate site repo like Night of Frights had.

## Next steps (in order)

1. **Victoria reviews the game and questions** in the artifact and sends changes.
2. **Narrator voice.** Done on November 3: Voice Design, grandfather storyteller (she was choosing between a Canadian and a soft southern English accent), voice ID `eFPFwIAgneOfhQZArsFc`, now the default in `voice-kit/generate-voice.ps1`. Prompts: `voice-kit/voice-design-prompts.md`. **Audio done (November 3):** all 136 lines voiced on her PC (voice name in ElevenLabs: "Santa", model eleven_v4), checked against `voice-lines.json` and committed to `audio/` (17.7 MB). If any narrator text changes later, re-export the lines, send her the new `voice-lines.json`, and she reruns the kit in the same folder (only changed lines are voiced). She sent the folder as a .rar; `node-unrar-js` (npm, WASM) extracts it in the cloud. Original note: she creates a voice in ElevenLabs (Voices → Voice Design) and sends the voice ID. Suggested prompt:
   > A warm, jolly storyteller in his sixties with a rich, slightly husky baritone and a gentle Canadian accent. He sounds like a beloved grandfather reading a Christmas story by the fireplace: cosy, twinkly and full of good humour, with a soft chuckle in his voice. Clear diction and an unhurried pace, perfect for reading trivia questions aloud to a room. For mischievous moments he can drop into a playful, slightly sly tone, but he is never scary.

   Then generate audio **on her PC**: ElevenLabs is not reachable from the cloud. `voice-kit/start-voice.bat` runs `generate-voice.ps1`, which reads `voice-lines.json`, asks for the key (hidden input), the voice and a YES, voices only new lines and writes `audio/manifest.json` plus MP3s. Her PC folder for the Halloween kit was `C:\Работа\Текущие проекты\Клод\NightsOfFrights`. Use a new folder for Christmas, otherwise the manifests mix. If her PC is linked to the session, copy files with the device tools; otherwise she uploads the `audio` folder.
3. **Domain.** Suggestions: merryquizmas.com, merryquizmas.fun, merry-quizmas.ca. Check availability on Namecheap in her Chrome; she buys it herself. DNS like Night of Frights: four A records `185.199.108.153` to `185.199.111.153`, CNAME `www` to `vaku0004.github.io.`, remove the Namecheap parking redirect, set the custom domain in GitHub Pages, then **Enforce HTTPS** once the certificate is issued (it took about a day last time; removing and re-adding the domain helped).
4. **Website repo.** Tools are ready (see "Website build"). Publish the site (index.html, `audio/`, icons, robots.txt, sitemap.xml, content pages) to GitHub Pages. This repo can hold it, or a separate one. Then a no-redirect copy on github.io (like `night-of-frights-game`).
5. **SEO pages** like Night of Frights: Christmas trivia questions with answers, virtual and hybrid Christmas games for work, host guide, FAQ (neutral voice, no first person; she was fine publishing the game's own questions). Then Google Search Console (verify with an HTML file in the repo; she can't give Namecheap passwords), sitemap, Request indexing, IndexNow for Bing.
6. **Google Analytics 4**: a new property in her existing account ("Default Account for Firebase", **not** inside BYSO; her other properties there are BYSO, francabulaire, thumbnail, Night of Frights). Time zone Regina, CAD, 14-month retention, custom dimensions special / team_count / round / from_page.
7. Offline single-file build (`python3 tools/build_offline.py <out.html>`) as a backup for the party. Works with the real audio (24 MB, no network needed); rebuild it after any change to the game.

## Things to keep in mind

- Her cloud-session bonus credit ends November 4, 2026, 11:59 PM PT; after that her weekly plan limits apply. Work efficiently and avoid repeated screenshots.
- Publishing, buying and account actions go through her own Chrome (Claude in Chrome). Ask before anything irreversible.
- Commit as `git -c user.name="Viktoriia" -c user.email="vaku0004@users.noreply.github.com"`.
