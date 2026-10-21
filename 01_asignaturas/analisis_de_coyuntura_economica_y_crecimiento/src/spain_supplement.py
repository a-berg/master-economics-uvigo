"""Integra series localizadas por concepto y fuentes ya descargadas, sin empalmes."""
from pathlib import Path
import json
import polars as pl
R=Path(__file__).resolve().parents[1]

def extend(data,catalog):
 extra=pl.read_parquet(R/'datos/silver/ampliacion_20261019/ameco_conceptos_recuperados.parquet')
 mapping=pl.read_csv(R/'output/revision_espana/filas_reconciliadas.csv').filter(pl.col('status')=='AMECO_CONCEPTO_CONFIRMADO')
 records=[]; cats=[]
 def add(series,source,code,name,unit,rows,sheet='',row=None,note='',locator='',transformation='none'):
  if series in set(catalog['series_id']):return
  vals=list(rows)
  if not vals:return
  for v in vals:
   records.append(dict(country='ESP',year=v['year'],series_id=series,value=v['value'],unit=unit,name=name,source=source,source_code=code,bronze_sha256=v['bronze_sha256'],forecast_period=v.get('forecast_period',False),status='ACEPTADA_CONCEPTO_Y_FUENTE',apta_analisis=True,population_basis=None,source_type_flag=None,source_period_flag=None,source_flag=v.get('flag'),source_locator=v.get('dimensions',locator),transformation=transformation))
  meta=json.loads((R/f'datos/bronze/{source}/latest.json').read_text())
  cats.append(dict(series_id=series,source=source,source_code=code,name=name,unit=unit,original_unit=None,excel_sheet=sheet,excel_row=row,initial_status='SIN_CODIGO_EXPLICITO_EN_FILA',status='ACEPTADA_CONCEPTO_Y_FUENTE',apta_analisis=True,decision_note=note,first=min(v['year'] for v in vals),last=max(v['year'] for v in vals),n=len(vals),bronze_sha256=vals[0]['bronze_sha256'],source_url=meta['url']))
 for code in extra['code'].unique().sort():
  d=extra.filter(pl.col('code')==code);m=mapping.filter(pl.col('source_reference')==code).row(0,named=True)
  add(code,'ameco_spring2026',code,d['title'][0],d['unit'][0],d.to_dicts(),m['sheet'],m['row'],'Concepto confirmado por título, sector, precios y unidad en catálogo AMECO completo; edición vigente adoptada. '+(m['decision_note'] or ''),d['zip_member'][0])
 raw=pl.read_parquet(R/'datos/silver/observations.parquet').filter(pl.col('country')=='ESP')
 for key,unit,name,row in [('emp','million_persons','Personas ocupadas (PWT 11)',22),('avh','hours_per_person_year','Horas anuales medias por persona ocupada (PWT 11)',23)]:
  d=raw.filter((pl.col('source')=='pwt110')&(pl.col('series')==key))
  add('PWT11.'+key.upper(),'pwt110',key,name,unit,d.to_dicts(),'mercado traballo',row,'Adoptar PWT 11 vigente. Excel cita 10.0; unidad y universo PWT preservados, sin sustituir empleo AMECO/EPA.')
 names={'output':('P1','Producción (P.1)',2),'intermediate_consumption':('P2','Consumos intermedios (P.2)',3),'product_taxes_net':('D21-D31','Impuestos netos sobre los productos',4),'gdp_market':('B1GQ','PIB a precios de mercado (cuentas integradas)',5),'ccf_nominal':('P51C','Consumo de capital fijo nominal (cuentas integradas)',None)}
 for key,(code,name,row) in names.items():
  d=raw.filter((pl.col('source')=='ine_integrated_accounts')&(pl.col('series')==key))
  add('INE.CEI.'+code,'ine_integrated_accounts',key,name,'million_EUR_current',d.to_dicts(),'Produzón-CI-VA',row,'Serie INE ya descargada; edición y fuente originales conservadas. No se declara que sea la última revisión de 2026.','Source!15–30')
 prod=raw.filter((pl.col('source')=='ine_integrated_accounts')&(pl.col('series')=='output')).select('year','value','bronze_sha256')
 ci=raw.filter((pl.col('source')=='ine_integrated_accounts')&(pl.col('series')=='intermediate_consumption')).select('year',pl.col('value').alias('ci'))
 derived=prod.join(ci,on='year',validate='1:1').with_columns((pl.col('value')-pl.col('ci')).alias('value'))
 add('INE.CEI.B1G','ine_integrated_accounts','P1-P2','VAB a precios básicos derivado: producción menos consumos intermedios','million_EUR_current',derived.to_dicts(),'Produzón-CI-VA',13,'Derivación con P1 y P2 de la misma edición de cuentas INE. No confundir con PIB de mercado.','P1;P2','P1-P2')
 for key,name,row in [('D11','Sueldos y salarios',15),('D12','Cotizaciones sociales a cargo de empleadores',16)]:
  vals=[]
  for v in raw.filter(pl.col('source')=='estat_nama_10_gdp').iter_rows(named=True):
   dims=json.loads(v['dimensions'])
   if dims.get('na_item')==key and dims.get('unit')=='CP_MEUR':vals.append(v)
  assert len(vals)==len({v['year'] for v in vals}),key
  add('EUROSTAT.CNA.'+key,'estat_nama_10_gdp',key,name,'million_EUR_current',vals,'Produzón-CI-VA',row,'Selección explícita na_item='+key+', unit=CP_MEUR, ESP, anual. No empalmar automáticamente con otra edición INE.')
 if records:
  data=pl.concat([data,pl.DataFrame(records,infer_schema_length=None)],how='diagonal_relaxed')
  catalog=pl.concat([catalog,pl.DataFrame(cats,infer_schema_length=None)],how='diagonal_relaxed')
 return data.sort(['series_id','year']),catalog.sort('series_id')
