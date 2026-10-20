(function () {
  'use strict';
  var carousel = document.querySelector('[data-carousel]');
  if (!carousel) return;
  var slides = Array.from(carousel.querySelectorAll('[data-slide]'));
  var tabs = Array.from(carousel.querySelectorAll('[data-slide-to]'));
  var previous = carousel.querySelector('[data-slide-prev]');
  var next = carousel.querySelector('[data-slide-next]');
  var pause = carousel.querySelector('[data-slide-pause]');
  var icon = carousel.querySelector('[data-pause-icon]');
  var status = carousel.querySelector('[data-slide-status]');
  var motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var current = 0;
  var timer;
  var userPaused = motion.matches;
  var hovered = false;
  var focused = false;
  var inView = true;
  var touchStart;
  var duration = 7500;
  if (slides.length < 2) return;
  carousel.classList.add('is-ready');

  function schedule() {
    window.clearTimeout(timer);
    timer = undefined;
    var running = !userPaused && !hovered && !focused && inView && !document.hidden;
    carousel.classList.toggle('is-running', running);
    pause.setAttribute('aria-label', userPaused ? 'Play slideshow' : 'Pause slideshow');
    pause.setAttribute('aria-pressed', String(userPaused));
    icon.textContent = userPaused ? '▶' : 'Ⅱ';
    if (running) timer = window.setTimeout(function () { show(current + 1, false); }, duration);
  }
  function show(index, manual) {
    current = (index + slides.length) % slides.length;
    slides.forEach(function (slide, i) {
      var active = i === current;
      slide.classList.toggle('is-active', active);
      slide.setAttribute('aria-hidden', String(!active));
      slide.inert = !active;
    });
    tabs.forEach(function (tab, i) {
      tab.classList.toggle('is-active', i === current);
      tab.setAttribute('aria-pressed', String(i === current));
    });
    if (manual && status) {
      var name = tabs[current].getAttribute('aria-label').replace(/^Show slide \d+: /, '');
      status.textContent = 'Slide ' + (current + 1) + ' of ' + slides.length + ': ' + name;
    }
    schedule();
  }
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () { show(Number(tab.getAttribute('data-slide-to')), true); });
  });
  previous.addEventListener('click', function () { show(current - 1, true); });
  next.addEventListener('click', function () { show(current + 1, true); });
  pause.addEventListener('click', function () { userPaused = !userPaused; schedule(); });
  carousel.addEventListener('mouseenter', function () { hovered = true; schedule(); });
  carousel.addEventListener('mouseleave', function () { hovered = false; schedule(); });
  carousel.addEventListener('focusin', function () { focused = true; schedule(); });
  carousel.addEventListener('focusout', function (event) {
    focused = carousel.contains(event.relatedTarget);
    schedule();
  });
  carousel.addEventListener('keydown', function (event) {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    show(current + (event.key === 'ArrowRight' ? 1 : -1), true);
  });
  carousel.addEventListener('touchstart', function (event) {
    touchStart = event.touches.length === 1 && !event.target.closest('a, button') ? { x: event.touches[0].clientX, y: event.touches[0].clientY } : null;
  }, { passive: true });
  carousel.addEventListener('touchend', function (event) {
    if (!touchStart || !event.changedTouches.length) return;
    var dx = event.changedTouches[0].clientX - touchStart.x;
    var dy = event.changedTouches[0].clientY - touchStart.y;
    touchStart = null;
    if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.4) show(current + (dx < 0 ? 1 : -1), true);
  }, { passive: true });
  carousel.addEventListener('touchcancel', function () { touchStart = null; }, { passive: true });
  document.addEventListener('visibilitychange', schedule);
  if (motion.addEventListener) motion.addEventListener('change', function (event) { if (event.matches) userPaused = true; schedule(); });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      inView = entries[0].isIntersecting;
      schedule();
    }, { threshold: 0.15 }).observe(carousel);
  }
  show(0, false);
})();
