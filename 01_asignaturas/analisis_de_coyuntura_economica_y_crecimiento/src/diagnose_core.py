"""Audita las diez hojas base y recupera series AMECO/ONU. No modifica la versión v0."""
import csv,hashlib,html,io,json,re,zipfile
from collections import defaultdict
from pathlib import Path
import polars as pl
import xlrd
from openpyxl import load_workbook
from acquire_core import SPECS,fetch
ROOT=Path(__file__).resolve().parents[1]
BASE=['Produzón-CI-VA','REAL','NOMINAL','POP','K','mercado traballo','Indices Prezos','Quebras','i-e','Money']

def main():
    out=ROOT/'output/diagnostico_fuentes';out.mkdir(parents=True,exist_ok=True)
    silver=ROOT/'datos/silver/ampliacion_20261019';silver.mkdir(parents=True,exist_ok=True)
    manifests={s['id']:fetch(s) for s in SPECS}
    b=xlrd.open_workbook(next((ROOT/'datos').glob('*.xls')))
    targets=defaultdict(list);sheet_counts=[]
    for name in BASE:
        sh=b.sheet_by_name(name);local=set()
        for i,row in enumerate(sh.get_rows(),1):
            for j,cell in enumerate(row[:11],1):
                text=str(cell.value).strip().replace(',','.')
                if re.fullmatch(r'[A-Z]{3}\.\d+\.\d+\.\d+\.\d+\.[A-Z0-9]+',text):
                    targets[text].append(f'{name}!fila {i},columna {j}');local.add(text)
        sheet_counts.append(dict(sheet=name,codes=len(local),note='Las series sin código AMECO se tratan aparte; las derivadas no forman el objetivo de esta auditoría.'))
    ameco={};records=[]
    m=manifests['ameco_spring2026'];z=zipfile.ZipFile(ROOT/m['artifact'])
    for name in z.namelist():
        for row in csv.DictReader(io.StringIO(z.read(name).decode('cp1252')),delimiter=';'):
            code=row['CODE'].strip()
            if code not in targets:continue
            ameco[code]=dict(row,member=name)
            for year,value in row.items():
                if year is None or not year.isdigit():continue
                value=value.strip()
                if value in ['', 'NA']:continue
                records.append(dict(code=code,country=code.split('.')[0],year=int(year),value=float(value),unit=row['UNIT'].strip(),title=row['TITLE'].strip(),source='ameco_spring2026',zip_member=name,bronze_sha256=m['sha256'],forecast_period=int(year)>=2026))
    data=pl.DataFrame(records)
    duplicate_check=data.group_by(['code','year']).agg(pl.len().alias('n'),pl.col('value').n_unique().alias('distinct_values'),pl.col('unit').n_unique().alias('distinct_units'),pl.col('zip_member').unique().sort().str.join('; ').alias('zip_members'))
    if duplicate_check.filter((pl.col('distinct_values')>1)|(pl.col('distinct_units')>1)).height:raise ValueError('Códigos AMECO repetidos con valores o unidades diferentes')
    duplicate_check.filter(pl.col('n')>1).write_csv(out/'ameco_repeticiones_identicas.csv')
    data=data.unique(subset=['code','year'],keep='first').sort(['code','year'])
    data.write_parquet(silver/'ameco_reference_codes.parquet');data.write_csv(silver/'ameco_reference_codes.csv')
    coverage=[]
    for code,locations in sorted(targets.items()):
        d=data.filter(pl.col('code')==code)
        coverage.append(dict(code=code,original_country=code[:3],locations='; '.join(locations),status='MISMO_CODIGO_RECUPERADO' if code in ameco else 'NO_LOCALIZADO_EN_EDICION_ACTUAL',n=d.height,
          first=d['year'].min() if d.height else None,last=d['year'].max() if d.height else None,
          title=ameco.get(code,{}).get('TITLE',''),unit=ameco.get(code,{}).get('UNIT',''),
          note='Mismo identificador no implica los mismos valores de la edición del profesor. Separar previsiones 2026–2027 de los años anteriores.'))
    pl.DataFrame(coverage,infer_schema_length=None).write_csv(out/'ameco_codigos_hojas_base.csv')
    pl.DataFrame(sheet_counts).write_csv(out/'hojas_base.csv')
    un=[];notes=[]
    for dataset in ['un_ama_current_lcu','un_ama_constant2020_lcu']:
        m=manifests[dataset];wb=load_workbook(ROOT/m['artifact'],read_only=True,data_only=True)
        sh=wb.worksheets[0];header=list(next(sh.iter_rows(min_row=3,max_row=3,values_only=True)))
        for rownum,row in enumerate(sh.iter_rows(min_row=4,values_only=True),4):
            if row[0] not in [156,724]:continue
            country={156:'CHN',724:'ESP'}[row[0]]
            for year,value in zip(header[4:],row[4:]):
                if not isinstance(year,int) or not isinstance(value,(int,float)):continue
                un.append(dict(source=dataset,country=country,year=year,indicator=row[3],currency=row[2],value=float(value),price_basis='current' if dataset.endswith('current_lcu') else 'constant_2020',bronze_sha256=m['sha256'],sheet=sh.title,row=rownum))
        sh=wb.worksheets[1]
        for row in sh.iter_rows(min_row=2,values_only=True):
            if row[0] in [156,724]:notes.append(dict(source=dataset,country_id=row[0],country=row[1],item=row[2],footnote=row[3],year_flags=list(row[4:])))
    undata=pl.DataFrame(un);undata.write_parquet(silver/'un_ama_china_spain_lcu.parquet');undata.write_csv(silver/'un_ama_china_spain_lcu.csv')
    (out/'un_footnotes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
    ucov=undata.group_by(['country','source','indicator','currency','price_basis']).agg(pl.col('year').min().alias('first'),pl.col('year').max().alias('last'),pl.len().alias('n')).sort(['country','source','indicator'])
    ucov.write_csv(out/'un_cobertura_china_espana.csv')
    correspondence=[]
    for suffix,label in [('OVGD','Gross Domestic Product (GDP)'),('OCPH','Household consumption expenditure (including Non-profit institutions serving households)'),('OCTG','General government final consumption expenditure'),('OITT','Gross capital formation'),('OIGT','Gross fixed capital formation (including Acquisitions less disposals of valuables)'),('OIST','Changes in inventories'),('OXGS','Exports of goods and services'),('OMGS','Imports of goods and services')]:
        d=ucov.filter((pl.col('country')=='CHN')&(pl.col('source')=='un_ama_constant2020_lcu')&(pl.col('indicator')==label))
        correspondence.append(dict(ameco_suffix=suffix,un_indicator=label,CHN_n=d['n'][0] if d.height else 0,CHN_first=d['first'][0] if d.height else None,CHN_last=d['last'][0] if d.height else None,
             correspondence='PARCIAL: incluye objetos valiosos' if suffix=='OIGT' else 'PARCIAL: AMECO incluye existencias y objetos valiosos; ONU separa existencias' if suffix=='OIST' else 'AGREGADO_COINCIDENTE; comprobar revisión, método y notas',unit='yuanes; precios constantes de 2020',publication_date='No acreditada; consulta 2026-10-19'))
    pl.DataFrame(correspondence).write_csv(out/'demanda_china_ameco_a_onu.csv')
    # Comprobaciones de integridad y unicidad; identidad nominal se registra como diagnóstico.
    assert not data.select(pl.struct(['code','year']).is_duplicated().any()).item()
    assert not undata.select(pl.struct(['country','source','indicator','year']).is_duplicated().any()).item()
    assert data['value'].is_finite().all() and undata['value'].is_finite().all()
    summary=dict(base_sheets=BASE,unique_ameco_codes=len(targets),exact_codes_retrieved=len(ameco),
       spain_codes=sum(c.startswith('ESP.') for c in targets),spain_exact_codes_retrieved=sum(c.startswith('ESP.') for c in ameco),
       missing_codes=sorted(set(targets)-set(ameco)),un_china_real_demand=correspondence,
       remaining='Producción bruta y consumos intermedios, rentas/CCF/capital de China, IO y extras monetarios/quiebras: revisar fuentes detalladas y requisitos, no declarar imposibilidad.',
       sources=manifests,checks='Claves únicas y valores finitos; no se certifican todavía identidades ni comparabilidad completa.')
    (out/'resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    text=['# Diagnóstico corregido de fuentes','',
      'Se auditan exclusivamente las diez hojas base indicadas por el alumno. El informe anterior describía descargas incompletas y equivalencias sin validar; no demostraba que las fuentes fueran insuficientes.','',
      f"AMECO: {len(ameco)} de {len(targets)} códigos recuperados con identificador exacto, incluidos {summary['spain_exact_codes_retrieved']} de {summary['spain_codes']} códigos de España.",
      'Los dos códigos no localizados son AMGE y AXGE: cuotas de comercio mundial excluyendo comercio intra-UE. No bloquean el núcleo de cantidades, precios, trabajo y crecimiento.','',
      'La edición AMECO se publicó el 3 de junio de 2026. Los valores pueden diferir del Excel por revisión. Las columnas 2026–2027 se mantienen identificadas como períodos de previsión; la clasificación detallada provisional/observado de años anteriores requiere metadatos.','',
      'ONU: China presenta 55 observaciones anuales, 1970–2024, tanto corrientes como constantes de 2020 y en yuanes, para PIB, consumo privado, público, FBC, formación fija que incluye objetos valiosos, existencias, exportaciones e importaciones.','',
      'No se equipara sin matiz FBCF incluyendo objetos valiosos con FBCF estricta; tampoco existencias con existencias más objetos valiosos. Se conservan las notas de país. No se exige aditividad de series reales sin comprobar el método.','',
      'El período común del análisis no tiene que empezar en 1960 ni acabar en 2025. Debe fijarse por bloque y de forma homogénea entre países; no se declara completo un intervalo sin observaciones.','',
      'Pendientes reales de China: cuentas de producción y rentas más detalladas, CCF/stock de capital compatibles, input-output y definiciones laborales. PWT e ILO siguen siendo fuentes de complemento. Las estadísticas de quiebras y agregados monetarios se inventarían aparte; su presencia en el Excel no demuestra que todos sean obligatorios en el ensayo.','',
      'Una base internacional puede redistribuir estadísticas nacionales o completar series; no se supone independencia respecto de NBS. El snapshot inicial v0 permanece intacto.']
    (out/'DIAGNOSTICO.md').write_text('\n'.join(text)+'\n')
    print(f"AMECO: {len(ameco)}/{len(targets)}; España {summary['spain_exact_codes_retrieved']}/{summary['spain_codes']}. ONU: {undata.height} observaciones CHN/ESP. Sin modificar v0.")
if __name__=='__main__':main()
