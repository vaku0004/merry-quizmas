"""Content pages of Victoria’s Pot o’ Gold (/stpatricks/...). Rendered by tools/build_site.py through tools/page_shell.py.

NAME and Q (the game's questions) are set by build_site.py before rendering. href="/" in the content means "play the game".
"""
import re
from page_shell import e, fig, play_box

NAME = ""
Q = {}

# ---------------------------------------------------------------- 1. Trivia questions
CATS = {
    "The Emerald Isle": ("Ireland trivia", "Dublin, the harp, the flag, the Shannon and the Cliffs of Moher."),
    "Luck & Legends": ("Luck and folklore trivia", "Four-leaf clovers, the Blarney Stone, leprechauns and banshees."),
    "Myths of Ireland": ("Irish mythology trivia", "Giants, swans, the Salmon of Knowledge and the Land of the Young."),
    "Going Green": ("Trivia about all things green", "Chlorophyll, emeralds, a famous green statue and a renamed fruit."),
    "Around the World": ("St. Patrick’s Day around the world", "A green river in Chicago, the oldest parade in New York and a Caribbean island that takes the day off."),
    "The Real St. Patrick": ("St. Patrick trivia", "Who the saint really was, where he was born and why March 17."),
    "Irish Words": ("Irish language trivia", "Craic, sláinte, smithereens and the Irish name for Ireland."),
    "Famous Irish": ("Famous Irish people trivia", "Writers, rock stars and a president with Irish roots."),
    "Music & Dance": ("Irish music and dance trivia", "Riverdance, the bodhrán and Irish stars. No lyrics required."),
    "A Taste of Ireland": ("Irish food trivia", "Soda bread, colcannon, boxty and the story behind corned beef and cabbage."),
}
slugify = lambda s: re.sub(r"-+", "-", "".join(c.lower() if c.isalnum() else "-" for c in s.replace("'", ""))).strip("-")


