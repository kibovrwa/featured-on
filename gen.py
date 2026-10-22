import json,html,datetime
d=json.load(open('/workspace/backlinks-push-2026-10/crawl-bing-success/urls.json'))
d=[x for x in d if x.get('status','LIVE')=='LIVE']
d=[x for x in d if not x.get('indexed')]+[x for x in d if x.get('indexed')]
B="https://kibovrwa.github.io/featured-on/"
now=datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
by={}
for x in d: by.setdefault(x['site'],[]).append(x['url'])
h=['<!doctype html><meta charset=utf-8><title>Featured on: press, directories and articles</title><link rel=alternate type=application/atom+xml href=feed.xml><h1>Featured on</h1><p>Third-party pages that mention our tools. Updated '+now[:10]+'.</p>']
import os as _o
_P='/workspace/backlinks-push-2026-10/crawl-bing-success/INDEX-CHECK-20261022.json'
if _o.path.exists(_P):
  _pr=[r for r in json.load(open(_P)).get('rows',[]) if r.get('bing')!='INDEXED' and r.get('own_article') and not r.get('noindex')]
  if _pr: h.append('<h2>Recently featured</h2><ul>'+''.join(f'<li><a href="{html.escape(r["url"])}">{html.escape(r["platform"])} - {html.escape(r["site"])}</a></li>' for r in _pr)+'</ul>')
for s,us in sorted(by.items()):
  h.append(f'<h2>{html.escape(s)}</h2><ul>'+''.join(f'<li><a href="{html.escape(u)}">{html.escape(u)}</a></li>' for u in us)+'</ul>')
open('index.html','w').write(''.join(h))
open('feed.xml','w').write(f'<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Featured on</title><id>{B}</id><updated>{now}</updated><link rel="hub" href="https://pubsubhubbub.appspot.com/"/><link rel="self" href="{B}feed.xml"/>'+''.join(f'<entry><title>{html.escape(x["platform"])} - {x["site"]}</title><id>{html.escape(x["url"])}</id><link href="{html.escape(x["url"])}"/><updated>{now}</updated></entry>' for x in d)+'</feed>')
open('sitemap.xml','w').write(f'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{B}</loc><lastmod>{now[:10]}</lastmod></url><url><loc>{B}feed.xml</loc></url></urlset>')
# mirrors footer (from mirrors.py state; no secrets, URLs only)
import os
if os.path.exists('/workspace/bl-hub/mirrors-state.json'):
  _m=json.load(open('/workspace/bl-hub/mirrors-state.json')).get('_urls',{})
  _l=[u for v in _m.values() for u in v.get('all',[v['url']])]
  if _l:
    open('index.html','a').write('<h2>Mirrors</h2><ul>'+''.join(f'<li><a href="{html.escape(u)}">{html.escape(u)}</a></li>' for u in _l)+'</ul>')
