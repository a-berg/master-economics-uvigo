"""Reconcilia las notas del alumno con conceptos, títulos y fuentes del Excel."""
import csv,json,re,hashlib,shutil,io
from pathlib import Path
import polars as pl
import xlrd
from catalogue import read_excel
from diagnose_core import BASE
from ameco_full_catalogue import build as index_build,extract
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/revision_espana'
RAW=ROOT/'datos/bronze/user_annotations_20261020'
INPUT=ROOT.parent/'anotaciones_usuario/filas_sin_codigo_inventario.csv'
MAP={('REAL',43):'ESP.1.1.0.0.OVGM',('REAL',44):'ESP.1.1.0.0.OVG0',('REAL',45):'ESP.1.1.0.0.OVG1',('REAL',46):'ESP.1.1.0.0.OVG2',('REAL',48):'ESP.1.1.0.0.OVG4',('REAL',49):'ESP.1.1.0.0.OVG5',('NOMINAL',7):'ESP.1.0.0.0.UIGG',('NOMINAL',8):'ESP.1.0.0.0.UIGP',('NOMINAL',22):'ESP.1.0.0.0.UKCG',('NOMINAL',24):'ESP.1.0.0.0.UQGD'}
ALIASES={('K',21):'ESP.1.0.0.0.UITT',('K',22):'ESP.1.0.0.0.UIGT',('K',24):'ESP.1.0.0.0.UIST',('K',27):'ESP.1.1.0.0.OITT',('K',28):'ESP.1.1.0.0.OIGT',('K',30):'ESP.1.0.0.0.OIST',('REAL',47):'ESP.1.1.0.0.OVGM'}