def trivia_body():
    n = 0
    toc_cols, sections = [], []
    for r_i, rnd in enumerate(Q["rounds"]):
        level = "warm-up" if r_i == 0 else "harder"
        items = []
        for cat in rnd["categories"]:
            sub, intro = CATS[cat["name"]]
            cid = slugify(cat["name"])
            items.append(f'<li><a href="#{cid}">{e(cat["name"])}</a> <span class="muted">· {e(sub)}</span></li>')
            lis = []
            for i, q in enumerate(cat["qs"]):
                n += 1
                tag = ""
                if q.get("special") == "cat":
                    tag = '<span class="tag cat">Leprechaun’s Trick</span>'
                elif q.get("special") == "witch":
                    tag = '<span class="tag witch">Over the Rainbow</span>'
                lis.append(f'''<li id="q{n}"><div class="qtop"><span class="qnum">{n}.</span><div class="qbody"><p class="qtext">{e(q["q"])}</p>{tag}
<details><summary>Show answer</summary><p class="ans">{e(q["a"])}</p>{f'<p class="why">{e(q["note"])}</p>' if q.get("note") else ""}</details></div><span class="pts">{rnd["values"][i]} pts</span></div></li>''')
            sections.append(f'''<section aria-labelledby="{cid}">
<h2 id="{cid}">{e(cat["name"])}<small>{e(sub)} · {rnd["name"]}, {rnd["values"][0]}–{rnd["values"][-1]:,} points</small></h2>
<p class="cat-intro">{e(intro)}</p>
<ol class="qlist">{"".join(lis)}</ol>
</section>''')
        toc_cols.append(f'<div><p class="eyebrow">{rnd["name"]} · {level}</p><ul>{"".join(items)}</ul></div>')
    F, T = Q["final"], Q["tiebreak"]
    toc_cols.append('<div><p class="eyebrow">Bonus</p><ul><li><a href="#end-of-the-rainbow">The final question and the tiebreaker</a></li>'
                    '<li><a href="#play">Play these questions as a game</a></li></ul></div>')
    bonus = f'''<section aria-labelledby="end-of-the-rainbow">
<h2 id="end-of-the-rainbow">Bonus: the final question<small>End of the Rainbow round · teams wager points before they see it</small></h2>
<p class="cat-intro">In the game, every team secretly wagers part of its score on the category alone, then sees the question. The category is <b>{e(F["category"])}</b>.</p>
<ol class="qlist" start="51">
<li id="q51"><div class="qtop"><span class="qnum">51.</span><div class="qbody"><p class="qtext">{e(F["q"])}</p>
<details><summary>Show answer</summary><p class="ans">{e(F["a"])}</p><p class="why">{e(F.get("note",""))}</p></details></div><span class="pts">wager</span></div></li>
<li id="q52"><div class="qtop"><span class="qnum">52.</span><div class="qbody"><p class="qtext">Tiebreaker: {e(T["q"])}</p>
<details><summary>Show answer</summary><p class="ans">{e(T["a"])}</p><p class="why">{e(T.get("note",""))}</p></details></div><span class="pts">closest wins</span></div></li>
</ol></section>'''
    play_sec = f'''<section aria-labelledby="play">
<h2 id="play">Play these questions as a team game</h2>
<div class="prose"><p>Every question on this page is part of <a href="/">{e(NAME)}</a>, a free quiz game for the big screen. Instead of reading from a list, teams pick categories and point values on a game-show board and race the clock.</p></div>
{fig("board", "Pot o’ Gold game board with five St. Patrick’s Day categories and point values from 100 to 500", "Round One board: teams take turns picking a category and a point value.")}
<ul class="features">
<li><b>Scores and turns</b>The board keeps the score and shows whose turn it is. A wrong answer costs the points.</li>
<li><b>A narrator</b>A friendly storyteller’s voice reads every question and answer aloud, so the host can play too.</li>
<li><b>30-second timer</b>Teams talk it over, then answer. The game keeps moving.</li>
<li><b>Two surprises</b>The Leprechaun’s Trick and Over the Rainbow hide on the board.</li>
<li><b>End of the Rainbow final</b>Secret wagers, one last question and a podium for the team that found the pot of gold.</li>
<li><b>Your own questions</b>Change any question or answer right in the game, for example to add questions about your office.</li>
</ul>
</section>'''
    return f'''<div class="prose">
<p class="lede">Fifty St. Patrick’s Day trivia questions with answers, written for office parties, team events and pub-style quiz nights. They cover Ireland and its legends, luck and folklore, Irish words, famous Irish people, music and dance, food, St. Patrick himself and how the world goes green on March 17.</p>
<p>Questions get harder within each category: the first ones warm everyone up, and the last ones decide who wins. Each answer comes with a short explanation, so the reveal is half the fun. Read them aloud, print them, or <a href="#play">play them on a big screen as a team game</a> with scores, a timer and a narrator.</p>
</div>
<div class="note-box no-print"><strong>How to use this page:</strong> answers are hidden. Read a question, let everyone guess, then press <b>Show answer</b>. Questions 1–25 are easier, 26–50 are harder.</div>
<div class="cta-row no-print">
<a class="btn primary" href="/">Play as a game</a>
<button class="btn" type="button" data-print="answers">Print with answers</button>
<button class="btn" type="button" data-print="questions">Print questions only</button>
<button class="btn" type="button" data-toggle-all>Show all answers</button>
</div>
<nav class="toc" aria-label="Categories">{"".join(toc_cols)}</nav>
{"".join(sections)}
{bonus}
{play_sec}
<section aria-labelledby="more"><h2 id="more">More for your St. Patrick’s Day party</h2>
<div class="prose"><ul>
<li><a href="/stpatricks/how-to-host-a-game-night/">How to host a St. Patrick’s Day game at work</a>: equipment, teams, timing and prizes.</li>
<li><a href="/stpatricks/virtual-games-for-work/">St. Patrick’s Day games for remote and hybrid teams</a>: how to include coworkers on a video call.</li>
<li><a href="/stpatricks/faq/">Questions about the game</a>: players, time, browsers and editing questions.</li>
</ul></div></section>
{play_box("Turn this list into a game", "Fifty of these questions are already on a game board with a narrator, a timer and scores. Open it on the big screen, name your teams and press Start.")}'''


