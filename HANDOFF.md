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
- Website build: see "Victoria's Game Nights" below.

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

- Game: `valentines/sweetheart-showdown.html`, built by `python3 tools/build_valentines.py night-of-frights.html valentines/sweetheart-showdown.html` (same text-replacement method as Christmas; asserts every replacement). Questions `valentines/questions.js` (50 + final "Royal Romance" = Edward VIII + tiebreaker Hershey's Kisses 1907; facts checked from memory, no song lyrics). Art `valentines/art.js`: heart, arrow-through-heart, heart box of chocolates, love letter, rose, bonbon. Palette: wine night `#1a0f17`, rose `#ef7d9a`, blush `#ffd6e0`, caramel `#d4935f`; display font **Yeseva One** (fontsource `yeseva-one`, added to `fontify.py`); rosy sparkles drifting up instead of snow; slow music-box ballad in the final. Storage keys `ss-state-v1`, `ss-questions-v1`, `ss-voice-v1`. Team names: Lovebirds, Sweethearts, Roses, Truffles.
- Site: `tools/pages_valentines.py` (four pages, made from the Christmas pages and rewritten), screenshots `games/valentines/shots/`. Preview build checked: 45 URLs, nothing broken, no JS errors.
- Narrator: 136 lines, 13,210 characters, in `valentines/voice-lines.json`. Voice made on Nov 4: ID `7elAVxKk0tXJT7YGjurH` (prompts in `valentines/voice-design-prompts.md`). Kit with this voice as default: `valentines/voice-kit/` (sent to her as SweetheartShowdown-voice.zip). **Audio done (Nov 4):** 136/136 lines (voice name in ElevenLabs "Valentine Vic", eleven_v4) checked and committed to `audio/valentines/`.
- Offline file for her review (browser voice, no audio): `python3 tools/build_offline.py valentines <out.html>` (works without audio now).

## Fact check of all questions (November 4, 2026)

All 3 × 52 questions reviewed; doubtful facts checked online. Fixed: Halloween "Windsor Pumpkin Regatta" (the 2019 race was cancelled; now "for about twenty years from 1999", note says it ended when the lake was drained) and "Ganong" (first wrapped bar is the company's own claim: now "says it made the first wrapped chocolate bar in North America"; 1898 vs 1910 dates disputed, removed); Christmas tiebreaker note (Gene Autry's Rudolph: about 1.75 million copies in the first season, not "more than 2 million"); Valentine's "Colombia" question reworded (largest supplier of cut flowers to the US, not "most flowers sold").
**Re-voicing: done the same day** (she sent both `audio` folders; checked: 136/136 lines match `voice-lines.json`, old files for the changed lines removed). For later changes the method is: She puts the new `voice-lines.json` (`games/halloween/voice-lines.json` → her Halloween kit folder, `quizmas/voice-lines.json` → her Merry Quizmas kit folder) next to `generate-voice.ps1`, runs `start-voice.bat`; only changed lines are voiced. Then copy the new MP3s and `manifest.json` into `audio/halloween/` and `audio/christmas/`. Until then those lines fall back to the browser voice.

## Narrator names in Voice settings (November 4, 2026)

No "ElevenLabs" or model name on screen any more. The button is "Game narrator" / "Browser voice", and the line under it reads "Narrator: <name>. All 136 lines are recorded." Names: Halloween "The Spooky Narrator", Christmas "Grandpa Noel", Valentine's "Valentine Vic" (`const NARRATOR` in `night-of-frights.html`, replaced in `build_quizmas.py` / `build_valentines.py`). ElevenLabs is still mentioned only in code comments and the voice kit.

## Money and growth plan (agreed November 3, 2026; do it when the site is published)

She liked this three-step test of demand and wants it built **together with the website**:

1. **Donations this winter.** Ko-fi page in the brand's name (she creates it and sends the link). Links: on the podium screen at the end of a game ("Enjoyed the game? Buy Victoria a hot chocolate"), small "Support the games" link on the home page and in every footer, an FAQ item "How can I support the games?". GA event `support_click`. Wording "Support"/"Tip", not "Donate" (only registered charities give donation receipts; tips are income).
2. **"Want a custom office edition? Contact us"** on every game page and the home page, to test the most expensive product. Needs a contact address or form from her (forms on a static site need a service such as Formspree, or just an email address shown as text).
3. **Paid full version** from Valentine's Day or St. Patrick's Day, once Analytics shows real traffic.

Pricing hypothesis (USD, to test): full game $19–29 one-time; office edition $99–249 (logo, company name, 5–10 office questions she writes, narrator says the company name); annual pass $49–99 once there are 4–5+ games; Etsy PDF packs $5–9. Revenue math at $19: 10,000 seasonal visitors × 1% ≈ $1,900; real income comes from many games per year plus office editions.

Payments: Stripe works for a Saskatchewan sole proprietor and is cheapest (~2.9% + 30¢), but she is then the seller of record for foreign taxes (EU/UK VAT on digital sales to consumers from the first sale; US states have high thresholds; Canada GST/HST only above $30k). Merchant-of-record services (Lemon Squeezy, owned by Stripe; Paddle; ~5% + 50¢) handle all of that; check whether Stripe's own merchant-of-record option (Managed Payments) is available in Canada. Plan: Stripe if selling mainly to Canada/US, a merchant of record if selling worldwide. She should see an accountant before paid sales start. When selling starts, move hosting from GitHub Pages to Cloudflare Pages or Netlify.

Direction: **the whole English-speaking world, US first**, neutral English for the rest. Ideas agreed in principle: swappable local category per country (Oh, Canada! / Stars & Stripes / Rule, Britannia / Down Under), dates in words, units in both systems, US spelling (decide; site is en_CA now), prices in USD. Holiday calendar for 2027 (launch 4–6 weeks ahead): Valentine's Day (~Jan 20), St. Patrick's Day (~Feb 10), all-year Team Trivia (spring, basis for the paid version), Canada Day / July 4, Thanksgiving (Canada October + US November), Halloween and Christmas with local packs; also International Women's Day and Employee Appreciation Day for HR buyers. Avoid trademarked names (Olympics, Super Bowl, Oscars, Eurovision, World Cup) and solemn days; cultural and religious holidays only with review by people from that culture. Before many new games: refactor to one engine + a theme file per game (questions, art, colours, narrator lines) instead of text replacement.

## Next steps (in order)

1. **Domain for Victoria's Game Nights.** Suggestions: victoriasgamenights.com / .ca. She checks on Namecheap and buys it; then set `URL` in `tools/site_common.py`. DNS like Night of Frights: four A records `185.199.108.153` to `185.199.111.153`, CNAME `www` to `vaku0004.github.io.`, remove the Namecheap parking redirect, set the custom domain in GitHub Pages, **Enforce HTTPS** once the certificate is issued (about a day last time; removing and re-adding the domain helped).
2. **Repo `vaku0004/game-nights`:** she creates it (public, for free Pages) and adds it to the session. Move the sources there, or keep the sources here and publish only the built site there. Publish the `build_site.py` output (without Christmas until Nov 15).
3. **After the new site is live:** run `build_redirects.py` on the night-of-frights repo and push. Search Console: add the new domain (HTML-file verification, she can't give Namecheap passwords), submit the sitemap, use the Change of Address tool from nightoffrights.monster; IndexNow for Bing. Update or retire the night-of-frights-game mirror. In GA: rename the property, add the new domain.
4. **November 15:** rebuild (Christmas appears by date), push, request indexing for the Christmas pages.
5. **She reviews the Christmas game** (offline file sent on Nov 3) and sends changes in one list. Changed narrator text needs re-voicing of those lines only (`voice-kit/start-voice.bat` on her PC, same folder; ElevenLabs is not reachable from the cloud). She sends audio as .rar; `node-unrar-js` (npm, WASM) extracts it in the cloud.
6. **Valentine's Day game:** built on Nov 4 (see "Sweetheart Showdown"). Voice and audio done. Remaining: her review. Goes live by date on January 20, 2027.

## Things to keep in mind

- Her cloud-session bonus credit ends November 4, 2026, 11:59 PM PT; after that her weekly plan limits apply. Work efficiently and avoid repeated screenshots.
- Publishing, buying and account actions go through her own Chrome (Claude in Chrome). Ask before anything irreversible.
- Commit as `git -c user.name="Viktoriia" -c user.email="vaku0004@users.noreply.github.com"`.