def build():
 OUT.mkdir(parents=True,exist_ok=True);RAW.mkdir(parents=True,exist_ok=True)
 original=RAW/'filas_sin_codigo_anotadas.csv'
 if not original.exists():shutil.copyfile(INPUT,original)
 digest=hashlib.sha256(original.read_bytes()).hexdigest()
 # El CSV mezcla texto UTF-8 con algunas notas en Windows-1252; preservar bytes originales.
 text=original.read_bytes().decode('utf-8-sig',errors='surrogateescape')
 text=''.join(bytes([ord(c)-0xdc00]).decode('cp1252') if 0xdc80<=ord(c)<=0xdcff else c for c in text)
 annotations=list(csv.DictReader(io.StringIO(text)))
 notes={(r['sheet'],int(r['row'])):r.get('Instrucciones para GPT','') for r in annotations}
 (RAW/'manifest.json').write_text(json.dumps(dict(provider='user',artifact=original.relative_to(ROOT).as_posix(),sha256=digest,received_date='2026-10-20',library_file_id='libfile_188947ddb3608191af487b2aa1171e5e',note='Original anotado conservado sin modificar; no es una descarga del proveedor estadístico.'),ensure_ascii=False,indent=2)+'\n')
 index=index_build()
 excel=next((ROOT/'datos').glob('*.xls'));book=xlrd.open_workbook(excel,formatting_info=True)
 sheet=book.sheet_by_name('Source');sources=[]
 for i in range(sheet.nrows):
  vals=[str(c.value) for c in sheet.row(i) if c.value!='']
  if vals:sources.append(dict(sheet='Source',row=i+1,text=' | '.join(vals),links=re.findall(r'https?://[^\s|]+',' '.join(vals))))
 for h in sheet.hyperlink_list:
  sources.append(dict(sheet='Source',row=h.frowx+1,text='hipervínculo de celda',links=[h.url_or_path]))
 (OUT/'excel_hoja_source.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
 inv,occ,other=read_excel(excel);records=[]
 # Todas las filas sin código de las diez hojas, incluidas las que no estaban en el CSV antiguo.
 for r in other:
  if r['sheet'] not in BASE:continue
  key=(r['sheet'],r['row']);note=notes.get(key,'');code=MAP.get(key) or ALIASES.get(key);status='FUENTE_DOCUMENTADA_PENDIENTE_INTEGRACION';source='';reference='';observation='';alt=''
  if note.strip().lower()=='ignorar':status='IGNORAR_COMO_INPUT_INDEPENDIENTE';observation='Decisión del alumno: cálculo o referencia ya cubierta; conservar trazabilidad.'
  elif code:
   found=index.filter(pl.col('CODE')==code)
   assert found.height,code
   status='AMECO_CONCEPTO_CONFIRMADO' if key in MAP else 'DUPLICADA_O_REFERENCIA_AMECO';source='ameco_spring2026';reference=code
   if key==('NOMINAL',22):observation='La nota del alumno propone OKCT, pero es real y total economía. El título del Excel pide nominal y gobierno: se confirma UKCG.';alt='ESP.1.1.0.0.OKCT (no equivalente)'
   if key==('NOMINAL',24):observation='Se selecciona variante EURO-ESP como la unidad de la fila; la variante ECU/EUR anotada también existe, pero no se confunden antes de 1999.';alt='ESP.1.0.99.0.UQGD'
   if key in [('NOMINAL',7),('NOMINAL',8)]:observation='El alias abreviado Private/Government contradice el título largo. Se sigue el título: fila 7 gobierno (UIGG), fila 8 privado (UIGP).';alt=code.replace('.0.0.0.','.0.99.0.')
  elif key in [('mercado traballo',22),('mercado traballo',23)]:
   status='PWT_CONFIRMADO_DISPONIBLE';source='pwt110';reference='emp' if r['row']==22 else 'avh';observation='Se adopta PWT 11 vigente. Source!35 y mercado traballo!21 dicen PWT 10.0/100; la nota del alumno menciona 11. Se preserva la diferencia de edición.'
  elif r['sheet']=='POP':
   source='INE';reference={'21':'https://www.ine.es/jaxiT3/Tabla.htm?t=6545&L=0','33':'https://www.ine.es/jaxiT3/Tabla.htm?t=6518&L=0','36':'https://www.ine.es/jaxiT3/Tabla.htm?t=6518&L=0','45':'https://www.ine.es/jaxiT3/Tabla.htm?t=6529&L=0'}.get(str(r['row']),'');observation='Fuente en Source!73–85. Defunciones por residencia, nacimientos por inscripción y matrimonios de diferente sexo: conservar universos.'
  elif r['sheet']=='Produzón-CI-VA':
   source='INE';reference='https://www.ine.es/jaxiT3/Tabla.htm?t=32449';observation='Fuente y cuentas en Source!15–30. Algunas filas son derivadas o duplicadas; seguir identidad de cuentas, no alias.'
   if r['row'] in [2,3,4,5]:status='INE_DISPONIBLE_EN_OBSERVATIONS'
   if r['row'] in [8,11,12,13,14,18]:status='DERIVADA_O_REFERENCIA_CUENTAS';observation+=' No tratar cada repetición como input independiente.'
   if r['row'] in [15,16]:status='EUROSTAT_DISPONIBLE_PENDIENTE_SELECCION';source='estat_nama_10_gdp';reference='D11' if r['row']==15 else 'D12'
  elif key==('mercado traballo',27):source='SEPE/INEM';reference='https://www.sepe.es/HomeSepe/que-es-el-sepe/estadisticas/datos-avance/paro';observation='Source!41–49: media de doce meses; origen 1981–2000 no reconstruido. No sustituir por EPA.'
  elif key in [('mercado traballo',28),('mercado traballo',29)]:status='INE_EPA_ACTUAL_INTEGRADA_HISTORICO_PENDIENTE';source='ine_epa_annual_parados';reference='INE.EPA.ANNUAL.PARADOS';observation='Serie oficial actual integrada 2006–2025. Source!51–61 documenta la tabla antigua y dudas del histórico; no igualar datos de origen desconocido.'
  elif key==('mercado traballo',32):source='Ministerio de Trabajo';reference='https://www.mites.gob.es/estadisticas/bel/SMI/smi1.xls';observation='Source!63–69. Diferenciar salario mensual, anual y prorrateo de cambios durante el año.'
  elif r['sheet']=='Quebras':
   source='INE';reference='https://www.ine.es/jaxi/Tabla.htm?path=/t38/bme2/t30/p148/l0/&file=0906003a.px&L=0' if r['row'] in [49,50,51] else 'https://www.ine.es/jaxi/Tabla.htm?path=/t38/bme2/t30/p148/l0/&file=0906001a.px&L=0';observation='Source!88–102: quiebras/suspensiones antiguas y concursos modernos, número y activos/pasivos; filas anuales mezcladas con datos trimestrales. Clasificar granularidad antes de sumar.'
   if r['row'] in [23,24,25,51]:
    status='DERIVADA_AGREGACION_ANUAL';observation='Fila calculada anual sobre columnas trimestrales; no es otra fuente ni otra serie primaria. Comprobar cuatro trimestres completos antes de agregar.'
   if r['row']==3:reference='https://www.ine.es/jaxi/Tabla.htm?path=/t38/bme2/t30/p148/l0/&file=0906003a.px&L=0'
  elif r['sheet']=='i-e':source='World Bank';reference='PA.NUS.FCRF';observation='Source!108–109 y código literal. ESP/peseta hasta 1998; EMU/EUR desde 1999. No empalmar sin documentar moneda y cobertura.'
  elif r['sheet']=='Money':
   source='Banco de España / fuente histórica por resolver';reference='Source!105–109';observation='La fuente es una pista documental, no una descarga acreditada. Marco monetario previo al euro.'
   if r['row'] in [9,10,11]:status='DERIVADA_MULTIPLICADOR_MONETARIO';observation='Cociente M1/BM, M2/BM o M3/BM; no requiere una descarga adicional si están sus componentes.'
  records.append(dict(sheet=r['sheet'],row=r['row'],label=r['label'],n=r['n'],first=r['first'],last=r['last'],user_note=note,frequency=('annual_derived_on_Q4_columns' if key[0]=='Quebras' and key[1] in [23,24,25,51] else r.get('frequency','annual')),status=status,source=source,source_reference=reference,alternative_code=alt,decision_note=observation))
 # Ninguna anotación desaparece aunque cambie el parser.
 keys={(r['sheet'],r['row']) for r in records}
 for key,note in notes.items():assert key in keys,key
 quarter_cells=[];annual_checks=[]
 for r in other:
  for period,value in r.get('period_values',{}).items():
   quarter_cells.append(dict(sheet=r['sheet'],row=r['row'],period=period,value=value))
 for derived_row,source_row in [(23,20),(24,21),(25,22),(51,49)]:
  a=next(r for r in other if r['sheet']=='Quebras' and r['row']==derived_row).get('period_values',{})
  b=next(r for r in other if r['sheet']=='Quebras' and r['row']==source_row).get('period_values',{})
  for period,reported in a.items():
   year=int(period[:4]);qs=[b.get(f'{year}Q{q}') for q in range(1,5)]
   annual_checks.append(dict(derived_row=derived_row,source_row=source_row,year=year,source_period_column=period,quarters_available=sum(v is not None for v in qs),reported_annual=reported,computed_annual=sum(qs) if all(v is not None for v in qs) else None,difference=reported-sum(qs) if all(v is not None for v in qs) else None))
 if quarter_cells:pl.DataFrame(quarter_cells).write_parquet(OUT/'excel_empresas_periodos.parquet')
 if annual_checks:pl.DataFrame(annual_checks).write_csv(OUT/'excel_empresas_comprobacion_anual.csv')
 df=pl.DataFrame(records,infer_schema_length=None).sort(['sheet','row']);df.write_csv(OUT/'filas_reconciliadas.csv');df.write_parquet(OUT/'filas_reconciliadas.parquet')
 new=extract(set(MAP.values()));new.write_parquet(ROOT/'datos/silver/ampliacion_20261019/ameco_conceptos_recuperados.parquet')
 print('Filas reconciliadas:',df.height,'; notas preservadas:',len(notes),'; códigos añadidos:',new['code'].n_unique())
 print(df.group_by('status').len())
 return df,new
if __name__=='__main__':build()
