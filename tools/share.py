"""Share and Bookmark buttons for the site (home page, content pages, a game's start screen).

Share: on phones and tablets it opens the system share sheet (navigator.share). On computers it opens a small menu:
copy link, email, WhatsApp, LinkedIn, Facebook, X, Pinterest, plus "More options" (the system dialog) where the
browser has one. The menu items are plain links: no social-network scripts, no third-party cookies.

Bookmark: browsers do not let a page create a bookmark, so the button shows how to do it on this device
(Ctrl+D / Cmd+D on a computer, the browser menu on a phone) and offers to send the link to yourself.

GA events: share_click {method, from_page, target}, bookmark_click {device, from_page}.
"""
import html

e = lambda s: html.escape(s, quote=True)

SITE_TEXT = "Quiz games for office parties and team events, with a narrator and a game-show board on the big screen."


def buttons(url, title, text, image, share_label="Share", save_label="Bookmark", target="site", cls="btn"):
    """The two buttons. url/title/text/image describe what is shared; target is a GA label ("site" or the game slug)."""
    data = f'data-url="{e(url)}" data-title="{e(title)}" data-text="{e(text)}" data-img="{e(image)}" data-target="{e(target)}"'
    icon_share = ('<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" '
                  'stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/>'
                  '<path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg>')
    icon_save = ('<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" '
                 'stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12v18l-6-4.5L6 21z"/></svg>')
    return (f'<span class="gn-share"><button type="button" class="{cls}" data-gn-share {data} aria-haspopup="true" aria-expanded="false">{icon_share}{e(share_label)}</button>'
            f'<button type="button" class="{cls}" data-gn-save {data} aria-haspopup="true" aria-expanded="false">{icon_save}{e(save_label)}</button></span>')


CSS = '''<style>
.gn-share{position:relative;display:inline-flex;flex-wrap:wrap;gap:10px}
.gn-share button{cursor:pointer;font-size:inherit}
.gn-share button svg{flex:none}
.gn-pop{position:absolute;z-index:20;top:calc(100% + 8px);left:0;width:max-content;max-width:min(320px,calc(100vw - 32px));
  background:var(--dusk,#1b1626);color:var(--bone,#f2e9d8);border:1px solid var(--line,#3a3248);border-radius:14px;
  box-shadow:0 14px 40px rgba(0,0,0,.45);padding:10px;font-family:var(--f-ui,"Alegreya Sans",system-ui,sans-serif);
  font-size:1rem;line-height:1.4;text-align:left}
.gn-pop a,.gn-pop button{display:flex;align-items:center;gap:10px;width:100%;padding:8px 10px;border:0;border-radius:8px;background:none;
  color:inherit;font:inherit;font-weight:700;text-decoration:none;cursor:pointer;text-align:left}
.gn-pop a:hover,.gn-pop button:hover,.gn-pop a:focus-visible,.gn-pop button:focus-visible{background:rgba(255,255,255,.08);color:var(--ember,#ffd58a)}
.gn-pop p{margin:4px 10px 10px;font-weight:400}
.gn-pop kbd{display:inline-block;min-width:1.6em;padding:1px 7px;border:1px solid var(--line,#3a3248);border-bottom-width:3px;border-radius:6px;
  font:700 .95em var(--f-ui,system-ui,sans-serif);color:var(--ember,#ffd58a);text-align:center}
.gn-pop .gn-note{font-size:.88rem;color:var(--ash,#ab9fbd)}
@media print{.gn-share,.gn-pop{display:none!important}}
</style>'''

