"""Build canonical sitemap coverage from public, indexable content pages."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime
from zoneinfo import ZoneInfo
import re,xml.etree.ElementTree as ET
W=Path(__file__).resolve().parents[1]
NS='http://www.sitemaps.org/schemas/sitemap/0.9'
BASE='https://www.websonfasteners.com/'
class Metadata(HTMLParser):
 def __init__(self,s):super().__init__();self.h1=0;self.canonical=None;self.noindex=False;self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='h1':self.h1+=1
  if t=='meta'and a.get('name','').lower()=='robots'and'noindex'in a.get('content','').lower():self.noindex=True
  if t=='link'and a.get('rel')=='canonical':self.canonical=a.get('href')
def build():
 p=W/'sitemap.xml';old=ET.fromstring(p.read_text());records={e.find('{'+NS+'}loc').text:e for e in old}
 pages=[]
 for file in sorted(W.glob('*.html'),key=lambda p:(p.name!='index.html',p.name)):
  d=Metadata(file.read_text())
  if not d.h1 or d.noindex:continue
  expected=BASE+(''if file.name=='index.html'else file.name)
  assert d.canonical==expected,(file.name,'unexpected canonical',d.canonical)
  pages.append(expected)
 lines=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="'+NS+'">']
 today=datetime.now(ZoneInfo('America/New_York')).date().isoformat()
 for url in pages:
  e=records.get(url);extras=''
  if e is not None:
   for child in e:
    tag=child.tag.split('}')[-1]
    if tag!='loc':extras+='<'+tag+'>'+child.text+'</'+tag+'>'
  else:extras='<lastmod>'+today+'</lastmod>'
  lines.append('  <url><loc>'+url+'</loc>'+extras+'</url>')
 p.write_text('\n'.join(lines+['</urlset>','']))
 return len(pages)
if __name__=='__main__':print('Sitemap contains',build(),'indexable canonical pages.')
