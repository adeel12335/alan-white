from pathlib import Path
import re
root=Path(__file__).resolve().parent.parent
for p in (root/'src/pages').glob('*.html'):
    text=p.read_text(encoding='utf-8')
    if p.stem=='index':
        continue
    if 'hero-glass-panel' not in text:
        def wrap(m):
            hero=m.group(0)
            opening='<div class="wrap">'
            start=hero.find(opening)
            end=hero.rfind('</div>')
            if start<0 or end<start:return hero
            start+=len(opening)
            return hero[:start]+'<div class="hero-glass-panel">'+hero[start:end]+'</div>'+hero[end:]
        text=re.sub(r'<section class="page-hero[^\"]*"[^>]*>.*?</section>',wrap,text,flags=re.S)
    p.write_text(text,encoding='utf-8')
print('Frosted-glass panels apply only to interior page heroes; the homepage slider is preserved.')
