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

**The website tools still contain Night of Frights values.** Before using them for Merry Quizmas, change:
- `tools/build_index.py`: URL, NAME, TITLE, DESC, OG text, static no-JS text, links to content pages.
- `tools/site_common.py`: `GA_ID` (needs a **new** GA4 property, see below). The consent-mode and game-events code can stay.
- `tools/build_pages.py`: page texts, categories (`CATS`), slugs and FAQ are Halloween content. Use it as a template for Christmas pages.
- `tools/build_mirror.py`: `BASE` path for the github.io copy.
- `tools/make_og.py`, `tools/make_page_og.py`: preview images.

## Next steps (in order)

1. **Victoria reviews the game and questions** in the artifact and sends changes.
2. **Narrator voice.** She creates a voice in ElevenLabs (Voices → Voice Design) and sends the voice ID. Suggested prompt:
   > A warm, jolly storyteller in his sixties with a rich, slightly husky baritone and a gentle Canadian accent. He sounds like a beloved grandfather reading a Christmas story by the fireplace: cosy, twinkly and full of good humour, with a soft chuckle in his voice. Clear diction and an unhurried pace, perfect for reading trivia questions aloud to a room. For mischievous moments he can drop into a playful, slightly sly tone, but he is never scary.

   Then generate audio **on her PC**: ElevenLabs is not reachable from the cloud. `voice-kit/start-voice.bat` runs `generate-voice.ps1`, which reads `voice-lines.json`, asks for the key (hidden input), the voice and a YES, voices only new lines and writes `audio/manifest.json` plus MP3s. Her PC folder for the Halloween kit was `C:\Работа\Текущие проекты\Клод\NightsOfFrights`. Use a new folder for Christmas, otherwise the manifests mix. If her PC is linked to the session, copy files with the device tools; otherwise she uploads the `audio` folder.
3. **Domain.** Suggestions: merryquizmas.com, merryquizmas.fun, merry-quizmas.ca. Check availability on Namecheap in her Chrome; she buys it herself. DNS like Night of Frights: four A records `185.199.108.153` to `185.199.111.153`, CNAME `www` to `vaku0004.github.io.`, remove the Namecheap parking redirect, set the custom domain in GitHub Pages, then **Enforce HTTPS** once the certificate is issued (it took about a day last time; removing and re-adding the domain helped).
4. **Website repo.** Publish the site (index.html, `audio/`, icons, robots.txt, sitemap.xml, content pages) to GitHub Pages. This repo can hold it, or a separate one. Then a no-redirect copy on github.io (like `night-of-frights-game`).
5. **SEO pages** like Night of Frights: Christmas trivia questions with answers, virtual and hybrid Christmas games for work, host guide, FAQ (neutral voice, no first person; she was fine publishing the game's own questions). Then Google Search Console (verify with an HTML file in the repo; she can't give Namecheap passwords), sitemap, Request indexing, IndexNow for Bing.
6. **Google Analytics 4**: a new property in her existing account ("Default Account for Firebase", **not** inside BYSO; her other properties there are BYSO, francabulaire, thumbnail, Night of Frights). Time zone Regina, CAD, 14-month retention, custom dimensions special / team_count / round / from_page.
7. Offline single-file build (`tools/build_offline.py`) as a backup for the party.

## Things to keep in mind

- Her cloud-session bonus credit ends November 4, 2026, 11:59 PM PT; after that her weekly plan limits apply. Work efficiently and avoid repeated screenshots.
- Publishing, buying and account actions go through her own Chrome (Claude in Chrome). Ask before anything irreversible.
- Commit as `git -c user.name="Viktoriia" -c user.email="vaku0004@users.noreply.github.com"`.
