"""Shared bits for every page of Victoria's Game Nights (not used by the artifact or the offline file).

Site settings live here, so the domain or the Analytics ID change in one place.
"""

URL = "https://victoriasgamenights.com/"   # TODO: the domain Victoria buys (with the trailing slash)
HOST = URL.split("/")[2]
BRAND = "Victoria’s Game Nights"
GA_ID = "G-JL1KBEZPQX"                      # the Night of Frights GA4 property, reused for the whole site
MIRROR_BASE = "/game-nights-play"           # the no-redirect copy on github.io (repo still to be created)

# Consent Mode v2: no ads storage anywhere. Analytics cookies are off by default in the EEA, the UK,
# Switzerland and Quebec (Google then receives cookieless pings only); elsewhere analytics is on.
_STRICT = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT",
           "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE", "IS", "LI", "NO", "GB", "CH", "CA-QC"]

GA_HEAD = '' if not GA_ID else f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('consent', 'default', {{ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied', analytics_storage:'denied', region:{_STRICT!r}}});
gtag('consent', 'default', {{ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied', analytics_storage:'granted'}});
gtag('js', new Date());
gtag('config', '{GA_ID}', {{allow_google_signals:false, allow_ad_personalization_signals:false}});
</script>'''

# Game events, read from the game's own state after each screen change. Only numbers and fixed labels
# are sent: never team names, answers or anything typed in the editor.
def game_events_js(game):
    return ('''<script>
(function(){
  if (typeof gtag !== 'function') return;
  var app = document.getElementById('app'), last = '', fired = {};
  var store = { get: function(k){ try { return sessionStorage.getItem(k); } catch(e){ return null; } },
                set: function(k,v){ try { sessionStorage.setItem(k,v); } catch(e){} } };
  try { fired = JSON.parse(store.get('__KEY__') || '{}'); } catch(e){ fired = {}; }
  var once = function(name, params){ if (fired[name]) return; fired[name] = 1; store.set('__KEY__', JSON.stringify(fired)); gtag('event', name, params || {}); };
  var check = function(){
    var s; try { s = S; } catch(e){ return; }
    if (!s) return;
    var key = s.screen + '|' + s.round + '|' + (s.deck || '') + '|' + (s.q ? s.q.c + '-' + s.q.i + '-' + s.round : '');
    if (key === last) return;
    var prev = last; last = key;
    var teams = s.teamCount;
    if (s.screen === 'rules' && s.deck === 'intro' && prev.indexOf('setup') === 0){
      fired = {}; store.set('__KEY__', '{}');
      once('game_start', { team_count: teams });
    }
    if (s.screen === 'board' && s.round === 1) once('round_two', { team_count: teams });
    if (s.screen === 'final') once('final_round', { team_count: teams });
    if (s.screen === 'tiebreak') once('tiebreaker', { team_count: teams });
    if (s.screen === 'podium') once('game_complete', { team_count: teams });
    if (s.screen === 'board' && s.q && prev.split('|')[3] !== key.split('|')[3]){
      gtag('event', 'question_open', { round: s.round + 1, value: s.q.value, special: (__SPECIALS__)[s.q.special] || 'none' });
    }
  };
  new MutationObserver(check).observe(app, { childList: true });
  document.addEventListener('click', function(e){
    var b = e.target.closest && e.target.closest('[data-act]'); if (!b) return;
    var act = b.getAttribute('data-act');
    if (act === 'edit') gtag('event', 'open_question_editor');
    if (act === 'voice') gtag('event', 'open_voice_settings');
    if (act === 'edone') gtag('event', 'questions_edited');
  }, true);
  check();
})();
</script>''').replace('__KEY__', game['slug'] + '-ga').replace('__SPECIALS__', __import__('json').dumps(game['specials']))

# Content pages: clicks that lead into the game, printing and copying.
PAGE_EVENTS_JS = '''<script>
(function(){
  if (typeof gtag !== 'function') return;
  var page = location.pathname.replace(/^\\/|\\/$/g, '').replace(/\\//g, '-') || 'home';
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[data-play]');
    if (a) gtag('event', 'play_click', { from_page: page, link_text: (a.textContent || '').trim().slice(0, 40) });
    var p = e.target.closest && e.target.closest('[data-print]');
    if (p) gtag('event', 'print_questions', { with_answers: p.getAttribute('data-print') === 'answers' ? 'yes' : 'no' });
    if (e.target.closest && e.target.closest('[data-toggle-all]')) gtag('event', 'show_all_answers');
    if (e.target.closest && e.target.closest('[data-copy]')) gtag('event', 'copy_invite');
    var s = e.target.closest && e.target.closest('summary');
    if (s && s.parentElement && !s.parentElement.open) gtag('event', 'show_answer', { question: (s.closest('li') || {}).id || '' });
  }, true);
})();
</script>'''

# Phones: the big-screen board layout (one screen tall, min 640px wide) does not fit a phone, so on small screens the
# board becomes a normal scrolling page with a compact scoreboard and a 5-column grid that fits the width.
MOBILE_CSS = '''<style id="nof-mobile">
@media (max-width:700px), (max-height:520px) and (orientation:landscape){
  .board-screen{height:auto;min-height:0;gap:10px}
  .board-screen .board-wrap{flex:none;overflow:visible}
  .board-screen .board,.board{min-width:0;height:auto;grid-template-rows:auto;gap:6px}
  .board-screen .cell{aspect-ratio:16/10;min-height:0}
  .board-screen .topbar{gap:8px 12px}
  .board-screen .tools{gap:6px}
  .board-screen .tools .btn{font-size:.8rem;padding:.4em .8em}
}
@media (max-width:700px){
  #app{padding-block:12px 28px}
  .board-screen .round-name{font-size:1.9rem}
  .board-screen .scores{grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}
  .board-screen .team{padding:6px 8px;gap:2px 6px;border-radius:8px}
  .board-screen .team .tname{font-size:.88rem;line-height:1.15}
  .board-screen .team .tag{font-size:.6rem;letter-spacing:.08em}
  .board-screen .team .score{font-size:1.45rem}
  .board-screen .team .adj{gap:4px}
  .board-screen .team .adj button{width:30px;height:24px}
  .board-screen .board{gap:5px}
  .board-screen .cat{font-size:.58rem;letter-spacing:.02em;padding:4px 1px 6px;min-height:42px;line-height:1.15;
    overflow-wrap:anywhere;hyphens:auto;border-bottom-width:2px}
  .board-screen .cell{aspect-ratio:1/1;font-size:1.05rem;border-radius:8px}
  .board-screen .board-foot{font-size:.82rem;gap:8px}
  .board-screen .board-foot .btn{font-size:.82rem;padding:.4em .85em}
  .reels{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
  .reel{padding:12px 8px;gap:8px;border-radius:12px}
  .reel-label{font-size:.6rem;letter-spacing:.08em}
  .reel-face{font-size:2.6rem}
  .reel-face.teamname{font-size:1.5rem}
  .reel .btn{font-size:.8rem;padding:.4em .8em}
  .howto{gap:8px}
  .howto li{padding:10px 12px;font-size:.95rem}
  .qhead .val{font-size:1.6rem}
  .cat-team{font-size:2rem}
}
@media (max-height:520px) and (orientation:landscape) and (min-width:701px){
  #app{padding-block:8px 16px}
  .board-screen{gap:6px}
  .board-screen .round-name{font-size:1.5rem}
  .board-screen .team{padding:4px 10px}
  .board-screen .team .score{font-size:1.3rem}
  .board-screen .team .adj button{height:22px}
  .board-screen .cat{min-height:0;padding:2px 4px 4px;font-size:.66rem}
  .board-screen .cell{aspect-ratio:auto;height:46px;font-size:1.25rem}
  .board-screen .board{gap:5px}
  .board-screen .board-foot{font-size:.8rem}
}
@media (max-width:380px){
  .board-screen .cat{font-size:.52rem}
  .board-screen .cell{font-size:.95rem}
  .reel-face{font-size:2.2rem}
}
</style>'''
