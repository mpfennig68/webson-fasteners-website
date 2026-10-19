/* Southco RFQ context; native form submission is preserved. */
(function(){'use strict';
const parts = {"F6-3-1": {"title": "Concealed Removable Hinge", "page": "Southco-F6-3-1.html"}, "V4-0006-52": {"title": "Versa-Latch Draw Latch", "page": "Southco-V4-0006-52.html"}, "96-50-510-50": {"title": "Removable Lift-Off Hinge", "page": "Southco-96-50-510-50.html"}, "C5-21-35": {"title": "Key-Locking Sealed Lever Latch", "page": "Southco-C5-21-35.html"}, "12-11020-13": {"title": "Fast-Lead Receptacle", "page": "Southco-12-11020-13.html"}, "V7-20-101-50": {"title": "Over-Center Draw Latch", "page": "Southco-V7-20-101-50.html"}, "C3-805": {"title": "Grabber Catch Latch", "page": "Southco-C3-805.html"}, "P2-54": {"title": "Large Snap-In Flush Pull", "page": "Southco-P2-54.html"}, "E3-16-21": {"title": "VISE ACTION\u00ae Compression Latch", "page": "Southco-E3-16-21.html"}, "P2-43-1": {"title": "Small Snap-In Flush Pull", "page": "Southco-P2-43-1.html"}, "P1-33": {"title": "Screw-Mounted Flush Pull", "page": "Southco-P1-33.html"}, "E6-10-208-50": {"title": "Constant-Torque Positioning Hinge", "page": "Southco-E6-10-208-50.html"}, "E3-16-35": {"title": "VISE ACTION\u00ae Compression Latch", "page": "Southco-E3-16-35.html"}, "catalog": {"title": "Southco product directory", "page": "Products-Southco.html"}};
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
 if(details && !details.value.trim()) details.value='Southco '+key+' - '+source.title+'\n';
}
}());
