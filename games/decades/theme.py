"""The Decades Showdown game's values for the engine slots (see engine/slots.py). Built by: python3 tools/build_game.py decades

Victoria's Decades Showdown ('80s, '90s, 2000s). Surprise 1 ("cat"): Tangled Tape. Surprise 2 ("witch"): Time Machine. Final: The Time Capsule.
Helpers: file(name) reads a file next to this theme; art(name, as_name) takes an SVG from art.js under the engine's name;
MOBILE_CSS is the phone layout from tools/site_common.py."""

VALUES = {
    'page_title': '<title>Victoria’s Decades Showdown</title>',
    'font_link': '&family=Righteous&display=swap',
    'css_comment_theme': 'Single dark theme by design (a neon retro night).',
    'css_comment_table': 'one cosy game table in the rec room',
    'color_night': '--night:#120d24',
    'color_dusk': '--dusk:#1c1533',
    'color_cell': '--cell:#281d47',
    'color_cell_hi': '--cell-hi:#36285e',
    'color_line': '--line:#43356e',
    'color_bone': '--bone:#f5f0ff',
    'color_ash': '--ash:#b3a8d6',
    'color_candle': '--candle:#ff5aa8',
    'color_ember': '--ember:#ffd1ec',
    'color_good': '--good:#3be8b0',
    'color_bad': '--bad:#ff6b5a',
    'color_witch': '--witch:#3fd5ff',
    'display_font': '--f-display:"Righteous","Arial Rounded MT Bold","Helvetica",sans-serif;',
    'atmosphere_css': '''
/* ---------- Neon: a faint retro grid on the floor and pink and cyan specks drifting up ---------- */
body::before,body::after{content:"";position:fixed;inset:-20vh 0 0;pointer-events:none;z-index:0;
  background-image:radial-gradient(2px 2px at 20px 30px,rgba(255,90,168,.5),transparent 60%),radial-gradient(1.5px 1.5px at 120px 80px,rgba(63,213,255,.45),transparent 60%),
  radial-gradient(2.5px 2.5px at 200px 160px,rgba(255,209,236,.35),transparent 60%),radial-gradient(1.5px 1.5px at 60px 210px,rgba(63,213,255,.4),transparent 60%),
  radial-gradient(2px 2px at 260px 250px,rgba(255,90,168,.3),transparent 60%);
  background-size:300px 300px;animation:snow 46s linear infinite;opacity:.45}
body::after{inset:auto 0 0;height:34vh;animation:none;opacity:.22;filter:none;
  background-image:linear-gradient(rgba(255,90,168,.9) 1px,transparent 1px),linear-gradient(90deg,rgba(63,213,255,.9) 1px,transparent 1px);
  background-size:60px 30px;-webkit-mask-image:linear-gradient(transparent,#000);mask-image:linear-gradient(transparent,#000)}
@keyframes snow{from{transform:translateY(20vh)}to{transform:translateY(0)}}
#app{position:relative;z-index:1}
.title,.round-name,.slide-title,.big-cat,.cat-ask,.cat-team,.reel-face,.special h3{letter-spacing:.01em}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition:none!important}
  body::before{display:none}
}''',
    'storage_keys': 'const KEY_S = "ds-state-v1", KEY_Q = "ds-questions-v1";',
    'storage_key_voice': 'const KEY_V = "ds-voice-v1";',
    'team_names': 'const TEAM_NAMES = ["Team Cassettes","Team Arcade","Team Neon","Team Dial-Up"];',
    'questions': file("questions.js").strip() + "\n",
    'migrate_old_questions': '',
    'art_cat_svg': art('TANGLED_SVG', 'CAT_SVG'),
    'art_hat_svg': art('TIMEMACHINE_SVG', 'HAT_SVG'),
    'art_moon_svg': art('CAPSULE_SVG', 'MOON_SVG'),
    'art_pumpkin_svg': art('CASSETTE_SVG', 'PUMPKIN_SVG'),
    'art_ghost_svg': art('BOOMBOX_SVG', 'GHOST_SVG'),
    'art_wand_svg': art('REWIND_SVG', 'WAND_SVG'),
    'narrator_name': 'const NARRATOR = "DJ Rewind";',
    'narrator_lines': '''const LINES = {
  test: "Welcome to Victoria's Decades Showdown. Pick a question, and let's rewind!",
  welcome: "Welcome to Victoria's Decades Showdown! Tonight, our teams travel back to the eighties, the nineties and the two thousands, for glory and for prizes. Here is how it works.",
  ready: "Ready? The first team, pick a question. Good luck, and may the most awesome team win.",
  rules: "Rules of the game. Pick a question from the board. Watch out for the tangled tape, and for the time machine. Play two rounds and the Time Capsule finale.",
  cat: "Oh no, a tangled tape! The team that found it must give this question to another team.",
  catWho: "Who gets the tangled tape?",
  witchTitle: "The time machine!",
  witch: "Step into the time machine! The first trip picks the price. The second trip picks the team that must answer. Answer right, and win it. Answer wrong, and lose it.",
  tie: "It's a tie! Time for a tiebreaker."
};''',
    'line_final_intro': 'const midnightLine = () => "It is time to open the Time Capsule. The final category is: "',
    'line_winner': 'const winnerLine = name => name + " rocked the decades!";',
    'line_surprise2_team': 'const dealLine = name => name + ", the time machine picked you!";',
    'narrator_moods': '''    [LINES.test]: "[cheerfully] Welcome to Victoria's Decades Showdown. Pick a question... and let's rewind!",
    [LINES.welcome]: "[excited] Welcome to Victoria's Decades Showdown! Tonight, our teams travel back to the eighties, the nineties and the two thousands... for glory, and for prizes. Here is how it works.",
    [LINES.ready]: "[cheerfully] Ready? The first team, pick a question. Good luck... and may the most awesome team win! [laughs]",
    [LINES.rules]: "[cheerfully] Rules of the game. Pick a question from the board. [mischievously] Watch out for the tangled tape... and for the time machine. [cheerfully] Play two rounds... and the Time Capsule finale.",
    [LINES.cat]: "[gasps] Oh no, a tangled tape! [mischievously] The team that found it... must give this question to another team.",
    [LINES.catWho]: "[mischievously] So... who gets the tangled tape?",
    [LINES.witchTitle]: "[whispers] The time... [excited] machine!",
''',
    'mood_surprise2': '    [LINES.witch]: "[excited] Step into the time machine! [laughs] The first trip picks the price. The second trip picks the team that must answer. Answer right... and win it. Answer wrong... [whispers] and lose it.",',
    'mood_winner': 'if (/ rocked the decades!$/.test(t)) return "[excited] " + t + " [applause]";',
    'music_comment': '''/* ===================== Time Capsule thinking music =====================
   An original synth arpeggio over a minor 80s-style bass line, with off-beat hi-hats.''',
    'music_chords': 'const M_CHORDS = [[69,72,76],[65,69,72],[60,64,67],[67,71,74],[69,72,76],[65,69,72],[60,64,67],[67,71,74]];',
    'music_bass': 'const M_BASS = [45,41,48,43,45,41,48,43];',
    'music_tempo': 'const M_STEP = 60 / 118 / 2;   // eighth notes at 118 bpm',
    'music_drone': 'o1.type = o2.type = "sawtooth"; o1.frequency.value = 55; o2.frequency.value = 55.5;',
    'music_drone_filter': 'f.type = "lowpass"; f.frequency.value = 600; g.gain.value = 0.03;',
    'music_ticks': '    if (pos % 2 === 1) this.note(7800, t, 0.02, "square", 0.004);   // off-beat synth hi-hat',
    'sound_surprise1': 'cat(){ tone(660,.45,"sawtooth",.05,0,180); tone(150,.3,"square",.04,.4,90); },',
    'sound_surprise2': 'witch(){ tone(200,.7,"sine",.08,0,1600); tone(1568,.3,"triangle",.07,.7); },',
    'slide_welcome_title': '{ eyebrow: "Welcome to", title: "Victoria’s Decades Showdown", art: hero(PUMPKIN_SVG),',
    'slide_welcome_text': 'Two rounds of retro trivia, two blasts from the past and one last wager in the time capsule.',
    'slide_rules_bullets': 'bullets: ["Pick a question from the board.", "Watch out for the tangled tape and the time machine.", "Play two rounds and the Time Capsule finale."],',
    'slide_surprise1': '''{ eyebrow: "Surprise", title: "Tangled Tape", art: hero(CAT_SVG),
      bullets: ["Find the tangled tape and you must give the question away.", "You choose which team gets it.", "That team answers for the full value, right or wrong."] },''',
    'slide_surprise2': '''{ eyebrow: "Surprise", title: "Time Machine", art: hero(HAT_SVG),
      bullets: ["The time machine makes two trips.", `The first trip picks the price:''',
    'slide_surprise2_second': '"The second trip picks t',
    'slide_final_title': '{ eyebrow: "The finale", title: "The Time Capsule", art: hero(MOON_SVG),',
    'slide_fair_play_last': '"Only one team rocks the decades."',
    'deck_final_filter': 'if (deck === "midnight") return list.filter(sl => sl.title === "The Time Capsule");',
    'deck_intro_filter': 'return list.filter(sl => !["Tangled Tape", "Time Machine", "Fast forward", "The Time Capsule"].includes(sl.title));',
    'slide_round2_title': '{ eyebrow: "Round Two", title: "Fast forward", art: ladder,',
    'deck_round2_filter': 'if (deck === "round2") return list.filter(sl => sl.title === "Fast forward");',
    'start_eyebrow': '<div class="eyebrow">A retro quiz for the whole office</div>',
    'start_title': '<h1 class="title"><span class="byline">Victoria’s</span>Decades Showdown</h1>',
    'start_intro': 'Two rounds of retro trivia from the ’80s, ’90s and 2000s, two blasts from the past on the board, and one last wager in the time capsule.',
    'start_surprise1': '<li>${CAT_SVG}<div><b>Tangled Tape</b><p>The team that finds the tangled tape must hand the question to another team.',
    'start_surprise2': '<li>${HAT_SVG}<div><b>Time Machine</b><p>The time machine makes two trips. The first picks a random price, the second picks the team that must answer.',
    'start_final': '<li>${MOON_SVG}<div><b>The Time Capsule</b><p>Round Two doubles every value.',
    'board_next_label': 'const nextLabel = finalDone ? "Back to the standings" : isLast ? "Go to the Time Capsule"',
    'board_eyebrow': '<div class="eyebrow">Victoria’s Decades Showdown</div>',
    'surprise1_card': '''<div class="special blackcat">${CAT_SVG}<div><h3>Tangled Tape</h3>
      <p>${esc(T[q.picker].name)} found a tangled tape and must hand this question to another team.''',
    'surprise1_ask': '<h3 class="cat-ask">Who gets the tape?</h3>',
    'surprise2_card': '''<div class="special witch">${HAT_SVG}<div><h3>Time Machine</h3>
      ${q.witchAsk ? `<p class="witch-quote" style="animation:rise-in .5s ease both">“Hold on tight, we’re going back in time…”</p>` : ""}''',
    'surprise2_step1': '<span><b>First trip</b> picks the price:',
    'surprise2_step2': '<span><b>Second trip</b> picks the team that must answer.',
    'surprise2_reel1_label': '<div class="reel-label">First trip · The price</div>',
    'surprise2_reel1_button': '${WAND_SVG} Start the time machine</button>',
    'surprise2_reel2_label': '<div class="reel-label">Second trip · The team</div>',
    'surprise2_reel2_button': '${WAND_SVG} Go again</button>',
    'question_surprise1_tag': '${q.special==="cat"?`<div class="special blackcat">${CAT_SVG}<div><h3>Tangled Tape</h3></div></div>`:""}',
    'question_surprise2_tag': '${q.special==="witch"?`<div class="special witch">${HAT_SVG}<div><h3>Time Machine</h3></div></div>`:""}',
    'final_eyebrow_category': '<div class="eyebrow">The Time Capsule · final category</div>',
    'final_eyebrow_question': '<div class="eyebrow">The Time Capsule · ${esc(F.category)}</div>',
    'podium_headline': 'const headline = winners.length === 1 ? esc(winners[0].name) + " rocked the decades"',
    'podium_eyebrow': '<div class="eyebrow">Victoria’s Decades Showdown · final standings</div>',
    'editor_surprise1_option': '<option value="cat" ${q.special==="cat"?"selected":""}>Tangled Tape</option>',
    'editor_surprise2_option': '<option value="witch" ${q.special==="witch"?"selected":""}>Time Machine</option>',
    'editor_final_tab': 'data-t="final" aria-selected="${tab==="final"}">Time Capsule</button>',
    'voice_preset_name': '<button class="btn" data-act="vpreset" data-p="spooky">Radio DJ voice</button>',
    'phone_layout': "</style>\n" + MOBILE_CSS + "\n\n<div id=\"app\"></div>",
}
