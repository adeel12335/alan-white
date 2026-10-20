"""Preserve source articles and add editorial entry points to the redesign."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / 'src/pages'
posts = json.loads((ROOT / 'tools/source-content/posts.json').read_text(encoding='utf-8'))
recent = (PAGES / 'recent-posts.html').read_text(encoding='utf-8')
for post in posts:
    title = html.unescape(re.sub('<[^>]+>', '', post['title']['rendered']))
    content = post['content']['rendered']
    # Preserve the original HTML, including footnotes and ordered lists.
    if post['slug'].startswith('a-partial-history'):
        content += '<p><a class="button" href="https://sites.williams.edu/awhite/files/2025/02/A-Partial-History-of-My-Work-on-the-Structural-Systematic-Philosophy-with-Lorenz-B.-Puntel-With-Particular-Emphasis-on-Being.pdf" target="_blank" rel="noopener">Read the updated full paper ↗</a></p>'
    for item in posts:
        content = content.replace(item['link'], item['slug'] + '.html')
    page = f'''<!-- title: {html.escape(title)} – Alan White | desc: {html.escape(title)}. An original essay by Alan White on the structural-systematic philosophy. -->
<section class="page-hero plain article-hero"><div class="page-hero-img" aria-hidden="true"></div><div class="wrap">
<a class="text-link" href="recent-posts.html">← Recent Posts</a>
<div class="eyebrow">Alan White · Essay</div><h1>{title}</h1>
</div></section>
<section class="section"><div class="wrap article-layout"><aside class="article-aside"><span class="eyebrow">On this page</span><a class="text-link" href="#essay">Read the essay ↓</a><a class="text-link" href="blog.html">Posts &amp; papers →</a><button class="text-link print-button" type="button" data-print>Print essay ↗</button></aside><article class="prose essay" id="essay">{content}</article></div></section>
<section class="article-end"><div class="wrap"><span class="eyebrow">Continue exploring</span><a href="recent-posts.html">Recent Posts <span aria-hidden="true">↗</span></a><a href="publications.html">Publications <span aria-hidden="true">↗</span></a></div></section>'''
    (PAGES / (post['slug'] + '.html')).write_text(page, encoding='utf-8')
    recent = recent.replace(post['link'], post['slug'] + '.html')
recent = recent.replace(' target="_blank" rel="noopener"', '')
(PAGES / 'recent-posts.html').write_text(recent, encoding='utf-8')

home = (PAGES / 'index.html').read_text(encoding='utf-8')
explore = '''
<section class="explore-section" aria-labelledby="explore-title"><div class="wrap">
<div class="section-head"><div><div class="eyebrow rule">Explore the work</div><h2 id="explore-title">Ways into the philosophy</h2></div><span class="explore-index">Reading · Research · Listening</span></div>
<div class="explore-grid">
<a class="explore-item" href="blog.html"><span class="explore-no">01 / READ</span><h3>Posts &amp; papers</h3><p>Blog</p><span class="explore-arrow" aria-hidden="true">↗</span></a>
<a class="explore-item" href="publications.html"><span class="explore-no">02 / RESEARCH</span><h3>Books &amp; publications</h3><p>Selected publications</p><span class="explore-arrow" aria-hidden="true">↗</span></a>
<a class="explore-item" href="podcasts.html"><span class="explore-no">03 / LISTEN</span><h3>The philosophy, in conversation</h3><p>Podcasts</p><span class="explore-arrow" aria-hidden="true">↗</span></a>
</div></div></section>
'''
if 'explore-section' not in home:
    home = home.replace('<section class="section" id="about">', explore + '\n<section class="section" id="about">')
    items = []
    for i, p in enumerate(posts):
        title = html.unescape(p['title']['rendered'])
        excerpt = html.unescape(re.sub('<[^>]+>', '', p['excerpt']['rendered']))
        excerpt = re.sub(r'\s+', ' ', excerpt).strip()
        items.append(f'<a class="writing-item" href="{p["slug"]}.html"><span class="explore-no">0{i+1} / ESSAY</span><h3>{title}</h3><p>{excerpt}</p><span class="text-link">Read essay <span aria-hidden="true">↗</span></span></a>')
    home += '<section class="section"><div class="wrap"><div class="section-head"><div><div class="eyebrow rule">Recent Posts</div><h2>From the writing desk</h2></div><a class="text-link" href="recent-posts.html">All recent posts →</a></div><div class="writing-grid">' + ''.join(items) + '</div></div></section>'
    (PAGES / 'index.html').write_text(home, encoding='utf-8')

cv = PAGES / 'cv.html'
cv.write_text(cv.read_text(encoding='utf-8').replace('https://structural-systematicphilosophy.com/wp-content/uploads/2025/12/AW-CV-7-Dec-2024.pdf', 'assets/documents/alan-white-cv.pdf'), encoding='utf-8')
print('Preserved all 3 full articles; added homepage discovery and recent writing sections.')
