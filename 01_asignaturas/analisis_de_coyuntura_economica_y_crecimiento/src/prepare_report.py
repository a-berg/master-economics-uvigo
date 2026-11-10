"""Offline report-ready data, tables and figures. Keeps all source deliveries intact."""
from __future__ import annotations
import csv
import hashlib
import html
import json
import math
from pathlib import Path
import textwrap
import polars as pl
from openpyxl import load_workbook
from pipeline import write_json

ROOT=Path(__file__).resolve().parents[1]
GOLD=ROOT/'datos/gold/informe'
OUT=ROOT/'output/preparacion_informe'
LABELS={'CHN':'China','ESP':'España'}

class ReportData:
    def __init__(self):
        self.config=json.loads((ROOT/'datos/catalogo/informe_config.json').read_text())
        self.rows=[];self.catalog={};self.values={};self.inputs={};self.artifacts=[]
        for p in [GOLD,OUT,OUT/'figuras',GOLD/'figuras_datos',GOLD/'tablas']:
            p.mkdir(parents=True,exist_ok=True)
    def track(self,p):
        p=Path(p);p=p if p.is_absolute() else ROOT/p
        key=p.relative_to(ROOT).as_posix()
        self.inputs[key]=hashlib.sha256(p.read_bytes()).hexdigest()
        return p
    def manifest(self,id):
        path=self.track(ROOT/'datos/bronze'/id/'latest.json');m=json.loads(path.read_text())
        a=self.track(ROOT/m['artifact']);assert self.inputs[m['artifact']]==m['sha256'],id
        return m,a
    def add(self,c,m,y,v,unit,source,quality='PUBLICADA',note='',parents=(),formula=''):
        if v is None or y>self.config['end']:return
        v=float(v);assert math.isfinite(v),(c,m,y)
        key=(c,m)
        if key not in self.values:self.values[key]={}
        assert y not in self.values[key],(c,m,y)
        self.values[key][int(y)]=v
        self.rows.append(dict(country=c,year=int(y),metric=m,value=v,unit=unit,source=source,
                              quality=quality,formula=formula,input_metrics=';'.join(parents)))
        self.catalog[key]=dict(country=c,metric=m,unit=unit,source=source,quality=quality,
                               note=note,formula=formula,input_metrics=';'.join(parents))
    def get(self,c,m):return self.values.get((c,m),{})
    def derive(self,c,m,parents,fn,unit,formula,note='',quality='DERIVADA'):
        source='DERIVADA'
        years=set.intersection(*(set(self.get(c,k)) for k in parents))
        for y in sorted(years):
            vals=[self.get(c,k)[y] for k in parents]
            result=fn(*vals)
            if result is not None:self.add(c,m,y,result,unit,source,quality,note,parents,formula)
    def index(self,c,m,target=None,signed=False):
        vals=self.get(c,m);base=vals.get(self.config['index_base'])
        if base is None or base==0:return
        if not signed:assert base>0,(c,m,base)
        denom=abs(base) if signed else base
        self.derive(c,target or m+'_index',[m],lambda v:100*v/denom,'index_2008_abs100' if signed else 'index_2008_100',
                    '100 * value / '+('abs' if signed else '')+'(value_2008)',
                    'Conserva signo del flujo; base en valor absoluto.' if signed else 'La escala monetaria constante se cancela.')
    def sources(self):
        china=pl.read_parquet(self.track('datos/silver/china_completada.parquet'))
        spain=pl.read_parquet(self.track('datos/silver/espana.parquet')).filter(pl.col('apta_analisis')&~pl.col('forecast_period'))
        obs=pl.read_parquet(self.track('datos/silver/observations.parquet'))
        self.track('datos/catalogo/requirements.json');self.track('datos/catalogo/informe_config.json')
        self.track('output/revision_china/complecion/seleccion_conceptos.csv')
        self.track('output/revision_china/contratos.csv')
        self.track('output/revision_china/complecion/provenance.json')
        self.track('output/revision_china/provenance.json')
        self.track('output/revision_espana/catalogo_espana.csv')
        for path in ['output/revision_china/provenance.json','output/revision_china/complecion/provenance.json']:
            for m in json.loads((ROOT/path).read_text()):
                if m.get('artifact') and m.get('sha256'):
                    self.track(m['artifact']);assert self.inputs[m['artifact']]==m['sha256']
        for id in ['wdi_common',*spain['source'].unique().to_list()]:
            if (ROOT/'datos/bronze'/id/'latest.json').exists():self.manifest(id)
        def pull(c,frame,sid,metric,scale=1,unit=None,note=''):
            for r in frame.filter(pl.col('series_id')==sid).iter_rows(named=True):
                q=r.get('quality',r.get('status','PUBLICADA'))
                self.add(c,metric,r['year'],r['value']*scale,unit or r['unit'],sid,q,note)
        self.pull=pull
        # Read PWT workbooks, not the stale gold panel. Same edition for both countries.
        for id,prefix in [('pwt110','PWT'),('pwt110_na','NA'),('pwt110_capital','CAP')]:
            m,path=self.manifest(id);book=load_workbook(path,read_only=True,data_only=True)
            sheet=book['Data'];sheet.reset_dimensions();it=sheet.iter_rows(values_only=True);header=next(it)
            for rr in it:
                r=dict(zip(header,rr));c=r.get('countrycode')
                if c not in LABELS:continue
                y=int(r['year'])
                if prefix=='PWT':
                    for src,metric,scale,unit in [
                        ('rgdpna','gdp_pwt',1,'million_USD_2021_national_constant'),('rnna','capital_pwt',1,'million_USD_2021_national_constant'),
                        ('rgdpe','gdp_ppp',1,'million_USD_2021_PPP'),('emp','employment_pwt',1e6,'persons'),
                        ('pop','population_pwt',1e6,'persons'),('avh','hours_average',1,'hours_per_person_year'),('delta','depreciation_pwt',100,'percent')]:
                        if r.get(src) is not None:self.add(c,metric,y,r[src]*scale,unit,id+':'+src,'ESTIMACION_PWT')
                elif prefix=='NA':
                    for k in ['q_gdp','q_c','q_i','q_g','q_gfcf','q_x','q_m','v_gdp','v_c','v_i','v_g','v_x','v_m']:
                        self.add(c,'na_'+k,y,r.get(k),'native_PWT_NA_scale_not_used_for_levels',id+':'+k,'ESTIMACION_PWT',
                                 'Solo índices, tasas y cocientes internos; no se afirma escala monetaria.')
                else:
                    assets=['Struc','Mach','TraEq','Other']
                    keys=[k+'_'+a for k in ['Dc','Nc','Np','Ip','Ic'] for a in assets]
                    if any(r.get(k) is None for k in keys):continue
                    self.add(c,'ccf_proxy',y,sum(r['Dc_'+a]/r['Np_'+a] for a in assets),'native_PWT_real_proxy',id,
                             'APROXIMACION','ΣDc/Np por cuatro activos; deflactores del stock, no específicos de CCF.')
                    self.add(c,'depreciation_assets',y,100*sum(r['Dc_'+a] for a in assets)/sum(r['Nc_'+a] for a in assets),'percent',id,
                             'APROXIMACION','CCF nominal / stock neto a coste corriente, cuatro activos. No dividir un índice de CCF por rnna.')
                    for k,metric in [('Ic_Mach','machinery_gross'),('Dc_Mach','machinery_replacement')]:
                        self.add(c,metric,y,r[k],'native_PWT_current',id+':'+k,'ESTIMACION_PWT',
                                 'Maquinaria y equipo no de transporte; inversión y CCF a precios corrientes, no unidades físicas de máquinas.')
            book.close()
        for c in LABELS:
            for m in ['FP.CPI.TOTL','NY.GDP.MKTP.CN','NY.GDP.MKTP.KN','SP.POP.TOTL','SP.POP.0014.TO','SP.POP.65UP.TO',
                      'SL.TLF.TOTL.IN','SL.UEM.TOTL.ZS','SI.POV.GINI']:
                if c=='CHN':z=china.filter(pl.col('series_id')=='WDI.'+m)
                else:z=obs.filter((pl.col('country')==c)&(pl.col('source')=='wdi_common')&(pl.col('series')==m)).rename({'series':'series_id'})
                target={'FP.CPI.TOTL':'cpi','NY.GDP.MKTP.CN':'gdp_nominal_wdi','NY.GDP.MKTP.KN':'gdp_real_wdi',
                        'SP.POP.TOTL':'population','SP.POP.0014.TO':'pop_0_14','SP.POP.65UP.TO':'pop_65plus',
                        'SL.TLF.TOTL.IN':'labor_force','SL.UEM.TOTL.ZS':'unemployment_rate_model','SI.POV.GINI':'gini'}[m]
                unit='persons' if target in ['population','pop_0_14','pop_65plus','labor_force'] else 'percent' if 'rate' in target else 'index_0_100' if target=='gini' else 'index_provider_base' if target=='cpi' else 'national_currency_provider_valuation'
                for r in z.iter_rows(named=True):self.add(c,target,r['year'],r['value'],unit,'WDI.'+m,
                    'MODELIZADA_OIT_WDI' if target in ['labor_force','unemployment_rate_model'] else 'PUBLICADA',
                    'Encuesta de hogares, bienestar y años observados; no causalidad.' if target=='gini' else '')
            # National accounts for wages and income: explicit source combinations.
            if c=='CHN':
                for sid,metric,scale,unit in [
                    ('OECD.INCOME.D1','compensation',1e6,'CNY_current'),('OECD.INCOME.B1GQ','income_gdp',1e6,'CNY_current'),
                    ('OECD.INCOME.B2A3G','surplus',1e6,'CNY_current'),('ALT.tax_net_oecd','tax_net',1e6,'CNY_current'),
                    ('ALT.gdp_factor_cost','factor_gdp',1e6,'CNY_current'),('ALT.NBS.PRICE_SUBSIDIES','subsidies',1e6,'CNY_current'),
                    ('ALT.INVENTORIES_REAL_INDEX','inventories',1,'index_2008_100'),
                    ('ALT.NBS.IO.OUTPUT','output',1e6,'CNY_current_scale_inferred'),
                    ('ALT.NBS.IO.INTERMEDIATE','intermediate',1e6,'CNY_current_scale_inferred'),
                    ('ALT.NBS.IO.VALUE_ADDED','value_added',1e6,'CNY_current_scale_inferred'),
                    ('NBS.REGISTERED_UNEMPLOYED.URBAN','registered_unemployment',1e4,'persons'),
                    ('ILO.UNE_TUNE_SEX_AGE_NB.BA:16044','survey_unemployment',1e3,'persons')]:
                    pull(c,china,sid,metric,scale,unit)
                self.derive(c,'gdp_nominal',['gdp_nominal_wdi'],lambda x:x,'CNY_current','WDI GDP current')
                self.derive(c,'gdp_real_national',['gdp_real_wdi'],lambda x:x,'CNY_constant_provider_base','WDI GDP volume')
            else:
                for suffix,metric in [('UVGD','gdp_nominal'),('UWCD','compensation'),('UOGD','surplus'),('UYGD','factor_gdp'),('UTVT','tax_gross'),('UYVT','subsidies'),('OIST','inventories')]:
                    pull(c,spain,'ESP.1.0.0.0.'+suffix,metric,1e9,'EUR_constant_2020' if suffix=='OIST' else 'EUR_current')
                pull(c,spain,'ESP.1.1.0.0.OVGD','gdp_real_national',1e9,'EUR_constant_2020')
                for sid,metric in [('INE.CEI.P1','output'),('INE.CEI.P2','intermediate'),('INE.CEI.B1G','value_added')]:pull(c,spain,sid,metric,1e6,'EUR_current')
                pull(c,spain,'SEPE.REGISTERED.UNEMPLOYED.ANNUAL_MEAN','registered_unemployment',1,'persons')
                pull(c,spain,'INE.EPA.ANNUAL.PARADOS','survey_unemployment',1e3,'persons')
                self.derive(c,'income_gdp',['gdp_nominal'],lambda x:x,'EUR_current','AMECO GDP')
                self.derive(c,'tax_net',['tax_gross','subsidies'],lambda a,b:a-b,'EUR_current','D2 - D3')
        self.indicators()
    def indicators(self):
        for c in LABELS:
            self.derive(c,'deflator',['gdp_nominal','gdp_real_national'],lambda a,b:100*a/b if b>0 else None,'index_provider_base','100 * GDP nominal / GDP real')
            self.derive(c,'pop_15plus',['population','pop_0_14'],lambda a,b:a-b,'persons','population - age 0–14')
            self.derive(c,'pop_15_64',['pop_15plus','pop_65plus'],lambda a,b:a-b,'persons','population 15+ - 65+')
            for m in ['pop_0_14','pop_15plus','pop_65plus']:
                self.derive(c,m+'_share',[m,'population'],lambda a,b:100*a/b,'percent_population',f'100 * {m} / population')
            self.derive(c,'unemployment_model',['labor_force','unemployment_rate_model'],lambda a,b:a*b/100,'persons','labor force * modeled unemployment rate / 100',
                        'Derivación para comparación común; no encuesta nacional ni paro registrado.')
            self.derive(c,'employment_model',['labor_force','unemployment_model'],lambda a,b:a-b,'persons','labor force - modeled unemployed')
            for m,out in [('labor_force','activity_rate'),('employment_model','employment_rate')]:
                self.derive(c,out,[m,'pop_15plus'],lambda a,b:100*a/b,'percent_15plus',f'100 * {m} / WDI population 15+',
                            'Tasa aproximada: combina activos modelizados con población WDI; no tasa EPA.')
            self.derive(c,'hours_total',['employment_pwt','hours_average'],lambda a,b:a*b,'hours_year','PWT employed persons * average hours')
            self.derive(c,'equivalent_employment',['hours_total'],lambda a:a/1760,'persons_equivalent','total hours / 1760','Aproximación docente, no FTE observado.')
            self.derive(c,'productivity_worker',['gdp_pwt','employment_pwt'],lambda a,b:a*1e6/b,'USD_2021_national_per_worker','GDP PWT * 1e6 / employed persons')
            self.derive(c,'productivity_worker_national',['gdp_real_national','employment_pwt'],lambda a,b:a/b,'national_constant_currency_per_worker',
                        'national real GDP / PWT employed persons','Base nacional para comparar evolución de productividad y remuneración real del tema 3.')
            self.derive(c,'productivity_hour',['gdp_pwt','hours_total'],lambda a,b:a*1e6/b,'USD_2021_national_per_hour','GDP PWT * 1e6 / total hours')
            self.derive(c,'capital_worker',['capital_pwt','employment_pwt'],lambda a,b:a*1e6/b,'USD_2021_national_per_worker','capital PWT * 1e6 / employed persons')
            self.derive(c,'capital_hour',['capital_pwt','hours_total'],lambda a,b:a*1e6/b,'USD_2021_national_per_hour','capital PWT * 1e6 / total hours')
            self.derive(c,'gdp_capital',['gdp_pwt','capital_pwt'],lambda a,b:a/b,'ratio','GDP PWT / capital PWT')
            self.derive(c,'gdp_pc_ppp',['gdp_ppp','population_pwt'],lambda a,b:a*1e6/b,'USD_2021_PPP_per_person','PWT expenditure-side PPP GDP / population')
            self.derive(c,'gdp_pc_national',['gdp_pwt','population_pwt'],lambda a,b:a*1e6/b,'USD_2021_national_per_person','PWT national-constant GDP / population')
            self.derive(c,'wage_nominal',['compensation','employment_pwt'],lambda a,b:a/b,'CNY_per_employed_year' if c=='CHN' else 'EUR_per_employed_year',
                        'National D1 / PWT employed persons','Promedio por ocupado, incluidos autónomos en el denominador. No salario por asalariado; numerador nacional y empleo PWT combinados explícitamente.',quality='APROXIMACION_POR_OCUPADO')
            self.index(c,'deflator')
            self.derive(c,'wage_real',['wage_nominal','deflator_index'],lambda a,b:100*a/b,'national_currency_2008_per_employed_year',
                        'nominal D1 per employed / (GDP deflator 2008=100 / 100)','Poder adquisitivo medido con deflactor del PIB, no con IPC.',quality='APROXIMACION_POR_OCUPADO')
            for m in ['c','i','g','x','m']:
                self.derive(c,'share_'+m,['na_v_'+m,'na_v_gdp'],lambda a,b:100*a/b,'percent_GDP',f'100 * NA.v_{m} / NA.v_gdp',
                            'Participación nominal, no suma de volúmenes. Importaciones se muestran positivas y se restan al cerrar PIB.')
            self.derive(c,'demand_gap',['share_c','share_i','share_g','share_x','share_m'],lambda a,b,d,e,f:100-(a+b+d+e-f),'percent_GDP','100 - (C+I+G+X-M) shares','Discrepancia conservada, sin ajuste.')
            for m in ['compensation','surplus']:
                self.derive(c,m+'_factor_share',[m,'factor_gdp'],lambda a,b:100*a/b,'percent_factor_GDP',f'100 * {m} / factor GDP',
                            'China: coste de factores aproximado y excedente incluye renta mixta. No imponer suma 100.')
            for m in ['intermediate','value_added']:
                self.derive(c,m+'_output_share',[m,'output'],lambda a,b:100*a/b,'percent_output',f'100 * {m} / gross output','VAB, no PIB de mercado.')
            self.derive(c,'machinery_replacement_share',['machinery_replacement','machinery_gross'],lambda a,b:100*a/b if b>0 else None,'percent_gross_machinery_investment',
                        '100 * Dc_Mach / Ic_Mach','Magnitudes nominales de maquinaria y equipo; el CCF no observa compras de reposición.')
            for m in ['gdp_pwt','capital_pwt','gdp_nominal','gdp_real_national','cpi','wage_nominal','wage_real','ccf_proxy',
                      'productivity_worker','productivity_hour','capital_worker','capital_hour','machinery_gross','machinery_replacement']:
                self.index(c,m)
            for m in ['gdp','c','i','g','gfcf','x','m']:self.index(c,'na_q_'+m)
            self.index(c,'inventories',signed=True)
        originals=list(self.values.items())
        for (c,m),vals in originals:
            if m.endswith('_index') or m in ['gini','registered_unemployment','survey_unemployment','inventories']:continue
            if m not in ['gdp_pwt','gdp_nominal','gdp_real_national','capital_pwt','ccf_proxy','employment_pwt','hours_total','labor_force','employment_model','unemployment_model',
                         'pop_0_14','cpi','deflator','wage_nominal','wage_real','productivity_worker','productivity_worker_national','productivity_hour'] and not m.startswith('na_q_'):continue
            for y,a in sorted(vals.items()):
                b=vals.get(y-1)
                if a>0 and b is not None and b>0:
                    self.add(c,'growth_'+m,y,100*(a/b-1),'percent_change',self.catalog[c,m]['source'],'DERIVADA',
                             'Años consecutivos observados y valores positivos.',(m,),'100 * (x_t / x_tminus1 - 1)')
            inv=self.get(c,'inventories_index')
            if m=='gdp_pwt':
                for y,a in inv.items():
                    if y-1 in inv:self.add(c,'change_inventories',y,a-inv[y-1],'index_points_change','DERIVADA','ADAPTACION_FLUJO',
                        'Cambio del flujo escalado, no tasa porcentual. Desviación relativa omitida.',('inventories_index',),'inventory index_t - inventory index_tminus1')
    def export(self):
        data=pl.DataFrame(self.rows).sort('country','metric','year')
        data.write_parquet(GOLD/'indicadores.parquet');data.write_csv(GOLD/'indicadores.csv')
        data.pivot(on='metric',index=['country','year'],values='value').sort('country','year').write_parquet(GOLD/'panel_anual.parquet')
        cat=[]
        for key,r in sorted(self.catalog.items()):
            ys=self.values[key];cat.append(dict(**r,first=min(ys),last=max(ys),n=len(ys)))
        pl.DataFrame(cat).write_csv(GOLD/'diccionario.csv')
        return data
    def register(self,id,title,kind,path,note='',status='PREPARADO',countries='CHN;ESP',reference='',data_path='',missing=''):
        self.artifacts.append(dict(id=id,title=title,kind=kind,path=path.relative_to(ROOT).as_posix() if isinstance(path,Path) else path,
                                   data_path=data_path.relative_to(ROOT).as_posix() if isinstance(data_path,Path) else data_path,
                                   status=status,countries=countries,reference=reference,note=note,missing=missing))
    def stats(self,id,title,variables,reference,notes='',pairs=False):
        rows=[];samples=[]
        for start,end in self.config['cycle_windows']:
            for metric in variables:
                common=set(range(start,end+1))
                for c in LABELS:common&=set(self.get(c,metric))&set(self.get(c,reference))
                for c in LABELS:
                    ys=sorted(common);a=[self.get(c,reference)[y] for y in ys];b=[self.get(c,metric)[y] for y in ys]
                    n=len(ys);sx=pl.Series(a).std(ddof=1) if n>=2 else None;sy=pl.Series(b).std(ddof=1) if n>=2 else None
                    corr=pl.DataFrame({'x':a,'y':b}).select(pl.corr('x','y')).item() if n>=3 and sx and sy else None
                    unit=self.catalog.get((c,metric),{}).get('unit','');same=unit==self.catalog.get((c,reference),{}).get('unit','')
                    rows.append(dict(country=c,window_start=start,window_end=end,metric=metric,reference_metric=reference,n=n,
                                     actual_first=min(ys) if ys else None,actual_last=max(ys) if ys else None,sample_years=';'.join(map(str,ys)),
                                     mean=sum(b)/n if n else None,sample_sd=sy,correlation=corr,
                                     relative_sd=sy/sx if same and sx and sy is not None else None,
                                     unit=unit,mean_reference=sum(a)/n if n else None,
                                     status='OK' if n>=3 else 'MUESTRA_INSUFICIENTE',note=notes))
                    samples.extend(dict(table=id,country=c,year=y,metric=metric,reference_metric=reference,
                                        value=v,reference_value=x,window_start=start,window_end=end) for y,x,v in zip(ys,a,b))
        path=GOLD/'tablas'/(id+'.csv');pl.DataFrame(rows,infer_schema_length=None).write_csv(path)
        if samples:pl.DataFrame(samples).write_csv(GOLD/'tablas'/(id+'_muestras.csv'))
        self.register(id,title,'tabla',path,notes,reference=reference)
    def means(self,id,title,variables,notes=''):
        rows=[]
        for start,end in self.config['mean_windows']:
            common=set(range(start,end+1))
            for c in LABELS:
                for m in variables:common&=set(self.get(c,m))
            for c in LABELS:
                for m in variables:
                    vals=[self.get(c,m)[y] for y in sorted(common)]
                    rows.append(dict(country=c,start=start,end=end,metric=m,n=len(vals),
                                     actual_first=min(common) if common else None,actual_last=max(common) if common else None,
                                     mean=sum(vals)/len(vals) if vals else None,sample_years=';'.join(map(str,sorted(common))),note=notes))
        path=GOLD/'tablas'/(id+'.csv');pl.DataFrame(rows,infer_schema_length=None).write_csv(path)
        self.register(id,title,'tabla',path,notes,status='PREPARADO_CON_NOTA' if notes else 'PREPARADO')
    def tables(self):
        self.means('2B.T1','Participaciones medias de demanda',['share_c','share_i','share_g','share_x','share_m'],
                   'Medias de cocientes nominales, no cociente de sumas; misma muestra de componentes y países.')
        self.stats('2B.T3','Ciclo de demanda',['growth_na_q_'+m for m in ['gdp','c','i','g','x','m']],
                   'growth_na_q_gdp','PIB y componentes de la misma edición PWT NA; tasas anuales.')
        self.means('2C.T1','Depreciación media del capital',['depreciation_assets','depreciation_pwt'],
                   'CCF/stock neto a coste corriente y tasa delta publicada PWT; alternativas separadas, no CCF índice / stock monetario.')
        self.stats('2C.T2','Ciclo de capital e inversión',['growth_capital_pwt','growth_na_q_i','growth_na_q_gfcf','change_inventories','growth_ccf_proxy'],
                   'growth_gdp_pwt','VE: correlación de cambios anuales escalados, sin desviación relativa; CCF aproximado.')
        self.stats('2C.T3','Ciclo de trabajo y productividad',['growth_gdp_pwt','growth_employment_pwt','growth_hours_total','growth_productivity_worker','growth_productivity_hour'],
                   'growth_gdp_pwt','PIB, empleo, horas y capital de PWT; horas totales=ocupados×horas medias.')
        self.means('2D.T1','Rentas respecto al PIB a coste de factores',['compensation_factor_share','surplus_factor_share'],
                   'China: coste de factores aproximado, excedente con renta mixta; muestra común termina en 2021. No imponer cierre.')
        io=pl.read_csv(self.track('output/revision_china/complecion/io_2023_coeficientes_tecnicos.csv'))
        path=GOLD/'tablas/2D.T2_CHN.csv';io.write_csv(path)
        self.register('2D.T2','Input-output en tres sectores','tabla',path,
                      'China 2023: flujos en unidad nativa y coeficientes técnicos. Tabla española aún sin incorporar.',
                      status='PARCIAL',countries='CHN',missing='Matriz española equivalente no incorporada.')
        self.stats('3.T1','Precios y PIB real',['growth_cpi','growth_deflator','growth_gdp_real_national'],'growth_gdp_real_national',
                   'Estadística sobre inflación y crecimiento, no sobre niveles crecientes.')
        self.stats('3.T2','Precios y PIB nominal',['growth_cpi','growth_deflator','growth_gdp_real_national','growth_gdp_nominal'],'growth_gdp_nominal')
        self.stats('3.T3','Rentas por ocupado y ciclo',['growth_gdp_real_national','growth_wage_nominal','growth_deflator','growth_wage_real'],'growth_gdp_real_national',
                   'Remuneración por ocupado, no por asalariado; numerador nacional y denominador PWT.')
        pair_rows=[]
        for a,b in [('growth_wage_real','growth_productivity_worker_national'),('growth_wage_real','growth_deflator'),
                    ('growth_wage_nominal','growth_deflator'),('growth_wage_nominal','growth_gdp_nominal')]:
            self.stats('3.T3_'+a.removeprefix('growth_')+'_'+b.removeprefix('growth_'),'Correlación '+a+' / '+b,[b],a,
                       'Correlación descriptiva de tasas; muestra común entre países.')
        self.stats('3.T4','Empleo y paro frente a remuneración real',['growth_unemployment_model','growth_employment_model'],'growth_wage_real',
                   'Empleo/paro modelizados OIT-WDI. No coeficiente causal de salarios sobre empleo.')
        self.stats('4.T1','Ciclo laboral',['growth_gdp_pwt','growth_pop_0_14','growth_labor_force','growth_employment_model','growth_unemployment_model'],'growth_gdp_pwt',
                   'Bloque laboral común OIT/WDI; no confundir con PWT empleo del bloque de producción.')
        growth=[]
        for c in LABELS:
            for start,end in self.config['growth_periods']:
                metrics=['gdp_pwt','capital_pwt','employment_pwt','population_pwt']
                assert all(start in self.get(c,m) and end in self.get(c,m) for m in metrics),(c,start,end)
                g={m:100*math.log(self.get(c,m)[end]/self.get(c,m)[start])/(end-start) for m in metrics}
                alpha=self.config['alpha'];gy=g['gdp_pwt'];gk=g['capital_pwt'];gl=g['employment_pwt'];gp=g['population_pwt']
                growth.append(dict(country=c,start=start,end=end,years=end-start,gdp_log_pp=gy,gdp_pc_log_pp=gy-gp,
                                   gdp_cagr_pct=100*math.expm1(gy/100),gdp_pc_cagr_pct=100*math.expm1((gy-gp)/100),
                                   capital_log_pp=gk,employment_log_pp=gl,population_log_pp=gp,
                                   capital_contribution_pp=alpha*gk,labor_contribution_pp=(1-alpha)*gl,
                                   solow_residual_pp=gy-alpha*gk-(1-alpha)*gl,alpha=alpha))
        g=pl.DataFrame(growth);g.write_csv(GOLD/'tablas/7.T1.csv')
        self.register('7.T1','Contabilidad del crecimiento 1960–2023','tabla',GOLD/'tablas/7.T1.csv',
                      'Mismos subperiodos que 6.T3–6.T4; logaritmos anualizados y α=1/3. Residuo no identifica solo tecnología.')
        for id,col,aggregate,title in [('6.T1','gdp_cagr_pct',True,'Crecimiento medio del PIB'),('6.T2','gdp_pc_cagr_pct',True,'Crecimiento medio por habitante'),
                                       ('6.T3','gdp_cagr_pct',False,'PIB por subperiodos'),('6.T4','gdp_pc_cagr_pct',False,'PIB por habitante y subperiodos')]:
            d=g.filter((pl.col('start')==1960)&(pl.col('end')==2023)) if aggregate else g.filter(
                ~((pl.col('start').is_in([1960,1990]))&(pl.col('end')==2023)))
            d.select('country','start','end','years',pl.col(col).alias('cagr_pct')).write_csv(GOLD/'tablas'/(id+'.csv'))
            self.register(id,title,'tabla',GOLD/'tablas'/(id+'.csv'),
                          'Comparativa China–España PWT. Las referencias históricas de otros países utilizadas en clase no se han reconstruido ni sustituido.',
                          status='ADAPTADO',missing='Referencias históricas docentes adicionales, si se exige reproducirlas literalmente.')
        self.growth=g
    def figure(self,id,title,metrics=None,x=None,ys=None,note='',status='PREPARADO',unit='',start=None,scale=1):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
        start=self.config['comparison_start'] if start is None else start
        inventory_panel=id=='2C.1'
        if inventory_panel:
            fig,grid_axes=plt.subplots(2,2,figsize=(12,7));axes=grid_axes[0]
        else:fig,axes=plt.subplots(1,2,figsize=(12,4.5))
        records=[];missing=[]
        for country_pos,(c,ax) in enumerate(zip(LABELS,axes)):
            if x:
                for m,label in ys:
                    years=sorted(set(self.get(c,x))&set(self.get(c,m))&set(range(start,self.config['end']+1)))
                    xx=[self.get(c,x)[y] for y in years];yy=[self.get(c,m)[y] for y in years]
                    ax.scatter(xx,yy,s=14,alpha=.7,label=label)
                    records.extend(dict(country=c,year=y,x_metric=x,y_metric=m,x_value=a,y_value=b,
                                        x_unit=self.catalog[c,x]['unit'],y_unit=self.catalog[c,m]['unit']) for y,a,b in zip(years,xx,yy))
                xlabel={'employment_pwt':'Ocupados (personas)','hours_total':'Horas totales anuales',
                        'growth_gdp_pwt':'Crecimiento del PIB (%)','capital_worker':'Capital por ocupado (USD nacionales 2021)',
                        'growth_wage_real':'Crecimiento de remuneración real por ocupado (%)',
                        'gdp_pc_ppp':'PIB por habitante (USD PPA de 2021)'}[x]
                ax.set_xlabel(xlabel);ax.set_ylabel(unit)
            else:
                for m,label in metrics:
                    data={y:v for y,v in self.get(c,m).items() if start<=y<=self.config['end']}
                    years=sorted(data)
                    # Preserve missing years as breaks; do not connect across missing observations.
                    if years:
                        grid=range(min(years),max(years)+1)
                        plot_ax=grid_axes[1,country_pos] if inventory_panel and m=='inventories_index' else ax
                        plot_ax.plot(list(grid),[data.get(y,float('nan'))/scale for y in grid],marker='o' if len(years)<7 else None,ms=3,label=label)
                        original_unit=self.catalog[c,m]['unit']
                        plotted_unit=('million_'+original_unit if scale==1e6 else 'billion_'+original_unit if scale==1e9 else original_unit)
                        records.extend(dict(country=c,year=y,metric=m,value=data[y]/scale,original_value=data[y],scale_divisor=scale,
                                            unit=plotted_unit,original_unit=original_unit) for y in years)
                ax.set_xlabel('Año');ax.set_ylabel(unit)
                if scale==1e9:ax.set_ylabel('Miles de millones '+('CNY' if c=='CHN' else 'EUR'))
                if id=='3.4':ax.set_ylabel(('CNY' if c=='CHN' else 'EUR')+' por ocupado y año')
                if inventory_panel:
                    ax.set_ylabel('2008 = 100')
                    inv_ax=grid_axes[1,country_pos];inv_ax.set(xlabel='Año',ylabel='VE: escala |valor 2008| = 100')
                    inv_ax.axhline(0,color='gray',lw=.8);inv_ax.grid(alpha=.2);inv_ax.legend(fontsize=7)
            n=sum(r['country']==c for r in records)
            if not n:
                ax.text(.5,.5,'Datos no incorporados',ha='center',va='center',transform=ax.transAxes);missing.append(c)
            else:ax.legend(fontsize=7,loc='best')
            ax.set_title(LABELS[c]);ax.grid(alpha=.2)
        fig.suptitle(id+' · '+title,fontsize=12)
        fig.text(.02,.01,textwrap.fill(note[:240],145),fontsize=7,va='bottom')
        fig.tight_layout(rect=(0,.10,1,.94))
        path=OUT/'figuras'/(id+'.svg');fig.savefig(path);fig.savefig(path.with_suffix('.png'),dpi=125);plt.close(fig)
        data_path=GOLD/'figuras_datos'/(id+'.csv')
        if records:pl.DataFrame(records,infer_schema_length=None).write_csv(data_path)
        self.register(id,title,'grafico',path,note,status='PARCIAL' if missing else status,data_path=data_path,
                      missing=';'.join(missing))
    def figures(self):
        f=self.figure
        f('2A.1','Producción, consumos intermedios y VAB',metrics=[('output','Producción'),('intermediate','Intermedios'),('value_added','VAB')],
          scale=1e9,unit='Miles de millones, moneda nacional',status='ADAPTADO',
          note='China: IO 2023 a precios de productor y escala inferida. España: cuentas integradas INE. Se muestra VAB; producción−CI no es PIB de mercado.')
        f('2A.3_ratios','Usos intermedios y valor añadido',metrics=[('intermediate_output_share','CI/producción'),('value_added_output_share','VAB/producción')],unit='% de producción',status='ADAPTADO',
          note='China: un año estructural, 2023. España: serie INE. Los cocientes cancelan la escala monetaria. Identificador 2A.3 duplicado en las instrucciones: aquí p.19.')
        f('2A.3_pib','PIB nominal y real',metrics=[('gdp_nominal_index','PIB nominal'),('gdp_real_national_index','PIB real')],unit='2008 = 100',status='ADAPTADO',
          note='Bases nacionales WDI China y AMECO España. Índices para mostrar divergencia de precios sin equiparar monedas ni bases; referencia docente p.27.')
        demand=[('na_q_'+m+'_index',label) for m,label in [('gdp','PIB'),('c','Hogares'),('i','Inversión'),('g','Gobierno'),('x','Exportaciones'),('m','Importaciones')]]
        f('2B.1','Demanda real',metrics=demand[1:],unit='2008 = 100',status='ADAPTADO',note='PWT NA: índices de cada componente. Se adapta la figura de niveles para evitar comparar escalas monetarias pendientes. No se suman volúmenes.')
        f('2B.3_shares','Composición nominal de la demanda',metrics=[('share_'+m,label) for m,label in [('c','C'),('i','Inversión'),('g','G'),('x','X'),('m','M')]],unit='% PIB',
          note='PWT NA, componentes y PIB corrientes de la misma edición. M se muestra positiva; en la identidad del PIB se resta. La discrepancia se conserva.')
        f('2B.3_growth','Crecimiento de los componentes de demanda',metrics=[('growth_na_q_'+m,label) for m,label in [('gdp','PIB'),('c','C'),('i','Inversión'),('g','G'),('x','X'),('m','M')]],unit='Variación anual (%)',
          note='Tasas de PWT NA. Solo años consecutivos observados y valores positivos; equivalente a cuatro paneles docentes p.26–30.')
        f('2B.4','Demanda desde la crisis financiera',metrics=demand,unit='2008 = 100',start=2008,note='PWT NA, misma edición para ambos países; normalización dentro de cada serie.')
        f('2C.1','Inversión, existencias y consumo de capital',metrics=[('na_q_i_index','Inversión'),('na_q_gfcf_index','FBCF'),('inventories_index','Existencias (flujo)'),('ccf_proxy_index','CCF aproximado')],
          unit='Índices; VE usa |valor 2008|',status='ADAPTADO',note='Escalas normalizadas, no identidad contable. CCF: aproximación por activos PWT. VE: flujo de distinta fuente y cobertura; conserva signo, no crecimiento porcentual.')
        f('2C.2','Inversión y consumo de capital en maquinaria',metrics=[('machinery_gross_index','Inversión bruta'),('machinery_replacement_index','CCF maquinaria')],unit='2008 = 100',status='ADAPTADO',
          note='PWT detalle de maquinaria y equipo no de transporte, magnitudes nominales normalizadas. CCF aproxima desgaste/reposición; no observa compras de máquinas de reposición.')
        f('2C.3','Producto por unidad de capital',metrics=[('gdp_capital','PIB/capital neto')],unit='Cociente',note='PIB y capital PWT a precios nacionales constantes, misma edición.')
        f('2C.4','Depreciación del capital',metrics=[('depreciation_assets','CCF/stock a coste corriente'),('depreciation_pwt','Delta publicada PWT')],unit='Porcentaje',status='ADAPTADO',
          note='Alternativas comparables dentro de PWT. No dividir un índice de CCF por un stock monetario ni mezclar monedas.')
        f('2C.5','Crecimiento de capital e inversión',metrics=[('growth_gdp_pwt','PIB'),('growth_capital_pwt','Capital'),('growth_na_q_i','Inversión'),('growth_na_q_gfcf','FBCF'),('growth_ccf_proxy','CCF aproximado')],unit='Variación anual (%)',status='ADAPTADO',note='Capital/PIB PWT; demanda NA y CCF aproximado por activos, sin empalmes ni suma de volúmenes.')
        f('2C.6','Empleo y producto',x='employment_pwt',ys=[('gdp_pwt','PIB')],unit='PIB: millones USD nacionales 2021',note='Empleo en personas; cada país conserva su escala. Relación de niveles tendenciales, no efecto causal del empleo.')
        f('2C.7','Horas y producto',x='hours_total',ys=[('gdp_pwt','PIB')],unit='PIB: millones USD nacionales 2021',note='Horas totales anuales = empleo × horas medias PWT. No horas medias en el eje horizontal.')
        f('2C.8','Productividad por ocupado y por hora',metrics=[('productivity_worker_index','Por ocupado'),('productivity_hour_index','Por hora')],unit='2008 = 100',note='PWT. Índices para comparar evolución de magnitudes con unidades distintas; niveles disponibles en indicadores.')
        f('2C.9','Crecimiento y productividad',metrics=[('growth_gdp_pwt','PIB'),('growth_productivity_worker','Por ocupado'),('growth_productivity_hour','Por hora')],unit='Variación anual (%)',note='Cálculos coherentes de PIB, empleo y horas PWT.')
        f('2C.10','Crecimiento del producto y del trabajo',x='growth_gdp_pwt',ys=[('growth_employment_pwt','Ocupados'),('growth_hours_total','Horas totales')],unit='Crecimiento del trabajo (%)',note='PIB en abcisas; empleo y horas en ordenadas. Aclaración de la errata de ejes del documento docente.')
        f('2C.11','Capital por ocupado y por hora',metrics=[('capital_worker_index','Por ocupado'),('capital_hour_index','Por hora')],unit='2008 = 100',note='PWT. Normalización para comparar evolución sin mezclar USD por persona y por hora.')
        f('2C.12','Intensidad de capital y productividad',x='capital_worker',ys=[('productivity_worker','PIB por ocupado')],unit='USD nacionales 2021 por ocupado',note='Capital por ocupado en abcisas. Relación de niveles, no identificación causal de rendimientos.')
        f('2D.1','Rentas y producto nominal',metrics=[('income_gdp','PIB'),('factor_gdp','PIB coste factores'),('compensation','Remuneración'),('surplus','Excedente'),('tax_net','Tributos netos'),('subsidies','Subvenciones (alcance distinto)')],
          scale=1e9,unit='Miles de millones, moneda nacional',status='PARCIAL',note='China: excedente incluye renta mixta; impuestos netos interpretados; subvenciones históricas parciales. No representa una identidad cerrada ni D2 y D3 separados.')
        f('2D.3','Rentas respecto al coste de factores',metrics=[('compensation_factor_share','Remuneración'),('surplus_factor_share','Excedente')],unit='% PIB coste de factores',status='ADAPTADO',note='China: denominador aproximado, excedente con renta mixta. La discrepancia no se reparte para forzar suma 100.')
        f('3.1','IPC y deflactor del PIB',metrics=[('cpi_index','IPC'),('deflator_index','Deflactor')],unit='2008 = 100',note='IPC nacional; deflactor del cociente nominal/real nacional. Se rebasa el índice, no se iguala la cesta.')
        price=[('growth_cpi','IPC'),('growth_deflator','Deflactor'),('growth_gdp_real_national','PIB real')]
        f('3.2','Inflación y crecimiento real',metrics=price,unit='Variación anual (%)',note='IPC nacional y deflactor tienen cestas diferentes; tasas anuales, sin causalidad atribuida.')
        f('3.3','Crecimiento nominal y precios',metrics=price+[('growth_gdp_nominal','PIB nominal')],unit='Variación anual (%)',note='En porcentajes discretos, crecimiento nominal no es exactamente la suma de crecimiento real e inflación; existe término producto.')
        f('3.4','Remuneración nominal por ocupado',metrics=[('wage_nominal','D1 / ocupados')],unit='Moneda nacional por ocupado y año',status='ADAPTADO',note='D1 nacional / ocupados PWT; incluye autónomos en el denominador. No salario medio de asalariados ni comparación directa CNY/EUR.')
        f('3.5','Remuneración real por ocupado',metrics=[('wage_real_index','Remuneración real')],unit='2008 = 100',status='ADAPTADO',note='D1/ocupados deflactado con el deflactor del PIB, base 2008. No índice del poder de compra de una cesta de consumo.')
        f('3.6','Remuneración real y productividad',metrics=[('growth_wage_real','Remuneración real'),('growth_productivity_worker_national','Productividad nacional'),('growth_gdp_real_national','PIB real nacional')],unit='Variación anual (%)',status='ADAPTADO',note='PIB nacional para deflactor y productividad; empleo PWT como denominador. Promedio por ocupado, no por asalariado.')
        for id,y,label in [('3.7','growth_unemployment_model','Desempleados'),('3.8','growth_employment_model','Ocupados')]:
            f(id,'Remuneración real y '+label.lower(),x='growth_wage_real',ys=[(y,label)],unit='Variación anual del número (%)',status='ADAPTADO',
              note='Salario real docente = remuneración por ocupado. Empleo y paro modelizados OIT/WDI. Asociación descriptiva; no efecto causal.')
        f('4.1','Población y edades',metrics=[('population','Total'),('pop_0_14','0–14'),('pop_15plus','15+'),('pop_65plus','65+')],scale=1e6,unit='Millones de personas',
          note='WDI. El grupo 65+ está incluido en 15+: las cuatro líneas no son categorías disjuntas.')
        f('4.2','Composición por edades',metrics=[('pop_0_14_share','0–14'),('pop_15plus_share','15+'),('pop_65plus_share','65+')],unit='% población',note='65+ se solapa con 15+. Para una partición, usar 0–14, 15–64 y 65+ del panel.')
        labor=[('labor_force','Activos'),('employment_model','Ocupados'),('unemployment_model','Desempleados')]
        f('4.3','Activos, ocupados y desempleados',metrics=labor,scale=1e6,unit='Millones de personas',status='ADAPTADO',note='Base común modelizada OIT/WDI. Ocupados y parados derivados con activos y tasa de paro; no encuesta directa.')
        f('4.4','Tasas del mercado laboral',metrics=[('activity_rate','Actividad 15+ aprox.'),('employment_rate','Ocupación 15+ aprox.'),('unemployment_rate_model','Paro / activos')],unit='Porcentaje',status='ADAPTADO',note='Actividad/ocupación: activos modelizados y población WDI 15+. Tasa de paro referida a activos; distinto denominador.')
        f('4.5','Paro registrado y de encuesta',metrics=[('registered_unemployment','Registrado'),('survey_unemployment','Encuesta nacional')],scale=1e6,unit='Millones de personas',status='ADAPTADO',note='China: registro urbano, momento no precisado, y encuesta nacional vía OIT. España: SEPE media anual y EPA. Coberturas diferentes, sin empalme.')
        for id,variables in [('4.6',['growth_gdp_pwt','growth_labor_force','growth_employment_model']),('4.8',['growth_gdp_pwt','growth_labor_force','growth_employment_model','growth_unemployment_model'])]:
            f(id,'Crecimiento y mercado laboral',metrics=[(m,{'growth_gdp_pwt':'PIB','growth_labor_force':'Activos','growth_employment_model':'Ocupados','growth_unemployment_model':'Desempleados'}[m]) for m in variables],unit='Variación anual (%)',status='ADAPTADO',note='PIB PWT y bloque laboral modelizado OIT/WDI; mismo criterio para los dos países.')
        f('4.10','Evolución del paro y remuneración real',metrics=[('growth_unemployment_model','Desempleados'),('growth_wage_real','Remuneración real')],unit='Variación anual (%)',status='ADAPTADO',note='Se conserva el gráfico de líneas solicitado. La referencia a 3.8 en las instrucciones es ambigua: allí figura empleo, aquí desempleo.')
        f('6.1','Renta por habitante y desigualdad',x='gdp_pc_ppp',ys=[('gini','Gini observado')],unit='Gini, 0–100',status='ADAPTADO',note='PIB por habitante PWT a PPA y solo Gini observado WDI. No se unen huecos ni se estima una curva causal de Kuznets.')
        aliases=[('4.7','2C.10','Reutiliza crecimiento de empleo y horas frente a PIB'),('4.9','3.7','Mismos pares paro/remuneración; docente invierte los ejes'),
                 ('5.demanda','2B.T3','Ciclos: reutilizar figuras 2B.3_growth y tabla 2B.T3'),('5.capital','2C.T2','Reutilizar 2C.5 y 2C.T2'),
                 ('5.trabajo','2C.T3','Reutilizar 2C.9, 2C.10 y 2C.T3'),('5.precios','3.T1','Reutilizar 3.2 y 3.T1'),
                 ('5.salarios','3.T3','Reutilizar 3.6 y 3.T3'),('5.laboral','4.T1','Reutilizar 4.6, 4.8 y 4.T1')]
        for id,target,note in aliases:self.register(id,note,'referencia','',note,status='REUTILIZAR',reference=target)
    def documentation(self):
        registry=pl.DataFrame(self.artifacts,infer_schema_length=None)
        registry.write_csv(OUT/'catalogo_resultados.csv')
        requirement_map={
            '2A.production':['2A.1','2A.3_ratios'],'2A.gdp':['2A.3_pib'],
            '2B.levels':['2B.1'],'2B.shares':['2B.3_shares','2B.T1'],'2B.growth':['2B.3_growth'],
            '2B.stats':['2B.T3'],'2B.2008':['2B.4'],'2C.investment':['2C.1','2C.2'],
            '2C.capital':['2C.3','2C.4','2C.T1'],'2C.capital_cycles':['2C.5','2C.T2'],
            '2C.labor':['2C.6','2C.7','2C.8','2C.9','2C.10','2C.T3'],
            '2C.intensity':['2C.11','2C.12'],'2D.income':['2D.1','2D.3','2D.T1'],'2D.io':['2D.T2'],
            '3.prices':['3.1','3.2','3.3','3.T1','3.T2'],
            '3.wages':['3.4','3.5','3.6','3.T3'],'3.wage_employment':['3.7','3.8','3.T4'],
            '4.demography':['4.1','4.2'],'4.labor':['4.3','4.4'],'4.registered':['4.5'],
            '4.cycles':['4.6','4.7','4.8','4.9','4.10','4.T1'],
            '6.1':['6.T1'],'6.2':['6.T2'],'6.3':['6.T3'],'6.4':['6.T4'],'6.kuznets':['6.1'],'7.1':['7.T1']}
        by={r['id']:r for r in self.artifacts};requirements=json.loads((ROOT/'datos/catalogo/requirements.json').read_text())
        req_rows=[]
        for r in requirements:
            deps=[by[id] for id in requirement_map[r['id']]];states={a['status'] for a in deps}
            status='PARCIAL' if 'PARCIAL' in states else 'ADAPTADO' if 'ADAPTADO' in states or 'PREPARADO_CON_NOTA' in states else 'PREPARADO'
            notes=list(dict.fromkeys(a['note'] for a in deps if a['note']))
            req_rows.append(dict(id=r['id'],title=r['title'],status=status,artifacts=';'.join(requirement_map[r['id']]),
                                 note=' | '.join(notes),remaining=' | '.join(a['missing'] for a in deps if a['missing'])))
        pl.DataFrame(req_rows).write_csv(OUT/'estado_requisitos.csv')
        limits=[
            ('L01','Producción e intermedios','China solo tiene un año IO 2023 y una escala monetaria inferida por cotejo de D1. Precios de productor, no mercado.',
             'Figura estructural y cocientes; sin reconstruir una historia anual.', '2A.1;2A.3_ratios'),
            ('L02','Demanda real','Las escalas y bases monetarias de componentes PWT no se han acreditado para comparar niveles nacionales.',
             'Índices dentro de cada serie, tasas y participaciones nominales internas. No sumar volúmenes.', '2B.1;2B.4;2B.T3'),
            ('L03','Consumo de capital fijo','Falta CCF real oficial chino comparable con AMECO. PWT aporta CCF corriente y precios por activos.',
             'CCF real aproximado ΣDc/Np; sensibilidad previa disponible. Depreciación por CCF/stock a coste corriente.', '2C.1;2C.4;2C.T1;2C.T2'),
            ('L04','Existencias','FMI/IFS real termina en 2019 y no acredita P53; España incluye P52+P53. El flujo puede ser cero o negativo.',
             'Escala con |valor 2008|; cambios anuales del índice. Sin tasas porcentuales ni relleno de 2020–2023.', '2C.1;2C.T2'),
            ('L05','Rentas','China: D2 distribuido coincide en 2023 con neto NBS; excedente incluye renta mixta y termina en 2021.',
             'Coste de factores aproximado; discrepancia explícita, sin atribuir residuo a D3.', '2D.1;2D.3;2D.T1'),
            ('L06','Subvenciones','D3 anual exacta no recuperada; solo categoría fiscal histórica parcial y referencia FMI 2023. Excel reciente FMI bloqueado por HTTP 403.',
             'Serie de subvenciones a precios con categoría parcial. No usarla para cerrar la identidad de rentas.', '2D.1'),
            ('L07','Salario medio docente','D1 corresponde a asalariados y el denominador solicitado incluye a todos los ocupados; se combina fuente nacional con PWT.',
             'Denominar remuneración por ocupado. Deflactor del PIB, no cesta IPC. Tasas e índices comparados.', '3.4;3.5;3.6;3.T3'),
            ('L08','Mercado laboral','Encuestas, modelos OIT y registros tienen distintos universos; registro chino urbano y momento no precisado.',
             'Bloque común modelizado WDI para ambos países; derivaciones explícitas. Encuesta y registro aparte, sin empalme.', '4.3;4.4;4.5;4.T1'),
            ('L09','Muestras estadísticas','Las coberturas por fuente y variable difieren; la pandemia cambia los estadísticos.',
             'Intersección de años de ambos países por par y ventana; n, años, media y desviación muestral visibles. Ventanas 1996–2019 y 1996–2023.', '2B.T3;2C.T2;2C.T3;3.T1;3.T2;3.T3;3.T4;4.T1'),
            ('L10','Input-output España','No se ha incorporado una matriz española a esta entrega. Los totales INE no permiten reconstruir nueve flujos intersectoriales.',
             'Tabla china preparada. Comparativa IO bilateral identificada como parcial.', '2D.T2'),
            ('L11','Referencias históricas docentes','No se han reconstruido las filas históricas de otros países empleadas en clase.',
             'Tablas comparativas China–España con PWT desde 1960; no presentarlas como reproducción literal de Maddison.', '6.T1;6.T2;6.T3;6.T4'),
            ('L12','Interpretación','Correlaciones y relaciones de niveles no identifican causalidad; el residuo de Solow recoge todos los factores omitidos.',
             'Resultados descriptivos, sin atribuir todo el residuo a tecnología ni identificar políticas por correlación.', '6.1;7.T1')]
        pl.DataFrame([dict(id=id,topic=topic,problem=problem,decision=decision,artifacts=arts) for id,topic,problem,decision,arts in limits]).write_csv(OUT/'limitaciones.csv')
        summary=dict(indicators=len(self.catalog),observations=len(self.rows),figures=registry.filter(pl.col('kind')=='grafico').height,
                     tables=registry.filter(pl.col('kind')=='tabla').height,reused=registry.filter(pl.col('kind')=='referencia').height,
                     requirements=len(req_rows),requirements_status=pl.DataFrame(req_rows).group_by('status').len().to_dicts(),
                     comparison_period=[self.config['comparison_start'],self.config['end']],growth_period=[1960,2023],
                     exact_data_complete=False,report_written=False,missing_values_filled=False,source_files_modified=False)
        write_json(OUT/'resumen.json',summary)
        outputs={}
        for folder in [GOLD,OUT/'figuras']:
            for p in sorted(folder.rglob('*')):
                if p.is_file():outputs[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
        write_json(OUT/'lineage.json',dict(inputs=self.inputs,outputs=outputs,config=self.config))
        self.summary=summary
        self.write_guide(req_rows,limits)
    def write_guide(self,requirements,limits):
        g=self.growth
        totals={r['country']:r for r in g.filter((pl.col('start')==1960)&(pl.col('end')==2023)).iter_rows(named=True)}
        c,e=totals['CHN'],totals['ESP']
        lines=['# Base preparada para redactar el informe China–España','',
               'Esta entrega transforma los datos auditados en resultados que pueden utilizarse directamente al escribir. '+
               f"Incluye {self.summary['figures']} figuras, {self.summary['tables']} tablas y una ficha para cada uno de los {len(requirements)} bloques de requisitos. "+
               'Las figuras que usan aproximaciones o adaptan el ejercicio lo indican en su pie. No es todavía el informe redactado.','',
               '## Empezar por estos archivos','',
               '- [Índice visual de resultados](index.html): gráficos, tablas y notas de uso.',
               '- [Estado por requisito](estado_requisitos.csv): qué está preparado, adaptado o parcial.',
               '- [Catálogo de figuras y tablas](catalogo_resultados.csv): identificadores y rutas para citar.',
               '- [Limitaciones](limitaciones.csv): problema encontrado, decisión e implicación para el informe.',
               '- [Indicadores](../../datos/gold/informe/indicadores.parquet) y [diccionario](../../datos/gold/informe/diccionario.csv): país, año, variable, unidad, fuente y fórmula.',
               '- [Notebook de revisión](../../notebooks/06_datos_informe.ipynb): cobertura, tablas y selección de gráficos.','',
               '## Decisiones de análisis','',
               'La comparación principal usa 1990–2023. Las tablas 6.3–6.4 y 7.1 comparten los subperiodos 1960–1989, 1989–2000, 2000–2008, 2008–2019 y 2019–2023. '+
               'Los promedios de participaciones usan ventanas sin solapamiento salvo la fila de conjunto. Las correlaciones usan 1996–2019 y 1996–2023, con los mismos años para ambos países dentro de cada par de variables. '+
               'Se conservan n y la lista exacta de años; el tamaño de muestra puede diferir entre variables.','',
               'PWT 11 es la base común de PIB, capital, empleo, horas y crecimiento. La demanda usa PWT NA. Precios y rentas nacionales se conservan en su propia base. '+
               'Para los salarios docentes se divide D1 nacional por empleo PWT y se deflacta con el PIB nacional. No se denomina salario de asalariados a este promedio por ocupado. '+
               'El bloque laboral comparable usa datos modelizados OIT/WDI para ambos países, con ocupados y parados derivados; encuestas y registros nacionales se muestran aparte.','',
               'Los niveles en monedas nacionales se presentan en paneles separados. Solo el PIB por habitante a PPA se usa para comparar niveles internacionales de renta. '+
               'En productividad se prefieren índices para mostrar evolución. Cada gráfico exporta sus datos a `datos/gold/informe/figuras_datos/`.','',
               '## Resultados descriptivos de partida','',
               f"- Entre 1960 y 2023 el PIB real PWT registra un crecimiento anual compuesto del {c['gdp_cagr_pct']:.2f}% en China y del {e['gdp_cagr_pct']:.2f}% en España.",
               f"- Por habitante, las tasas compuestas son {c['gdp_pc_cagr_pct']:.2f}% y {e['gdp_pc_cagr_pct']:.2f}%, respectivamente.",
               f"- En la descomposición logarítmica, China presenta {c['capital_contribution_pp']:.2f} puntos de capital, {c['labor_contribution_pp']:.2f} de empleo y {c['solow_residual_pp']:.2f} de residuo; "+
               f"España, {e['capital_contribution_pp']:.2f}, {e['labor_contribution_pp']:.2f} y {e['solow_residual_pp']:.2f}. Estas contribuciones suman crecimiento logarítmico, no CAGR.",
               '- El comentario económico debe contrastar estos resultados con demanda, productividad y subperiodos. Las cifras no identifican por sí solas causas ni efectos de políticas.','',
               '## A qué nos hemos enfrentado','']
        for id,topic,problem,decision,arts in limits:lines.extend([f'**{topic}.** {problem} {decision}',''])
        lines.extend(['## Estado de cada bloque','', '| Bloque | Estado | Resultados |','|---|---|---|'])
        lines.extend(f"| {r['id']} · {r['title']} | {r['status']} | {r['artifacts']} |" for r in requirements)
        lines.extend(['','## Lo que falta para entregar el informe','',
                      '1. Incorporar la matriz IO española si se quiere una comparación bilateral; la tabla de China sí está preparada.',
                      '2. Decidir si se añaden literalmente las referencias históricas de otros países de las tablas docentes 6.1–6.4.',
                      '3. Redactar la interpretación por temas, seleccionar los gráficos imprescindibles y trasladarlos al apéndice con sus notas.',
                      '4. Actualizar el borrador Typst, que todavía usa la base antigua de octubre. No tratarlo como reflejo de esta entrega.',
                      '5. Revisar bibliografía temática, conclusiones y exposición oral. Las limitaciones estadísticas anteriores acompañan los resultados; no impiden escribir el resto.','',
                      '## Reproducción','', '```sh','uv run --offline python src/prepare_report.py',
                      'uv run --offline --group analysis python src/create_report_notebook.py',
                      'uv run --offline --group analysis python src/verify_report_data.py','```','',
                      'La ejecución lee silver y los originales archivados. Escribe únicamente la nueva capa `datos/gold/informe/` y sus resultados. España, China y v0 se conservan.'])
        (OUT/'GUIA_PARA_REDACTAR.md').write_text('\n'.join(lines)+'\n')
        cards=[]
        import os
        for r in self.artifacts:
            if r['kind']=='referencia':continue
            path=html.escape(os.path.relpath(ROOT/r['path'],OUT));id=html.escape(r['id']);title=html.escape(r['title'])
            preview=f'<img loading="lazy" src="{path.replace(".svg",".png")}" alt="{title}">' if r['kind']=='grafico' else ''
            cards.append(f'<article data-search="{id} {title} {html.escape(r["status"])}"><h2>{id} · {title}</h2><p class="status">{html.escape(r["status"])}</p>'+preview+
                         f'<p>{html.escape(r["note"])}</p><a href="{path}">Abrir {html.escape(r["kind"])}</a></article>')
        page='''<!doctype html><html lang="es"><meta charset="utf-8"><title>Resultados China–España</title>
<style>body{font:16px system-ui;max-width:1200px;margin:35px auto;padding:0 20px;color:#17212c;background:#f5f7fa}input{padding:12px;width:90%;margin:12px 0}article{background:white;padding:22px;margin:20px 0;border-radius:8px}h2{font-size:20px}img{width:100%;height:auto}.status{color:#345e87;font-weight:600}a{color:#17508b}</style>
<h1>Datos y resultados para el informe China–España</h1><p>Comparación 1990–2023; crecimiento desde 1960. Las notas distinguen adaptaciones y resultados parciales.</p>
<p><a href="GUIA_PARA_REDACTAR.md">Guía para redactar</a> · <a href="estado_requisitos.csv">Requisitos</a> · <a href="limitaciones.csv">Limitaciones</a></p>
<label>Buscar por tema, identificador o estado <input id="search" placeholder="Por ejemplo: salarios, 2C, PARCIAL"></label>'''+''.join(cards)+'''
<script>document.querySelector('#search').oninput=e=>{let q=e.target.value.toLocaleLowerCase();document.querySelectorAll('article').forEach(a=>a.hidden=!a.dataset.search.toLocaleLowerCase().includes(q))}</script></html>'''
        (OUT/'index.html').write_text(page)

def main():
    r=ReportData();r.sources();data=r.export();r.tables();r.figures();r.documentation()
    # All registered inputs remain unchanged through the entire preparation.
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in r.inputs.items())
    print(json.dumps(r.summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
