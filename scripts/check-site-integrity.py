"""Check public pages, local destinations, shared chrome and canonical sitemap coverage."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter,defaultdict
import json,re,xml.etree.ElementTree as ET,runpy
W=Path(__file__).resolve().parents[1]
BASE='https://www.websonfasteners.com/'
class Page(HTMLParser):
 def __init__(self,s):
  super().__init__();self.ids=[];self.refs=[];self.h1=0;self.meta={};self.canon=[];self.mains=[];self.images=[];self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  if t=='h1':self.h1+=1
  if t=='main':self.mains.append(a)
  if t=='img':self.images.append(a)
  if t=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
  if t=='link'and a.get('rel')=='canonical':self.canon.append(a.get('href'))
  for k in ['href','src','action']:
   if k in a:self.refs.append((t,k,a[k]))

def check():
 files={p.relative_to(W).as_posix():p.read_text()for p in W.rglob('*.html')if not any(v in p.relative_to(W).parts for v in ['scripts','docs','.git'])}
 pages={n:Page(s)for n,s in files.items()};errors=[];count=0;graph=defaultdict(set)
 def require(ok,message):
  if not ok:errors.append(message)
 def check_ref(n,ref,tag=''):
  nonlocal count
  u=urlsplit(ref)
  if u.scheme in ['https','http'] and u.netloc in ['websonfasteners.com','www.websonfasteners.com']:target=W/unquote(u.path).lstrip('/')
  elif u.scheme or u.netloc:return
  elif u.path.startswith('/'):target=W/unquote(u.path).lstrip('/')
  else:target=(W/n).parent/unquote(u.path) if u.path else W/n
  if target.is_dir():target/= 'index.html'
  count+=1
  require(target.exists(),n+': missing '+ref)
  if target.exists()and target.is_relative_to(W):
   key=target.relative_to(W).as_posix()
   if key in pages:
    if tag=='a':graph[n].add(key)
    if u.fragment:require(unquote(u.fragment)in pages[key].ids,n+': missing anchor '+ref)
 content=[n for n,p in pages.items()if p.h1];indexed=[];titles=[];descs=[];headers=set();footers=set()
 active=runpy.run_path(str(W/'scripts/site-chrome.py'))['active_section']
 def normalize(s):
  s=re.sub(r'Quote\.html\?[^" ]+','Quote.html',s)
  s=re.sub(r' class="nav-active" aria-current="(?:page|location)"','',s)
  return s
 for n,s in files.items():
  p=pages[n]
  for t,k,ref in p.refs:check_ref(n,ref,t)
  require(len(p.ids)==len(set(p.ids)),n+': duplicate IDs')
  for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
   try:json.loads(raw)
   except ValueError:errors.append(n+': invalid JSON-LD')
  if n not in content:
   refresh=re.search(r'http-equiv="refresh" content="0;url=([^"]+)"',s)
   if refresh:
    require('noindex'in p.meta.get('robots',''),n+': alias must be noindex')
    require(p.canon==[BASE+refresh[1].lstrip('/')],n+': alias canonical mismatch')
    require(('a','href',refresh[1])in p.refs,n+': alias fallback mismatch')
   continue
  require(p.h1==1,n+': expected one H1')
  require(len(p.mains)==1 and p.mains[0].get('id')=='main',n+': expected accessible main landmark')
  require('href="#main"'in s,n+': missing skip link')
  require(p.canon==[BASE+(''if n=='index.html'else n)],n+': canonical mismatch')
  title=re.search(r'<title>(.*?)</title>',s,re.S)
  require(bool(title and title[1].strip()),n+': missing title')
  require(bool(p.meta.get('description')),n+': missing description')
  titles.append(title[1] if title else'');descs.append(p.meta.get('description',''))
  require(all('alt'in a for a in p.images),n+': image missing alt attribute')
  header=re.search(r'<nav class="site-nav".*?</nav>',s,re.S);footer=re.search(r'<footer class="site-footer".*?</footer>',s,re.S)
  require(bool(header and footer),n+': missing shared header/footer')
  if header:
   headers.add(normalize(header[0]));currents=re.findall(r'<a href="([^"]+)" class="nav-active" aria-current="(?:page|location)"',header[0]);expected=active(n)
   require(currents==([expected]if expected else[]),n+': active navigation mismatch')
  if footer:footers.add(normalize(footer[0]))
  if 'noindex'not in p.meta.get('robots',''):indexed.append(p.canon[0])
 require(len(headers)==1,'Headers drift from shared template')
 require(len(footers)==1,'Footers drift from shared template')
 require(len(titles)==len(set(titles)),'Duplicate content-page titles')
 require(len(descs)==len(set(descs)),'Duplicate content-page descriptions')
 # Stylesheet assets and imports are part of the internal-link audit.
 for css in (W/'assets').rglob('*.css'):
  for ref in re.findall(r'url\([\'"]?([^\)\'\"]+)',css.read_text()):check_ref(css.relative_to(W).as_posix(),ref)
 reached=set();todo=['index.html']
 while todo:
  n=todo.pop()
  if n in reached:continue
  reached.add(n);todo.extend(graph[n]-reached)
 for n in content:
  if n!='thank-you.html':require(n in reached,n+': not reachable from the home page')
 root=ET.fromstring((W/'sitemap.xml').read_text());urls=[e.text for e in root.iter()if e.tag.endswith('}loc')]
 require(len(urls)==len(set(urls)),'Sitemap duplicate URLs')
 require(set(urls)==set(indexed),'Sitemap differs from canonical indexable content')
 require('noindex'in pages['thank-you.html'].meta.get('robots',''),'Confirmation page should be noindex')
 require('Sitemap: '+BASE+'sitemap.xml'in(W/'robots.txt').read_text(),'robots.txt sitemap mismatch')
 q=files['Quote.html']
 require('action="https://formcarry.com/s/JfMCu3MsY3E"'in q,'RFQ provider changed')
 require('type="file"'not in q,'Unexpected file-upload field')
 require('aria-describedby="rfq-custom-hint"'in q,'RFQ hint is not associated with its field')
 require('Matthew@websonfasteners.com'not in(W/'assets/rfq-submit-feedback.js').read_text(),'Outdated RFQ contact address')
 require((W/'_config.yml').read_text().find('  - docs')>=0 and (W/'_config.yml').read_text().find('  - scripts')>=0,'Internal maintenance files must be excluded from hosting')
 if errors:raise SystemExit('\n'.join(errors))
 report={'html_pages':len(files),'content_pages':len(content),'indexable_pages':len(indexed),'local_destinations_checked':count,'header_variants':len(headers),'footer_variants':len(footers),'broken_links':0,'broken_anchors':0,'orphan_content_pages':0,'duplicate_titles':0,'duplicate_descriptions':0}
 print(json.dumps(report,indent=2));return report
if __name__=='__main__':check()
