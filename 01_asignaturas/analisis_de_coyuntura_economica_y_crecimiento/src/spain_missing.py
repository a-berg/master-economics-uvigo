"""Normaliza fuentes recuperadas para España; anualiza solo periodos completos."""
from pathlib import Path
from datetime import date
from collections import defaultdict
import json,csv,re,io,zipfile,hashlib,html,statistics
import polars as pl
import xlrd
from python_calamine import CalamineWorkbook
R=Path(__file__).resolve().parents[1];OUT=R/'output/revision_espana';SILVER=R/'datos/silver'

def manifest(id):
 m=json.loads((R/f'datos/bronze/{id}/latest.json').read_text());p=R/m['artifact']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']
 return m,p

def build():
 annual=[];periods=[];catalog=[];notes=[];aggregation=[]
 def add(series,source,code,name,unit,values,note,aggregation_method='none',status='ACEPTADA_FUENTE_OFICIAL',apta=True):
  m,p=manifest(source);rows=[]
  for y,v,*extra in values:
   row=dict(country='ESP',year=int(y),series_id=series,value=float(v),unit=unit,name=name,source=source,source_code=code,bronze_sha256=m['sha256'],forecast_period=False,status=status,apta_analisis=apta,population_basis=None,source_type_flag=extra[0] if extra else None,source_period_flag=28,source_flag=None,source_locator=code,transformation=aggregation_method,definition_note=note)
   annual.append(row);rows.append(row)
  if not rows:return
  catalog.append(dict(series_id=series,source=source,source_code=code,name=name,unit=unit,original_unit=unit,excel_sheet=None,excel_row=None,initial_status='FUENTE_IDENTIFICADA_PENDIENTE',status=status,apta_analisis=apta,decision_note=note,first=min(x['year'] for x in rows),last=max(x['year'] for x in rows),n=len(rows),bronze_sha256=m['sha256'],source_url=m['url']))
 def ine_series(source,exact,series,name,unit='count'):
  m,p=manifest(source);raw=json.loads(p.read_text());matches=[r for r in raw if r['Nombre'].strip()==exact.strip()]
  assert len(matches)==1,(source,exact,len(matches));s=matches[0]
  vals=[(v['Anyo'],v['Valor'],v.get('FK_TipoDato')) for v in s['Data'] if v['Valor'] is not None and not v.get('Secreto') and v['FK_Periodo']==28]
  assert len(vals)==len(s['Data']),(source,'Periodicidad no anual o huecos')
  add(series,source,s['COD'],name,unit,vals,s['Nombre']+f" FK_Unidad={s['FK_Unidad']}; FK_Escala={s['FK_Escala']}. No se empalma con otros universos.")
 ine_series('ine_deaths_residence_20261020','Total Nacional. Defunción. Total. Todas las edades. Lugar de residencia. Dato base.','INE.MNP.DEATHS.RESIDENCE','Defunciones, residencia, total nacional')
 ine_series('ine_deaths_historical_20261020','Total Nacional. Defunción. Total. Todas las edades. Lugar de inscripción. Dato base.','INE.MNP.DEATHS.REGISTRATION.HIST','Defunciones históricas, inscripción, total nacional')
 ine_series('ine_births_registration_20261020','Total Nacional. Nacimiento. Total. Todas las edades. Total. Lugar de inscripción. Dato base.','INE.MNP.BIRTHS.REGISTRATION','Nacimientos, inscripción, total nacional')
 ine_series('ine_marriages_different_sex_20261020','Total Nacional. Matrimonio diferente sexo. Total. Todas las edades. Total. Lugar de residencia. Dato base.','INE.MNP.MARRIAGES.DIFFERENT_SEX','Matrimonios de diferente sexo, residencia')
 ine_series('ine_insolvency_20261020','Total Nacional. Total CNAE. Total de personas y empresas. Empresas. Anual.','INE.INSOLVENCY.ENTERPRISES','Empresas concursadas, total nacional')
 ine_series('ine_sector_accounts_20261020','Total Nacional. Otros impuestos netos sobre la producción. Total CNAE. Precios corrientes. Dato base.','INE.CNA.D29_MINUS_D39','Otros impuestos netos sobre la producción','million_EUR_current')
 for row in annual:
  if row['series_id']=='INE.INSOLVENCY.ENTERPRISES' and row['year']==2004:
   row['source_flag']='PARTIAL_YEAR_LAST_FOUR_MONTHS'
   row['apta_analisis']=False
   row['status']='PERIODO_PARCIAL_EXCLUIDO_VISTA_ANALITICA'
   row['definition_note']+=' 2004: solo últimos cuatro meses; no comparable con un año completo.'
 for row in catalog:
  if row['series_id']=='INE.INSOLVENCY.ENTERPRISES':row['decision_note']+=' 2004 cubre solo los últimos cuatro meses.'
 # Tipo de cambio: monedas y territorios explícitos; no se fabrica una continuidad peseta/euro.
 src='wdi_fx_esp_emu_20261020';m,p=manifest(src);raw=json.loads(p.read_text());assert isinstance(raw,list) and len(raw)==2
 for country,unit,last in [('ESP','pesetas_per_USD',1998),('EMU','EUR_per_USD',2025)]:
  vals=[(int(v['date']),v['value']) for v in raw[1] if v['countryiso3code']==country and v['value'] is not None and int(v['date'])<=last and (country=='ESP' or int(v['date'])>=1999)]
  add('WDI.FX.'+country+'.LCU_USD',src,'PA.NUS.FCRF;'+country,'Cambio oficial medio '+('España, peseta/USD' if country=='ESP' else 'zona euro, EUR/USD'),unit,vals,'Promedio del periodo. EMU es zona euro, usada como tipo de cambio de la moneda común; no se etiqueta como medición exclusivamente española.')
 # Históricos de empresas: cantidades y unidades extraídas de cada etiqueta, no de la posición.
 business=[]
 for source,short in [('ine_suspensions_historical_20261020','SUSPENSIONS'),('ine_bankruptcies_historical_20261020','BANKRUPTCIES')]:
  m,p=manifest(source);reader=csv.DictReader(io.StringIO(p.read_text(encoding='utf-8-sig')),delimiter=';');groups=defaultdict(list)
  for r in reader:
   label=r['Series'].strip();period=r['Periodo'].strip();rawvalue=r['Total'].strip()
   if rawvalue in ['', '.', '..','...']:continue
   v=float(rawvalue.replace('.','').replace(',','.'))
   assert re.fullmatch(r'\d{4}Q[1-4]',period)
   business.append(dict(source=source,label=label,period=period,value=v))
   if short=='SUSPENSIONS':
    key={'Suspensiones. Total':'TOTAL','ACTIVO (miles euros)':'ASSETS','PASIVO (miles euros)':'LIABILITIES'}.get(label)
   else:key={'TOTAL quiebras':'TOTAL','ACTIVO (miles euros)':'ASSETS','PASIVO (miles euros)':'LIABILITIES'}.get(label)
   if not key:continue
   unit='count' if key=='TOTAL' else 'thousand_EUR';series='INE.HIST.'+short+'.'+key
   groups[(series,unit)].append((period,v))
   periods.append(dict(country='ESP',series_id=series,period=period,frequency='Q',value=v,unit=unit,source=source,bronze_sha256=m['sha256'],source_locator=label))
  for (series,unit),values in groups.items():
   years=defaultdict(dict)
   for per,v in values:years[int(per[:4])][int(per[-1])]=v
   vals=[]
   for y,qs in sorted(years.items()):
    aggregation.append(dict(series_id=series,year=y,n_periods=len(qs),required=4,included=len(qs)==4))
    if len(qs)==4:vals.append((y,sum(qs.values())))
   add(series,source,series,series,unit,vals,'Flujo anual: suma de cuatro trimestres completos. No se empalma con empresas concursadas del régimen posterior. Los periodos parciales permanecen en tabla subanual.','sum_four_quarters')
 pl.DataFrame(business).write_parquet(OUT/'empresas_historicas_detalle.parquet')
 # SEPE: los archivos del proveedor requieren lectores distintos; originales intactos.
 monthly=[]
 for source in ['sepe_registered_2001_2016_20261020','sepe_registered_2017_current_20261020']:
  m,p=manifest(source)
  if source.startswith('sepe_registered_2001'):
   sheet=xlrd.open_workbook(p).sheet_by_name('Sectores');rows=[sheet.row_values(i) for i in range(sheet.nrows)]
  else:rows=CalamineWorkbook.from_path(str(p)).get_sheet_by_name('Sectores').to_python()
  yearcol,datecol=(1,2) if source.startswith('sepe_registered_2001') else (0,1)
  month_names={name:i for i,name in enumerate(['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE'],1)}
  active_year=None;sequential_count=0;first_year=2001 if source.startswith('sepe_registered_2001') else 2017
  for rn,row in enumerate(rows,1):
   if len(row)<=datecol+2:continue
   if isinstance(row[yearcol],(int,float)) and 2001<=row[yearcol]<=2026:active_year=int(row[yearcol])
   month=month_names.get(str(row[datecol+1]).strip().upper())
   if month is None or active_year is None:continue
   assert isinstance(row[datecol+2],(int,float)),(source,rn)
   selected_year=first_year+sequential_count//12;expected_month=sequential_count%12+1;sequential_count+=1
   assert month==expected_month,(source,rn,'Secuencia de meses incompleta')
   token=row[datecol];token_year=int(token)//100 if isinstance(token,(int,float)) else None
   assert selected_year in [active_year,token_year],(source,rn,'Ningún campo respalda el año cronológico')
   per=f'{selected_year}-{month:02}';value=float(row[datecol+2])
   if token_year!=selected_year or active_year!=selected_year:
    notes.append(dict(source=source,row=rn,issue='INCONSISTENT_YEAR_FIELDS',raw_token=str(token),year_block=active_year,selected_period=per,reason='Secuencia enero-diciembre contrastada con rango del archivo y al menos uno de los dos campos de año; no sobrescribir otro año.'))
   monthly.append(dict(source=source,period=per,value=value,row=rn))
   periods.append(dict(country='ESP',series_id='SEPE.REGISTERED.UNEMPLOYED',period=per,frequency='M',value=value,unit='persons',source=source,bronze_sha256=m['sha256'],source_locator=f'Sectores row {rn}'))
 assert len(monthly)==len({x['period'] for x in monthly}), 'Mes SEPE repetido'
 for source in sorted({x['source'] for x in monthly}):
  groups=defaultdict(dict)
  for x in monthly:
   if x['source']==source:groups[int(x['period'][:4])][x['period']]=x['value']
  vals=[]
  for y,months in sorted(groups.items()):
   aggregation.append(dict(series_id='SEPE.REGISTERED.UNEMPLOYED.ANNUAL_MEAN',year=y,n_periods=len(months),required=12,included=len(months)==12))
   if len(months)==12:vals.append((y,statistics.mean(months.values())))
  add('SEPE.REGISTERED.UNEMPLOYED.ANNUAL_MEAN',source,'registered_total','Paro registrado, media de doce meses','persons',vals,'Total nacional. No es paro EPA. Antes de mayo de 2005 existen reconstrucciones SISPE; conservar notas del original. XLS de 2017+ leído con Calamine por cabecera no estándar.','mean_twelve_months')
 # SMI: conservar fechas publicadas y corregir retroactividad 2023 según BOE, expresamente.
 source='mites_smi_public_20261020';m,p=manifest(source);sheet=xlrd.open_workbook(p).sheet_by_name('smi');events=[];romans={'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,'XI':11,'XII':12}
 for i in range(sheet.nrows):
  row=sheet.row_values(i);match=re.fullmatch(r'(\d{1,2})-([IVX]+)-(\d{4})',str(row[0]).strip())
  if not match or not isinstance(row[5],(int,float)):continue
  d=date(int(match[3]),romans[match[2]],int(match[1]));effective=date(2023,1,1) if d==date(2023,2,14) else d
  events.append(dict(source_row=i+1,published_effective_date=d.isoformat(),effective_date=effective.isoformat(),monthly_eur=row[5],annual_eur=row[6],norm=' '.join(str(v) for v in row[1:4]),override_evidence='https://www.boe.es/eli/es/rd/2023/02/14/99' if d!=effective else None))
 assert next(e for e in events if e['effective_date']=='2026-01-01')['monthly_eur']==1221
 pl.DataFrame(events,infer_schema_length=None).write_csv(OUT/'smi_effective_dates.csv')
 vals_by_year=defaultdict(list)
 for y in range(1980,2026):
  for month in range(1,13):
   active=[e for e in events if date.fromisoformat(e['effective_date'])<=date(y,month,1)]
   if not active:continue
   e=max(active,key=lambda e:e['effective_date']);v=e['monthly_eur'];vals_by_year[y].append(v)
   periods.append(dict(country='ESP',series_id='MITES.SMI.MONTHLY_RATE',period=f'{y}-{month:02}',frequency='M',value=v,unit='EUR_per_month_14_payments',source=source,bronze_sha256=m['sha256'],source_locator=f"smi row {e['source_row']}"))
 note='Tasa mensual legal (14 pagas), no salario medio observado. Hasta 1998, trabajadores de 18+; cambios de edad documentados. 2023 retroactivo a enero por BOE. Archivo público recuperado con limitación TLS declarada en manifiesto; cuantía 2026 contrastada con BOE.'
 add('MITES.SMI.MONTHLY_RATE.ANNUAL_MEAN',source,'smi monthly legal rate','SMI mensual legal, promedio anual','EUR_per_month_14_payments',[(y,statistics.mean(v)) for y,v in vals_by_year.items() if len(v)==12],note,'mean_twelve_legal_monthly_rates')
 add('MITES.SMI.MONTHLY_RATE.YEAR_END',source,'smi monthly legal rate at December','SMI mensual legal de diciembre','EUR_per_month_14_payments',[(y,v[-1]) for y,v in vals_by_year.items()],note,'December_legal_monthly_rate')
 # FRED: redistribución oficial de datos IMF/IFS, diferenciada de los originales docentes MOISEES.
 for key in ['M1','M2','M3']:
  source='fred_imf_spain_myag'+key.lower()+'esm189n';m,p=manifest(source);t=p.read_text()
  cells=re.findall(r'<th\b[^>]*>\s*(\d{4}-\d{2}-\d{2})\s*</th>\s*<td\b[^>]*>\s*([^<]+)</td>',t,re.S)
  assert len(cells)==444,(source,len(cells));groups=defaultdict(dict)
  for per,v in cells:
   value=float(html.unescape(v).strip().replace(',',''));groups[int(per[:4])][per[:7]]=value
   periods.append(dict(country='ESP',series_id='IMF.IFS.'+key,period=per[:7],frequency='M',value=value,unit='pesetas',source=source,bronze_sha256=m['sha256'],source_locator='MYAG'+key+'ESM189N'))
  add('IMF.IFS.'+key+'.ANNUAL_MEAN',source,'MYAG'+key+'ESM189N',key+' España (IMF/IFS vía FRED), media anual','pesetas',[(y,statistics.mean(v.values())) for y,v in groups.items() if len(v)==12],'Fuente IMF/IFS redistribuida por Reserva Federal de St. Louis, adicional a las fuentes docentes. Mensual sin ajuste estacional; moneda nacional pre-euro. No se presenta como reproducción exacta de MOISEES ni se prolonga con zona euro.','mean_twelve_months')
  add('IMF.IFS.'+key+'.YEAR_END',source,'MYAG'+key+'ESM189N',key+' España (IMF/IFS vía FRED), diciembre','pesetas',[(y,v[f'{y}-12']) for y,v in groups.items() if f'{y}-12' in v],'Stock de diciembre; separado del promedio anual y de variantes BdE.','December_stock')
 # BdE: BM y M3 observados en el anexo histórico. 1998 es octubre, no un cierre anual.
 source='bde_money_statistical_annex_2018';m,p=manifest(source);z=zipfile.ZipFile(p);member='Monetary-Statistics-1962-1998.xls';book=xlrd.open_workbook(file_contents=z.read(member))
 tables={}
 for sheetname,ycol,vcol,key in [('High-powered money',6,11,'BM'),('Money supply',0,4,'M3')]:
  sheet=book.sheet_by_name(sheetname);vals=[];allvals=[]
  for i in range(sheet.nrows):
   row=sheet.row_values(i);v=row[ycol];match=re.match(r'^(19\d{2})',str(v))
   if not match or not isinstance(row[vcol],(int,float)):continue
   year=int(match[1]);value=float(row[vcol]);allvals.append((year,value))
   if year<1998:vals.append((year,value))
   else:periods.append(dict(country='ESP',series_id='BDE.HIST.'+key,period='1998-10',frequency='M',value=value,unit='million_pesetas',source=source,bronze_sha256=m['sha256'],source_locator=member+';'+sheetname+';October'))
  tables[key]=dict(vals)
  add('BDE.HIST.'+key+'.YEAR_END',source,member+';'+sheetname,key+' histórico España, cierre anual (BdE)','million_pesetas',vals,'Reconstrucción de Martín-Aceña 2018, publicada por BdE. Definiciones históricas y cambio de M3 alrededor de 1990/1992. Última fila 1998 corresponde a octubre y se conserva separada, no se anualiza.','year_end_original')
 ratio=[(y,tables['M3'][y]/v) for y,v in tables['BM'].items() if y in tables['M3'] and v]
 add('BDE.HIST.M3_BM.YEAR_END',source,'V4.M3/V3.BM','Multiplicador M3/BM, variante histórica BdE','ratio',ratio,'Cociente de stocks de cierre publicados en el mismo anexo; no equivale al cociente de promedios MOISEES.','M3_year_end/BM_year_end')
 # Persistencia y control: una serie anual SEPE puede usar dos originales, pero no dos valores/año.
 df=pl.DataFrame(annual,infer_schema_length=None);cf=pl.DataFrame(catalog,infer_schema_length=None)
 assert not df.select(pl.struct(['series_id','year']).is_duplicated().any()).item()
 assert df['value'].is_finite().all()
 # Unir metadatos de la serie SEPE multiarchivo manteniendo evidencia completa por fila.
 merged=[]
 for series in cf['series_id'].unique():
  group=cf.filter(pl.col('series_id')==series);row=group.row(0,named=True)
  if group.height>1:
   row.update(first=group['first'].min(),last=group['last'].max(),n=group['n'].sum(),source=';'.join(group['source']),source_url=';'.join(group['source_url']),bronze_sha256=';'.join(group['bronze_sha256']))
  merged.append(row)
 df.write_parquet(SILVER/'espana_fuentes_recuperadas.parquet');pl.DataFrame(merged,infer_schema_length=None).write_parquet(SILVER/'espana_fuentes_recuperadas_catalogo.parquet')
 pl.DataFrame(periods,infer_schema_length=None).write_parquet(SILVER/'espana_periodos.parquet')
 pl.DataFrame(aggregation).write_csv(OUT/'periodos_completos_anualizacion.csv')
 coverage=df.group_by(['series_id','unit','source']).agg(pl.col('year').min().alias('first'),pl.col('year').max().alias('last'),pl.len().alias('n')).sort('series_id')
 coverage.write_csv(OUT/'fuentes_recuperadas_cobertura.csv')
 if notes:pl.DataFrame(notes).write_csv(OUT/'source_anomalies.csv')
 print(coverage)
 return df,pl.DataFrame(merged,infer_schema_length=None)
if __name__=='__main__':build()
