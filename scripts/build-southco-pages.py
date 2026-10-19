"""Build the Southco purchasing pages from the reviewed part register."""
from pathlib import Path
import html,json,re
W=Path(__file__).resolve().parents[1]
D=json.loads((W/'scripts/southco-data.json').read_text())
BASE='https://www.websonfasteners.com/'
HUB='Products-Southco.html'
h=lambda x:html.escape(str(x),quote=True)
base=(W/'Products-Mil-Spec-Hardware.html').read_text()
base=re.sub(r'href="Quote\.html(?:\?[^"]*)?"', 'href="Quote.html"', base)
nav=re.search(r'<nav class="site-nav".*?</nav>',base,re.S)[0]
footer=re.search(r'<footer class="site-footer".*?</footer>',base,re.S)[0]
fonts=re.search(r'<link rel="preconnect".*?<style>',base,re.S)[0].removesuffix('<style>')
icons='\n'.join(re.findall(r'<link rel="(?:icon|apple-touch-icon)"[^>]+>',base))
def file(p):return 'Southco-'+p['part']+'.html'
def photo(p,thumb=False):
 src=p['thumbnail'] if thumb else p['image']
 alt=('Representative Southco '+p['name'] if p['image_representative'] else 'Southco '+p['part']+' '+p['name'])
 if thumb:return '<img class="southco-thumb" src="'+src+'" alt="'+h(alt)+'" width="72" height="72" loading="lazy" decoding="async">'
 return '<figure class="southco-product-photo"><img src="'+src+'" alt="'+h(alt)+'" width="800" height="800" decoding="async"><figcaption>'+h(p['image_caption'])+'</figcaption></figure>'
def quote(p=None):return 'Quote.html?southco='+h(p['part'] if p else 'catalog')
def action(p=None):return '<div class="ref-actions"><a class="ref-button" href="'+quote(p)+'">Request '+(h(p['part'])+' pricing' if p else 'a Southco quote')+' →</a><a href="'+HUB+'#part-directory">Browse Southco parts →</a></div>'
def section(title,body,kicker='',id=''):
 return '<section class="ref-section"'+(' id="'+id+'"' if id else '')+'><p class="ref-kicker">// '+h(kicker)+'</p><h2>'+h(title)+'</h2>'+body+'</section>'
def table(headers,rows,caption,attrs=''):
 return '<div class="ref-table-wrap" role="region" tabindex="0" aria-label="'+h(caption)+'"><table '+attrs+'><caption>'+h(caption)+'</caption><thead><tr>'+''.join('<th scope="col">'+h(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr'+a+'>'+''.join(('<th scope="row">' if i==0 else '<td>')+c+('</th>' if i==0 else '</td>') for i,c in enumerate(cells))+'</tr>' for a,cells in rows)+'</tbody></table></div>'
def links(parts):return '<div class="ref-links">'+''.join('<a href="'+file(p)+'">'+h(p['part'])+' · '+h(p['name'])+' →</a>' for p in parts)+'</div>'
def page(path,title,desc,heading,intro,body,p=None):
 crumbs=[('Home','index.html'),('Products','Products.html'),('Southco',HUB)]+([(p['part'],path)] if p else [])
 ld=[{'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':n,'item':BASE+u} for i,(n,u) in enumerate(crumbs)]},{'@context':'https://schema.org','@type':'WebPage','name':title,'description':desc,'url':BASE+path}]
 if p:ld.append({'@context':'https://schema.org','@type':'Product','name':'Southco '+p['part']+' '+p['name'],'mpn':p['part'],'image':BASE+p['image'],'brand':{'@type':'Brand','name':'Southco'},'manufacturer':{'@type':'Organization','name':'Southco'},'description':p['summary'],'url':BASE+path,'additionalProperty':[{'@type':'PropertyValue','name':k,'value':v} for k,v in p['specs']]})
 else:ld.append({'@context':'https://schema.org','@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':'Southco '+x['part'],'url':BASE+file(x)} for i,x in enumerate(D['parts'])]})
 out='''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>'''+h(title)+'</title><meta name="description" content="'+h(desc)+'">'+icons+fonts+'''
<link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/mil-spec-reference.css"><link rel="stylesheet" href="assets/southco.css">
<link rel="canonical" href="'''+BASE+path+'"><meta property="og:type" content="website"><meta property="og:title" content="'+h(title)+'"><meta property="og:description" content="'+h(desc)+'"><meta property="og:url" content="'+BASE+path+'">'+''.join('<script type="application/ld+json">'+json.dumps(x)+'</script>' for x in ld)+'''
<script src="assets/mil-spec-reference.js" defer></script></head><body><a class="ref-skip" href="#main">Skip to content</a>'''+nav+'<main id="main" class="site-main reference-main southco-main"><header class="ref-hero"><nav class="ref-breadcrumb" aria-label="Breadcrumb">'+' / '.join('<span aria-current="page">'+h(n)+'</span>' if u==path else '<a href="'+u+'">'+h(n)+'</a>' for n,u in crumbs)+'</nav><p class="ref-kicker">// SOUTHCO ACCESS HARDWARE</p><h1>'+h(heading)+'</h1><p class="ref-lead">'+h(intro)+'</p>'+action(p)+'<nav class="ref-subnav" aria-label="Southco products"><a href="'+HUB+'#part-directory">Part-number directory</a><a href="'+HUB+'#product-families">Product families</a><a href="'+HUB+'#purchasing">Purchasing questions</a></nav></header>'+body+section('Source Southco hardware with Webson','<p>Send your complete Southco part number, quantity, required delivery date and any documentation requirements. Include annual usage or scheduled releases if this is a recurring requirement. Webson will review pricing and availability for your inquiry.</p>'+action(p),'REQUEST PRICING')+'</main>'+footer+'</body></html>\n'
 if p:
  titleblock='<h1>'+h(heading)+'</h1><p class="ref-lead">'+h(intro)+'</p>'
  out=out.replace(titleblock,'<div class="southco-product-hero"><div>'+titleblock+'</div>'+photo(p)+'</div>')
  out=out.replace('<meta property="og:type" content="website">','<meta property="og:image" content="'+BASE+p['image']+'"><meta property="og:type" content="website">')
 out=out.replace('href="Quote.html"','href="'+quote(p)+'"')
 (W/path).write_text(out)
