"""Silver de España y catálogo vigente; conserva valores y decisiones por separado."""
from pathlib import Path
import csv,json,hashlib
import polars as pl
from catalogue import read_excel
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/revision_espana'; SILVER=ROOT/'datos/silver'
def manifest(id):
 m=json.loads((ROOT/f'datos/bronze/{id}/latest.json').read_text())
 assert hashlib.sha256((ROOT/m['artifact']).read_bytes()).hexdigest()==m['sha256']
 return m

def build():
 OUT.mkdir(parents=True,exist_ok=True)
 policy=json.loads((ROOT/'datos/catalogo/decisiones_espana.json').read_text())
 audit=pl.read_csv(ROOT/'output/revision_equivalencias/ameco_decisiones.csv').filter(pl.col('country')=='ESP')
 source=pl.read_parquet(SILVER/'ampliacion_20261019/ameco_reference_codes.parquet').filter(pl.col('country')=='ESP')
 am=manifest('ameco_spring2026');cat=[]
 for r in audit.iter_rows(named=True):
  status=r['status'];reason='Coincidencia numérica con la referencia en años comunes.' if status=='ACEPTADA_COINCIDENCIA_NUMERICA' else 'Revisión visual y documental pendiente en notebook.'
  if status==policy['base_changes']['initial_status']:
   status=policy['base_changes']['final_status'];reason=policy['base_changes']['note']
  manual=policy['manual_decisions'].get(r['code'])
  if manual:
   assert manual.get('note') and manual.get('action') in ['accept_current_edition','keep_pending']
   if manual['action']=='accept_current_edition':status='ACEPTADA_REVISION_MANUAL';reason=manual['note']
  if r['code'] in policy.get('excluded_current_codes',{}):
   status='EXCLUIDA_NO_PUBLICADA_EDICION_ACTUAL';reason=policy['excluded_current_codes'][r['code']]['note']
  d=source.filter(pl.col('code')==r['code'])
  cat.append(dict(series_id=r['code'],source='ameco_spring2026',source_code=r['code'],name=r['new_title'] or r['original_title'],unit=r['new_units'],original_unit=r['original_units'],excel_sheet=r['sheet'],excel_row=r['row'],initial_status=r['status'],status=status,apta_analisis=status.startswith('ACEPTADA'),decision_note=reason,first=d['year'].min() if d.height else None,last=d['year'].max() if d.height else None,n=d.height,bronze_sha256=am['sha256'],source_url=am['url']))
 catalog=pl.DataFrame(cat,infer_schema_length=None)
 source=source.join(catalog.select(pl.col('series_id').alias('code'),'status','apta_analisis'),on='code',validate='m:1')
 source=source.select('country','year',pl.col('code').alias('series_id'),'value','unit',pl.col('title').alias('name'),'source',pl.col('code').alias('source_code'),'bronze_sha256','forecast_period','status','apta_analisis',pl.lit(None,dtype=pl.String).alias('population_basis'),pl.lit(None,dtype=pl.Int64).alias('source_type_flag'),pl.lit(None,dtype=pl.Int64).alias('source_period_flag'))
 epa=[];epa_cat=[]
 for label,table in [('activos','65949'),('ocupados','65962'),('parados','65994')]:
  m=manifest('ine_epa_annual_'+label); raw=json.loads((ROOT/m['artifact']).read_text())
  matches=[r for r in raw if r['Nombre'].strip()==f'Total Nacional. Ambos sexos. 16 y más años. {label.capitalize()}. Personas.']
  assert len(matches)==1,(label,'Filtro ambiguo')
  r=matches[0];assert r['FK_Unidad']==3 and r['FK_Escala']==4
  series='INE.EPA.ANNUAL.'+label.upper();vals=[]
  for v in r['Data']:
   assert v['FK_Periodo']==28
   if v['Valor'] is None or v.get('Secreto'):continue
   vals.append(v)
   epa.append(dict(country='ESP',year=v['Anyo'],series_id=series,value=float(v['Valor']),unit='thousand_persons',name=r['Nombre'],source='ine_epa_annual_'+label,source_code=r['COD'],bronze_sha256=m['sha256'],forecast_period=False,status='ACEPTADA_FUENTE_INE_ACTUAL',apta_analisis=True,population_basis='2011' if v['Anyo']<=2020 else '2021',source_type_flag=v['FK_TipoDato'],source_period_flag=v['FK_Periodo']))
  epa_cat.append(dict(series_id=series,source='ine_epa_annual_'+label,source_code=r['COD'],name=r['Nombre'],unit='thousand_persons',original_unit='Miles personas (cabecera oficial); FK_Unidad=3, FK_Escala=4',excel_sheet='mercado traballo' if label=='parados' else '',excel_row=29 if label=='parados' else None,initial_status='ORIGEN_EXCEL_NO_RECONSTRUIDO' if label=='parados' else 'COMPLEMENTO_INE_UNIVERSO_EPA',status='ACEPTADA_FUENTE_INE_ACTUAL',apta_analisis=True,decision_note=policy['ine_epa_policy'],first=min(v['Anyo'] for v in vals),last=max(v['Anyo'] for v in vals),n=len(vals),bronze_sha256=m['sha256'],source_url=m['url']))
 catalog=pl.concat([catalog,pl.DataFrame(epa_cat,infer_schema_length=None)],how='diagonal_relaxed')
 data=pl.concat([source,pl.DataFrame(epa,infer_schema_length=None)],how='diagonal_relaxed').sort(['series_id','year'])
 assert not data.select(pl.struct(['series_id','year']).is_duplicated().any()).item()
 assert data['value'].is_finite().all()
 from spain_supplement import extend
 if (SILVER/'ampliacion_20261019/ameco_conceptos_recuperados.parquet').exists():
  data,catalog=extend(data,catalog)
 recovered=pl.read_parquet(SILVER/'espana_fuentes_recuperadas.parquet')
 recovered_catalog=pl.read_parquet(SILVER/'espana_fuentes_recuperadas_catalogo.parquet')
 assert not set(data['series_id']) & set(recovered['series_id'])
 data=pl.concat([data,recovered],how='diagonal_relaxed').sort(['series_id','year'])
 catalog=pl.concat([catalog,recovered_catalog],how='diagonal_relaxed').sort('series_id')
 assert not data.select(pl.struct(['series_id','year']).is_duplicated().any()).item()
 data.write_parquet(SILVER/'espana.parquet');data.write_csv(SILVER/'espana.csv')
 catalog.write_csv(OUT/'catalogo_espana.csv');catalog.write_parquet(SILVER/'espana_catalogo.parquet')
 # Vista analítica: solo series aceptadas y años anteriores al horizonte de previsión.
 view=data.filter(pl.col('apta_analisis')&~pl.col('forecast_period')).pivot(on='series_id',index=['country','year'],values='value').sort('year')
 view.write_parquet(SILVER/'espana_anual.parquet');view.write_csv(SILVER/'espana_anual.csv')
 _,_,other=read_excel(next((ROOT/'datos').glob('*.xls')))
 evidence=next(r for r in other if r['sheet']=='mercado traballo' and r['row']==29)
 (OUT/'excel_fila29_evidencia.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
 # Contraste de filas 28 y 29 con INE, sin empalmarlas.
 comparisons=[];unemp={r['year']:r['value'] for r in epa if r['series_id']=='INE.EPA.ANNUAL.PARADOS'}
 for row in [28,29]:
  original=next(r for r in other if r['sheet']=='mercado traballo' and r['row']==row)
  for y,v in original['values'].items():
   year=int(y)
   if year in unemp:comparisons.append(dict(excel_row=row,year=year,excel=v,ine=unemp[year],difference=unemp[year]-v,unit='thousand_persons'))
 pl.DataFrame(comparisons).write_csv(OUT/'epa_comparacion_excel.csv')
 # Cada fila sin código se conserva para que 76 códigos AMECO no se interpreten como todo el Excel.
 from diagnose_core import BASE
 uncoded=[{k:v for k,v in x.items() if k not in ['values','period_values']} for x in other if x['sheet'] in BASE]
 pl.DataFrame(uncoded).write_csv(OUT/'filas_sin_codigo_inventario.csv')
 summary=dict(version='2026-10-21',ameco_target_spain=audit.height,ameco_recovered=data.filter(pl.col('source')=='ameco_spring2026')['series_id'].n_unique(),ameco_accepted=catalog.filter((pl.col('source')=='ameco_spring2026')&pl.col('apta_analisis')).height,ameco_review_notebook=catalog.filter((pl.col('source')=='ameco_spring2026')&~pl.col('apta_analisis')&(pl.col('n')>0)).height,ameco_missing=catalog.filter((pl.col('source')=='ameco_spring2026')&(pl.col('status')=='PENDIENTE_CODIGO_NO_RECUPERADO')).height,ameco_excluded=catalog.filter(pl.col('status')=='EXCLUIDA_NO_PUBLICADA_EDICION_ACTUAL').height,ine_added=3,long_observations=data.height,analytic_series=view.width-2,analytic_years=view.height,status_counts=catalog.group_by('status').len().to_dicts(),scope='Fuentes recuperadas integradas; AMECO explícito y localizado por concepto, EPA, PWT, cuentas INE y componentes salariales Eurostat. Clasificación completa de las 69 filas sin código en filas_reconciliadas.csv; los huecos históricos y diferencias de universo se documentan por separado.',provenance_note='La fila 29 no se usa como fuente de datos analíticos; la serie INE es nueva y documentada. Cobertura EPA 2006–2025, sin relleno anterior.',policy=policy)
 summary['ameco_added_by_concept']=catalog.filter((pl.col('source')=='ameco_spring2026')&(pl.col('initial_status')=='SIN_CODIGO_EXPLICITO_EN_FILA')).height
 summary['ameco_total_catalogue']=catalog.filter(pl.col('source')=='ameco_spring2026').height
 summary['series_by_source']=data.group_by('source').agg(pl.col('series_id').n_unique().alias('series')).sort('source').to_dicts()
 # La clasificación de cada fila y su integración son estados distintos.
 reconciled=OUT/'filas_reconciliadas.csv'
 if reconciled.exists():
  rr=pl.read_csv(reconciled).to_dicts();ids=set(data['series_id'])
  row_ids={2:'INE.CEI.P1',3:'INE.CEI.P2',4:'INE.CEI.D21-D31',5:'INE.CEI.B1GQ',13:'INE.CEI.B1G',15:'EUROSTAT.CNA.D11',16:'EUROSTAT.CNA.D12',17:'INE.CNA.D29_MINUS_D39'}
  for x in rr:
   ref=x.get('source_reference')
   if x['sheet']=='mercado traballo' and x['row'] in [22,23]:ref='PWT11.'+('EMP' if x['row']==22 else 'AVH')
   if x['sheet']=='Produzón-CI-VA':ref=row_ids.get(x['row'],ref)
   mapping={('POP',21):'INE.MNP.DEATHS.RESIDENCE',('POP',33):'INE.MNP.BIRTHS.REGISTRATION',('POP',36):'INE.MNP.BIRTHS.REGISTRATION',('POP',45):'INE.MNP.MARRIAGES.DIFFERENT_SEX',('i-e',15):'WDI.FX.ESP.LCU_USD',('i-e',16):'WDI.FX.EMU.LCU_USD',('mercado traballo',27):'SEPE.REGISTERED.UNEMPLOYED.ANNUAL_MEAN',('mercado traballo',32):'MITES.SMI.MONTHLY_RATE.ANNUAL_MEAN',('Quebras',3):'INE.HIST.BANKRUPTCIES.TOTAL',('Quebras',4):'INE.HIST.SUSPENSIONS.TOTAL',('Quebras',20):'INE.HIST.SUSPENSIONS.TOTAL',('Quebras',21):'INE.HIST.SUSPENSIONS.ASSETS',('Quebras',22):'INE.HIST.SUSPENSIONS.LIABILITIES',('Quebras',49):'INE.HIST.BANKRUPTCIES.TOTAL'}
   ref=mapping.get((x['sheet'],x['row']),ref)
   x['silver_reference']=ref if ref in ids else None
   x['integration_status']='INTEGRADA_O_REFERENCIADA' if ref in ids else 'NO_REQUIERE_INPUT_INDEPENDIENTE' if x['status'].startswith(('IGNORAR','DERIVADA','DUPLICADA')) else 'FUENTE_IDENTIFICADA_PENDIENTE'
   if (x['sheet'],x['row']) in [('POP',21),('Quebras',3),('Quebras',4),('mercado traballo',27),('mercado traballo',29)]:x['integration_status']='INTEGRADA_COBERTURA_HISTORICA_PARCIAL'
   if x['sheet']=='Money' and x['row'] in [4,5,6,7]:
    x['silver_reference']={4:'IMF.IFS.M3.ANNUAL_MEAN',5:'IMF.IFS.M1.ANNUAL_MEAN',6:'IMF.IFS.M2.ANNUAL_MEAN',7:'BDE.HIST.BM.YEAR_END'}[x['row']]
    x['integration_status']='ALTERNATIVA_INTEGRADA_NO_EQUIVALENCIA_MOISEES'
   if x['sheet']=='Quebras' and x['row']==50:x['integration_status']='DETALLE_SUBANUAL_ARCHIVADO'
  rd=pl.DataFrame(rr,infer_schema_length=None);rd.write_csv(reconciled);rd.write_parquet(OUT/'filas_reconciliadas.parquet')
 (OUT/'resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='policy'},ensure_ascii=False,indent=2))
 return data,catalog
if __name__=='__main__':build()
