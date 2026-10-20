"""Add a cinematic homepage carousel and image-led discovery section."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'src/pages/index.html'
text=p.read_text(encoding='utf-8')
hero='''<section class="showcase" aria-label="Featured philosophy, publications and podcasts" aria-roledescription="carousel" tabindex="0" data-carousel>
  <div class="showcase-stage">
    <article class="showcase-slide is-active" data-slide role="group" aria-roledescription="slide" aria-label="1 of 3" aria-hidden="false">
      <picture class="showcase-image"><source srcset="assets/img/hero-home.webp" type="image/webp"><img src="assets/img/hero-home.jpg" alt="Classical stone arcade with a stone sphere overlooking a valley" width="2000" height="1333" fetchpriority="high" decoding="async"></picture>
      <div class="wrap showcase-content"><div class="showcase-kicker">Alan White <span></span> Philosophy</div><h1 id="home-title">Structural-<br>Systematic<br><em>Philosophy</em></h1><p class="showcase-description">Mark Hopkins Professor of Philosophy, Williams College</p><div class="showcase-actions"><a class="showcase-primary" href="publications.html">Explore publications <span aria-hidden="true">↗</span></a><a class="showcase-secondary" href="blog.html">Posts &amp; papers <span aria-hidden="true">→</span></a></div></div>
    </article>
    <article class="showcase-slide" data-slide role="group" aria-roledescription="slide" aria-label="2 of 3" aria-hidden="true" inert>
      <picture class="showcase-image"><source srcset="assets/img/hero-publications.webp" type="image/webp"><img src="assets/img/hero-publications.jpg" alt="Antique books beside a stone sphere" width="2000" height="1333" decoding="async"></picture>
      <div class="wrap showcase-content"><div class="showcase-kicker">Alan White <span></span> Publications</div><h2>Toward a Philosophical<br><em>Theory of Everything</em></h2><p class="showcase-description showcase-sentence">Contributions to the Structural-Systematic Philosophy. Bloomsbury (formerly Continuum), 2014.</p><div class="showcase-actions"><a class="showcase-primary" href="publications.html">Discover the books <span aria-hidden="true">↗</span></a><a class="showcase-secondary" href="#taptoe-feature">Explore TAPTOE <span aria-hidden="true">→</span></a></div></div>
    </article>
    <article class="showcase-slide" data-slide role="group" aria-roledescription="slide" aria-label="3 of 3" aria-hidden="true" inert>
      <picture class="showcase-image"><source srcset="assets/img/hero-podcasts.webp" type="image/webp"><img src="assets/img/hero-podcasts.jpg" alt="Vintage microphone beside antique books" width="2000" height="1333" decoding="async"></picture>
      <div class="wrap showcase-content"><div class="showcase-kicker">Listen &amp; explore <span></span> Podcasts</div><h2>The Structural-<br>Systematic<br><em>Philosophy</em></h2><p class="showcase-description showcase-sentence">My podcasts are available on a number of sites, including those listed below.</p><div class="showcase-actions"><a class="showcase-primary" href="podcasts.html">Listen to the podcasts <span aria-hidden="true">↗</span></a><a class="showcase-secondary" href="recent-posts.html">Recent essays <span aria-hidden="true">→</span></a></div></div>
    </article>
  </div>
  <div class="showcase-bottom wrap">
    <a class="showcase-scroll" href="#explore-title"><span aria-hidden="true">↓</span> Explore the work</a>
    <div class="showcase-pagination" role="group" aria-label="Choose featured slide"><button type="button" class="showcase-tab is-active" data-slide-to="0" aria-label="Show slide 1: Structural-Systematic Philosophy" aria-pressed="true"><span>01</span><span class="showcase-track" aria-hidden="true"><i></i></span></button><button type="button" class="showcase-tab" data-slide-to="1" aria-label="Show slide 2: Publications" aria-pressed="false"><span>02</span><span class="showcase-track" aria-hidden="true"><i></i></span></button><button type="button" class="showcase-tab" data-slide-to="2" aria-label="Show slide 3: Podcasts" aria-pressed="false"><span>03</span><span class="showcase-track" aria-hidden="true"><i></i></span></button></div>
    <div class="showcase-controls"><button type="button" data-slide-prev aria-label="Previous slide">←</button><button type="button" data-slide-pause aria-label="Pause slideshow" aria-pressed="false"><span data-pause-icon aria-hidden="true">Ⅱ</span></button><button type="button" data-slide-next aria-label="Next slide">→</button></div>
  </div>
  <p class="sr-only" data-slide-status aria-live="polite" aria-atomic="true"></p>
</section>'''
text=re.sub(r'<section class="hero home-hero".*?</section>',hero,text,count=1,flags=re.S)
paths='''<section class="pathways-section" aria-labelledby="explore-title"><div class="wrap">
  <div class="pathways-heading"><div><div class="eyebrow rule">Explore the work</div><h2 id="explore-title">Ways into the <em>philosophy</em></h2></div><p>Reading · Research · Listening</p></div>
  <div class="pathways-grid">
    <a class="pathway-card" href="blog.html"><div class="pathway-image"><img src="assets/img/thumb-bust.jpg" alt="" width="600" height="600" loading="lazy"><span class="pathway-number">01 / READ</span></div><div class="pathway-copy"><div><span class="pathway-label">Blog</span><h3>Posts &amp; papers</h3></div><span class="pathway-arrow" aria-hidden="true">↗</span></div></a>
    <a class="pathway-card" href="publications.html"><div class="pathway-image"><img src="assets/img/thumb-books.jpg" alt="" width="600" height="600" loading="lazy"><span class="pathway-number">02 / RESEARCH</span></div><div class="pathway-copy"><div><span class="pathway-label">Selected publications</span><h3>Books &amp; publications</h3></div><span class="pathway-arrow" aria-hidden="true">↗</span></div></a>
    <a class="pathway-card" href="podcasts.html"><div class="pathway-image"><img src="assets/img/thumb-mic.jpg" alt="" width="600" height="600" loading="lazy"><span class="pathway-number">03 / LISTEN</span></div><div class="pathway-copy"><div><span class="pathway-label">Podcasts</span><h3>The philosophy, in conversation</h3></div><span class="pathway-arrow" aria-hidden="true">↗</span></div></a>
  </div>
</div></section>'''
text=re.sub(r'<section class="explore-section".*?</section>',paths,text,count=1,flags=re.S)
text=text.replace('<div class="wrap taptoe">','<div class="wrap taptoe" id="taptoe-feature">')
p.write_text(text,encoding='utf-8')
print('Homepage: three-slide cinematic hero and three image-led discovery cards.')
