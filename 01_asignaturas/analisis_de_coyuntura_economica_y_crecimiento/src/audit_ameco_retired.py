"""Comprobación de presencia histórica, separada de la decisión de exclusión actual."""
import json,zipfile,io,csv,hashlib
from pathlib import Path
from acquire_core import fetch
R=Path(__file__).resolve().parents[1]
SPEC=dict(id='ameco_autumn2021_audit',url='https://economy-finance.ec.europa.eu/document/download/a522fc1a-c386-4c3e-80dd-50de123fb773_en?filename=ameco_autumn2021.zip',extension='zip',publication_date='2021-11-11',landing_url='https://economy-finance.ec.europa.eu/economic-research-and-databases/economic-databases/ameco-database/ameco-archive_en')
def codes(m):
 p=R/m['artifact'];assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'];z=zipfile.ZipFile(p)
 if 'ameco0.zip' in z.namelist():z=zipfile.ZipFile(io.BytesIO(z.read('ameco0.zip')))
 return {row['CODE'].strip() for n in z.namelist() if n.lower().endswith('.txt') for row in csv.DictReader(io.StringIO(z.read(n).decode('cp1252')),delimiter=';')}
def main():
 old=fetch(SPEC);current=json.loads((R/'datos/bronze/ameco_spring2026/latest.json').read_text());a=codes(old);b=codes(current);records=[]
 policy_path=R/'datos/catalogo/decisiones_espana.json';policy=json.loads(policy_path.read_text());policy['excluded_current_codes']={}
 for suffix in ['AMGE','AXGE']:
  code='ESP.1.0.0.0.'+suffix
  assert code not in b
  note='No publicada en la edición actual: se excluye de los objetivos activos siguiendo la revisión del alumno. Tampoco aparece en el archivo oficial Autumn 2021 inspeccionado; no se acredita fecha exacta de retirada ni que todo el Excel pertenezca a 2021.'
  records.append(dict(code=code,present_autumn2021=code in a,present_spring2026=code in b,decision='EXCLUIDA_EDICION_ACTUAL',retirement_date=None,retirement_date_verified=False,note=note,source_2021=old,source_2026=current))
  policy['excluded_current_codes'][code]={'note':note,'evidence':'output/revision_espana/ameco_series_excluidas.json'}
 policy_path.write_text(json.dumps(policy,ensure_ascii=False,indent=2)+'\n')
 (R/'output/revision_espana/ameco_series_excluidas.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
 print([(r['code'],r['present_autumn2021'],r['present_spring2026']) for r in records])
if __name__=='__main__':main()
