"""Selección explícita de series oficiales y resultados descriptivos adicionales."""
import json, math
from pathlib import Path
import polars as pl

def build(df, root):
    gold=root/'datos/gold';records=[];mapping=[]
    # selection es filtro exacto sobre las dimensiones conservadas de JSON-stat.
    specs={
      'gdp_nominal':('estat_nama_10_gdp',{'unit':'CP_MEUR','na_item':'B1GQ'},'million_EUR_current'),
      'gdp_real':('estat_nama_10_gdp',{'unit':'CLV20_MEUR','na_item':'B1GQ'},'million_EUR_chain_2020'),
      'gdp_deflator':('estat_nama_10_gdp',{'unit':'PD20_EUR','na_item':'B1GQ'},'index_2020_100'),
      'c_real':('estat_nama_10_gdp',{'unit':'CLV20_MEUR','na_item':'P31_S14_S15'},'million_EUR_chain_2020'),
      'g_real':('estat_nama_10_gdp',{'unit':'CLV20_MEUR','na_item':'P3_S13'},'million_EUR_chain_2020'),
      'i_real':('estat_nama_10_gdp',{'unit':'CLV20_MEUR','na_item':'P5G'},'million_EUR_chain_2020'),
      'gfcf_real':('estat_nama_10_gdp',{'unit':'CLV20_MEUR','na_item':'P51G'},'million_EUR_chain_2020'),
      'inventories_valuables_real':('estat_nama_10_gdp',{'unit':'CLV20_MEUR','na_item':'P52_P53'},'million_EUR_chain_2020'),
      'x_real':('estat_nama_10_gdp',{'unit':'CLV20_MEUR','na_item':'P6'},'million_EUR_chain_2020'),
      'm_real':('estat_nama_10_gdp',{'unit':'CLV20_MEUR','na_item':'P7'},'million_EUR_chain_2020'),
      'compensation':('estat_nama_10_gdp',{'unit':'CP_MEUR','na_item':'D1'},'million_EUR_current'),
      'operating_surplus_mixed':('estat_nama_10_gdp',{'unit':'CP_MEUR','na_item':'B2A3G'},'million_EUR_current'),
      'taxes':('estat_nama_10_gdp',{'unit':'CP_MEUR','na_item':'D2'},'million_EUR_current'),
      'subsidies':('estat_nama_10_gdp',{'unit':'CP_MEUR','na_item':'D3'},'million_EUR_current'),
      'employment_domestic':('estat_nama_10_pe',{'unit':'THS_PER','na_item':'EMP_DC'},'thousand_persons'),
      'employees_domestic':('estat_nama_10_pe',{'unit':'THS_PER','na_item':'SAL_DC'},'thousand_persons'),
      'capital_net_real':('estat_nama_10_nfa_st',{'unit':'CLV20_MEUR','asset10':'N11N','nace_r2':'TOTAL'},'million_EUR_chain_2020'),
      'hours_domestic':('estat_nama_10_a10_e',{'unit':'THS_HW','na_item':'EMP_DC','nace_r2':'TOTAL'},'thousand_hours'),
    }
    for series,(source,selection,unit) in specs.items():
        n=0
        for r in df.filter(pl.col('source')==source).iter_rows(named=True):
            dims=json.loads(r['dimensions'])
            if all(dims.get(k)==v for k,v in selection.items()):
                records.append(dict(country='ESP',year=r['year'],series=series,value=r['value'],unit=unit,source=source,flag=r['flag'],bronze_sha256=r['bronze_sha256']));n+=1
        mapping.append(dict(series=series,source=source,selection=selection,observations=n,status='selected' if n else 'missing'))
    for r in df.filter(pl.col('source')=='ine_integrated_accounts').iter_rows(named=True):
        records.append({k:r[k] for k in ['country','year','series','value','unit','source','flag','bronze_sha256']})
    pl.DataFrame(records,infer_schema_length=None).write_csv(gold/'spain_official.csv')
    (gold/'official_mapping.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n')
    # WDI modelized labor identities. No se presenta como dato nacional de encuesta.
    macro=[]
    w=df.filter(pl.col('source')=='wdi_common')
    for country in ['CHN','ESP']:
        vals={s:{r['year']:r['value'] for r in w.filter((pl.col('country')==country)&(pl.col('series')==s)).iter_rows(named=True)} for s in w['series'].unique()}
        for year in range(1960,2026):
            def v(s):return vals.get(s,{}).get(year)
            cpi=v('FP.CPI.TOTL');yp=v('NY.GDP.MKTP.CN');yr=v('NY.GDP.MKTP.KN')
            pop=v('SP.POP.TOTL');young=v('SP.POP.0014.TO');old=v('SP.POP.65UP.TO');active=v('SL.TLF.TOTL.IN');u=v('SL.UEM.TOTL.ZS')
            # Datos por edades: WDI puede publicar 0–14 como % en otra serie, aquí solo código absoluto.
            working=pop-young if pop is not None and young is not None else None
            unemployed=active*u/100 if active is not None and u is not None else None
            employed=active-unemployed if active is not None and unemployed is not None else None
            def pct(a,b):return 100*a/b if a is not None and b else None
            prev=vals.get('FP.CPI.TOTL',{}).get(year-1)
            row=dict(country=country,year=year,cpi=cpi,cpi_inflation_pct=100*(cpi/prev-1) if cpi and prev else None,
                gdp_deflator_implicit=100*yp/yr if yp and yr else None,population=pop,pop_0_14=young,pop_65plus=old,pop_15plus=working,
                labor_force=active,unemployment_rate_modeled=u,unemployment_modeled_derived=unemployed,employment_modeled_derived=employed,
                participation_15plus_pct=pct(active,working),employment_15plus_pct=pct(employed,working),gini=v('SI.POV.GINI'))
            macro.append(row)
    macro=pl.DataFrame(macro,infer_schema_length=None)
    macro.write_csv(gold/'prices_labor_demography.csv')
    # Cruzar Gini solo por años observados con la base PPA de la misma edición WDI.
    pairs=[]
    for country in ['CHN','ESP']:
        for r in macro.filter((pl.col('country')==country)&pl.col('gini').is_not_null()).iter_rows(named=True):
            g=w.filter((pl.col('country')==country)&(pl.col('series')=='NY.GDP.PCAP.PP.KD')&(pl.col('year')==r['year']))
            if g.height:pairs.append(dict(country=country,year=r['year'],gdp_pc_ppp=g['value'][0],gini=r['gini']))
    pl.DataFrame(pairs).write_csv(gold/'kuznets_observed.csv')
    # Figuras adicionales con datos y unidades explícitas.
    import matplotlib.pyplot as plt
    dest=root/'output/figuras'
    for col,name,ylabel in [('cpi_inflation_pct','inflation','Inflación IPC (%)'),('unemployment_rate_modeled','unemployment','Desempleo (% activos, estimación OIT)'),('participation_15plus_pct','participation','Actividad (% población 15+)')]:
        fig,ax=plt.subplots(figsize=(7.2,4))
        for country,label in [('CHN','China'),('ESP','España')]:
            p=macro.filter((pl.col('country')==country)&pl.col('year').is_between(1990,2023)).select('year',col).drop_nulls()
            ax.plot(p['year'],p[col],label=label)
        ax.set(xlabel='Año',ylabel=ylabel);ax.legend();ax.grid(alpha=.2);fig.tight_layout()
        fig.savefig(dest/(name+'.svg'));fig.savefig(dest/(name+'.png'),dpi=130);plt.close(fig)
    fig,ax=plt.subplots(figsize=(7.2,4))
    for country,label in [('CHN','China'),('ESP','España')]:
        p=[r for r in pairs if r['country']==country];ax.scatter([r['gdp_pc_ppp'] for r in p],[r['gini'] for r in p],label=label,s=20)
    ax.set(xlabel='PIB por habitante, PPA constante de 2021 (WDI)',ylabel='Índice de Gini (0–100)');ax.legend();ax.grid(alpha=.2);fig.tight_layout()
    fig.savefig(dest/'kuznets.svg');fig.savefig(dest/'kuznets.png',dpi=130);plt.close(fig)
    return mapping
