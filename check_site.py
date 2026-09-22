#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
root=Path(__file__).resolve().parent/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.headings=0
 def handle_starttag(self,t,a):
  d=dict(a)
  if 'id' in d:self.ids.add(d['id'])
  if t=='h1':self.headings+=1
  for k in ['href','src']:
   if k in d:self.links.append(d[k])
pages={}
for p in root.rglob('*.html'):
 parser=Page();parser.feed(p.read_text());pages[p.resolve()]=parser
errors=[]
for p,parser in pages.items():
 for u in parser.links:
  q=urlsplit(u)
  if q.scheme or q.netloc or not u:continue
  target=(p.parent/unquote(q.path)).resolve() if q.path else p
  if not target.exists():errors.append(f'{p.relative_to(root)}: missing {u}')
  elif q.fragment and target in pages and q.fragment not in pages[target].ids and not q.fragment.isdigit():errors.append(f'{p.relative_to(root)}: missing anchor {u}')
for p in root.glob('*.html'):
 if p.name not in ['xlerobot-deck.html','sensor-shopping.html']:
  text=p.read_text()
  assert text.count('aria-current="page"')==1,p
  assert pages[p.resolve()].headings==1,p
  assert '/Users/' not in text and '11222' not in text,p
shop=json.loads((root/'data/shopping.json').read_text())
assert all(i['asin']!='B007SNN0WC' for i in shop['items'])
assert round(sum(i['usd'] for i in shop['items'] if i['in_latest_cart']),2)==shop['farm_subtotal_usd']
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} HTML pages; links, anchors, navigation, public inventory and local-path checks.')