TRIVIA_JS = '''<script>
(function(){
  var all = function(open){ document.querySelectorAll('.qlist details').forEach(function(d){ d.open = open; }); };
  var t = document.querySelector('[data-toggle-all]');
  if (t) t.addEventListener('click', function(){ var open = t.getAttribute('aria-pressed') !== 'true'; all(open);
    t.setAttribute('aria-pressed', open); t.textContent = open ? 'Hide all answers' : 'Show all answers'; });
  document.querySelectorAll('[data-print]').forEach(function(b){ b.addEventListener('click', function(){
    var withAnswers = b.getAttribute('data-print') === 'answers';
    document.body.classList.toggle('print-no-answers', !withAnswers);
    var was = Array.prototype.map.call(document.querySelectorAll('.qlist details'), function(d){ return d.open; });
    all(withAnswers); window.print();
    document.querySelectorAll('.qlist details').forEach(function(d, i){ d.open = was[i]; });
    document.body.classList.remove('print-no-answers'); }); });
})();
</script>'''


# ---------------------------------------------------------------- 2. Remote and hybrid teams
def virtual_body():
    invite = ("Subject: St. Patrick’s Day trivia, [day] at [time] \u2618\ufe0f\n\n"
              "Hi everyone,\n\n"
              "On [day] at [time] we're playing Victoria’s Pot o’ Gold, a St. Patrick’s Day trivia game for teams. "
              "It takes about an hour.\n\n"
              "Joining remotely? Use the usual meeting link. You’ll be on a team, hear the narrator and answer like everyone else.\n\n"
              "Wear something green if you like. The winning team gets a prize (gold chocolate coins, probably).\n\n"
              "See you there!")
    return f'''<div class="prose">
<p class="lede">Most office St. Patrick’s Day activities are built for people in the same room. Green-food potlucks, hat contests and parties leave coworkers on a video call watching from a small window.</p>
<p>A St. Patrick’s Day game works for a hybrid team when three things are true: everyone sees the same screen, everyone hears the same voice, and remote players are part of a team instead of an audience. This page shows how to set that up in Microsoft Teams, Zoom and Google Meet, plus a few more ideas for remote and hybrid teams.</p>
</div>

<h2>A St. Patrick’s Day trivia game built for hybrid teams</h2>
<div class="prose"><p><a href="/">{e(NAME)}</a> is a free trivia game made for exactly this situation: one big screen in the office, with part of the team joining by video. The host opens the game in a browser and shares that window in the meeting.</p></div>
<ul class="features">
<li><b>One shared screen</b>The board, the scores and the timer are the same for the room and for the call.</li>
<li><b>A narrator for everyone</b>Every question is read aloud, so remote players don’t depend on a small, blurry screen.</li>
<li><b>Remote players on teams</b>Coworkers on the call join a team and help answer, not just watch.</li>
<li><b>Same 30 seconds</b>Every team gets the same time to talk it over, wherever they sit.</li>
<li><b>Nothing to install</b>Only the host opens the website. Players don’t need an app, an account or a phone.</li>
<li><b>About an hour</b>Two rounds, two surprises on the board and a final round with secret wagers.</li>
</ul>
{fig("question", "A Pot o’ Gold question on screen with a 30-second timer and buttons to read the question again or show the answer", "A question on the shared screen. The narrator reads it aloud, then the 30-second timer starts.")}

<h2>How to share the game with sound</h2>
<div class="prose"><p>The one setting that matters: share the game <b>with computer sound</b>, otherwise remote players see the questions but don’t hear the narrator. Menu names change from time to time, but the option is always in the screen-sharing window.</p></div>
<ol class="steps">
<li><b>Open the game in Chrome or Edge</b> on the computer connected to the big screen, name the teams and press F11 for full screen.</li>
<li><b>Start the meeting on the same computer</b> and connect the room’s speakers, so people in the office hear the narrator too.</li>
<li><b>Share the browser window with sound turned on</b> (see below for your app).</li>
<li><b>Ask someone on the call to confirm</b> that they can hear the test line in <b>Voice settings</b> before you start.</li>
</ol>
<h3>Microsoft Teams</h3>
<div class="prose"><p>Select <b>Share</b> in the meeting controls, turn on <b>Include sound</b>, then choose the browser window with the game. If you already started sharing without sound, stop and share again with the option on.</p></div>
<h3>Zoom</h3>
<div class="prose"><p>Select <b>Share Screen</b>, pick the browser window, and tick <b>Share sound</b> at the bottom of the sharing window before you press Share.</p></div>
<h3>Google Meet</h3>
<div class="prose"><p>Select <b>Share screen</b> and choose <b>a tab</b> rather than a window, pick the game’s tab and keep <b>Also share tab audio</b> turned on. Tab audio works best in Chrome.</p></div>

<h2>How remote players join a team</h2>
<div class="prose">
<ul>
<li><b>Mix them in.</b> Put each remote coworker on a team with people in the room, rather than making one “remote team”.</li>
<li><b>Give each team a side chat.</b> A small group chat per team lets remote players share answers during the 30 seconds without everyone hearing.</li>
<li><b>Name a captain.</b> One person per team says the final answer out loud. It keeps things fair and fast.</li>
<li><b>Final round on paper, or in the chat.</b> In the End of the Rainbow round teams write down a secret wager and an answer. Remote players can send theirs to the host in a private message.</li>
</ul></div>
{fig("rainbow", "Over the Rainbow screen: the first rainbow picks a price of 300 points and the second picks the team that must answer", "Over the Rainbow: the rainbow picks the price and then the team that must answer. It plays the same for the room and the call.")}

<h2>More St. Patrick’s Day ideas for remote and hybrid teams</h2>
<div class="prose"><p>Want to fill a longer party, or warm up before the trivia? These work on a call and in the room at the same time.</p>
<ol>
<li><b>Wear green on camera.</b> Everyone wears something green, then the team votes in a meeting poll for the greenest outfit.</li>
<li><b>Lucky charm show-and-tell.</b> Each person shows a lucky object or shares a superstition from their family.</li>
<li><b>Guess the green.</b> Share close-up photos of green things around the house or office; others guess what they are.</li>
<li><b>Tall tale relay.</b> One person starts an Irish-style tall tale with a single sentence, the next adds one more, alternating between the room and the call.</li>
<li><b>Two truths and a lie, lucky edition.</b> Each person shares three “facts” about their luckiest moments; everyone guesses the lie.</li>
</ol></div>

<h2>Invitation template</h2>
<div class="prose"><p>Copy it into an email or a chat message and fill in the day and time.</p></div>
<div class="copybox" id="invite">{e(invite)}<button class="btn" type="button" data-copy="invite">Copy</button></div>

{play_box("Ready for a hybrid St. Patrick’s Day?", "Open the game, share it with sound on, and let the narrator do the talking. Free, no sign-up, nothing for players to install.")}
<div class="prose" style="margin-top:28px"><p class="muted">Also useful: <a href="/stpatricks/how-to-host-a-game-night/">the host guide</a>, <a href="/stpatricks/trivia-questions/">all 50 trivia questions with answers</a> and <a href="/stpatricks/faq/">frequently asked questions</a>.</p></div>'''