JS = '''<script>
(function(){
  var page = location.pathname.replace(/^\\/|\\/$/g, '').replace(/\\//g, '-') || 'home';
  var ga = function(name, params){ if (typeof gtag === 'function') gtag('event', name, params); };
  var touch = window.matchMedia && matchMedia('(pointer: coarse)').matches;
  var ua = navigator.userAgent, ios = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  var android = /Android/.test(ua), mac = /Mac/.test(navigator.platform || ua) && !ios;
  var open = null;
  var esc = function(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
  var close = function(){ if (!open) return; open.pop.remove(); open.btn.setAttribute('aria-expanded', 'false'); var b = open.btn; open = null; return b; };
  var info = function(b){ return { url: b.getAttribute('data-url'), title: b.getAttribute('data-title'), text: b.getAttribute('data-text'),
                                  img: b.getAttribute('data-img'), target: b.getAttribute('data-target') }; };
  var show = function(btn, html){
    close();
    var vw = document.documentElement.clientWidth, vh = document.documentElement.clientHeight;   // before the menu exists: on phones it would widen the page
    var pop = document.createElement('div'); pop.className = 'gn-pop'; pop.setAttribute('role', 'dialog'); pop.innerHTML = html;
    btn.parentNode.appendChild(pop);
    pop.style.left = (btn.offsetLeft) + 'px';
    var r = pop.getBoundingClientRect();
    if (r.right > vw - 12) pop.style.left = Math.max(btn.offsetLeft - (r.right - vw + 12), -btn.parentNode.getBoundingClientRect().left + 12) + 'px';
    var br = btn.getBoundingClientRect();
    if (r.bottom > vh - 8 && br.top - 8 > r.height){ pop.style.top = 'auto'; pop.style.bottom = 'calc(100% + 8px)'; }   // no room below: open upwards
    btn.setAttribute('aria-expanded', 'true'); open = { btn: btn, pop: pop };
    var first = pop.querySelector('a,button'); if (first) first.focus();
    return pop;
  };
  var system = function(d, from){
    return navigator.share({ title: d.title, text: d.text, url: d.url }).then(function(){ ga('share_click', { method: 'system', from_page: page, target: d.target }); },
      function(err){ if (!err || err.name !== 'AbortError') { if (from) menu(from, d, true); } });
  };
  var copy = function(text, el){
    var done = function(){ el.textContent = 'Link copied'; setTimeout(close, 1200); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function(){ prompt('Copy this link:', text); });
    else prompt('Copy this link:', text);
  };
  var menu = function(btn, d, noSystem){
    var u = encodeURIComponent(d.url), t = encodeURIComponent(d.title), x = encodeURIComponent(d.text);
    var items = [
      ['copy', 'Copy link', null],
      ['email', 'Email', 'mailto:?subject=' + t + '&body=' + x + '%0A%0A' + u],
      ['whatsapp', 'WhatsApp', 'https://wa.me/?text=' + t + '%20' + u],
      ['linkedin', 'LinkedIn', 'https://www.linkedin.com/sharing/share-offsite/?url=' + u],
      ['facebook', 'Facebook', 'https://www.facebook.com/sharer/sharer.php?u=' + u],
      ['x', 'X (Twitter)', 'https://x.com/intent/tweet?text=' + t + '&url=' + u],
      ['pinterest', 'Pinterest', 'https://www.pinterest.com/pin/create/button/?url=' + u + '&media=' + encodeURIComponent(d.img) + '&description=' + t]
    ];
    if (navigator.share && !noSystem) items.push(['system', 'More options…', null]);
    var html = items.map(function(it){
      return it[2] ? '<a href="' + esc(it[2]) + '" data-m="' + it[0] + '"' + (it[0] === 'email' ? '' : ' target="_blank" rel="noopener"') + '>' + it[1] + '</a>'
                   : '<button type="button" data-m="' + it[0] + '">' + it[1] + '</button>';
    }).join('');
    var pop = show(btn, html);
    pop.addEventListener('click', function(ev){
      var el = ev.target.closest('[data-m]'); if (!el) return;
      var m = el.getAttribute('data-m');
      if (m === 'copy'){ ev.preventDefault(); copy(d.url, el); ga('share_click', { method: 'copy', from_page: page, target: d.target }); return; }
      if (m === 'system'){ ev.preventDefault(); close(); system(d, null); return; }
      ga('share_click', { method: m, from_page: page, target: d.target });
      setTimeout(close, 50);
    });
  };
  var bookmark = function(btn, d){
    var device = ios ? 'ios' : android ? 'android' : touch ? 'touch' : mac ? 'mac' : 'computer';
    var how = ios ? '<p>In Safari, tap the <b>Share</b> button, then <b>Add Bookmark</b> or <b>Add to Home Screen</b>.</p>'
      : android ? '<p>Tap the browser menu <b>⋮</b>, then the <b>☆</b> star to bookmark, or <b>Add to Home screen</b>.</p>'
      : touch ? '<p>Open the browser menu and choose <b>Bookmark</b> or <b>Add to Home Screen</b>.</p>'
      : '<p>Press ' + (mac ? '<kbd>⌘</kbd> + <kbd>D</kbd>' : '<kbd>Ctrl</kbd> + <kbd>D</kbd>') + ' to bookmark this page.</p>';
    var send = (touch && navigator.share) ? '<button type="button" data-m="send">Send the link to myself</button>'
      : '<a data-m="send" href="mailto:?subject=' + encodeURIComponent(d.title) + '&body=' + encodeURIComponent(d.text + '\\n\\n' + d.url) + '">Email the link to myself</a>';
    var pop = show(btn, how + send + '<p class="gn-note">Handy for opening the game later on the computer connected to the big screen.</p>');
    ga('bookmark_click', { device: device, from_page: page });
    pop.addEventListener('click', function(ev){
      var el = ev.target.closest('[data-m="send"]'); if (!el) return;
      if (el.tagName === 'BUTTON'){ ev.preventDefault(); close(); system(d, null); }
      else setTimeout(close, 50);
    });
  };
  document.addEventListener('click', function(ev){
    var b = ev.target.closest && ev.target.closest('[data-gn-share],[data-gn-save]');
    if (!b){ if (open && !open.pop.contains(ev.target)) close(); return; }
    if (open && open.btn === b){ close(); return; }
    var d = info(b);
    if (b.hasAttribute('data-gn-share')){
      if (touch && navigator.share){ close(); system(d, b); } else menu(b, d);
    } else bookmark(b, d);
  });
  document.addEventListener('keydown', function(ev){ if (ev.key === 'Escape' && open){ var b = close(); if (b) b.focus(); } });
})();
</script>'''

WIDGET = CSS + "\n" + JS
