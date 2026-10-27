"""Index only published table values; leave inventory and RFQ allowlists untouched."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlencode
import json,re

SEARCH_PAGE='Resources-Mil-Spec-Part-Search.html'
PART=re.compile(r'^(?:MS|NASM|NAS|AN|AS)\d+[A-Z0-9.\-]*$')
ROOT=re.compile(r'^(?:MS|NASM|NAS|AN|AS)\d+')
def slug(value):return re.sub('[^a-z0-9]+','-',value.lower()).strip('-')

class Tables(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tables=[];self.table=None;self.row=None;self.cell=None;self.caption=False;self.feed(text)
 def handle_starttag(self,tag,attrs):
  if tag=='table':self.table={'caption':'','headers':[],'rows':[]}
  if self.table is None:return
  if tag=='caption':self.caption=True
  if tag=='tr':self.row=[]
  if tag in ['td','th']:self.cell=''
 def handle_data(self,data):
  if self.caption and self.table is not None:self.table['caption']+=data
  if self.cell is not None:self.cell+=data
 def handle_endtag(self,tag):
  if self.table is None:return
  if tag=='caption':self.caption=False
  if tag in ['td','th'] and self.cell is not None:
   if self.row is not None:self.row.append(' '.join(self.cell.split()))
   self.cell=None
  if tag=='tr' and self.row:
   if not self.table['headers']:self.table['headers']=self.row
   else:self.table['rows'].append(self.row)
   self.row=None
  if tag=='table':self.tables.append(self.table);self.table=None

def build(root,guide_map):
 root=Path(root);parts={}
 for path in sorted(root.glob('Reference-*.html')):
  for table in Tables(path.read_text()).tables:
   for row in table['rows']:
    for column,part in enumerate(row):
     if not PART.fullmatch(part) or part==ROOT.match(part)[0]:continue
     series=ROOT.match(part)[0]
     # Prefer a part's own family guide and stocked row over comparison copies.
     stocked='Stocked item' in row
     score=(100 if stocked else 0)+(50 if series in path.stem.split('-')[1:] else 0)
     summary=[]
     for heading,value in zip(table['headers'],row):
      if not value or PART.fullmatch(value) or heading in ['Request pricing','Stock status','Resource']:continue
      if 'quote' in value.lower() or '→' in value:continue
      summary.append(heading+': '+value)
     if column>0:summary.append(('Material group: 'if path.name=='Reference-MS35338.html'else'Reference: ')+table['headers'][column])
     item={'part':part,'series':series,'page':path.name,'anchor':'reference-table-'+slug(table['caption']),'summary':' · '.join(summary),'stocked':stocked}
     if part not in parts or score>parts[part][0]:parts[part]=(score,item)
 data=json.loads((root/'scripts/mil-spec-data.json').read_text())
 series=[]
 for item in data['series']:
  page=guide_map.get(item['root']) or 'Reference-Family-'+slug(item['family'])+'.html'
  series.append({'part':item['root'],'page':page,'summary':item['description'],'family':item['family']})
 def natural(part):return [int(v)if v.isdigit()else v for v in re.split(r'(\d+)',part)]
 index={'parts':[parts[key][1]for key in sorted(parts,key=natural)],'series':series}
 (root/'assets/mil-spec-search-index.json').write_text(json.dumps(index,ensure_ascii=False,separators=(',',':'))+'\n')
 print('Mil-Spec search indexes',len(parts),'exact part entries and',len(series),'series.')
 return index
