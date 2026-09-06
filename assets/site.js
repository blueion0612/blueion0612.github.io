/* Yuhyeon Lee — portfolio: scroll reveal and the day/night toggle.
   The theme is read before paint by the inline script in <head>; this file only
   wires the button and the observer. */
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
})();

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