COPY_JS = '''<script>
document.querySelectorAll('[data-copy]').forEach(function(b){ b.addEventListener('click', function(){
  var box = document.getElementById(b.getAttribute('data-copy')); var text = box.firstChild.textContent;
  var done = function(){ b.textContent = 'Copied'; setTimeout(function(){ b.textContent = 'Copy'; }, 1800); };
  if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function(){}); }); });
</script>'''


# ---------------------------------------------------------------- 3. Host guide
def host_body():
    return f'''<div class="prose">
<p class="lede">Got asked to “do something fun for St. Patrick’s Day”? A team trivia game is one of the easiest office activities to run: it needs no crafts, works for any age and keeps everyone involved for an hour.</p>
<p>This guide walks through hosting <a href="/">{e(NAME)}</a>, a free St. Patrick’s Day quiz for the big screen, from the equipment to the prizes. Most of it applies to any office game night.</p>
</div>

<h2>What you need</h2>
<div class="prose"><ul>
<li><b>A laptop</b> with Chrome or Edge and an internet connection.</li>
<li><b>A big screen:</b> a TV, a projector or a meeting-room display, connected by HDMI.</li>
<li><b>Speakers</b> loud enough for the room. The narrator reads every question aloud.</li>
<li><b>A presentation clicker</b> (optional). Its arrow buttons move through the rules slides.</li>
<li><b>Paper and pens</b> for the final round, where teams write a secret wager and an answer.</li>
<li><b>Prizes</b> for the winning team, and gold chocolate coins for everyone.</li>
<li><b>A video call</b> if some people join remotely. See <a href="/stpatricks/virtual-games-for-work/">how to set it up for hybrid teams</a>.</li>
</ul></div>

<h2>Before the day</h2>
<ol class="steps">
<li><b>Open the game</b> on the laptop you’ll use and choose the number of teams (2 to 4).</li>
<li><b>Check the narrator.</b> Open <b>Voice settings</b> and play the test line through the room’s speakers.</li>
<li><b>Read the questions</b> in <b>Edit questions</b>, and change any that don’t fit your group. You can add questions about your own office (more on that below).</li>
<li><b>Do a two-minute rehearsal</b> on the big screen: open one question, show the answer, then press <b>Undo</b>.</li>
</ol>
<div class="note-box"><strong>Good to know:</strong> the game saves its progress in the browser. If the laptop goes to sleep or someone closes the tab, open the site again on the same computer and pick up where you left off.</div>

<h2>Split into teams</h2>
<div class="prose"><ul>
<li><b>2 to 4 teams of 3 to 5 people</b> work best. With more people, make bigger teams rather than more of them.</li>
<li><b>Mix departments</b> so the same groups don’t always sit together. It’s a team-building game, after all.</li>
<li><b>Put remote coworkers on mixed teams</b> with people in the room.</li>
<li><b>Let teams pick a name.</b> “Team Reindeer” is fine, but the funny names are half the fun.</li>
</ul></div>

<h2>How the game runs</h2>
<div class="prose">
<p>The game opens with a few short rules slides, read aloud by the narrator, so you don’t need to explain anything yourself.</p>
<ul>
<li><b>Round One.</b> A board of five categories with questions worth 100 to 500 points. Teams take turns picking a cell. The team that picks it answers within 30 seconds. A right answer wins the points, a wrong one loses them.</li>
<li><b>Leprechaun’s Trick.</b> Two cells on each board hide a leprechaun. The team that finds him must give the question to another team.</li>
<li><b>Over the Rainbow.</b> One cell on each board hides a rainbow. It appears twice: first it picks a random price, then the team that must answer.</li>
<li><b>Round Two.</b> New categories, and every value doubles: 200 to 1,000 points.</li>
<li><b>End of the Rainbow.</b> The final round. Teams see only the category, secretly wager up to half of their score (or up to 500 if that is more), then get 60 seconds to write down the answer.</li>
<li><b>The podium.</b> The game adds up the scores and announces the team that found the pot of gold. If two teams tie for first, a tiebreaker decides: the closest number wins.</li>
</ul></div>
<div class="two">
{fig("leprechaun", "Leprechaun’s Trick screen with a green leprechaun hat, asking which team gets the question", "Leprechaun’s Trick: the team that found him hands the question to another team.")}
{fig("final", "End of the Rainbow final category Irish in America with each team’s highest allowed wager", "End of the Rainbow: the game shows each team’s highest allowed wager.")}
</div>

<h2>Make it about your office</h2>
<div class="prose"><p>The quickest way to make the game memorable is to swap in a few questions about your own workplace. Open <b>Edit questions</b> and replace any question, answer or explanation. Some ideas:</p>
<ul>
<li>In what year did the company open its first location?</li>
<li>Who in the office has Irish roots, and in which county?</li>
<li>Who wore the most green to last year’s St. Patrick’s Day?</li>
<li>Which team has the luckiest track record at office raffles?</li>
</ul>
<p>Keep them friendly: questions everyone can laugh about, not at.</p></div>

<h2>A one-hour timeline</h2>
<div class="prose"><p>You don’t have to open every cell. When time is short, move on to the next round with the button under the board.</p></div>
<table class="tbl">
<thead><tr><th>Time</th><th>What happens</th></tr></thead>
<tbody>
<tr><td>0–5 min</td><td>Welcome, teams sit together, the rules slides play.</td></tr>
<tr><td>5–25 min</td><td>Round One: about 12–15 questions, including the first surprises.</td></tr>
<tr><td>25–30 min</td><td>Short break for soda bread and green cupcakes. Remote players stay on the call.</td></tr>
<tr><td>30–50 min</td><td>Round Two: double points, so the scores can still turn around.</td></tr>
<tr><td>50–56 min</td><td>End of the Rainbow: secret wagers, the final question, 60 seconds to answer.</td></tr>
<tr><td>56–60 min</td><td>Podium, prizes and a group photo.</td></tr>
</tbody></table>

<h2>Prize ideas under $25</h2>
<div class="prose"><ul>
<li><b>A pot of gold chocolate coins</b> to share among the winning team.</li>
<li><b>Coffee gift cards</b>, one per player on the winning team.</li>
<li><b>A trophy:</b> a small pot painted black and filled with gold coins, passed on to next year’s winners.</li>
<li><b>Bragging rights:</b> the winning team picks the next team lunch spot.</li>
<li><b>Small extra prizes</b> for the best team name, the greenest outfit or the bravest wager.</li>
</ul></div>
{fig("podium", "Final standings podium: Team Shamrocks in first place with 3,400 points", "The podium at the end of the night.")}

<h2>Common problems and quick fixes</h2>
<div class="prose"><ul>
<li><b>Remote players can’t hear the narrator.</b> Stop sharing and share again with computer sound turned on.</li>
<li><b>A team argues with an answer.</b> The host has the last word. The explanation under each answer usually settles it.</li>
<li><b>Points went to the wrong team.</b> Press <b>Undo</b>, or fix a score with the + and − buttons on the team’s card.</li>
<li><b>One team is far behind.</b> Let it play out: doubled values in Round Two, the rainbow and the End of the Rainbow wagers can still change the result.</li>
<li><b>Two teams tie.</b> The game offers a tiebreaker question where the closest number wins.</li>
<li><b>The room is too loud for the timer.</b> Turn up the speakers or name a timekeeper who calls “time!”.</li>
</ul></div>

{play_box("Your game night is ready", "Everything above is built into the game: rules slides, the narrator, the timer, scores and the podium. Open it, name your teams and press Start.")}
<div class="prose" style="margin-top:28px"><p class="muted">Also useful: <a href="/stpatricks/trivia-questions/">all 50 trivia questions with answers</a>, <a href="/stpatricks/virtual-games-for-work/">St. Patrick’s Day games for remote and hybrid teams</a> and <a href="/stpatricks/faq/">frequently asked questions</a>.</p></div>'''


