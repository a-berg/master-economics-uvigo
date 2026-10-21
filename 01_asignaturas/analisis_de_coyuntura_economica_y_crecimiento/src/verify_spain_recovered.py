"""Controles de integración y anualización de las fuentes recuperadas."""
from pathlib import Path
import json,hashlib
import polars as pl
R=Path(__file__).resolve().parents[1]
def verify():
 a=pl.read_parquet(R/'datos/silver/espana.parquet');r=pl.read_parquet(R/'datos/silver/espana_fuentes_recuperadas.parquet');p=pl.read_parquet(R/'datos/silver/espana_periodos.parquet');c=pl.read_parquet(R/'datos/silver/espana_catalogo.parquet')
 assert r.height==835 and r['series_id'].n_unique()==26
 assert a.height==6434 and a['series_id'].n_unique()==123 and c.height==125
 assert not p.select(pl.struct(['series_id','period']).is_duplicated().any()).item()
 assert p['value'].is_finite().all()
 assert a.filter(pl.col('series_id').is_in(r['series_id'].unique().to_list())).sort(['series_id','year']).equals(r.select(a.columns).sort(['series_id','year']))
 for source in r['source'].unique():
  m=json.loads((R/f'datos/bronze/{source}/latest.json').read_text());assert hashlib.sha256((R/m['artifact']).read_bytes()).hexdigest()==m['sha256']
  assert set(r.filter(pl.col('source')==source)['bronze_sha256'])=={m['sha256']}
 # Independientemente del normalizador, reconstruir todas las medias, sumas y cierres desde los periodos.
 checks=0
 for row in r.iter_rows(named=True):
  method=row['transformation'];sid=row['series_id'];y=row['year'];perid=sid
  if method=='sum_four_quarters':op='sum';required=4
  elif method in ['mean_twelve_months','mean_twelve_legal_monthly_rates']:
   op='mean';required=12;perid=sid.removesuffix('.ANNUAL_MEAN')
  elif method in ['December_stock','December_legal_monthly_rate']:
   op='last';required=1;perid=sid.removesuffix('.YEAR_END')
  else:continue
  q=p.filter((pl.col('series_id')==perid)&pl.col('period').str.starts_with(str(y)))
  if op=='last':q=q.filter(pl.col('period').str.ends_with('-12'))
  assert q.height==required,(sid,y,q.height)
  v=q['value'].sum() if op=='sum' else q['value'].mean() if op=='mean' else q['value'][0]
  assert abs(v-row['value'])<=max(1e-8,abs(v)*1e-12),(sid,y)
  checks+=1
 def series(s):return r.filter(pl.col('series_id')==s)
 def value(s,y):return series(s).filter(pl.col('year')==y)['value'][0]
 assert series('SEPE.REGISTERED.UNEMPLOYED.ANNUAL_MEAN')['year'].sort().to_list()==list(range(2001,2026))
 assert series('MITES.SMI.MONTHLY_RATE.ANNUAL_MEAN')['year'].min()==1981
 assert value('MITES.SMI.MONTHLY_RATE.ANNUAL_MEAN',2021)==955
 assert value('MITES.SMI.MONTHLY_RATE.ANNUAL_MEAN',2023)==1080
 assert value('MITES.SMI.MONTHLY_RATE.ANNUAL_MEAN',2025)==1184
 assert series('BDE.HIST.BM.YEAR_END')['year'].max()==1997
 assert p.filter(pl.col('series_id').str.starts_with('BDE.HIST.')&(pl.col('period')=='1998-10')).height==2
 partial=series('INE.INSOLVENCY.ENTERPRISES').filter(pl.col('year')==2004)
 assert partial['source_flag'][0]=='PARTIAL_YEAR_LAST_FOUR_MONTHS' and not partial['apta_analisis'][0]
 for row in series('BDE.HIST.M3_BM.YEAR_END').iter_rows(named=True):
  assert abs(row['value']-value('BDE.HIST.M3.YEAR_END',row['year'])/value('BDE.HIST.BM.YEAR_END',row['year']))<1e-12
 result=dict(status='OK',series=123,observations=6434,new_series=26,new_observations=835,subannual_observations=p.height,independent_aggregation_checks=checks,partial_2004_excluded_from_analytic_view=True)
 (R/'output/revision_espana/verificacion_integracion.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
 return result
if __name__=='__main__':verify()
