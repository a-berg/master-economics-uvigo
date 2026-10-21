"""Invariantes relevantes de la revisión y conservación de v0."""
import csv,json
from pathlib import Path
from snapshot import verify
R=Path(__file__).resolve().parents[1];D=R/'output/revision_equivalencias'
def read(name):return list(csv.DictReader((D/name).open()))
a=read('registro_equivalencias.csv');assert len(a)==80 and len({r['code'] for r in a})==80
for code in ['ESP.1.1.0.0.OITT','ESP.1.0.0.0.OKND']:
 r=next(r for r in a if r['code']==code);assert int(r['n_overlap'])==int(r['equal_values'])==66
r=next(r for r in a if r['code']=='ESP.1.0.0.0.URTG');assert r['status'].startswith('PENDIENTE')
p=read('pwt_comprobaciones.csv')
for r in p:
 if 'main vs labor detail' in r['test']:assert r['n']==r['n_equal']
c=read('pwt_derivaciones_candidatas.csv');r=next(r for r in c if r['countrycode']=='CHN' and r['year']=='2023');assert r['comp_sh_quality']=='constante_asumida_o_interpolada'
u=json.loads((D/'un26_presencia.json').read_text());assert next(r for r in u if r['country']=='CHN')['records']==0;assert next(r for r in u if r['country']=='ESP')['records']>0
verify('v0_2026-10-16')
print('OK: 80 códigos, coincidencias principales, excepciones conservadas, coherencia PWT, calidad CHN, control UN y hashes v0.')
