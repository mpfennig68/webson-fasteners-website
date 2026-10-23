"""Apply the shared header/footer to public content pages; preserve RFQ attribution."""
from pathlib import Path
import re
W=Path(__file__).resolve().parents[1]
HEADER=(W/'scripts/templates/site-header.html').read_text().strip()
FOOTER=(W/'scripts/templates/site-footer.html').read_text().strip()
def active_section(name):
 if name=='index.html':return 'index.html'
 if name.startswith(('Products','Southco-','Reference-')):return 'Products.html'
 if name.startswith('Resources-Mil-Spec'):return 'Products.html'
 if name=='Resources-Custom-Fastener-Guide.html':return 'Products.html'
 if name.startswith('Services'):return 'Services.html'
 if name.startswith('Industries'):return 'Industries.html'
 if name in ['Certifications.html','About.html','Quote.html']:return name
 return None

def apply():
 count=0
 for p in sorted(W.glob('*.html')):
  s=p.read_text()
  if not re.search(r'<h1[ >]',s):continue
  name=p.name;active=active_section(name)
  nav=HEADER
  if active:
   aria='page' if active==name else 'location'
   nav=nav.replace(f'<a href="{active}">',f'<a href="{active}" class="nav-active" aria-current="{aria}">',1)
  # Use the precise existing product/reference route on quote links.
  match=re.search(r'href="(Quote\.html\?(?:context|reference|southco)=[^"]+)"',s)
  quote=match[1] if match else 'Quote.html' if name=='Quote.html' else 'Quote.html?context='+name
  nav=nav.replace('href="Quote.html"',f'href="{quote}"')
  footer=FOOTER.replace('href="Quote.html"',f'href="{quote}"')
  s,n=re.subn(r'<nav (?:aria-label="Main navigation" )?class="site-nav".*?</nav>',lambda m:nav,s,count=1,flags=re.S)
  assert n==1,name+' missing main navigation'
  s,n=re.subn(r'<footer class="site-footer".*?</footer>',lambda m:footer,s,count=1,flags=re.S)
  assert n==1,name+' missing footer'
  main=re.search(r'<main\b([^>]*)>',s)
  if main and not re.search(r'\bid=',main[1]):s=s[:main.start()]+main[0].replace('<main','<main id="main"',1)+s[main.end():]
  if not re.search(r'<a[^>]+href="#main"',s):s=s.replace('<body>','<body>\n<a class="site-skip" href="#main">Skip to content</a>',1)
  # Only the form completion page should be excluded, not the RFQ landing page.
  if name=='thank-you.html' and 'name="robots"'not in s:s=s.replace('</head>','<meta name="robots" content="noindex,follow">\n</head>')
  p.write_text(s);count+=1
 return count
if __name__=='__main__':print('Shared header/footer applied to',apply(),'content pages.')
