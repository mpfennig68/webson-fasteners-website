"""Carry page context into RFQs without intercepting native form submission."""
from pathlib import Path
import re,json,html,runpy
W=Path(__file__).resolve().parents[1]
def clean(s):return ' '.join(html.unescape(re.sub('<[^>]+>',' ',s)).split()).rstrip('.')
runpy.run_path(str(W/'scripts/site-chrome.py'))['apply']()
pages={}
for path in sorted(W.glob('*.html')):
 s=path.read_text()
 if not re.search('<h1[ >]',s) or path.name=='Quote.html':continue
 title=re.search(r'<title>(.*?)</title>',s,re.S)
 heading=re.search(r'<h1[^>]*>(.*?)</h1>',s,re.S)
 name=clean(title[1].split('|')[0]) if title else clean(heading[1])
 if path.name.startswith(('Reference-','Resources-','Southco-')):name=clean(heading[1])
 if path.name.startswith('Reference-Family-'):name='Mil-Spec '+name.lower()
 if path.name=='index.html':prefill='General fastener inquiry\n'
 elif path.name.startswith(('Reference-','Southco-')):prefill=name+'\n'
 else:prefill='Inquiry regarding: '+name+'\n'
 pages[path.name]={'title':name,'prefill':prefill}
 s=re.sub(r'href="Quote\.html\?context=[^"]*"', 'href="Quote.html?context='+path.name+'"', s)
 s=s.replace('href="Quote.html"','href="Quote.html?context='+path.name+'"')
 path.write_text(s)
part_guides=json.loads((W/'scripts/mil-spec-data.json').read_text()).get('stocked_part_guides',{})
lookup_guides=json.loads((W/'scripts/mil-spec-lookup-data.json').read_text()).get('reference_part_guides',{})
part_guides={**lookup_guides,**part_guides}
# Shoulder references are selectable for quotation without implying stocked status.
shoulders=json.loads((W/'scripts/mil-spec-data.json').read_text())
for key,root,drive in [('shoulder_socket','MS51576','hex-socket'),('shoulder_slotted','MS51575','slotted')]:
 part_guides['Reference-'+root+'.html']={'description':root+' stainless '+drive+' shoulder screw','parts':[r['part']for r in shoulders[key]]}
# Reference selections are explicitly allowed for quotation, without stock claims.
for root,data in json.loads((W/'scripts/mil-spec-additional-screw-data.json').read_text()).items():
 part_guides['Reference-'+root+'.html']={'description':data['description'],'parts':[r['part']for r in data['rows']]}
search_index=W/'assets/mil-spec-search-index.json'
if search_index.exists():
 part_guides['Resources-Mil-Spec-Part-Search.html']={'description':'Mil-Spec part reference','parts':[r['part']for r in json.loads(search_index.read_text())['parts']]}
script='''/* Site-wide RFQ context. No submission interception, network request or browser storage. */
(function(){
 'use strict';
 const pages = '''+json.dumps(pages,ensure_ascii=False)+''';
 const partGuides = '''+json.dumps(part_guides,ensure_ascii=False)+''';
 const form=document.querySelector('form.rfq-form');
 const script=document.currentScript;
 if(!form || !script || !script.src)return;
 const params=new URL(window.location.href).searchParams;
 let key=params.get('context') || params.get('reference');
 const part=params.get('southco');
 if(part){key=part==='catalog'?'Products-Southco.html':'Southco-'+part+'.html';}
 if(!key || !Object.prototype.hasOwnProperty.call(pages,key))return;
 const source=pages[key];
 const url=new URL('../'+key,script.src);
 if(url.origin!==window.location.origin)return;
 const details=document.querySelector('#rfq-details');
 if(details && !details.value.trim()){
  const requestedPart=params.get('part');
  const guide=Object.prototype.hasOwnProperty.call(partGuides,key) ? partGuides[key] : null;
  const selectedPart=guide && guide.parts.includes(requestedPart);
  details.value=selectedPart ? requestedPart+' - '+guide.description+'\\n' : source.prefill;
 }
 for(const [name,value] of [['rfq_source_page',source.title],['rfq_source_url',url.href]]){
  const input=document.createElement('input');input.type='hidden';input.name=name;input.value=value;form.appendChild(input);
 }
}());
'''
(W/'assets/rfq-site-context.js').write_text(script)
p=W/'Quote.html';s=p.read_text()
if 'src="assets/rfq-site-context.js"' not in s:s=s.replace('<script src="assets/southco-rfq.js" defer></script>','<script src="assets/southco-rfq.js" defer></script>\n<script src="assets/rfq-site-context.js" defer></script>')
p.write_text(s)
(W/'scripts/rfq-site-context-pages.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False)+'\n')
print('RFQ page context available for',len(pages),'content pages.')

# Keep canonical sitemap coverage in step with all page generators.
runpy.run_path(str(W/'scripts/build-sitemap.py'))['build']()
