"""Verificación de selección, inmutabilidad de valores y notebook ejecutado."""
from pathlib import Path
import hashlib,json
import polars as pl
import nbformat
from snapshot import verify
R=Path(__file__).resolve().parents[1]
a=pl.read_parquet(R/'datos/silver/espana.parquet');c=pl.read_parquet(R/'datos/silver/espana_catalogo.parquet');w=pl.read_parquet(R/'datos/silver/espana_anual.parquet')
assert a['country'].unique().to_list()==['ESP']
assert not a.select(pl.struct(['series_id','year']).is_duplicated().any()).item()
assert a['value'].is_finite().all()
assert c.filter(pl.col('status')=='ACEPTADA_BASE_EDICION_ACTUAL').height==10
policy=json.loads((R/'datos/catalogo/decisiones_espana.json').read_text())
for suffix in ['URTG','UUTG']:
 code='ESP.1.0.0.0.'+suffix
 manually_accepted=policy['manual_decisions'].get(code,{}).get('action')=='accept_current_edition'
 assert bool(a.filter(pl.col('series_id')==code)['apta_analisis'].all())==manually_accepted
# No se trasladan factores de diagnóstico ni valores del Excel a silver.
original=pl.concat([pl.read_parquet(R/'datos/silver/ampliacion_20261019/ameco_reference_codes.parquet'),pl.read_parquet(R/'datos/silver/ampliacion_20261019/ameco_conceptos_recuperados.parquet')],how='vertical_relaxed').filter(pl.col('country')=='ESP').select(pl.col('code').alias('series_id'),'year',pl.col('value').alias('original'))
check=a.filter(pl.col('source')=='ameco_spring2026').join(original,on=['series_id','year'],validate='1:1')
assert check.height==original.height
assert check.filter(pl.col('value')!=pl.col('original')).height==0
approved=a.filter(pl.col('apta_analisis')&~pl.col('forecast_period'))
assert set(w.columns)-{'country','year'}==set(approved['series_id'])
assert w['year'].max()==2025
# Cada dato no nulo de la vista procede de un valor aceptado y no de forecast.
unpivot=w.unpivot(index=['country','year'],variable_name='series_id').drop_nulls('value')
expected=approved.select('country','year','series_id','value')
assert unpivot.sort(['series_id','year']).equals(expected.sort(['series_id','year']))
for source in a['source'].unique():
 m=json.loads((R/f'datos/bronze/{source}/latest.json').read_text())
 assert hashlib.sha256((R/m['artifact']).read_bytes()).hexdigest()==m['sha256']
e=a.filter(pl.col('source').str.starts_with('ine_epa_annual')).pivot(on='series_id',index='year',values='value')
assert e['year'].min()==2006 and e['year'].max()==2025
assert (e['INE.EPA.ANNUAL.ACTIVOS']-e['INE.EPA.ANNUAL.OCUPADOS']-e['INE.EPA.ANNUAL.PARADOS']).abs().max()<.11
n=nbformat.read(R/'notebooks/02_revision_espana.ipynb',as_version=4);nbformat.validate(n)
code=[x for x in n.cells if x.cell_type=='code'];assert all(x.execution_count for x in code)
assert not any(o.output_type=='error' for x in code for o in x.outputs)
appendix=[x for x in code if x.source.startswith('show(')];assert len(appendix)==31
assert all(any('image/png' in o.get('data',{}) for o in x.outputs) for x in appendix)
# Pruebas específicas de las correspondencias añadidas y del lector trimestral.
for code in ['ESP.1.1.0.0.OVGM','ESP.1.1.0.0.OVG0','ESP.1.0.0.0.UKCG','ESP.1.0.0.0.UIGG']:
 assert code in set(a['series_id'])
assert c.filter(pl.col('status')=='EXCLUIDA_NO_PUBLICADA_EDICION_ACTUAL').height==2
rr=pl.read_csv(R/'output/revision_espana/filas_reconciliadas.csv')
assert rr.filter((pl.col('sheet')=='NOMINAL')&(pl.col('row')==22))['source_reference'][0]=='ESP.1.0.0.0.UKCG'
assert rr.filter((pl.col('sheet')=='Quebras')&(pl.col('row')==20))['first'][0]==1990
qc=pl.read_csv(R/'output/revision_espana/excel_empresas_comprobacion_anual.csv')
assert qc.height==56 and qc['quarters_available'].min()==4 and qc['difference'].abs().max()==0
cei=a.filter(pl.col('series_id').str.starts_with('INE.CEI.')).pivot(on='series_id',index='year',values='value')
assert (cei['INE.CEI.P1']-cei['INE.CEI.P2']-cei['INE.CEI.B1G']).abs().max()==0
assert (cei['INE.CEI.B1G']+cei['INE.CEI.D21-D31']-cei['INE.CEI.B1GQ']).abs().max()==0
verify('v0_2026-10-16')
print('OK: selección por decisión; 10 cambios de base aceptados; valores AMECO intactos; vista anual sin forecast; identidades EPA/producción; 56 agregados trimestrales; hashes; notebook ejecutado y 31 figuras; v0 intacto.')