parts=D['parts']
for p in parts:
 body=section('Product details','<p>'+h(p['summary'])+'</p>'+table(['Specification','Detail'],[('',[h(k),h(v)]) for k,v in [('Manufacturer','Southco'),('Part number',p['part']),('Product family',p['family'])]+p['specs']],'Southco '+p['part']+' product identification'),'PART IDENTIFICATION')
 body+=section('What to check before ordering','<p>'+h(p['check'])+'</p><p>Include the full manufacturer part number on your RFQ. If your drawing adds a revision, approved-source restriction or documentation requirement, send those details with the inquiry.</p>','FIT & SELECTION')
 related=[x for x in parts if x['family']==p['family'] and x!=p]
 if related:body+=section('Related Southco parts',links(related)+'<p>Compare the configuration of each part against your drawing. Related products are not automatically interchangeable.</p>','CONTINUE BROWSING')
 body+=section('Support for your assembly','<p>Combine this item with other hardware on one bill of material. Webson can review '+h(p['part'])+' alongside your fasteners and electronic hardware, including quantities and release schedules for production purchasing.</p><div class="ref-links"><a href="Products-Electronic-Hardware.html">Electronic hardware →</a><a href="Industries-Enclosures.html">Enclosure hardware →</a><a href="Services-Blanket-Orders-Scheduled-Releases.html">Blanket orders & scheduled releases →</a></div>','PURCHASE THROUGH WEBSON')
 page(file(p),'Southco '+p['part']+' '+p['name']+' | Webson','Request Southco '+p['part']+' '+p['name'].lower()+' pricing from Webson Fasteners. Review product details and send your quantity and delivery requirements.','Southco '+p['part']+' '+p['name'],p['summary'],body,p)
