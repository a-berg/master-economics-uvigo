"""Contrasta cobertura, clasificación y ejemplos críticos del catálogo generado."""
import json,re
from pathlib import Path
import polars as pl
from snapshot import ROOT,verify
version='v0_2026-10-16';manifest=verify(version)
x=json.loads((ROOT/'datos/catalogo/series_crosswalk.json').read_text());rows=x['entries']
assert len(rows)==80 and len({r['code'] for r in rows})==80
assert sum(r['original_country']=='ESP' for r in rows)==76
for row in rows:
 for country in ['ESP','CHN']:
  d=row[country]
  assert d['n']==len(set(d['years']))
  assert set(d['original_years_missing'])==set(row['original_years'])-set(d['years'])
  assert d['original_years_covered']==len(set(d['years'])&set(row['original_years']))
  assert d['full_original_period']==(bool(row['original_years']) and set(row['original_years']).issubset(d['years']))
  assert not d['same_ameco_code_downloaded']
oitt=next(r for r in rows if r['code']=='ESP.1.1.0.0.OITT')
oigt=next(r for r in rows if r['code']=='ESP.1.1.0.0.OIGT')
assert oitt['selection_specifications']['ESP']['selection']['na_item']=='P5G'
assert oigt['selection_specifications']['ESP']['selection']['na_item']=='P51G'
assert oitt['CHN']['locator']=='pwt110_na / q_i'
assert oigt['CHN']['locator']=='pwt110_na / q_gfcf'
assert oitt['ESP']['original_years_missing']==list(range(1960,1995))
assert oitt['CHN']['original_years_missing']==[2024,2025]
assert next(r for r in rows if r['code']=='ESP.1.0.0.0.UWCD')['CHN']['status']=='FALTA'
dic=json.loads((ROOT/'datos/catalogo/series_dictionary.json').read_text())
assert all(r['definition_original'] for r in dic)
assert any(r['series']=='avh' and r['source']=='pwt110' and 'NO son horas totales' in r['note'] for r in dic)
df=pl.read_parquet(ROOT/'datos/snapshots'/version/'frozen/datos/silver/observations.parquet')
assert {(r['source'],r['series']) for r in dic}==set(df.select('source','series').unique().iter_rows())
assert len(pl.read_csv(ROOT/'output/catalogo/correspondencias_ameco_espana_china.csv'))==80
print('OK: inventario 80 códigos; cobertura y huecos por país; FBC/FBCF; avh; no equivalencias exactas inventadas; todas las series fuente de v0 definidas.')
