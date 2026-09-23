/* Yuhyeon Lee — portfolio: the day/night toggle.
   The theme is read before paint by the inline script in <head>; this file only
   wires the button. */
(function () {
  var tg = document.querySelector('.theme-toggle');
  if (!tg) return;
  var mt = document.querySelector('meta[name="theme-color"]');
  // Themed images are <picture>s whose dark <source> follows the system scheme until
  // this runs; pin every one to the theme on screen so only that palette is fetched.
  function pictures(day) {
    document.querySelectorAll('source[data-dark]').forEach(function (s) {
      s.media = day ? 'not all' : 'all';
    });
  }
  // print always uses the paper palette
  window.addEventListener('beforeprint', function () { pictures(true); });
  window.addEventListener('afterprint', function () {
    pictures(document.documentElement.hasAttribute('data-theme'));
  });
  function apply(day, remember) {
    if (day) { document.documentElement.setAttribute('data-theme', 'day'); }
    else { document.documentElement.removeAttribute('data-theme'); }
    tg.textContent = day ? '☾' : '☀';
    tg.setAttribute('aria-label', day ? 'Switch to night mode' : 'Switch to day mode');
    if (mt) { mt.setAttribute('content', day ? '#e8dcc2' : '#0c0d0b'); }
    pictures(day);
    if (remember) {
      try { localStorage.setItem('theme', day ? 'day' : 'night'); } catch (e) {}
    }
  }
  apply(document.documentElement.hasAttribute('data-theme'), false);
  tg.addEventListener('click', function () {
    apply(!document.documentElement.hasAttribute('data-theme'), true);
  });
})();

(function () {
  // the narrow-screen section menu: close it once a section is chosen, on Escape, and
  // on a tap anywhere outside it
  var menu = document.querySelector('.nav-menu');
  if (!menu) return;
  menu.addEventListener('click', function (ev) {
    if (ev.target.closest('.nav-menu-panel a')) { menu.open = false; }
  });
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape' && menu.open) {
      menu.open = false;
      menu.querySelector('summary').focus();
    }
  });
  document.addEventListener('click', function (ev) {
    if (menu.open && !menu.contains(ev.target)) { menu.open = false; }
  });
})();
