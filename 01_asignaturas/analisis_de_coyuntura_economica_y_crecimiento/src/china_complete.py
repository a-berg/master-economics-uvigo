"""Offline, practical China alternatives. Does not overwrite original silver or user contracts."""
from __future__ import annotations
import hashlib
import json
import math
import re
from html.parser import HTMLParser
from pathlib import Path
import polars as pl
from openpyxl import load_workbook
from pipeline import write_json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/revision_china/complecion'
SILVER=ROOT/'datos/silver'
ASSETS=['Struc','Mach','TraEq','Other']

class TableRows(HTMLParser):
    def __init__(self):
        super().__init__();self.rows=[];self.row=None;self.cell=None
    def handle_starttag(self,tag,attrs):
        if tag=='tr':self.row=[]
        elif tag in ['td','th']:self.cell=[]
    def handle_data(self,data):
        if self.cell is not None:self.cell.append(data)
    def handle_endtag(self,tag):
        if tag in ['td','th'] and self.cell is not None:
            if self.row is not None:self.row.append(' '.join(''.join(self.cell).split()))
            self.cell=None
        elif tag=='tr' and self.row is not None:
            self.rows.append(self.row);self.row=None

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    rows=[];catalog={};used={}
    def source(id):
        m=json.loads((ROOT/'datos/bronze'/id/'latest.json').read_text())
        assert hashlib.sha256((ROOT/m['artifact']).read_bytes()).hexdigest()==m['sha256'],id
        used[id]=m
        return m,ROOT/m['artifact']
    def add(sid,year,value,unit,name,manifests,quality,note,formula='',inputs='',dimensions=None,analytic=True):
        assert math.isfinite(value),(sid,year)
        hashes=sorted({m['sha256'] for m in manifests})
        dim=dict(dimensions or {},input_hashes=hashes)
        rows.append(dict(country='CHN',year=int(year),series_id=sid,value=float(value),unit=unit,
                         source=';'.join(m['id'] for m in manifests),source_code=sid,
                         bronze_sha256=hashes[0] if len(hashes)==1 else '',flag=quality,
                         dimensions=json.dumps(dim,ensure_ascii=False,sort_keys=True),quality=quality,
                         analytic=analytic and year<=2025,formula=formula,input_series=inputs))
        catalog[sid]=dict(series_id=sid,name=name,unit=unit,quality=quality,analytic=analytic,
                          method_note=note,formula=formula,input_series=inputs,
                          source_url=';'.join(m['url'] for m in manifests),
                          bronze_sha256=';'.join(hashes),
                          independence='NO_ACREDITADA; coincidencia entre distribuidores no es validación independiente')
    def pwt(id):
        m,path=source(id);book=load_workbook(path,read_only=True,data_only=True)
        sheet=book['Data'];sheet.reset_dimensions();it=sheet.iter_rows(values_only=True);header=next(it)
        vals=[dict(zip(header,r)) for r in it if r[header.index('countrycode')]=='CHN']
        book.close();return m,pl.DataFrame(vals,infer_schema_length=None)

    # OECD annual national accounts, exact SDMX selection; all local units are millions CNY.
    om,op=source('china_complete_oecd_table1_20261102')
    source('china_complete_oecd_table1_structure_20261102')
    oecd=pl.read_csv(op,infer_schema_length=None)
    assert oecd['REF_AREA'].unique().to_list()==['CHN']
    oecd.group_by('TRANSACTION','PRICE_BASE','UNIT_MEASURE','TABLE_IDENTIFIER').agg(
        pl.len().alias('n'),pl.col('TIME_PERIOD').min().alias('first'),pl.col('TIME_PERIOD').max().alias('last')
    ).sort('TRANSACTION','PRICE_BASE','UNIT_MEASURE','TABLE_IDENTIFIER').write_csv(OUT/'oecd_inventario.csv')
    monetary=oecd.filter((pl.col('UNIT_MEASURE')=='XDC')&(pl.col('PRICE_BASE')=='V')&
                         (pl.col('TRANSFORMATION')=='N')&(pl.col('SECTOR')=='S1')&
                         (pl.col('COUNTERPART_SECTOR')=='S1'))
    assert monetary['UNIT_MULT'].unique().to_list()==[6]
    assert monetary['CURRENCY'].unique().to_list()==['CNY']
    income=monetary.filter(pl.col('TABLE_IDENTIFIER')=='T0103')
    assert not income.select(pl.struct('TRANSACTION','TIME_PERIOD').is_duplicated().any()).item()
    names={'D1':'Remuneración de asalariados distribuida por OCDE',
           'D2':'Impuestos publicados bajo D2 por OCDE; indicios de magnitud neta',
           'B2A3G':'Excedente bruto de explotación y renta mixta', 'B1GQ':'PIB nominal OCDE, tabla de rentas'}
    for r in income.iter_rows(named=True):
        if r['TRANSACTION'] not in names:continue
        code=r['TRANSACTION'];sid='OECD.INCOME.'+code
        note={'D1':'Coincide con usos domésticos NBS 2023 salvo redondeo. El tratamiento chino de trabajadores por cuenta propia puede diferir de España.',
              'D2':'Etiqueta OCDE D2; en 2023 coincide con impuestos NETOS NBS. No interpretar automáticamente como D2 bruto ni inferir D3=0.',
              'B2A3G':'Incluye renta mixta. No coincide exactamente con el residuo calculado con el PIB de esta edición; se preserva la serie publicada sin corrección.',
              'B1GQ':'PIB a precios de mercado; no sustituye producción bruta.'}[code]
        add(sid,r['TIME_PERIOD'],r['OBS_VALUE'],'million_CNY_current',names[code],[om],
            'PUBLICADA_ALCANCE_DIFERENTE' if code!='B1GQ' else 'PUBLICADA',note,
            dimensions={k:r[k] for k in ['TRANSACTION','ACTIVITY','TABLE_IDENTIFIER','PRICE_BASE','OBS_STATUS','UNIT_MULT']})
    wide=income.pivot(on='TRANSACTION',index='TIME_PERIOD',values='OBS_VALUE').rename({'TIME_PERIOD':'year'})
    income_checks=[]
    for r in wide.sort('year').iter_rows(named=True):
        if r.get('D1') is None or r.get('D2') is None or r.get('B1GQ') is None:continue
        y=r['year'];g=r['B1GQ'];tax=r['D2'];co=r['D1'];surplus=g-tax-co
        for sid,value,name,formula,note in [
            ('ALT.tax_net_oecd',tax,'Tributos netos: interpretación de la serie D2 china','OECD.INCOME.D2',
             'Hipótesis de trabajo respaldada por coincidencia 2023 con NBS y metodología nacional; no acreditada para cada año.'),
            ('ALT.gdp_factor_cost',g-tax,'PIB a coste de factores aproximado','OECD.INCOME.B1GQ - OECD.INCOME.D2',
             'Interpreta la serie tributaria china como neta; la hipótesis determina el resultado. No añadir después subvenciones de otra fuente.'),
            ('ALT.gross_surplus_residual',surplus,'Excedente bruto residual, incluida renta mixta y discrepancias','PIB - D1 - tributos_netos_aproximados',
             'Residuo de esta edición. Incluye renta mixta y discrepancias; no empalmar con B2A3G publicado.'),
        ]:
            add(sid,y,value,'million_CNY_current',name,[om],'APROXIMACION_DOCUMENTADA',note,formula,
                'OECD.INCOME.B1GQ;OECD.INCOME.D1;OECD.INCOME.D2')
        for code,value in [('D1',co),('D2',tax),('B2A3G',r.get('B2A3G'))]:
            if value is not None:
                add('SHARE.OECD.'+code,y,100*value/g,'percent_GDP','Peso en PIB de '+code,[om],
                    'DERIVADA_ALCANCE_DIFERENTE',names[code],f'100 * {code} / B1GQ','OECD.INCOME.'+code+';OECD.INCOME.B1GQ')
        if r.get('B2A3G') is not None:
            gap=surplus-r['B2A3G']
            income_checks.append(dict(year=y,published_surplus=r['B2A3G'],residual_surplus=surplus,
                                     difference=gap,difference_percent_GDP=100*gap/g))
    pl.DataFrame(income_checks).write_csv(OUT/'rentas_discrepancia.csv')
    for code in ['P52','P5M']:
        d=monetary.filter((pl.col('TRANSACTION')==code)&(pl.col('TABLE_IDENTIFIER')=='T0102'))
        assert not d['TIME_PERIOD'].is_duplicated().any()
        for r in d.iter_rows(named=True):
            y=r['TIME_PERIOD'];sid='OECD.DEMAND.'+code
            add(sid,y,r['OBS_VALUE'],'million_CNY_current','Existencias '+code+' nominales',[om],
                'PUBLICADA_NOMINAL','P5M=P52+P53; P52 solo existencias. Los dos coinciden en esta edición; no demuestra que P53 se mida como cero.')
            g=wide.filter(pl.col('year')==y)['B1GQ'][0]
            add('SHARE.OECD.'+code,y,100*r['OBS_VALUE']/g,'percent_GDP','Existencias nominales / PIB',[om],
                'DERIVADA_NOMINAL','Alternativa para peso de existencias; no crecimiento real.',f'100 * {code} / B1GQ',sid+';OECD.INCOME.B1GQ')

    # Fixed capital consumption: asset-specific approximation, never delta * GDP.
    cm,cap=pwt('pwt110_capital');nm,na=pwt('pwt110_na');source('pwt110_userguide')
    assert cap.filter(pl.col('year')==2021).select([pl.col('Np_'+a)==1 for a in ASSETS]).row(0)==(True,)*4
    cap=cap.drop_nulls([k+'_'+a for k in ['Dc','Np','Ip','Ic'] for a in ASSETS])
    assert cap.select(pl.all_horizontal([pl.col(k+'_'+a)>0 for k in ['Np','Ip'] for a in ASSETS]).all()).item()
    c=cap.select('year',pl.sum_horizontal([pl.col('Dc_'+a)/pl.col('Np_'+a) for a in ASSETS]).alias('ccf_np'),
                 pl.sum_horizontal([pl.col('Dc_'+a)/pl.col('Ip_'+a) for a in ASSETS]).alias('ccf_ip'),
                 pl.sum_horizontal([pl.col('Dc_'+a) for a in ASSETS]).alias('ccf_nominal'),
                 pl.sum_horizontal([pl.col('Ic_'+a) for a in ASSETS]).alias('investment_capital_detail'))
    c=c.join(na.select('year','v_gdp','v_gfcf'),on='year',how='left').sort('year')
    bases=c.filter(pl.col('year')==2021).row(0,named=True)
    c=c.with_columns((100*pl.col('ccf_np')/bases['ccf_np']).alias('index_np'),
                     (100*pl.col('ccf_ip')/bases['ccf_ip']).alias('index_ip'))
    c=c.with_columns((100*(pl.col('index_ip')/pl.col('index_np')-1)).alias('sensitivity_percent'),
                     (pl.col('investment_capital_detail')/pl.col('v_gfcf')).alias('investment_scale_ratio'))
    c.write_csv(OUT/'ccf_calculo_y_sensibilidad.csv')
    for r in c.iter_rows(named=True):
        for suffix,col,formula in [('NP','index_np','100 * sum(Dc_a/Np_a)_t / sum(Dc_a/Np_a)_2021'),
                                   ('IP','index_ip','100 * sum(Dc_a/Ip_a)_t / sum(Dc_a/Ip_a)_2021')]:
            add('ALT.CCF_REAL_INDEX_'+suffix,r['year'],r[col],'index_2021_100','CCF real aproximado, deflactor '+suffix,[cm],
                'ESTIMACION_PROPIA_SOBRE_PWT','Deflactación de CCF por cuatro grupos de activos. Np (stock) o Ip (inversión) no son deflactores específicos de CCF. Índice para evolución, no nivel comparable con AMECO.',formula,
                ';'.join('CAP.'+k+'_'+a for k in ['Dc','Np' if suffix=='NP' else 'Ip'] for a in ASSETS))
        if r['v_gdp'] is not None:
            add('SHARE.PWT.CCF',r['year'],100*r['ccf_nominal']/r['v_gdp'],'percent_GDP','CCF nominal PWT / PIB PWT',[cm,nm],
                'ESTIMACION_PWT_DERIVADA','Cociente monetario interno; escala común respaldada por inversión CAP/NA. No medida independiente NBS.',
                '100 * sum(Dc_a) / NA.v_gdp','CAP.Dc_Struc;CAP.Dc_Mach;CAP.Dc_TraEq;CAP.Dc_Other;NA.v_gdp')
    # Independent construction in WDI (but upstream sources may overlap).
    for short,sid,unit in [('ny_adj_dkap_gn_zs','WDI.CCF.PCT_GNI','percent_GNI'),
                           ('gc_tax_gsrv_cn','WDI.FISCAL.TAX_GOODS_SERVICES','CNY_current'),
                           ('gc_tax_intt_cn','WDI.FISCAL.TAX_TRADE','CNY_current')]:
        m,p=source('china_complete_wdi_'+short+'_20261102');obj=json.loads(p.read_text())
        assert obj[0]['pages']==1
        for r in obj[1]:
            if r['value'] is None:continue
            add(sid,int(r['date']),r['value'],unit,r['indicator']['value'],[m],
                'ALTERNATIVA_CONTEXTO','CCF nominal en % de RNB o impuestos fiscales parciales. No sustituyen CCF real, PIB ni D2 de contabilidad nacional.')
    # FRED published real inventory series: scaling cancels, concept limitation remains.
    fm,fp=source('china_inventory_search_fred_table_extract_20261102');f=json.loads(fp.read_text())
    base=next(r['value'] for r in f['observations'] if r['date'].startswith('2008'))
    for r in f['observations']:
        add('ALT.INVENTORIES_REAL_INDEX',int(r['date'][:4]),100*r['value']/base,'index_2008_100',
            'Variación real de existencias FMI/IFS, índice',[fm],'ALTERNATIVA_REAL_ALCANCE_PENDIENTE',
            'Escala monetaria y base originales sin resolver; se cancelan en el índice. Título Changes in Inventories, P53 no acreditado. Flujo anual, no stock; volátil y posible signo negativo.',
            '100 * NINVRXDCCNA_t / NINVRXDCCNA_2008','FRED.NINVRXDCCNA')
    # NBS 2023: use explicit working scale inference + scale-free ratios and coefficients.
    im,ip=source('china_nbs_03_21');flowm,flowp=source('china_nbs_03_15')
    source('china_complete_nbs_notes_2020_20261102')
    io_go=[159781.0,74035.5,114711.5,64191.7,74526.1,235448.9,73435.8,218778.1,521966.4,22817.4,
           127261.6,308711.4,184284.1,158842.1,64909.4,167609.5,127127.6,123358.8,147278.3,412386.9]
    go=3381462.2;inter=2080497.0;va=1300965.2
    assert abs(sum(io_go)-go)<1.1
    scale_note='Escala de trabajo inferida: 100 millones CNY por unidad nativa. D1 687230.1 coincide exactamente con tabla 3-15, que sí explicita unidad. No es metadato de unidad de la imagen IO. Precios de productor, año 2023.'
    for key,value in [('OUTPUT',go),('INTERMEDIATE',inter),('VALUE_ADDED',va)]:
        add('ALT.NBS.IO.'+key,2023,value*100,'million_CNY_current_scale_inferred','IO NBS '+key,[im,flowm],
            'ESCALA_INFERIDA_DOCUMENTADA',scale_note,'native_value * 100')
    for key,value,note in [('OUTPUT_VA',go/va,'Producción bruta/VAB; no producción/PIB mercado'),
                           ('INTERMEDIATE_OUTPUT',inter/go,'Consumos intermedios/producción'),
                           ('VA_OUTPUT',va/go,'VAB/producción')]:
        add('RATIO.NBS.IO.'+key,2023,value,'ratio',note,[im],'DERIVADA_ESTRUCTURAL','Escala se cancela; precios de productor 2023.',note)
    # Rows and columns are the same product order as the archived 20x20 transcription.
    matrix=pl.read_csv(ROOT/'output/revision_china/io_2023_20_sectors.csv')
    assert matrix.height==400 and matrix['bronze_sha256'].unique().to_list()==[im['sha256']]
    sectors=['agriculture']+['industry']*11+['services']*8
    gross={s:sum(x for x,g in zip(io_go,sectors) if g==s) for s in set(sectors)}
    tech=matrix.group_by('supplying_sector','using_sector').agg(pl.col('value').sum()).sort('supplying_sector','using_sector')
    tech=tech.with_columns(pl.col('using_sector').replace_strict(gross,return_dtype=pl.Float64).alias('gross_output_using'))
    tech=tech.with_columns((pl.col('value')/pl.col('gross_output_using')).alias('technical_coefficient'),
                          pl.lit(2023).alias('year'),pl.lit(im['sha256']).alias('bronze_sha256'))
    tech.write_csv(OUT/'io_2023_coeficientes_tecnicos.csv')
    pl.DataFrame({'product':list(range(1,21)),'sector':sectors,'gross_output_native':io_go}).write_csv(OUT/'io_produccion_transcrita.csv')
    # Point estimate, not a manufactured annual D3 series.
    sm,sp=source('china_complete_imf_cash_subsidy_extract_20261102');subsidies=json.loads(sp.read_text())
    for r in subsidies['observations']:
        add('ALT.IMF.CASH_SUBSIDIES',r['year'],r['value'],'percent_GDP',
            'Subvenciones monetarias a empresas no financieras, estimación FMI',[sm],
            'REFERENCIA_PUNTUAL_NO_D3','Estimación extrapolada de empresas cotizadas. Cifra redondeada; no D3 de economía total. Excel anual localizado pero inaccesible (403). No usar para cerrar PIB por rentas.')
    hm,hp=source('china_complete_nbs_price_subsidies_20261102')
    parser=TableRows();parser.feed(hp.read_bytes().decode('gb18030',errors='replace'))
    subsidy_rows=[]
    for cells in parser.rows:
        if not cells or not re.fullmatch(r'(19|20)\d{2}',cells[0]):continue
        assert len(cells)==6,cells
        year=int(cells[0]);vals=[float(v.replace(',','')) if v else None for v in cells[1:]]
        total=vals[0];assert total is not None
        assert abs(total-sum(v for v in vals[1:] if v is not None))<0.031,(year,vals)
        subsidy_rows.append(dict(year=year,total=total,grain_cotton_oil=vals[1],curbing_price_increase=vals[2],meat=vals[3],other=vals[4]))
        add('ALT.NBS.PRICE_SUBSIDIES',year,total*100,'million_CNY_current',
            'Gasto presupuestario en subvenciones a precios',[hm],'ALTERNATIVA_FISCAL_PARCIAL',
            'Solo subvenciones a precios, no D3 total; algunas ayudas pueden dirigirse a consumidores. Antes de 1986 se registraban como ingresos negativos. Años seleccionados 1978–1985 y anual 1990–2006; no empalmar con FMI 2023.',
            'NBS table 8-9 total * 100')
    assert len(subsidy_rows)==20,len(subsidy_rows)
    pl.DataFrame(subsidy_rows).write_csv(OUT/'subvenciones_precios_desglose.csv')
    new=pl.DataFrame(rows,infer_schema_length=None).sort('series_id','year')
    assert not new.select(pl.struct('series_id','year').is_duplicated().any()).item()
    old=pl.read_parquet(SILVER/'china.parquet')
    assert not set(old['series_id'])&set(new['series_id'])
    combined=pl.concat([old,new],how='vertical_relaxed').sort('series_id','year')
    for basename,d in [('china_suplemento',new),('china_completada',combined)]:
        d.write_parquet(SILVER/(basename+'.parquet'));d.write_csv(SILVER/(basename+'.csv'))
    annual=combined.filter(pl.col('analytic')).pivot(on='series_id',index='year',values='value').sort('year')
    annual.write_parquet(SILVER/'china_completada_anual.parquet');annual.write_csv(SILVER/'china_completada_anual.csv')
    for sid,r in catalog.items():
        ys=new.filter(pl.col('series_id')==sid)['year'];r.update(first=ys.min(),last=ys.max(),n=len(ys))
    pl.DataFrame(list(catalog.values())).sort('series_id').write_csv(OUT/'catalogo_suplemento.csv')
    write_json(OUT/'provenance.json',list(used.values()))
    # Working selection, keeping user-edited contracts byte-for-byte intact.
    selection=pl.read_csv(ROOT/'output/revision_china/contratos.csv',infer_schema_length=None).to_dicts()
    choices={
        'inventories_real':('ALT.INVENTORIES_REAL_INDEX','ALTERNATIVA_REAL','Índice 2008=100; 1980–2019; P53 no acreditado. Nominal OCDE disponible hasta 2024.'),
        'ccf_real':('ALT.CCF_REAL_INDEX_NP','ESTIMACION_EN_VOLUMEN','Índice 2021=100 con deflactores de stock por activo; sensibilidad Ip separada.'),
        'compensation':('OECD.INCOME.D1','ALTERNATIVA_PUBLICADA','Remuneración publicada; revisar tratamiento de cuenta propia.'),
        'gross_operating_surplus':('OECD.INCOME.B2A3G','ALTERNATIVA_PUBLICADA','Incluye renta mixta; hasta 2021. Residuo 1992–2023 separado, no prolongación de esta serie.'),
        'taxes':('ALT.tax_net_oecd','ALTERNATIVA_NETA','Magnitud interpretada como neta; no D2 bruto acreditado.'),
        'subsidies':('ALT.NBS.PRICE_SUBSIDIES','ALTERNATIVA_FISCAL_PARCIAL','Subvenciones a precios: 1978, 1980, 1985 y 1990–2006. No D3 total. FMI 2023 (2% PIB) separado, sin empalme.'),
        'gdp_factor_cost':('ALT.gdp_factor_cost','APROXIMACION_DOCUMENTADA','PIB menos tributos OCDE, interpretados como netos; no sumar la estimación FMI de subvenciones.'),
        'output':('ALT.NBS.IO.OUTPUT','ESTRUCTURAL_ESCALA_INFERIDA','2023, precios de productor, escala inferida; cocientes de escala libre disponibles.'),
        'intermediate_consumption':('ALT.NBS.IO.INTERMEDIATE','ESTRUCTURAL_ESCALA_INFERIDA','2023, precios de productor; cociente sobre producción disponible.'),
    }
    panel=[]
    for r in selection:
        k=r['concept'];r['original_status']=r['status'];r['original_selected_series']=r['selected_series']
        if k in choices:r['selected_series'],r['status'],r['usage_note']=choices[k]
        elif k in ['c_real','g_real','i_real','gfcf_real','x_real','m_real']:
            r['selected_series']='INDEX.'+r['candidate_series'];r['status']='INDICE_PWT_UTILIZABLE'
            r['usage_note']='Índice 2008=100 para evolución; no nivel monetario ni suma de volúmenes.'
        elif k=='input_output':
            r['status']='MATRIZ_ESTRUCTURAL_UTILIZABLE';r['usage_note']='Coeficientes técnicos 3×3 = flujos/producción del sector usuario, 2023.'
            r['structural_artifact']='output/revision_china/complecion/io_2023_coeficientes_tecnicos.csv'
        else:r['usage_note']='Serie previa conservada; cobertura y universo documentados en el catálogo original.'
        if k in choices or r['status']=='INDICE_PWT_UTILIZABLE':
            r['comparability']='ALTERNATIVA PARA EL TRABAJO: '+r['usage_note']
            r['decision']=r['usage_note']
        sid=r['selected_series'] or ''
        d=combined.filter((pl.col('series_id')==sid)&pl.col('analytic'))
        r.update(first=d['year'].min(),last=d['year'].max(),n=d.height)
        if d.height:
            r['unit']=d['unit'][0]
            r['missing_1960_2023']=';'.join(str(y) for y in sorted(set(range(1960,2024))-set(d['year'])))
            if sid in catalog:r['source_url']=catalog[sid]['source_url']
            panel.extend(dict(concept=k,year=x['year'],value=x['value'],series_id=sid,unit=x['unit'],status=r['status']) for x in d.iter_rows(named=True))
    pl.DataFrame(selection,infer_schema_length=None).write_csv(OUT/'seleccion_conceptos.csv')
    selected=pl.DataFrame(panel)
    selected.write_parquet(SILVER/'china_seleccion.parquet');selected.write_csv(SILVER/'china_seleccion.csv')
    selected.pivot(on='concept',index='year',values='value').sort('year').write_csv(SILVER/'china_seleccion_anual.csv')
    summary=dict(supplement_series=new['series_id'].n_unique(),supplement_observations=new.height,
                 combined_series=combined['series_id'].n_unique(),combined_observations=combined.height,
                 concepts=len(selection),concepts_with_numeric_data=len({r['concept'] for r in panel}),
                 structural_matrix=True,subsidies_D3_recovered=False,subsidies_partial_series_recovered=True,
                 ccf_sensitivity_max_percent=float(c['sensitivity_percent'].abs().max()),
                 income_discrepancy_max_percent_GDP=max(abs(r['difference_percent_GDP']) for r in income_checks))
    write_json(OUT/'resumen.json',summary);print(summary)

if __name__=='__main__':build()
