"""Índice de toda la edición AMECO, sin limitarse a códigos visibles del Excel."""
import csv,io,json,hashlib,zipfile,re
from pathlib import Path
import polars as pl
ROOT=Path(__file__).resolve().parents[1]
def normalize(s):return re.sub(r'\s+',' ',s).strip()
def build():
 m=json.loads((ROOT/'datos/bronze/ameco_spring2026/latest.json').read_text());p=ROOT/m['artifact']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']
 records=[]
 z=zipfile.ZipFile(p)
 for member in z.namelist():
  for row in csv.DictReader(io.StringIO(z.read(member).decode('cp1252')),delimiter=';'):
   meta={k:normalize(v) for k,v in row.items() if k and not k.isdigit() and v is not None}
   meta.update(source_member=member,bronze_sha256=m['sha256'],source_url=m['url'])
   records.append(meta)
 dest=ROOT/'datos/catalogo';df=pl.DataFrame(records,infer_schema_length=None).sort('CODE');df.write_parquet(dest/'ameco_completo.parquet');df.write_csv(dest/'ameco_completo.csv')
 print('Índice AMECO completo:',df.height,'entradas; códigos únicos:',df['CODE'].n_unique())
 return df

def search(title_regex,country='Spain'):
 p=ROOT/'datos/catalogo/ameco_completo.parquet';df=pl.read_parquet(p) if p.exists() else build()
 return df.filter((pl.col('COUNTRY')==country)&pl.col('TITLE').str.contains('(?i)'+title_regex)).select('CODE','TITLE','SUB-CHAPTER','UNIT','source_member')

def extract(codes):
 m=json.loads((ROOT/'datos/bronze/ameco_spring2026/latest.json').read_text());z=zipfile.ZipFile(ROOT/m['artifact']);out=[]
 for member in z.namelist():
  for row in csv.DictReader(io.StringIO(z.read(member).decode('cp1252')),delimiter=';'):
   if row['CODE'].strip() not in codes:continue
   for year,value in row.items():
    if year and year.isdigit() and value.strip() not in ['','NA']:
     out.append(dict(code=row['CODE'].strip(),country='ESP',year=int(year),value=float(value),unit=row['UNIT'].strip(),title=normalize(row['TITLE']),source='ameco_spring2026',zip_member=member,bronze_sha256=m['sha256'],forecast_period=int(year)>=2026))
 d=pl.DataFrame(out)
 assert d.group_by(['code','year']).agg(pl.col('value').n_unique().alias('n'),pl.col('unit').n_unique().alias('units')).filter((pl.col('n')>1)|(pl.col('units')>1)).is_empty(), 'Valores repetidos incompatibles entre capítulos'
 return d.unique(['code','year']).sort(['code','year'])
if __name__=='__main__':build()