rows=[(' data-family="'+h(p['family'])+'" data-search="'+h(' '.join([p['part'],p['part'].replace('-',''),p['name'],p['summary'],p['family']]))+'"',['<a href="'+file(p)+'">'+h(p['part'])+'</a>','<div class="southco-directory-product">'+photo(p,True)+'<div>'+h(p['name'])+('<small class="southco-representative">Representative image</small>' if p['image_representative'] else '')+'</div></div>',h(p['family']),'<a href="'+file(p)+'">Details →</a><br><a href="'+quote(p)+'">Request pricing →</a>']) for p in parts]
families=list(D['families'])
controls='''<div data-reference-block><div class="ref-filters" data-reference-filters hidden><div class="ref-search"><label for="southco-search">Search Southco parts</label><input id="southco-search" type="search" data-reference-search placeholder="Part number, product or material"></div><div><label for="southco-family">Product family</label><select id="southco-family" data-reference-family><option value="">All families</option>'''+''.join('<option>'+h(f)+'</option>' for f in families)+'''</select></div><button type="button" class="ref-clear" data-reference-clear>Clear filters</button></div><p class="ref-count" data-reference-count role="status" aria-live="polite"></p><p data-reference-empty hidden>No matching parts. Clear the filters or send Webson your part number for review.</p>'''
body=section('Find your Southco part','<p>Search the listed part numbers, browse product details and send Webson your requirements for current pricing and availability. Have a different Southco number? Include it in your inquiry.</p>'+controls+table(['Southco part number','Product','Family','Next step'],rows,'Southco part-number directory','data-reference-table')+'</div>','PART-NUMBER DIRECTORY','part-directory')
body+=section('Southco product families',''.join('<div class="southco-family"><h3>'+h(f)+'</h3><p>'+h(D['families'][f])+'</p>'+links([p for p in parts if p['family']==f])+'</div>' for f in families),'BROWSE THE RANGE','product-families')
body+=section('Plan your hardware requirement','<p>For enclosure and electronics purchasing, the latch, hinge, pull and panel fastener each have a separate role. Group them on one bill of material, retaining every complete Southco number and any installation or documentation requirements.</p><p>Webson can review individual replacement items as well as recurring production requirements. Include estimated annual usage if you would like to discuss scheduled releases or a broader hardware sourcing program.</p>','SOURCE WITH WEBSON')
faq=[('Can I request a quote for a part that is not listed?','Yes. Send the complete Southco part number, quantity and required delivery date. Webson will review the requirement and available sourcing options.'),('Do these pages show live inventory?','Request a quote for current pricing, availability and lead time. The product directory provides identification details for purchasing.'),('Can similarly named Southco parts replace each other?','Check the complete designation and installation requirements first. Panel thickness, grip, finish, mounting style and access restriction can differ within the same product family.'),('What should I include with a production RFQ?','Provide a line for each part number and quantity, plus delivery dates, annual usage and required certificates. Include any applicable drawing notes or source restrictions.')]
body+=section('Southco purchasing questions','<div class="ref-faq">'+''.join('<h3>'+h(q)+'</h3><p>'+h(a)+'</p>' for q,a in faq)+'</div>','WORK WITH WEBSON','purchasing')
page(HUB,'Southco Latches, Hinges, Pulls & Fasteners | Webson','Source Southco hinges, compression latches, draw latches, flush pulls and fast-lead receptacles from Webson. Find part numbers and request pricing.','Southco latches, hinges & access hardware.','Find Southco hardware for doors, panels and enclosures. Browse removable and positioning hinges, compression and draw latches, grabber catches, recessed pulls and fast-lead receptacles.',body)
# Link the existing manufacturer mention and relevant category pages.
p=W/'Products.html';s=p.read_text();s=s.replace('>Southco</div>','><a href="Products-Southco.html" style="color:#2a2d6b;text-decoration:underline;text-underline-offset:3px">Southco →</a></div>');p.write_text(s)
for name in ['Products-Electronic-Hardware.html','Industries-Enclosures.html']:
 p=W/name;s=p.read_text()
 if 'Products-Southco.html' not in s:s=s.replace('</main>','<section style="padding:32px 40px;border-top:1px solid #e4ded2"><h2 style="font-family:Spectral,Georgia,serif;font-weight:400">Southco access hardware</h2><p style="font-size:15px;line-height:1.8">Browse Southco hinges, latches, flush pulls and fast-lead hardware by manufacturer part number.</p><a href="Products-Southco.html" style="color:#2a2d6b;text-decoration:underline">Explore Southco products →</a></section>\n</main>')
 p.write_text(s)
# Product quote attribution uses a separate allowlist; Mil-Spec tracking remains independent.
allow={p['part']:{'title':p['name'],'page':file(p)} for p in parts};allow['catalog']={'title':'Southco product directory','page':HUB}
tracking='''/* Southco RFQ context; native form submission is preserved. */
(function(){'use strict';
const parts = '''+json.dumps(allow)+''';
const key=new URL(window.location.href).searchParams.get('southco');
const form=document.querySelector('form.rfq-form');
if(!form || !key || !Object.prototype.hasOwnProperty.call(parts,key))return;
const source=parts[key];
const script=document.currentScript;
if(!script || !script.src)return;
const url=new URL('../'+source.page,script.src);
if(url.origin!==window.location.origin)return;
function field(name,value){const input=document.createElement('input');input.type='hidden';input.name=name;input.value=value;form.appendChild(input);}
field('rfq_southco_source',url.href);
if(key!=='catalog'){
 field('manufacturer','Southco');field('manufacturer_part_number',key);
 const details=document.querySelector('#rfq-details');
 if(details && !details.value.trim()) details.value='Southco '+key+' - '+source.title+'\\n';
}
}());
'''
(W/'assets/southco-rfq.js').write_text(tracking)
p=W/'Quote.html';s=p.read_text()
if 'assets/southco-rfq.js' not in s:s=s.replace('<script src="assets/rfq-reference-tracking.js" defer></script>','<script src="assets/rfq-reference-tracking.js" defer></script>\n<script src="assets/southco-rfq.js" defer></script>')
p.write_text(s)
p=W/'sitemap.xml';s=p.read_text()
for path in [HUB]+[file(p) for p in parts]:
 if BASE+path not in s:s=s.replace('</urlset>','  <url><loc>'+BASE+path+'</loc><lastmod>2026-10-19</lastmod></url>\n</urlset>')
p.write_text(s)
print('Built Southco hub and',len(parts),'part pages.')

# Reapply site-wide RFQ context after regenerating pages.
import runpy
runpy.run_path(str(W/'scripts/build-site-rfq-context.py'),run_name='__main__')
