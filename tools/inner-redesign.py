from pathlib import Path
import re
root=Path(__file__).resolve().parent.parent
pages=root/'src/pages'
# Keep all paper entries and their full titles; place the research note after the grid.
p=pages/'blog.html';s=p.read_text(encoding='utf-8')
note=re.search(r'\s*<li class="post note-row reveal">.*?</li>',s,re.S)
if note:
    text=note.group(0);s=s[:note.start()]+s[note.end():]
    s=s.replace('    </ul>',text+'\n    </ul>',1)
p.write_text(s,encoding='utf-8')
# Group each existing date/detail pair into a semantic timeline entry.
p=pages/'cv.html';s=p.read_text(encoding='utf-8')
s=s.replace('>CV</h1>','>Curriculum vitae</h1>')
if 'cv-introduction' not in s:
    s=s.replace('    <a class="button load"','    <p class="cv-introduction">Mark Hopkins Professor of Philosophy, Williams College</p>\n    <a class="button load"',1)
def timeline(m):
    content=m.group(1)
    if 'timeline-entry' not in content:
        content=re.sub(r'(<dt>.*?</dt>)\s*(<dd>.*?</dd>)',r'<div class="timeline-entry">\1\2</div>',content,flags=re.S)
    return '<dl class="timeline">'+content+'</dl>'
s=re.sub(r'<dl class="timeline">(.*?)</dl>',timeline,s,flags=re.S)
p.write_text(s,encoding='utf-8')
# A direct show destination avoids displaying an unavailable third-party embed.
p=pages/'podcasts.html';s=p.read_text(encoding='utf-8')
s=re.sub(r'<div class="embed reveal">\s*<div class="eyebrow">Spotify</div>\s*<iframe.*?</iframe>\s*</div>', '''<aside class="podcast-feature">
      <div class="podcast-art"><img src="assets/img/hero-podcasts.jpg" alt="Vintage microphone beside antique books" width="2000" height="1333" loading="lazy"><span>Alan White · Podcasts</span></div>
      <div class="podcast-feature-copy"><div class="eyebrow">The listening room</div><h2>The Structural-Systematic Philosophy</h2><div class="gold-rule"></div><p>My podcasts are available on a number of sites, including those listed below.</p><div class="podcast-actions"><a class="button" href="https://open.spotify.com/show/7ypUVMqn1uhGEPk3DV2mXB" target="_blank" rel="noopener">Open Spotify <span aria-hidden="true">↗</span></a><a class="text-link" href="#listening-platforms">All listening platforms <span aria-hidden="true">↓</span></a></div></div>
    </aside>''',s,count=1,flags=re.S)
s=s.replace('<div class="pods">','<div class="pods" id="listening-platforms">')
s=re.sub(r'\s*<iframe[^>]*src="https://open\.spotify\.com/embed/.*?</iframe>\s*</div>', '', s, count=1, flags=re.S)
p.write_text(s,encoding='utf-8')
# All inner-page headings receive a consistent home breadcrumb.
for p in pages.glob('*.html'):
    if p.stem in ['index','404']:continue
    s=p.read_text(encoding='utf-8')
    if 'class="page-hero' not in s or 'class="page-breadcrumb"' in s or 'article-hero' in s:continue
    title=re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S).group(1)
    breadcrumb='<nav class="page-breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">'+title+'</span></nav>'
    s=s.replace('<div class="wrap">','<div class="wrap">\n    '+breadcrumb,1)
    p.write_text(s,encoding='utf-8')
print('Unified inner-page headers; rebuilt blog grid, CV groups and podcast feature without the failing iframe.')
