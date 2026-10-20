(function () {
  // Mobile menu
  var toggle = document.querySelector('.mobile-toggle');
  var menu = document.querySelector('.menu');
  var setMenu = function (open) {
    menu.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  };
  if (toggle && menu) {
    toggle.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });
    menu.addEventListener('click', function (e) { if (e.target.tagName === 'A') setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  }

  // Header state on scroll
  var header = document.querySelector('.site-header');
  var floatTop = document.querySelector('.float-top');
  var heroImg = document.querySelector('.hero-img img, .page-hero-img img');
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY;
    header && header.classList.toggle('scrolled', y > 20);
    floatTop && floatTop.classList.toggle('show', y > window.innerHeight * 1.2);
    // Subtle parallax on the hero image (desktop only)
    if (heroImg && !still && !ticking) {
      ticking = true;
      requestAnimationFrame(function () {
        heroImg.style.transform = window.innerWidth > 900 && y < 1000 ? 'translateY(' + (y * 0.18).toFixed(1) + 'px) scale(1.04)' : '';
        ticking = false;
      });
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  var progress = document.querySelector('.reading-progress');
  window.addEventListener('scroll', function () {
    var distance = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) progress.style.width = (distance > 0 ? window.scrollY / distance * 100 : 0) + '%';
  }, { passive: true });
  document.querySelectorAll('[data-print]').forEach(function (button) {
    button.addEventListener('click', function () { window.print(); });
  });

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -6% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Blog search
  var posts = document.querySelectorAll('.posts .post:not(.note-row)');
  var notes = document.querySelectorAll('.posts .note-row');
  var search = document.querySelector('#post-search');
  var count = document.querySelector('#post-count');
  var empty = document.querySelector('.empty');
  if (search && posts.length) {
    search.addEventListener('input', function () {
      var q = search.value.trim().toLowerCase();
      var shown = 0;
      posts.forEach(function (p) {
        p.hidden = !!q && p.textContent.toLowerCase().indexOf(q) === -1;
        if (!p.hidden) shown++;
      });
      notes.forEach(function (n) { n.hidden = !!q && n.textContent.toLowerCase().indexOf(q) === -1; });
      if (count) { count.setAttribute('aria-live', 'polite'); count.textContent = shown; }
      if (empty) empty.style.display = shown ? 'none' : 'block';
    });
  }

  // CV: highlight the current section
  var side = document.querySelector('.cv-side');
  var links = document.querySelectorAll('.cv-side a');
  if (links.length && 'IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (l) {
          var on = l.getAttribute('href') === '#' + e.target.id;
          l.classList.toggle('active', on);
          // keep the active tab visible in the mobile tab bar
          if (on && side.scrollWidth > side.clientWidth) side.scrollTo({ left: l.offsetLeft - 16, behavior: 'smooth' });
        });
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    document.querySelectorAll('.cv-section').forEach(function (s) { spy.observe(s); });
  }

  // Lightbox for covers
  var zooms = document.querySelectorAll('[data-lightbox]');
  if (zooms.length) {
    var box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Image preview');
    box.setAttribute('aria-hidden', 'true');
    box.innerHTML = '<button type="button" aria-label="Close">×</button>';
    document.body.appendChild(box);
    var img = document.createElement('img');
    var last;
    var close = function () { box.classList.remove('open'); box.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; if (last) last.focus(); };
    zooms.forEach(function (z) {
      z.addEventListener('click', function (e) {
        e.preventDefault();
        last = z;
        img.src = z.getAttribute('href');
        if (!img.parentNode) box.appendChild(img);
        img.alt = (z.querySelector('img') || {}).alt || '';
        box.classList.add('open');
        box.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        box.querySelector('button').focus();
      });
    });
    box.addEventListener('click', function (e) { if (e.target !== img) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && box.classList.contains('open')) close(); });
    box.addEventListener('keydown', function (e) { if (e.key === 'Tab') { e.preventDefault(); box.querySelector('button').focus(); } });
  }
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Tab' || !menu || !menu.classList.contains('open')) return;
    var first = menu.querySelector('a');
    var lastLink = toggle;
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); lastLink.focus(); }
    else if (!e.shiftKey && document.activeElement === lastLink) { e.preventDefault(); first.focus(); }
  });
})();
