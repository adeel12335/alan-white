(function () {
  // Mobile menu
  var toggle = document.querySelector('.mobile-toggle');
  var menu = document.querySelector('.menu');
  var setMenu = function (open) {
    menu.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
    document.querySelectorAll('main, .footer, .float-top').forEach(function (el) { el.inert = open; });
  };
  if (toggle && menu) {
    toggle.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && menu.classList.contains('open')) { setMenu(false); toggle.focus(); } });
    window.addEventListener('resize', function () { if (window.innerWidth > 900 && menu.classList.contains('open')) setMenu(false); });
  }

  // Header state on scroll
  var header = document.querySelector('.site-header');
  var floatTop = document.querySelector('.float-top');
  var onScroll = function () {
    var y = window.scrollY;
    header && header.classList.toggle('scrolled', y > 20);
    floatTop && floatTop.classList.toggle('show', y > window.innerHeight * 1.2);
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
  var topicButtons = document.querySelectorAll('[data-topic]');
  var selectedTopic = 'all';
  if (search && posts.length) {
    var filterPosts = function () {
      var q = search.value.trim().toLowerCase();
      var shown = 0;
      var notesShown = 0;
      var matchesTopic = function (text) {
        if (selectedTopic === 'all') return true;
        if (selectedTopic === 'ssp') return /ssp|philosophy professors|puntel/.test(text);
        return text.indexOf(selectedTopic) !== -1;
      };
      posts.forEach(function (p) {
        var text = p.querySelector('h2').textContent.toLowerCase();
        p.hidden = (q && text.indexOf(q) === -1) || !matchesTopic(text);
        if (!p.hidden) shown++;
      });
      notes.forEach(function (n) {
        var text = n.textContent.toLowerCase();
        n.hidden = (q && text.indexOf(q) === -1) || !matchesTopic(text);
        if (!n.hidden) notesShown++;
      });
      if (count) { count.setAttribute('aria-live', 'polite'); count.textContent = shown; }
      if (empty) empty.style.display = shown + notesShown ? 'none' : 'block';
    };
    search.addEventListener('input', filterPosts);
    topicButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        selectedTopic = button.getAttribute('data-topic');
        topicButtons.forEach(function (b) {
          var active = b === button;
          b.classList.toggle('active', active);
          b.setAttribute('aria-pressed', String(active));
        });
        filterPosts();
      });
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
