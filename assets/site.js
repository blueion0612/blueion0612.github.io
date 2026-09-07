/* Yuhyeon Lee — portfolio: the day/night toggle.
   The theme is read before paint by the inline script in <head>; this file only
   wires the button. */
(function () {
  var tg = document.querySelector('.theme-toggle');
  if (!tg) return;
  var mt = document.querySelector('meta[name="theme-color"]');
  function apply(day, remember) {
    if (day) { document.documentElement.setAttribute('data-theme', 'day'); }
    else { document.documentElement.removeAttribute('data-theme'); }
    tg.textContent = day ? '☾' : '☀';
    tg.setAttribute('aria-label', day ? 'Switch to night mode' : 'Switch to day mode');
    if (mt) { mt.setAttribute('content', day ? '#e8dcc2' : '#0c0d0b'); }
    if (remember) {
      try { localStorage.setItem('theme', day ? 'day' : 'night'); } catch (e) {}
    }
  }
  apply(document.documentElement.hasAttribute('data-theme'), false);
  tg.addEventListener('click', function () {
    apply(!document.documentElement.hasAttribute('data-theme'), true);
  });
})();