# ---------------------------------------------------------------- 4. FAQ
FAQ = [
    ("Is Pot o’ Gold free? Do players need to sign up?",
     "Yes, it’s free, with no account and no download. Only the host opens the website. Players just watch the shared screen and answer out loud."),
    ("How many people can play?",
     "The game is built for 2 to 4 teams. It works best with about 6 to 20 players: with more people, make the teams bigger rather than adding more of them."),
    ("How long does a game take?",
     "About an hour. A full board of 50 questions takes longer, but you don’t need to open every cell: the host can move on to the next round at any time. The <a href=\"/stpatricks/how-to-host-a-game-night/\">host guide</a> has a one-hour timeline."),
    ("Can remote coworkers play?",
     "Yes. Share the game in Microsoft Teams, Zoom or Google Meet with computer sound turned on, and put remote players on teams with people in the room. See <a href=\"/stpatricks/virtual-games-for-work/\">St. Patrick’s Day games for remote and hybrid teams</a>."),
    ("Do players need their phones?",
     "No. Everything happens on one screen. Teams only need paper and a pen for the final round."),
    ("What do I need to run it?",
     "A computer with Chrome or Edge, a big screen or projector and speakers. A presentation clicker is handy but optional."),
    ("Is there a narrator? Can I turn the sound off?",
     "A warm, jolly narrator reads every question, answer and announcement. You can turn the voice or the sound effects off at any time with the buttons above the board."),
    ("Can I change the questions?",
     "Yes. Open <b>Edit questions</b> on the start screen to change any question, answer or explanation. Your changes are saved in the browser on that computer."),
    ("What happens if the browser closes in the middle of a game?",
     "The game saves its progress in the browser. Open the site again on the same computer and continue where you left off."),
    ("Is it appropriate for work and for kids?",
     "Yes. The questions are about Ireland, legends, words, music, food, nature and history. Drinks are mentioned only in passing, and there is nothing a team would find awkward. It suits teens and adults best; younger kids may need a grown-up on their team."),
    ("Can I see all the questions before playing?",
     "Yes, all 50 questions and answers are on the <a href=\"/stpatricks/trivia-questions/\">St. Patrick’s Day trivia questions</a> page. You can also print them for a quiz without a screen."),
    ("Which browser works best?",
     "Chrome or Microsoft Edge on a laptop or desktop computer. Other modern browsers should work too."),
    ("Is there a Halloween version?",
     "Yes: <a href=\"/halloween/\" data-home>Victoria’s Night of Frights</a> is the same game with Halloween questions, a black cat, a witch and a midnight wager."),
    ("Does the site collect any data?",
     "The site uses Google Analytics to count visits and to see which parts of the game are used, for example how many games are started and finished. It does not collect team names, answers or anything typed into the question editor, and it does not use advertising cookies. For visitors in the European Economic Area, the UK, Switzerland and Quebec, analytics cookies are turned off. You can also block analytics with any browser privacy setting or extension; the game works the same."),
    ("Are there games for other holidays?",
     "Yes. Victoria’s Pot o’ Gold is one of the free quiz games on <a href=\"/\" data-home>Victoria’s Game Nights</a>, with a new game for each season."),
    ("Who made the game?",
     f"{NAME} was designed and written by Victoria for office St. Patrick’s Day parties, then shared free for anyone to use."),
]


