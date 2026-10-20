"""Reshape presentation without removing original paragraphs or resources."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent.parent
PAGES=ROOT/'src/pages'
home=(PAGES/'index.html').read_text(encoding='utf-8')
old=re.search(r'<section class="hero">.*?</section>',home,re.S)
if old:
    hero='''<section class="hero home-hero" aria-labelledby="home-title">
  <div class="wrap hero-layout">
    <div class="hero-copy">
      <div class="eyebrow">Alan White <span class="hero-tiny-rule" aria-hidden="true"></span> Philosophy</div>
      <h1 id="home-title"><span>Structural-</span><span>Systematic</span><em>Philosophy</em></h1>
      <p class="lead">Mark Hopkins Professor of Philosophy, Williams College</p>
      <div class="hero-actions"><a class="button" href="publications.html">Explore publications <span class="arr" aria-hidden="true">↗</span></a><a class="hero-secondary" href="blog.html">Posts &amp; papers <span aria-hidden="true">→</span></a></div>
      <a class="hero-bottom" href="#about"><span class="hero-scroll-icon" aria-hidden="true">↓</span> The philosopher &amp; the project</a>
    </div>
    <figure class="hero-art">
      <!--hero:hero-home|Classical stone arcade with a stone sphere overlooking a valley|hero-img-->
      <figcaption><span>Structural-Systematic Philosophy</span><span aria-hidden="true">01 — ∞</span></figcaption>
    </figure>
  </div>
</section>'''
    home=home[:old.start()]+hero+home[old.end():]
    (PAGES/'index.html').write_text(home,encoding='utf-8')

blog=(PAGES/'blog.html').read_text(encoding='utf-8')
if 'topic-filters' not in blog:
    blog=blog.replace('<div class="toolbar">','''<div class="journal-heading"><div><div class="eyebrow">The reading room</div><h2>Posts &amp; papers</h2></div><a class="text-link" href="recent-posts.html">Recent essays <span aria-hidden="true">↗</span></a></div>
    <div class="topic-filters" role="group" aria-label="Filter posts by topic"><button class="topic-filter active" data-topic="all" aria-pressed="true" type="button">All papers</button><button class="topic-filter" data-topic="being" aria-pressed="false" type="button">Being</button><button class="topic-filter" data-topic="ssp" aria-pressed="false" type="button">SSP</button><button class="topic-filter" data-topic="corrigenda" aria-pressed="false" type="button">Corrigenda</button></div>
    <div class="toolbar">''')
    blog=blog.replace('<span id="post-count">','<span id="post-count" role="status" aria-live="polite">')
    blog=blog.replace('>Read <span class="arr">','>Read paper <span class="arr">')
    blog=blog.replace('<p class="empty">','<p class="empty" role="status">')
    (PAGES/'blog.html').write_text(blog,encoding='utf-8')
print('Updated home composition and journal navigation. Original prose and resource links retained.')
