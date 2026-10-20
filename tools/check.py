"""Validate local page targets, fragments, images and preserved source links."""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent.parent
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.refs=[];self.ids=set();self.feed(text)
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.add(d['id'])
        for key in ['href','src']:
            if key in d:self.refs.append(d[key])
        if tag=='source' and 'srcset' in d:self.refs.extend(x.strip().split(' ')[0] for x in d['srcset'].split(','))

errors=[];count=0
docs={p.name:Document(p.read_text(encoding='utf-8')) for p in ROOT.glob('*.html') if p.name!='_head.html'}
for name,doc in docs.items():
    for ref in doc.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=unquote(u.path) or name
        if target=='/':target='index.html'
        path=ROOT/target.lstrip('/')
        count+=1
        if not path.is_file():errors.append(f'{name}: missing {ref}')
        elif u.fragment and path.suffix=='.html' and u.fragment not in docs[path.name].ids:errors.append(f'{name}: missing fragment {ref}')
original=json.loads((ROOT/'tools/source-content/pages.json').read_text(encoding='utf-8'))
allhtml='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'src/pages').glob('*.html'))
missing=[]
for p in original:
    for ref in Document(p['content']['rendered']).refs:
        if 'amazon.com' in ref or 'sites.williams.edu' in ref or 'doi.org' in ref or 'transistor.fm' in ref:
            if html.escape(ref,quote=True) not in allhtml and ref not in allhtml:
                # The original publications CV is an older 2012 file. Preserve it as an archive link.
                missing.append(ref)
report={'pages':len(docs)-1,'checked_local_references':count,'errors':errors,'source_links_requiring_review':sorted(set(missing)),'source_notes':['Original history post PDF returns HTTP 404; retained source link and added the updated 2025 paper.','Williams College PDF downloads returned HTTP 403 to the automated fetch; their original external URLs are retained.','Source WordPress corrigenda contain replacement characters; original content is preserved verbatim.']}
(ROOT/'CONTENT-AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:raise SystemExit(1)
