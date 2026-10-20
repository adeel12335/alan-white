from pathlib import Path
import re
root=Path(__file__).resolve().parent.parent
p=root/'src/pages/index.html'
s=p.read_text(encoding='utf-8')
start=s.index('<section class="pathways-section"')
end=s.index('</section>',start)+len('</section>')
old=s[start:end]
cards=re.findall(r'<a class="pathway-card".*?</a>',old,re.S)
if len(cards)!=3:raise SystemExit('Expected exactly the three original discovery cards.')
cards='\n'.join('<div class="swiper-slide">'+card+'</div>' for card in cards)
new='''<section class="pathways-section pathways-motion" aria-labelledby="explore-title"><div class="wrap">
<div class="pathways-heading"><div><div class="eyebrow rule">Explore the work</div><h2 id="explore-title">Ways into the <em>philosophy</em></h2></div><div class="pathways-intro"><p>Reading · Research · Listening</p><span>Drag to explore <span aria-hidden="true">↔</span></span></div></div>
<div class="pathways-carousel swiper" data-pathways-carousel aria-label="Explore the work carousel">
<div class="pathways-grid swiper-wrapper">'''+cards+'''</div>
</div>
<div class="pathways-controls" data-pathways-controls><div class="pathways-pagination" aria-label="Choose a section"></div><div class="pathways-progress" aria-hidden="true"><span data-pathway-progress></span></div><div class="pathways-navigation"><span class="pathways-count" data-pathways-count aria-live="polite">01 / 03</span><button type="button" data-pathways-prev aria-label="Previous section">←</button><button type="button" data-pathways-pause aria-label="Pause section carousel" aria-pressed="false">Ⅱ</button><button type="button" data-pathways-next aria-label="Next section">→</button></div></div>
</div></section>'''
s=s[:start]+new+s[end:]
p.write_text(s,encoding='utf-8')
print('Converted the 3 original discovery cards into a Swiper carousel.')
