"""Catálogo legible y correspondencia exhaustiva de códigos AMECO del Excel con snapshot v0."""
from __future__ import annotations
import csv,html,json,re
from collections import Counter,defaultdict
from pathlib import Path
import polars as pl
import xlrd
from snapshot import ROOT,verify
VERSION='v0_2026-10-16'
CODE=re.compile(r'[A-Z]{3}\.\d+\.\d+\.\d+\.\d+\.[A-Z0-9]+')

def write_json(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def fmt_years(xs):return ','.join(map(str,sorted(xs)))

def read_excel(path):
    b=xlrd.open_workbook(path);occ=[];other=[]
    priority={s:i for i,s in enumerate(['REAL','NOMINAL','POP','K','mercado traballo','Indices Prezos','i-e'])}
    for sheet in b.sheets():
        header={};quarter_header={}
        for i in range(sheet.nrows):
            row=sheet.row_values(i)
            quarter_cells={j:str(v).strip() for j,v in enumerate(row) if isinstance(v,str) and re.fullmatch(r'(?:19|20)\d{2}Q[1-4]',v.strip())}
            if len(quarter_cells)>=4:
                quarter_header=quarter_cells;header={};continue
            year_cells={j:int(float(v)) for j,v in enumerate(row) if (isinstance(v,(int,float)) or isinstance(v,str) and v.isdigit()) and 1900<=float(v)<=2035 and float(v).is_integer()}
            # Algunos encabezados empiezan con un año de edición aislado (p. ej. 2024),
            # seguido de la serie cronológica 1995..2024. Usar el bloque consecutivo más largo.
            runs=[];run=[]
            for col,year in year_cells.items():
                if run and (col!=run[-1][0]+1 or year!=run[-1][1]+1):
                    runs.append(run);run=[]
                run.append((col,year))
            if run:runs.append(run)
            best=max(runs,key=len,default=[])
            if len(best)>=4:
                header=dict(best);quarter_header={};continue
            refs=[]
            for j,v in enumerate(row[:11]):
                if isinstance(v,str) and CODE.fullmatch(v.strip().replace(',','.')):refs.append((j,v.strip().replace(',','.')))
            vals={str(year):float(row[j]) for j,year in header.items() if j<len(row) and isinstance(row[j],(int,float)) and not isinstance(row[j],bool)}
            meta=[str(v).strip() for j,v in enumerate(row[:11]) if v!='' and j not in header]
            title=(str(row[9]) if len(row)>10 and str(row[6]) in [code.split('.')[-1] for j,code in refs] else str(row[4]) if len(row)>5 and isinstance(row[4],str) and len(row[4])>12 else ' | '.join(meta))
            unit=str(row[10]) if len(row)>10 and str(row[6]) in [code.split('.')[-1] for j,code in refs] else str(row[5]) if len(row)>5 and isinstance(row[5],str) else ''
            if refs and len(row)>10 and isinstance(row[9],str) and len(row[9].strip())>12 and isinstance(row[10],str) and row[10].strip():
                title=row[9].strip();unit=row[10].strip()
            if refs:
                for j,code in refs:occ.append(dict(code=code,sheet=sheet.name,row=i+1,code_column=j+1,title=title,unit=unit,n=len(vals),first=min(map(int,vals)) if vals else None,last=max(map(int,vals)) if vals else None,years=vals,metadata=meta,priority=priority.get(sheet.name,100)))
            elif quarter_header and meta:
                periods={period:float(row[j]) for j,period in quarter_header.items() if j<len(row) and isinstance(row[j],(int,float)) and not isinstance(row[j],bool)}
                if periods:
                    other.append(dict(sheet=sheet.name,row=i+1,label=' | '.join(meta),n=len(periods),first=min(int(p[:4]) for p in periods),last=max(int(p[:4]) for p in periods),frequency='quarterly_header',status='fila_sin_codigo_AMECO_requiere_clasificacion',values={},period_values=periods))
            elif vals and meta:
                other.append(dict(sheet=sheet.name,row=i+1,label=' | '.join(meta),n=len(vals),first=min(map(int,vals)),last=max(map(int,vals)),status='fila_sin_codigo_AMECO_requiere_clasificacion',values=vals))
    groups=defaultdict(list)
    for r in occ:groups[r['code']].append(r)
    inventory=[]
    for code,items in sorted(groups.items()):
        primary=min(items,key=lambda x:(x['priority'],-x['n']))
        years=set().union(*(set(map(int,x['years'])) for x in items))
        inventory.append(dict(code=code,original_country=code[:3],suffix=code.split('.')[-1],title=primary['title'],unit=primary['unit'],
            locations=[dict(sheet=x['sheet'],row=x['row'],column=x['code_column'],n=x['n'],unit=x['unit']) for x in items],
            original_years=sorted(years),original_n=len(years),original_first=min(years) if years else None,original_last=max(years) if years else None,
            original_status='con_datos' if years else 'rotulo_sin_valores',
            original_note='Las filas duplicadas pueden pertenecer a distintas bases, unidades o cálculos. Cobertura de años no implica coincidencia de valores.'))
    return inventory,occ,other


def rules():
    # No se declara equivalencia numérica exacta entre proveedores ni entre ediciones.
    out={}
    def rule(code,name,spain=None,china=None,note='',core=True):out[code]=dict(name=name,ESP=spain,CHN=china,note=note,core=core)
    def raw(source,series,quality='CONCEPTUAL',unit='',note=''):return dict(kind='raw',source=source,series=series,quality=quality,unit=unit,note=note)
    def est(item,unit='CP_MEUR',dataset='estat_nama_10_gdp',extra=None):
        return dict(kind='dimensions',source=dataset,selection=dict(na_item=item,unit=unit,**(extra or {})),quality='CONCEPTUAL',unit=unit)
    def wdi(s,q='CONCEPTUAL'):return raw('wdi_common',s,q)
    def pwt(s,q='PARCIAL'):return raw('pwt110',s,q)
    def na(s):return raw('pwt110_na',s,'CONCEPTUAL_CON_UNIDAD_PENDIENTE','moneda nacional; escala monetaria por validar')
    def derived(expr,inputs,quality='DERIVABLE_NO_VALIDADA',unit=''):return dict(kind='derived',formula=expr,inputs=inputs,quality=quality,unit=unit)
    # Reales y nominales: FBC no es FBCF.
    for code,name,item,var in [('OVGD','PIB real','B1GQ','q_gdp'),('OCPH','Consumo privado real','P31_S14_S15','q_c'),('OITT','Formación bruta de capital real (FBC)','P5G','q_i'),('OIGT','Formación bruta de capital fijo real (FBCF)','P51G','q_gfcf'),('OCTG','Consumo público real','P3_S13','q_g'),('OXGS','Exportaciones de bienes y servicios reales','P6','q_x'),('OMGS','Importaciones de bienes y servicios reales','P7','q_m')]:
        rule(code,name,est(item,'CLV20_MEUR'),wdi('NY.GDP.MKTP.KN') if code=='OVGD' else na(var),
             'Precios constantes/volúmenes. España: millones EUR encadenados referencia 2020, no miles de millones. AMECO y PWT/Eurostat no comparten necesariamente revisión ni método. Consumo privado: verificar hogares e ISFLSH. q_i se registra como inversión en la leyenda PWT; confirmar alcance FBC frente a FBCF antes de certificar equivalencia.')
    for code,name,item,var in [('UVGD','PIB nominal','B1GQ','v_gdp'),('UCPH','Consumo privado nominal','P31_S14_S15','v_c'),('UITT','Formación bruta de capital nominal (FBC)','P5G','v_i'),('UIGT','Formación bruta de capital fijo nominal (FBCF)','P51G','v_gfcf'),('UCTG','Consumo público nominal','P3_S13','v_g'),('UXGS','Exportaciones de bienes y servicios nominales','P6','v_x'),('UMGS','Importaciones de bienes y servicios nominales','P7','v_m')]:
        rule(code,name,est(item),wdi('NY.GDP.MKTP.CN') if code=='UVGD' else na(var),'Precios corrientes. Escalar millones/miles de millones antes de contrastar niveles; comprobar alcance sectorial y revisión. No convertir a USD para este requisito.')
    rule('OIST','Variación de existencias y adquisición neta de objetos valiosos, real',est('P52_P53','CLV20_MEUR'),None,'La selección Eurostat probada no contiene datos. No reemplazar por una resta de volúmenes encadenados sin validar aditividad.')
    rule('UIST','Variación de existencias y objetos valiosos, nominal',est('P52_P53'),derived('v_i - v_gfcf',[na('v_i'),na('v_gfcf')]),'La diferencia FBC−FBCF debe contrastarse con el alcance de objetos valiosos y discrepancias estadísticas; no se declara serie observada.')
    rule('UWCD','Remuneración de asalariados',est('D1'),None,'No equivale a salario medio ni a la participación laboral ajustada labsh de PWT.')
    rule('UOGD','Excedente bruto de explotación',est('B2A3G'),None,'Eurostat B2A3G incluye renta mixta. Verificar si el EBE de AMECO la incluye: equivalencia parcial.',True)
    out['UOGD']['ESP']['quality']='PARCIAL'
    rule('UTVT','Impuestos sobre producción e importación',est('D2'),None)
    rule('UYVT','Subvenciones sobre producción e importación',est('D3'),None)
    rule('UYGD','PIB a coste de los factores',derived('PIB nominal - D2 + D3',[est('B1GQ'),est('D2'),est('D3')]),None,'Derivable con datos de España. El PIB a precios básicos no es necesariamente PIB a coste de factores.')
    rule('UKCT','Consumo de capital fijo nominal',raw('ine_integrated_accounts','ccf_nominal'),derived('Dc_Struc + Dc_Mach + Dc_TraEq + Dc_Other',[raw('pwt110_capital','Dc_'+s,'PARCIAL') for s in ['Struc','Mach','TraEq','Other']]),'China: componentes nominales disponibles; su suma requiere validar cobertura y escala. No confundir con delta, una tasa.')
    rule('OKCT','Consumo de capital fijo real',None,None,'Falta una serie real validada. No deflactar automáticamente por el deflactor del PIB.')
    rule('OKND','Stock neto de capital real',dict(kind='dimensions',source='estat_nama_10_nfa_st',selection=dict(asset10='N11N',nace_r2='TOTAL',unit='CLV20_MEUR'),quality='PARCIAL',unit='millones EUR, volumen encadenado 2020'),pwt('rnna'),'PWT rnna: millones de USD de 2021 a precios nacionales constantes. NO cumple moneda local; distinta cobertura de activos y método posible. Variante 99: además distinguir EUR/ECU de moneda nacional.')
    rule('NPTD','Población total, concepto cuentas nacionales',est('POP_NC','THS_PER','estat_nama_10_pe'),pwt('pop'),'PWT pop es población en millones, no se certifica concepto idéntico de cuentas nacionales.')
    rule('NPTN','Población total',wdi('SP.POP.TOTL'),wdi('SP.POP.TOTL'),'WDI personas; Excel miles. Verificar media anual vs fin de año y delimitación territorial.')
    for code,name,w in [('NPCN','Población 0–14 años','SP.POP.0014.TO'),('NPAN','Población 15–64 años','SP.POP.1564.TO'),('NPON','Población de 65 años o más','SP.POP.65UP.TO')]:rule(code,name,wdi(w),wdi(w),'WDI personas, Excel miles; no confundir 15–64 con 15+.')
    rule('NLTN','Población activa',wdi('SL.TLF.TOTL.IN','PARCIAL'),wdi('SL.TLF.TOTL.IN','PARCIAL'),'Estimación internacional; no certificar mismo universo, edad, método o edición que AMECO.')
    rule('NETN','Ocupados totales de cuentas nacionales',est('EMP_DC','THS_PER','estat_nama_10_pe'),pwt('emp'),'PWT emp: millones de ocupados; no horas ni equivalentes a tiempo completo. Concepto doméstico/nacional y ajuste de fuentes deben validarse.')
    rule('NSTD','Trabajadores por cuenta propia',est('SELF_DC','THS_PER','estat_nama_10_pe'),None)
    rule('FETD','Empleo equivalente a tiempo completo',derived('horas totales / 1760',[dict(kind='dimensions',source='estat_nama_10_a10_e',selection=dict(na_item='EMP_DC',unit='THS_HW',nace_r2='TOTAL'),quality='CONCEPTUAL',unit='miles de horas')],quality='APROXIMACION',unit='miles de equivalentes'),derived('emp * 1e6 * avh / 1760',[pwt('emp'),pwt('avh')],quality='APROXIMACION',unit='equivalentes'),'Aproximación autorizada por las instrucciones si no existe la serie. No es un dato observado FETD.')
    rule('NUTN','Desempleados',derived('activos * tasa de paro / 100',[wdi('SL.TLF.TOTL.IN'),wdi('SL.UEM.TOTL.ZS')],quality='APROXIMACION'),derived('activos * tasa de paro / 100',[wdi('SL.TLF.TOTL.IN'),wdi('SL.UEM.TOTL.ZS')],quality='APROXIMACION'),'No se declara equivalencia con desempleo EPA/encuesta nacional de AMECO ni paro registrado. Serie derivada con tasa modelizada OIT.')
    rule('ZCPIN','Índice nacional de precios al consumo',wdi('FP.CPI.TOTL'),wdi('FP.CPI.TOTL'),'Bases distintas: WDI 2010=100 frente a Excel 2020=100; rebasar para índices. Inflación invariante al rebase, sujeto a cobertura y revisión.')
    rule('PVGD','Deflactor del PIB',est('B1GQ','PD20_EUR'),derived('100 * PIB nominal / PIB real',[wdi('NY.GDP.MKTP.CN'),wdi('NY.GDP.MKTP.KN')]),'Referencia de precios WDI varía por país. La presencia de este código USA en Excel no implica tener datos USA en nuestro panel.')
    for code,name,expr,inputs in [('RKNDE','Capital neto real por ocupado','rnna / emp',[pwt('rnna'),pwt('emp')]),('AKNDV','Ratio capital/producto','rnna / rgdpna',[pwt('rnna'),pwt('rgdpna')]),('AVGDK','Productividad media del capital','rgdpna / rnna',[pwt('rgdpna'),pwt('rnna')])]:rule(code,name,derived(expr,inputs),derived(expr,inputs),'Candidato calculable en base PWT. No réplica exacta AMECO; bases, unidades y definición requieren validación.',False)
    for code,name in [('USGP','Ahorro bruto privado'),('USGG','Ahorro bruto de las administraciones públicas'),('USGN','Ahorro nacional bruto'),('URTG','Ingresos totales de las administraciones públicas'),('UUTG','Gasto total de las administraciones públicas'),('UVGN','Renta nacional bruta nominal'),('UVGT','Renta nacional disponible bruta'),('UVNN','Renta nacional neta'),('UVNT','Renta nacional disponible neta'),('ISN','Tipo de interés nominal a corto plazo'),('ILN','Tipo de interés nominal a largo plazo'),('ZNAWRU','Tasa de desempleo no aceleradora de salarios (NAWRU)'),('APNDK','Rentabilidad neta del stock neto de capital'),('ZVGDF','Productividad total de los factores, índice AMECO'),('ZVGDE','Componente del trabajo en la PTF AMECO'),('ZVGDK','Componente del capital en la PTF AMECO'),('ZKNDE','Sustitución trabajo-capital, índice AMECO'),('ZEKND','Sustitución capital-trabajo, índice AMECO'),('AKGDV','Eficiencia marginal del capital')]:rule(code,name,None,None,'Sin correspondencia validada en las descargas actuales. PTF de PWT o un residuo de Solow propio no se declara equivalente automáticamente.',False)
    rule('XNEF','Conversión fija euro/antigua moneda de la zona euro',None,None,'Conversión histórica EUR/peseta: no tiene equivalente conceptual directo para China.',False)
    for code,name in [('UVG0','VAB nominal total'),('UVG1','VAB nominal agricultura, silvicultura y pesca'),('UVG2','VAB nominal industria excepto construcción'),('UVGM','VAB nominal manufacturas'),('UVG4','VAB nominal construcción'),('UVG5','VAB nominal servicios')]:
        rule(code,name,est('B1G','CP_MEUR','estat_nama_10_a10',dict(nace_r2='TOTAL')) if code=='UVG0' else None,None,'Se descargó TOTAL; no las ramas. Serie adicional del Excel: la existencia del PIB no cubre VAB por ramas.',False)
    return out


def match(df,spec,country):
    if not spec:return dict(status='FALTA',n=0,years=[],locator='',formula='',unit='',hashes=[],note='No hay equivalente validado seleccionado; el catálogo no certifica la ausencia en todas las fuentes posibles.')
    if spec['kind']=='derived':
        ins=[match(df,x,country) for x in spec['inputs']]
        years=sorted(set.intersection(*(set(x['years']) for x in ins))) if ins else []
        return dict(status=spec['quality'] if years else 'FALTA_INPUTS',n=len(years),years=years,
            locator=' + '.join(x['locator'] for x in ins),formula=spec['formula'],unit=spec.get('unit',''),
            hashes=sorted(set(h for x in ins for h in x['hashes'])),note='Años con todos los inputs. Fórmula candidata NO se incorpora automáticamente a silver ni se certifica comparabilidad.')
    d=df.filter((pl.col('country')==country)&(pl.col('source')==spec['source']))
    if spec['kind']=='raw':d=d.filter(pl.col('series')==spec['series'])
    else:
        keep=[i for i,r in enumerate(d.iter_rows(named=True)) if all(json.loads(r['dimensions']).get(k)==v for k,v in spec['selection'].items())]
        d=d[keep] if keep else d.head(0)
    years=sorted(set(d['year'].to_list()));unit=spec.get('unit') or '; '.join(d['unit'].unique().to_list())
    locator=spec['source']+' / '+(spec['series'] if spec['kind']=='raw' else json.dumps(spec['selection'],ensure_ascii=False,sort_keys=True))
    return dict(status=spec['quality'] if years else 'SIN_OBSERVACIONES',n=len(years),years=years,locator=locator,
       formula='',unit=unit,hashes=sorted(d['bronze_sha256'].unique().to_list()),note=spec.get('note',''))


def dictionary(df,root,base):
    legends={}
    for p in (base/'datos/silver').glob('*_legend.json'):
        legends[p.stem.replace('_legend','')]={str(r[0]):str(r[1]) for r in json.loads(p.read_text()) if len(r)>1 and r[0] and r[1]}
    metadata={}
    frozen_manifest=json.loads((base.parent/'manifest.json').read_text()) if (base.parent/'manifest.json').exists() else json.loads((root/'datos/snapshots'/VERSION/'manifest.json').read_text())
    metadata_paths=[root/r['path'] for r in frozen_manifest['bronze_files'] if Path(r['path']).name.startswith('Metadata_Indicator')]
    for path in metadata_paths:
        with path.open(encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):metadata[r['INDICATOR_CODE']]=r
    # Labels Eurostat se recuperan de los mismos archivos originales que alimentaron v0.
    lineage=json.loads((base/'datos/gold/lineage.json').read_text());estat={}
    for m in lineage['inputs']:
        if m.get('provider')=='eurostat':estat[m['id']]=json.loads((root/m['artifact']).read_text())
    translations={'avh':'Horas medias anuales trabajadas por ocupado','emp':'Número de ocupados','pop':'Población','rgdpna':'PIB real a precios nacionales constantes, expresado en USD de 2021','rnna':'Stock de capital a precios nacionales constantes, expresado en USD de 2021','rgdpe':'PIB real por el lado del gasto a PPA encadenadas','labsh':'Participación laboral ajustada en el PIB','delta':'Tasa media de depreciación del stock de capital',
     'q_gdp':'PIB real en moneda nacional','q_c':'Consumo de hogares real','q_i':'Inversión real (alcance FBC por confirmar)','q_gfcf':'Formación bruta de capital fijo real','q_g':'Consumo público real','q_x':'Exportaciones reales','q_m':'Importaciones reales','v_gdp':'PIB nominal en moneda nacional','v_c':'Consumo de hogares nominal','v_i':'Inversión nominal (alcance FBC por confirmar)','v_gfcf':'Formación bruta de capital fijo nominal','v_g':'Consumo público nominal','v_x':'Exportaciones nominales','v_m':'Importaciones nominales'}
    rows=[]
    for (source,series),d in df.group_by(['source','series'],maintain_order=True):
        definition='';name=translations.get(series,'');unit='; '.join(d['unit'].unique().to_list());notes=''
        if source in legends:
            definition=legends[source].get(series,'')
            if series=='avh':unit='horas por ocupado y año';notes='NO son horas totales. Total = avh × emp × 1e6 si emp está en millones.'
            elif source=='pwt110' and series in ['emp','pop']:unit='millones de personas'
            elif source=='pwt110' and series in ['rgdpna','rnna','rgdpe','rgdpo']:unit='millones de USD de 2021; distinguir precios nacionales y PPA según variable'
            elif source=='pwt110_na' and series.startswith(('q_','v_')):unit='moneda nacional; real/nominal según código; escala monetaria por documentar'
            notes=notes or 'Consultar la definición literal preservada y la metodología de la edición 11.0.'
        elif source in estat:
            dims=json.loads(d['dimensions'][0]);obj=estat[source]
            definition='; '.join(k+'='+str(obj['dimension'][k]['category'].get('label',{}).get(v,v)) for k,v in dims.items())
            name=name or definition
        elif source.startswith('wdi'):
            meta=metadata.get(series,{})
            definition=meta.get('INDICATOR_NAME','');name=name or definition
            notes='Metadatos de indicador procedentes del CSV local; no acreditan independencia de la fuente nacional.'
        elif source=='ine_integrated_accounts':name=name or series;definition='Código operación '+str(d['source_code'][0])+' en cuentas económicas integradas INE.'
        rows.append(dict(source=source,series=series,name_es=name or definition or series,definition_original=definition,unit=unit,
            country_coverage='; '.join(c+': '+str(v['year'].min())+'–'+str(v['year'].max())+' ('+str(v.height)+')' for (c,),v in d.group_by('country')),note=notes))
    return rows


def build(root=ROOT):
    verify(VERSION,root);base=root/'datos/snapshots'/VERSION/'frozen';df=pl.read_parquet(base/'datos/silver/observations.parquet')
    dest=root/'output/catalogo';dest.mkdir(parents=True,exist_ok=True)
    cat=root/'datos/catalogo'
    frozen_manifest=json.loads((root/'datos/snapshots'/VERSION/'manifest.json').read_text())
    excel_paths=[root/x['path'] for x in frozen_manifest['bronze_files'] if x['path'].endswith('.xls')]
    if len(excel_paths)!=1:raise ValueError('Referencia Excel ambigua')
    inv,occ,others=read_excel(excel_paths[0]);maps=rules();cross=[]
    for item in inv:
        code=item['code'];suffix=item['suffix'];spec=maps.get(suffix,dict(name=item['title'],ESP=None,CHN=None,note='Sin correspondencia revisada; no se equiparan automáticamente otras series del mismo tema.',core=False))
        row={**item,'selection_specifications':{c:spec[c] for c in ['ESP','CHN']},'name_es':spec['name'],'scope':'nucleo_informe' if spec['core'] and item['original_country']=='ESP' else 'adicional_excel_o_referencia_externa','mapping_note':spec['note']}
        for country in ['ESP','CHN']:
            mapped=match(df,spec[country],country)
            if suffix=='XNEF' and country=='CHN':mapped['status']='NO_APLICA'
            if item['original_country']!='ESP':mapped['note']+=' Código original '+item['original_country']+': el mapeo ESP/CHN es orientativo y NO una réplica del dato USA.'
            original=set(item['original_years']);years=set(mapped['years'])
            mapped.update(first=min(years) if years else None,last=max(years) if years else None,
                 original_years_covered=len(original&years),original_years_missing=sorted(original-years),
                 full_original_period=bool(original) and original.issubset(years),same_ameco_code_downloaded=False)
            row[country]=mapped
        row['common_years']=sorted(set(row['ESP']['years'])&set(row['CHN']['years']))
        row['both_full_original_period']=row['ESP']['full_original_period'] and row['CHN']['full_original_period']
        cross.append(row)
    # Añadidos esenciales que no tienen un código AMECO propio visible en el archivo.
    extras=[('PWT.avh','Horas medias anuales por ocupado',dict(kind='raw',source='pwt110',series='avh',quality='CONCEPTUAL'), 'El profesor copia avh de PWT 10.0; nosotros 11.0. Horas por ocupado, NO totales.'),
      ('HORAS_TOTALES','Horas totales anuales',dict(kind='derived',formula='emp × 1e6 × avh',inputs=[dict(kind='raw',source='pwt110',series=x,quality='PARCIAL') for x in ['emp','avh']],quality='DERIVABLE_NO_VALIDADA',unit='horas anuales'),'La fórmula requiere emp y avh de la misma base y universo.'),
      ('Gini','Índice de Gini',dict(kind='raw',source='wdi_common',series='SI.POV.GINI',quality='PARCIAL'),'Solo años observados; definición de bienestar y cobertura de encuestas por validar.')]
    additional=[]
    for code,name,spec,note in extras:additional.append(dict(code=code,name_es=name,note=note,ESP=match(df,spec,'ESP'),CHN=match(df,spec,'CHN')))
    for code,name in [('PARO_REGISTRADO','Paro registrado'),('INPUT_OUTPUT','Tabla input-output tres sectores')]:additional.append(dict(code=code,name_es=name,note='Requisito no cubierto por el panel actual.',ESP=match(df,None,'ESP'),CHN=match(df,None,'CHN')))
    for code,series,name in [('PRODUCCION','output','Producción bruta nominal'),('CONSUMOS_INTERMEDIOS','intermediate_consumption','Consumos intermedios nominales')]:additional.append(dict(code=code,name_es=name,note='INE España en millones de euros corrientes; falta China.',ESP=match(df,dict(kind='raw',source='ine_integrated_accounts',series=series,quality='CONCEPTUAL'),'ESP'),CHN=match(df,None,'CHN')))
    dic=dictionary(df,root,base)
    write_json(cat/'series_crosswalk.json',dict(snapshot=VERSION,entries=cross,additional=additional))
    write_json(cat/'series_dictionary.json',dic)
    write_json(dest/'excel_code_occurrences.json',occ)
    pl.DataFrame([{k:v for k,v in x.items() if k!='values'} for x in others],infer_schema_length=None).write_csv(dest/'excel_rows_without_ameco_code.csv')
    flat=[]
    for r in cross:
        out={k:r[k] for k in ['code','name_es','scope','title','unit','original_n','original_first','original_last','original_status','mapping_note']}
        out['excel_locations']='; '.join(f"{x['sheet']}!fila {x['row']}" for x in r['locations'])
        for c in ['ESP','CHN']:
            for key in ['status','locator','formula','unit','n','first','last','original_years_covered','full_original_period','same_ameco_code_downloaded','note']:out[c+'_'+key]=r[c][key]
            out[c+'_missing_original_years']=fmt_years(r[c]['original_years_missing'])
        out['common_period']=f"{min(r['common_years'])}–{max(r['common_years'])}" if r['common_years'] else ''
        out['common_n']=len(r['common_years']);out['both_full_original_period']=r['both_full_original_period'];flat.append(out)
    pl.DataFrame(flat,infer_schema_length=None).write_csv(dest/'correspondencias_ameco_espana_china.csv')
    pl.DataFrame(dic,infer_schema_length=None).sort(['source','series']).write_csv(dest/'diccionario_series.csv')
    stats=dict(snapshot=VERSION,codes=len(cross),codes_spain=sum(r['original_country']=='ESP' for r in cross),
        codes_with_original_values=sum(r['original_n']>0 for r in cross),codes_labels_only=sum(r['original_n']==0 for r in cross),
        uncoded_annual_rows=len(others),dictionary_entries=len(dic),
        statuses={c:dict(Counter(r[c]['status'] for r in cross)) for c in ['ESP','CHN']},
        exact_ameco_downloads=0,certification='NO: no se ha completado la réplica de todas las series y períodos del Excel, ni sus equivalentes para China.')
    write_json(dest/'resumen_cobertura.json',stats)
    render(dest,flat,dic,additional,stats)
    print(json.dumps(stats,ensure_ascii=False,indent=2))
    return cross,additional


def render(dest,flat,dic,additional,stats):
    import html
    esc=lambda x:html.escape(str(x) if x is not None else '')
    def table(rows,fields):
        return '<table><thead><tr>'+''.join('<th>'+esc(label)+'</th>' for key,label in fields)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(r.get(key,''))+'</td>' for key,label in fields)+'</tr>' for r in rows)+'</tbody></table>'
    sections=[]
    for r in flat:
        display={**r}
        for c in ['ESP','CHN']:
            display[c+'_summary']=f"{r[c+'_status']} | {r[c+'_locator']} | {r[c+'_first']}–{r[c+'_last']} ({r[c+'_n']} años). Fórmula: {r[c+'_formula']}. Unidad: {r[c+'_unit']}. Cubre {r[c+'_original_years_covered']}/{r['original_n']} años del Excel."
            if r[c+'_n']==0:display[c+'_summary']=r[c+'_status']+' | Sin serie validada con observaciones. '+r[c+'_locator']
        sections.append(display)
    fields=[('code','Código del Excel'),('name_es','Significado'),('original_status','Datos originales'),('excel_locations','Ubicación en Excel'),('ESP_summary','España: datos nuestros'),('CHN_summary','China: datos nuestros'),('common_period','Período común'),('mapping_note','Diferencias y advertencias')]
    doc='''<!doctype html><html lang="es"><meta charset="utf-8"><title>Catálogo de series China y España</title><style>body{font:15px system-ui;margin:32px;color:#202020}h1,h2{max-width:1000px}p{max-width:1050px;line-height:1.5}input{font:inherit;padding:10px;width:min(850px,95%);margin:15px 0}table{border-collapse:collapse;font-size:12px;width:100%}th{position:sticky;top:0;background:#e8eef3}td,th{border:1px solid #ccc;padding:8px;text-align:left;vertical-align:top}td{min-width:100px;overflow-wrap:anywhere}tr:nth-child(even){background:#fafafa}nav a{margin-right:20px}section{overflow:auto;margin-bottom:45px}.fixed{font-family:monospace}</style><h1>Catálogo de series y correspondencias con el Excel</h1>'''
    doc+=f'<p>Versión analizada: <b>{VERSION}</b>. {stats["codes"]} códigos AMECO distintos localizados, de los que {stats["codes_labels_only"]} son rótulos sin valores numéricos identificados. Se inventarían además {stats["uncoded_annual_rows"]} filas anuales sin código AMECO (incluyen cálculos, controles y otras fuentes; requieren clasificación).</p>'
    doc+='<p><b>No tenemos todavía todos los datos ni todos los años del Excel, para España ni para China.</b> Ninguna serie descargada se certifica como réplica numérica exacta de AMECO. Las correspondencias conceptuales no implican misma base, revisión, población o escala.</p>'
    doc+='<nav><a href="#ameco">Excel → España y China</a><a href="#extras">Otras series esenciales</a><a href="#dictionary">Diccionario de nuestras series</a></nav><input id="search" placeholder="Buscar OITT, avh, inversión, horas, una fuente o un código…" aria-label="Buscar en todas las tablas">'
    doc+='<p>CONCEPTUAL: mismo agregado candidato, distinta fuente/edición. CONCEPTUAL_CON_UNIDAD_PENDIENTE: falta validar alcance o escala. PARCIAL/APROXIMACION: no satisface exactamente la definición. DERIVABLE_NO_VALIDADA: hay inputs, pero aún no una serie equivalente certificada. FALTA/SIN_OBSERVACIONES: no hay un equivalente validado con valores. NO_APLICA: sin análogo directo. Las filas USA no se cuentan como España.</p>'
    doc+='<section id="ameco"><h2>Del Excel a los datos de España y China</h2>'+table(sections,fields)+'</section>'
    extra=[]
    for r in additional:
        extra.append(dict(code=r['code'],name=r['name_es'],spain=f"{r['ESP']['status']} | {r['ESP']['locator']} | {r['ESP']['n']} años",china=f"{r['CHN']['status']} | {r['CHN']['locator']} | {r['CHN']['n']} años",note=r['note']))
    doc+='<section id="extras"><h2>Otras series esenciales</h2>'+table(extra,[('code','ID'),('name','Qué es'),('spain','España'),('china','China'),('note','Notas')])+'</section>'
    doc+='<section id="dictionary"><h2>Diccionario de todas nuestras series</h2>'+table(sorted(dic,key=lambda r:(r['source'],r['series'])),[('source','Fuente'),('series','Código nuestro'),('name_es','Nombre legible'),('definition_original','Definición de origen'),('unit','Unidad'),('country_coverage','Cobertura real'),('note','Notas')])+'</section>'
    doc+='''<script>document.getElementById('search').addEventListener('input',function(){const q=this.value.toLocaleLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLocaleLowerCase().includes(q));});</script></html>'''
    (dest/'catalogo_series.html').write_text(doc)
    lines=['# Catálogo y correspondencias','',f'Versión de datos: {VERSION}.','',stats['certification'],'',
       f"- {stats['codes']} códigos AMECO localizados ({stats['codes_spain']} de España).",
       f"- {stats['codes_with_original_values']} con valores en el Excel; {stats['codes_labels_only']} solo rótulos.",
       f"- {stats['uncoded_annual_rows']} filas anuales sin código inventariadas; no se supone que sean series independientes ni datos pendientes de descarga.",
       '- Correspondencia conceptual y cobertura temporal se comprueban por separado. No se acredita igualdad numérica entre proveedores.',
       '- Las series copiadas del Excel están archivadas como referencia; no cuentan como descargas oficiales nuevas.',
       '- PWT avh: horas medias anuales por ocupado. Total = emp (millones) × 1e6 × avh.',
       '- AMECO OITT: formación bruta de capital real (FBC), NO formación bruta de capital fijo (OIGT).',
       '- España: OITT → Eurostat nama_10_gdp, P5G, CLV20_MEUR. China: candidato q_i de PWT NA; falta validar el alcance y la escala.',
       '- Rebasar precios o escalar millones no elimina diferencias de revisión o definición.','',
       '## Archivos','',
       '- catalogo_series.html: consulta con buscador.',
       '- correspondencias_ameco_espana_china.csv: equivalencias, fórmulas, unidades, cobertura y años del Excel que faltan.',
       '- diccionario_series.csv: significado de todos los identificadores que aparecen en silver, por fuente.',
       '- excel_code_occurrences.json: trazabilidad hoja, fila, título, unidad y valores de cada aparición de un código.',
       '- excel_rows_without_ameco_code.csv: inventario de filas sin código para completar la clasificación.',
       '- datos/catalogo/series_crosswalk.json: correspondencias estructuradas con filtros exactos, fórmulas y hashes.']
    (dest/'LEEME.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':build()
