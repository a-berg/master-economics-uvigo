"""Verificaciones de datos y cálculos con controles independientes."""
import hashlib,json,math
from pathlib import Path
import polars as pl
from pipeline import eurostat_rows
R=Path(__file__).resolve().parents[1];G=R/'datos/gold'
for p in (R/'datos/bronze').rglob('*.json'):
 m=json.loads(p.read_text())
 if 'artifact' in m:assert hashlib.sha256((R/m['artifact']).read_bytes()).hexdigest()==m['sha256'],p
s=pl.read_parquet(R/'datos/silver/observations.parquet')
assert not s.select(pl.struct(['country','year','series','source']).is_duplicated().any()).item()
assert s['value'].is_finite().all()
assert s['bronze_sha256'].null_count()==0
p=pl.read_csv(G/'comparison.csv');a=pl.read_csv(G/'growth_accounting.csv')
for r in a.iter_rows(named=True):
 d=p.filter(pl.col('country')==r['country'])
 y0=d.filter(pl.col('year')==r['start'])['gdp_real'].item();y1=d.filter(pl.col('year')==r['end'])['gdp_real'].item()
 n=r['end']-r['start'];reconstructed=y0*(1+r['gdp_cagr_pct']/100)**n
 assert math.isclose(reconstructed,y1,rel_tol=1e-12)
 assert math.isclose(r['gdp_log_pp'],r['capital_contribution_pp']+r['labor_contribution_pp']+r['solow_residual_pp'],abs_tol=1e-10)
# Prueba de decodificación con celdas ausentes y flag en la segunda dimensión.
fixture=dict(id=['geo','time'],size=[2,2],dimension={'geo':{'category':{'index':{'ES':0,'CN':1}}},'time':{'category':{'index':{'2020':0,'2021':1}}}},value={'0':10,'3':20},status={'3':'p'})
assert list(eurostat_rows(fixture))==[dict(geo='ES',time='2020',value=10,flag=None),dict(geo='CN',time='2021',value=20,flag='p')]
o=pl.read_csv(G/'spain_official.csv')
for series in ['gdp_real','gdp_nominal','employment_domestic','hours_domestic','capital_net_real']:
 assert o.filter(pl.col('series')==series).height>=20,series
m=pl.read_csv(G/'prices_labor_demography.csv')
for country in ['CHN','ESP']:
 d=m.filter((pl.col('country')==country)&pl.col('year').is_between(1991,2023))
 assert d['participation_15plus_pct'].null_count()==0
 for r in d.iter_rows(named=True):
  assert 0<=r['participation_15plus_pct']<=100
  assert math.isclose(r['employment_modeled_derived']+r['unemployment_modeled_derived'],r['labor_force'],rel_tol=1e-12)
print('OK: hashes bronze, claves silver, valores finitos, CAGR, identidad de crecimiento, JSON-stat, cobertura oficial e identidades laborales.')

# Identidad de oferta en la edición INE: PIB=P1-P2+impuestos netos productos.
for year in range(1995,2025):
 d=o.filter((pl.col('source')=='ine_integrated_accounts')&(pl.col('year')==year))
 v={r['series']:r['value'] for r in d.iter_rows(named=True)}
 assert abs(v['output']-v['intermediate_consumption']+v['product_taxes_net']-v['gdp_market'])<=1
print('OK: identidad de oferta INE para los 30 años.')
