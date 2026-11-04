"""The Countdown Quiz game's values for the engine slots (see engine/slots.py). Built by: python3 tools/build_game.py newyear

Victoria's Countdown Quiz (New Year's Eve). Surprise 1 ("cat"): Party Popper. Surprise 2 ("witch"): Fortune Cookie. Final: The Midnight Countdown.
Helpers: file(name) reads a file next to this theme; art(name, as_name) takes an SVG from art.js under the engine's name;
MOBILE_CSS is the phone layout from tools/site_common.py."""

VALUES = {
    'page_title': '<title>Victoria’s Countdown Quiz</title>',
    'font_link': '&family=Bungee&display=swap',
    'css_comment_theme': "Single dark theme by design (a midnight-blue New Year's Eve).",
    'css_comment_table': 'one cosy game table at the countdown party',
    'color_night': '--night:#0d0f24',
    'color_dusk': '--dusk:#151838',
    'color_cell': '--cell:#1f2350',
    'color_cell_hi': '--cell-hi:#2a2f66',
    'color_line': '--line:#363b78',
    'color_bone': '--bone:#f4f3ff',
    'color_ash': '--ash:#aeb2d6',
    'color_candle': '--candle:#f5cf6b',
    'color_ember': '--ember:#fff0bf',
    'color_good': '--good:#6ee0a8',
    'color_bad': '--bad:#ff6b81',
    'color_witch': '--witch:#f0a35e',
    'display_font': '--f-display:"Bungee","Impact","Arial Black",sans-serif;',
    'atmosphere_css': '''
/* ---------- Confetti and gold sparkles: two slow layers drifting down behind the game ---------- */
body::before,body::after{content:"";position:fixed;inset:-20vh 0 0;pointer-events:none;z-index:0;
  background-image:radial-gradient(2px 2px at 20px 30px,rgba(245,207,107,.6),transparent 60%),radial-gradient(2.5px 1.5px at 120px 80px,rgba(255,107,129,.45),transparent 60%),
  radial-gradient(2px 2.5px at 200px 160px,rgba(110,224,168,.4),transparent 60%),radial-gradient(1.5px 1.5px at 60px 210px,rgba(255,240,191,.55),transparent 60%),
  radial-gradient(2.5px 2px at 260px 250px,rgba(240,163,94,.4),transparent 60%);
  background-size:300px 300px;animation:snow 40s linear infinite;opacity:.5}
body::after{background-size:420px 420px;animation-duration:56s;opacity:.38;filter:blur(.6px)}
@keyframes snow{from{transform:translateY(0)}to{transform:translateY(20vh)}}
#app{position:relative;z-index:1}
.title{font-size:clamp(2.6rem,5.4vw,5rem)}   /* Bungee is very wide: keep COUNTDOWN inside its column */
.title,.round-name,.slide-title,.big-cat,.cat-ask,.cat-team,.reel-face,.special h3{letter-spacing:.01em}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition:none!important}
  body::before,body::after{display:none}
}''',
    'storage_keys': 'const KEY_S = "ny-state-v1", KEY_Q = "ny-questions-v1";',
    'storage_key_voice': 'const KEY_V = "ny-voice-v1";',
    'team_names': 'const TEAM_NAMES = ["Team Confetti","Team Sparklers","Team Party Hats","Team Midnight"];',
    'questions': file("questions.js").strip() + "\n",
    'migrate_old_questions': '',
    'art_cat_svg': art('POPPER_SVG', 'CAT_SVG'),
    'art_hat_svg': art('COOKIE_SVG', 'HAT_SVG'),
    'art_moon_svg': art('FIREWORK_SVG', 'MOON_SVG'),
    'art_pumpkin_svg': art('CLOCK_SVG', 'PUMPKIN_SVG'),
    'art_ghost_svg': art('PARTYHAT_SVG', 'GHOST_SVG'),
    'art_wand_svg': art('SPARKLE_SVG', 'WAND_SVG'),
    'narrator_name': 'const NARRATOR = "Midnight Mae";',
    'narrator_lines': '''const LINES = {
  test: "Welcome to Victoria's Countdown Quiz. Pick a question, and let the countdown begin!",
  welcome: "Welcome to Victoria's Countdown Quiz! Tonight, our teams compete to end the year on top. Here is how it works.",
  ready: "Ready? The first team, pick a question. Good luck, and may the best team ring in the New Year as champions.",
  rules: "Rules of the game. Pick a question from the board. Watch out for the party popper, and for the fortune cookie. Play two rounds and the Midnight Countdown.",
  cat: "Pop! A party popper! The team that found it must give this question to another team.",
  catWho: "Who gets the party popper?",
  witchTitle: "A fortune cookie!",
  witch: "Let's crack open the fortune cookies! The first fortune picks the price. The second fortune picks the team that must answer. Answer right, and win it. Answer wrong, and lose it.",
  tie: "It's a tie! Time for a tiebreaker."
};''',
    'line_final_intro': 'const midnightLine = () => "It is time for the Midnight Countdown. The final category is: "',
    'line_winner': 'const winnerLine = name => name + " ring in the New Year!";',
    'line_surprise2_team': 'const dealLine = name => name + ", the fortune cookie picked you!";',
    'narrator_moods': '''    [LINES.test]: "[cheerfully] Welcome to Victoria's Countdown Quiz. Pick a question... and let the countdown begin!",
    [LINES.welcome]: "[warmly] Welcome to Victoria's Countdown Quiz! Tonight, our teams compete to end the year... on top. Here is how it works.",
    [LINES.ready]: "[cheerfully] Ready? The first team, pick a question. Good luck... and may the best team ring in the New Year as champions! [laughs]",
    [LINES.rules]: "[warmly] Rules of the game. Pick a question from the board. [mischievously] Watch out for the party popper... and for the fortune cookie. [cheerfully] Play two rounds... and the Midnight Countdown.",
    [LINES.cat]: "[excited] Pop! A party popper! [mischievously] The team that found it... must give this question to another team.",
    [LINES.catWho]: "[mischievously] So... who gets the party popper?",
    [LINES.witchTitle]: "[whispers] A fortune... [excited] cookie!",
''',
    'mood_surprise2': '    [LINES.witch]: "[excited] Let\'s crack open the fortune cookies! [laughs] The first fortune picks the price. The second fortune picks the team that must answer. Answer right... and win it. Answer wrong... [whispers] and lose it.",',
    'mood_winner': 'if (/ ring in the New Year!$/.test(t)) return "[excited] " + t + " [applause]";',
    'music_comment': '''/* ===================== Midnight Countdown thinking music =====================
   An original, festive waltz-like tune over a warm bass, with a ticking clock and a midnight chime every other bar.''',
    'music_chords': 'const M_CHORDS = [[65,69,72],[65,70,74],[64,67,72],[65,69,72],[62,65,69],[65,70,74],[64,67,70],[65,69,72]];',
    'music_bass': 'const M_BASS = [41,46,48,41,38,46,48,41];',
    'music_tempo': 'const M_STEP = 60 / 100 / 2;   // eighth notes at 100 bpm',
    'music_drone': 'o1.type = o2.type = "sine"; o1.frequency.value = 87.3; o2.frequency.value = 87.7;',
    'music_drone_filter': 'f.type = "lowpass"; f.frequency.value = 500; g.gain.value = 0.025;',
    'music_ticks': '    if (pos % 2 === 0) this.note(pos % 4 === 0 ? 1900 : 1500, t, 0.02, "square", 0.007); if (pos === 0 && bar % 2 === 0) { this.note(midi(77), t, 2.6, "sine", 0.05); this.note(midi(77) * 2.76, t, 1.2, "sine", 0.012); }   // tick, tock and the midnight chime',
    'sound_surprise1': 'cat(){ tone(160,.09,"square",.12,0,60); [1320,1580,1860,2200,2640].forEach((f,i)=>tone(f,.09,"sine",.05,.1+i*.05)); },',
    'sound_surprise2': 'witch(){ tone(320,.05,"square",.08,0,120); tone(260,.05,"square",.06,.07,100); [988,1319,1568].forEach((f,i)=>tone(f,.3,"sine",.05,.25+i*.12)); },',
    'slide_welcome_title': '{ eyebrow: "Welcome to", title: "Victoria’s Countdown Quiz", art: hero(PUMPKIN_SVG),',
    'slide_welcome_text': "Two rounds of New Year's trivia, two surprises on the board and one last wager in the Midnight Countdown.",
    'slide_rules_bullets': 'bullets: ["Pick a question from the board.", "Watch out for the party popper and the fortune cookie.", "Play two rounds and the Midnight Countdown."],',
    'slide_surprise1': '''{ eyebrow: "Surprise", title: "Party Popper", art: hero(CAT_SVG),
      bullets: ["Pop a party popper and you must give the question away.", "You choose which team gets it.", "That team answers for the full value, right or wrong."] },''',
    'slide_surprise2': '''{ eyebrow: "Surprise", title: "Fortune Cookie", art: hero(HAT_SVG),
      bullets: ["Two fortune cookies wait on the plate.", `The first fortune picks the price:''',
    'slide_surprise2_second': '"The second fortune picks t',
    'slide_final_title': '{ eyebrow: "The finale", title: "The Midnight Countdown", art: hero(MOON_SVG),',
    'slide_fair_play_last': '"Only one team rings in the New Year as champions."',
    'deck_final_filter': 'if (deck === "midnight") return list.filter(sl => sl.title === "The Midnight Countdown");',
    'deck_intro_filter': 'return list.filter(sl => !["Party Popper", "Fortune Cookie", "The last hour", "The Midnight Countdown"].includes(sl.title));',
    'slide_round2_title': '{ eyebrow: "Round Two", title: "The last hour", art: ladder,',
    'deck_round2_filter': 'if (deck === "round2") return list.filter(sl => sl.title === "The last hour");',
    'start_eyebrow': '<div class="eyebrow">A New Year’s quiz for the whole office</div>',
    'start_title': '<h1 class="title"><span class="byline">Victoria’s</span>Countdown Quiz</h1>',
    'start_intro': 'Two rounds of New Year’s trivia, from midnight traditions around the world to party food and famous countdowns, two surprises on the board, and one last wager in the Midnight Countdown.',
    'start_surprise1': '<li>${CAT_SVG}<div><b>Party Popper</b><p>The team that pops a party popper must hand the question to another team.',
    'start_surprise2': '<li>${HAT_SVG}<div><b>Fortune Cookie</b><p>Two fortune cookies crack open. The first picks a random price, the second picks the team that must answer.',
    'start_final': '<li>${MOON_SVG}<div><b>The Midnight Countdown</b><p>Round Two doubles every value.',
    'board_next_label': 'const nextLabel = finalDone ? "Back to the standings" : isLast ? "Go to the Midnight Countdown"',
    'board_eyebrow': '<div class="eyebrow">Victoria’s Countdown Quiz</div>',
    'surprise1_card': '''<div class="special blackcat">${CAT_SVG}<div><h3>Party Popper</h3>
      <p>${esc(T[q.picker].name)} popped a party popper and must hand this question to another team.''',
    'surprise1_ask': '<h3 class="cat-ask">Who gets the party popper?</h3>',
    'surprise2_card': '''<div class="special witch">${HAT_SVG}<div><h3>Fortune Cookie</h3>
      ${q.witchAsk ? `<p class="witch-quote" style="animation:rise-in .5s ease both">“Let’s see what the cookies say…”</p>` : ""}''',
    'surprise2_step1': '<span><b>First fortune</b> picks the price:',
    'surprise2_step2': '<span><b>Second fortune</b> picks the team that must answer.',
    'surprise2_reel1_label': '<div class="reel-label">First fortune · The price</div>',
    'surprise2_reel1_button': '${WAND_SVG} Crack the first cookie</button>',
    'surprise2_reel2_label': '<div class="reel-label">Second fortune · The team</div>',
    'surprise2_reel2_button': '${WAND_SVG} Crack the second cookie</button>',
    'question_surprise1_tag': '${q.special==="cat"?`<div class="special blackcat">${CAT_SVG}<div><h3>Party Popper</h3></div></div>`:""}',
    'question_surprise2_tag': '${q.special==="witch"?`<div class="special witch">${HAT_SVG}<div><h3>Fortune Cookie</h3></div></div>`:""}',
    'final_eyebrow_category': '<div class="eyebrow">The Midnight Countdown · final category</div>',
    'final_eyebrow_question': '<div class="eyebrow">The Midnight Countdown · ${esc(F.category)}</div>',
    'podium_headline': 'const headline = winners.length === 1 ? esc(winners[0].name) + " ring in the New Year"',
    'podium_eyebrow': '<div class="eyebrow">Victoria’s Countdown Quiz · final standings</div>',
    'editor_surprise1_option': '<option value="cat" ${q.special==="cat"?"selected":""}>Party Popper</option>',
    'editor_surprise2_option': '<option value="witch" ${q.special==="witch"?"selected":""}>Fortune Cookie</option>',
    'editor_final_tab': 'data-t="final" aria-selected="${tab==="final"}">Midnight Countdown</button>',
    'voice_preset_name': '<button class="btn" data-act="vpreset" data-p="spooky">Party host voice</button>',
    'phone_layout': "</style>\n" + MOBILE_CSS + "\n\n<div id=\"app\"></div>",
}
