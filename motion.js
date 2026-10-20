(function () {
  'use strict';
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  var gsap = window.gsap;
  var region = document.querySelector('.pathways-motion');
  var viewport = document.querySelector('[data-pathways-carousel]');
  if (viewport && window.Swiper) {
    var count = region.querySelector('[data-pathways-count]');
    var progress = region.querySelector('[data-pathway-progress]');
    var pause = region.querySelector('[data-pathways-pause]');
    var paused = reduced.matches;
    var focused = false;
    var inView = !('IntersectionObserver' in window);
    var swiper;
    function sync() {
      if (!swiper) return;
      var active = swiper.realIndex;
      count.textContent = String(active + 1).padStart(2, '0') + ' / 03';
      progress.style.transform = 'scaleX(' + ((active + 1) / 3) + ')';
      pause.setAttribute('aria-label', paused ? 'Play section carousel' : 'Pause section carousel');
      pause.setAttribute('aria-pressed', String(paused));
      pause.textContent = paused ? '▶' : 'Ⅱ';
    }
    function autoplay() {
      if (!swiper) return;
      if (!paused && !focused && inView && !document.hidden) swiper.autoplay.start();
      else swiper.autoplay.stop();
      sync();
    }
    viewport.classList.add('is-ready');
    region.classList.add('is-ready');
    viewport.setAttribute('tabindex', '0');
    swiper = new window.Swiper(viewport, {
      effect: 'slide',
      centeredSlides: false,
      slidesPerView: 1,
      spaceBetween: 24,
      loop: false,
      rewind: true,
      speed: reduced.matches ? 0 : 700,
      grabCursor: true,
      watchSlidesProgress: true,
      preventClicks: true,
      preventClicksPropagation: true,
      breakpoints: { 600: { slidesPerView: 1, spaceBetween: 24 }, 1000: { slidesPerView: 2, spaceBetween: 26 } },
      autoplay: { delay: 3500, disableOnInteraction: false, pauseOnMouseEnter: false },
      navigation: { prevEl: region.querySelector('[data-pathways-prev]'), nextEl: region.querySelector('[data-pathways-next]') },
      pagination: {
        el: region.querySelector('.pathways-pagination'), clickable: true,
        renderBullet: function (index, className) { return '<button type="button" class="' + className + '" aria-label="Show section ' + (index + 1) + '">' + String(index + 1).padStart(2, '0') + '</button>'; }
      },
      a11y: { enabled: true, prevSlideMessage: 'Previous section', nextSlideMessage: 'Next section', paginationBulletMessage: 'Show section {{index}}', slideLabelMessage: 'Section {{index}} of {{slidesLength}}' },
      on: {
        slideChange: function () {
          sync();
          if (gsap && !reduced.matches) {
            var active = this.slides[this.activeIndex];
            if (active) gsap.fromTo(active.querySelectorAll('.pathway-label, h3, .pathway-arrow'), { y: 15, opacity: 0.45 }, { y: 0, opacity: 1, duration: 0.65, stagger: 0.07, ease: 'power3.out', overwrite: true, clearProps: 'transform,opacity' });
          }
        }
      }
    });
    autoplay();
    pause.addEventListener('click', function () { paused = !paused; autoplay(); });
    region.addEventListener('focusin', function () { focused = true; autoplay(); });
    region.addEventListener('focusout', function (event) { focused = region.contains(event.relatedTarget); autoplay(); });
    viewport.addEventListener('keydown', function (event) {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      event.preventDefault();
      if (event.key === 'ArrowRight') swiper.slideNext(); else swiper.slidePrev();
    });
    document.addEventListener('visibilitychange', autoplay);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) { inView = entries[0].isIntersecting; autoplay(); }, { threshold: 0.15 }).observe(region);
    }
    if (reduced.addEventListener) reduced.addEventListener('change', function (event) {
      swiper.params.speed = event.matches ? 0 : 700;
      if (event.matches) paused = true;
      swiper.update();
      autoplay();
    });
  }
  if (!gsap) return;
  var media = gsap.matchMedia();
  media.add('(prefers-reduced-motion: no-preference)', function () {
    if (window.ScrollTrigger) {
      gsap.registerPlugin(window.ScrollTrigger);
      document.querySelectorAll('.pathways-heading, .section-head, .about > div, .taptoe > div, .journal-heading, .extra-card').forEach(function (element) {
        gsap.from(element, { y: 28, autoAlpha: 0, duration: 0.85, ease: 'power3.out', clearProps: 'transform,opacity,visibility', scrollTrigger: { trigger: element, start: 'top 93%', once: true } });
      });
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { window.ScrollTrigger.refresh(); });
      window.addEventListener('load', function () { window.ScrollTrigger.refresh(); }, { once: true });
    }
    var cleanups = [];
    document.querySelectorAll('.pathway-card').forEach(function (card) {
      var image = card.querySelector('img');
      var arrow = card.querySelector('.pathway-arrow');
      var enter = function (event) {
        if (event.pointerType === 'touch') return;
        gsap.to(image, { scale: 1.055, duration: 0.8, ease: 'power3.out', overwrite: true });
        gsap.to(arrow, { rotate: 8, duration: 0.4, ease: 'power2.out', overwrite: true });
      };
      var leave = function () {
        gsap.to(image, { scale: 1, duration: 0.8, ease: 'power3.out', overwrite: true, clearProps: 'transform' });
        gsap.to(arrow, { rotate: 0, duration: 0.4, overwrite: true, clearProps: 'transform' });
      };
      card.addEventListener('pointerenter', enter);
      card.addEventListener('pointerleave', leave);
      cleanups.push(function () { card.removeEventListener('pointerenter', enter); card.removeEventListener('pointerleave', leave); gsap.set([image, arrow], { clearProps: 'transform' }); });
    });
    return function () { cleanups.forEach(function (fn) { fn(); }); };
  });
})();