def faq_body():
    items = "".join(f'<h2 id="{"privacy" if q.startswith("Does the site collect") else f"q{k+1}"}">{e(q)}</h2><p>{a}</p>' for k, (q, a) in enumerate(FAQ))
    return f'''<div class="prose"><p class="lede">Short answers about {e(NAME)}, a free St. Patrick’s Day trivia game for teams in the office and on video calls.</p></div>
<div class="faq">{items}</div>
{play_box()}'''


def faq_ld():
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return [{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in FAQ]}]


PAGES = [
    dict(slug="trivia-questions",
         title="50 St. Patrick’s Day Trivia Questions and Answers for Work",
         desc="St. Patrick’s Day trivia for adults and teams: Ireland, legends, luck, Irish words, music, food and the real St. Patrick. Every answer comes with a short explanation.",
         og_title="50 St. Patrick’s Day Trivia Questions and Answers",
         h1="50 St. Patrick’s Day Trivia Questions and Answers", crumb="St. Patrick’s trivia questions",
         eyebrow="For office parties, team events and quiz nights", body=trivia_body, scripts=TRIVIA_JS,
         og=("Trivia with answers", "50 St. Patrick’s Trivia Questions", "Ireland · legends · luck · music")),
    dict(slug="virtual-games-for-work",
         title="Virtual & Hybrid St. Patrick’s Day Games for Work (Free)",
         desc="St. Patrick’s Day games for teams where part of the group joins by video: a free trivia game with a narrator, setup steps for Teams, Zoom and Meet, and more ideas.",
         og_title="St. Patrick’s Day Games for Remote and Hybrid Teams",
         h1="St. Patrick’s Day Games for Remote and Hybrid Teams", crumb="Remote & hybrid teams",
         eyebrow="Office plus video call", body=virtual_body, scripts=COPY_JS,
         og=("Office plus video call", "St. Patrick’s Games for Hybrid Teams", "Teams · Zoom · Google Meet")),
    dict(slug="how-to-host-a-game-night",
         title="How to Host a St. Patrick’s Day Game at Work: Step-by-Step Guide",
         desc="Everything a host needs for an office St. Patrick’s Day game: equipment, teams, a one-hour timeline, prize ideas and quick fixes for common problems.",
         og_title="How to Host a St. Patrick’s Day Game at Work",
         h1="How to Host a St. Patrick’s Day Game at Work", crumb="Host guide",
         eyebrow="A step-by-step guide for the host", body=host_body,
         og=("Step-by-step host guide", "Host a St. Patrick’s Game Night", "Teams · timeline · prizes")),
    dict(slug="faq",
         title="Pot o’ Gold FAQ: Free St. Patrick’s Day Trivia Game",
         desc="Answers about the free St. Patrick’s Day trivia game: how many players, how long it takes, remote coworkers, editing questions and what you need to run it.",
         og_title="Pot o’ Gold: Frequently Asked Questions",
         h1="Frequently Asked Questions", crumb="FAQ",
         eyebrow=NAME, body=faq_body, ld=faq_ld,
         og=("Questions and answers", "Pot o’ Gold FAQ", "Free · no sign-up · 2–4 teams")),
]