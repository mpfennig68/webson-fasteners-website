"""Check sourced screw mappings, dimension bounds and reference-only routes."""
from pathlib import Path
from decimal import Decimal
import json,re,html
W=Path(__file__).resolve().parents[1]
D=json.loads((W/'scripts/mil-spec-fillister-cap-data.json').read_text())
index=json.loads((W/'assets/mil-spec-search-index.json').read_text());lookup={r['part']:r for r in index['parts']};parts={}
for root,count in [('MS35275',119),('MS35311',53),('MS35312',66)]:
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
# Independently reviewed dash boundaries, dimension distinctions and length tolerances.
for part,thread,length in [('MS35275-201','2-56','0.125'),('MS35275-217','4-40','0.500'),('MS35275-230','6-32','0.500'),('MS35275-263','10-24','0.500'),('MS35275-276','1/4-20','0.312'),('MS35275-319','3/8-16','3.000'),('MS35311-3','1/4-20','0.500'),('MS35311-109','1/2-13','1.000'),('MS35311-168','5/8-11','3.000'),('MS35312-3','1/4-28','0.500'),('MS35312-109','1/2-20','1.000'),('MS35312-168','5/8-18','3.000')]:
 assert (parts[part]['thread'],parts[part]['length'])==(thread,length),part
assert parts['MS35275-263']['total_head_height_limits']=='0.165–0.180'
assert D['MS35275']['head_geometry'][4]['head_side_height_limits']=='0.123–0.130'
assert D['MS35275']['head_geometry'][4]['drilled_hole_nominal']=='0.046'
assert parts['MS35275-267']['length_tolerance']=='+0.000 / −0.031'
assert parts['MS35275-268']['length_tolerance']=='+0.000 / −0.062'
assert parts['MS35275-272']['length_tolerance']=='+0.000 / −0.094'
assert parts['MS35311-109']['length_tolerance']=='+0.000 / −0.030'
assert parts['MS35311-111']['length_tolerance']=='+0.000 / −0.060'
assert parts['MS35311-118']['length_tolerance']=='+0.000 / −0.090'
assert parts['MS35312-17']['length_tolerance']=='+0.000 / −0.060'
assert parts['MS35312-167']['length_tolerance']=='+0.000 / −0.100'
assert parts['MS35312-155']['head_height_limits']=='0.378–0.403'
for dash in [2,4,9,11,54,56,61,63,105,110,112,159,161]:assert f'MS35311-{dash}'not in parts
for dash in list(range(27,53))+list(range(130,155)):assert f'MS35311-{dash}'not in parts
for root in D:
 assert f'{root}-999'not in lookup
assert 'inactive for new design after 15 February 1973' in (W/'Reference-MS35312.html').read_text()
assert 'does not guarantee Type 316' in (W/'Reference-MS35275.html').read_text()
assert len(parts)==238
print('238 screw references pass thread/length mappings, fillister head distinctions, asymmetric length tolerances, inactive exclusions and search/stock boundaries.')
