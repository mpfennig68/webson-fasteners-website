"""Check sourced screw mappings, dimension bounds and reference-only routes."""
from pathlib import Path
from decimal import Decimal
import json,re,html
W=Path(__file__).resolve().parents[1]
D=json.loads((W/'scripts/mil-spec-hex-cap-data.json').read_text())
index=json.loads((W/'assets/mil-spec-search-index.json').read_text());lookup={r['part']:r for r in index['parts']};parts={}
for root,count in [('MS90725',129),('MS90726',129),('MS90727',97),('MS90728',97)]:
 data=D[root];page=(W/f'Reference-{root}.html').read_text()
 assert len(data['rows'])==len({r['part']for r in data['rows']})==count
 assert data['reviewed_issue'] in html.unescape(page)
 assert 'Stocked item' not in page and 'ref-dimension-figure' in page
 for r in data['rows']:
  parts[r['part']]=r
  row=re.search(r'<tr\b[^>]*><th scope="row">'+re.escape(r['part'])+r'</th>.*?</tr>',page);assert row,r['part']
  for field,value in r.items():
   if field=='part':continue
   assert '>'+value+'<' in html.unescape(row[0]),(r['part'],field)
   if field.endswith('_limits'):
    low,high=map(Decimal,value.split('–'));assert 0<low<=high
  assert 'part='+r['part']+'"' in html.unescape(row[0])
  assert lookup[r['part']]['page']==f'Reference-{root}.html' and not lookup[r['part']]['stocked']
 assert next(s for s in index['series']if s['part']==root)['page']==f'Reference-{root}.html'
 for r in data.get('head_geometry',[]):
  for field,value in r.items():
   assert '>'+value+'<' in html.unescape(page)
   if field.endswith('_limits'):
    low,high=map(Decimal,value.split('–'));assert 0<low<=high
# Independently reviewed drawing examples, table boundaries and revision differences.
for root,coarse in [('MS90725',True),('MS90726',False),('MS90727',False),('MS90728',True)]:
 for dash,thread,length in [(3,'1/4-'+('20' if coarse else '28'),'0.500'),(109,'1/2-'+('13' if coarse else '20'),'1.000'),(179,'3/4-'+('10' if coarse else '16'),'0.750'),(191,'3/4-'+('10' if coarse else '16'),'3.000')]:
  row=parts[f'{root}-{dash}'];assert (row['thread'],row['length'])==(thread,length)
 assert all(Decimal(r['length'])<=3 for r in D[root]['rows'])
 assert f'{root}-999' not in lookup and f'{root}-3L' not in lookup
 page=(W/f'Reference-{root}.html').read_text()
 assert 'twice the nominal diameter plus 1/4 inch' in page
 if D[root]['grade']=='8':
  assert f'{root}-79' not in parts and f'{root}-130' not in parts
  assert 'not intended for aerospace applications' in page and 'zinc coating' in page
 else:
  assert parts[f'{root}-79']['length']=='0.438'
  assert 'cadmium plating' in page
assert parts['MS90728-155']['head_height_limits']=='0.378–0.405'
assert parts['MS90727-155']['head_height_limits']=='0.378–0.403'
assert len(parts)==452
print('452 hex cap references pass drawing examples, thread/length mappings, head limits, omitted sizes, quote links and search/stock boundaries.')
