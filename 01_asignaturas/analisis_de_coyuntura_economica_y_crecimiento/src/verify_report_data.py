"""Validate source values, units, samples and accounting in the report-ready layer."""
import hashlib
import json
import math
from pathlib import Path
import statistics
import nbformat
import polars as pl
from openpyxl import load_workbook
from pipeline import write_json

ROOT=Path(__file__).resolve().parents[1]
GOLD=ROOT/'datos/gold/informe'
OUT=ROOT/'output/preparacion_informe'

def main():
    lineage=json.loads((OUT/'lineage.json').read_text())
    for group in ['inputs','outputs']:
        for path,sha in lineage[group].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
    d=pl.read_parquet(GOLD/'indicadores.parquet')
    assert d['value'].is_finite().all() and d['year'].max()==2023
    assert not d.select(pl.struct('country','metric','year').is_duplicated().any()).item()
    data={(c,m):dict(zip(z['year'],z['value'])) for (c,m),z in d.group_by('country','metric')}
    def value(c,m,y):return data[c,m][y]
    def close(a,b):assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-7),(a,b)
    # Independent cell comparison against archived PWT workbook and national silver.
    m=json.loads((ROOT/'datos/bronze/pwt110/latest.json').read_text())
    b=load_workbook(ROOT/m['artifact'],read_only=True,data_only=True);s=b['Data'];s.reset_dimensions()
    it=s.iter_rows(values_only=True);header=next(it);source_checks=0
    for rr in it:
        r=dict(zip(header,rr));c=r.get('countrycode')
        if c not in ['CHN','ESP']:continue
        y=int(r['year'])
        if y>2023:continue
        for src,target,scale in [('rgdpna','gdp_pwt',1),('rnna','capital_pwt',1),('emp','employment_pwt',1e6),('avh','hours_average',1),('pop','population_pwt',1e6)]:
            if r[src] is None:
                assert y not in data[c,target]
                continue
            close(value(c,target,y),r[src]*scale);source_checks+=1
    b.close()
    ch=pl.read_parquet(ROOT/'datos/silver/china_completada.parquet')
    sp=pl.read_parquet(ROOT/'datos/silver/espana.parquet')
    for y in [1992,2008,2023]:
        close(value('CHN','compensation',y),ch.filter((pl.col('series_id')=='OECD.INCOME.D1')&(pl.col('year')==y))['value'][0]*1e6)
        close(value('ESP','compensation',y),sp.filter((pl.col('series_id')=='ESP.1.0.0.0.UWCD')&(pl.col('year')==y))['value'][0]*1e9)
    for c in ['CHN','ESP']:
        for y in [1996,2008,2019,2023]:
            close(value(c,'wage_nominal',y),value(c,'compensation',y)/value(c,'employment_pwt',y))
            close(value(c,'wage_real',y),value(c,'wage_nominal',y)*value(c,'deflator',2008)/value(c,'deflator',y))
            close(value(c,'hours_total',y),value(c,'employment_pwt',y)*value(c,'hours_average',y))
            close(value(c,'productivity_hour',y),value(c,'gdp_pwt',y)*1e6/value(c,'hours_total',y))
            close(value(c,'labor_force',y),value(c,'employment_model',y)+value(c,'unemployment_model',y))
            close(value(c,'population',y),value(c,'pop_0_14',y)+value(c,'pop_15_64',y)+value(c,'pop_65plus',y))
        for (country,metric),vs in data.items():
            if country!=c or not metric.startswith('growth_'):continue
            original=data[c,metric.removeprefix('growth_')]
            for y,v in vs.items():
                assert y-1 in original and original[y]>0 and original[y-1]>0
                close(v,100*(original[y]/original[y-1]-1))
        for y,v in data[c,'change_inventories'].items():close(v,value(c,'inventories_index',y)-value(c,'inventories_index',y-1))
    assert 'growth_inventories' not in set(d['metric'])
    assert max(data['CHN','inventories'])==2019
    # Recompute every paired-sample statistic with Python statistics, separately from Polars.
    statistic_checks=0
    for path in sorted((GOLD/'tablas').glob('*_muestras.csv')):
        samples=pl.read_csv(path);table=pl.read_csv(path.with_name(path.name.replace('_muestras','')),infer_schema_length=None)
        for r in table.iter_rows(named=True):
            z=samples.filter((pl.col('country')==r['country'])&(pl.col('metric')==r['metric'])&
                             (pl.col('window_start')==r['window_start'])&(pl.col('window_end')==r['window_end'])).sort('year')
            ys=z['year'].to_list();assert len(ys)==r['n']
            other=samples.filter((pl.col('country')!=r['country'])&(pl.col('metric')==r['metric'])&
                                 (pl.col('window_start')==r['window_start'])&(pl.col('window_end')==r['window_end'])).sort('year')
            assert ys==other['year'].to_list()
            expected=set(range(r['window_start'],r['window_end']+1))
            for c in ['CHN','ESP']:expected&=set(data[c,r['metric']])&set(data[c,r['reference_metric']])
            assert ys==sorted(expected)
            a=z['reference_value'].to_list();b=z['value'].to_list()
            for y,x,v in zip(ys,a,b):close(x,value(r['country'],r['reference_metric'],y));close(v,value(r['country'],r['metric'],y))
            if b:close(r['mean'],statistics.mean(b))
            if len(b)>=2:close(r['sample_sd'],statistics.stdev(b))
            if r['correlation'] is not None:close(r['correlation'],statistics.correlation(a,b))
            if r['relative_sd'] is not None:close(r['relative_sd'],statistics.stdev(b)/statistics.stdev(a))
            if r['metric']=='change_inventories':assert r['relative_sd'] is None
            statistic_checks+=1
    growth=pl.read_csv(GOLD/'tablas/7.T1.csv')
    for r in growth.iter_rows(named=True):
        c=r['country'];a=r['start'];b=r['end'];years=b-a
        gy=math.log(value(c,'gdp_pwt',b)/value(c,'gdp_pwt',a))*100/years
        close(gy,r['gdp_log_pp']);close(gy,r['capital_contribution_pp']+r['labor_contribution_pp']+r['solow_residual_pp'])
        close(r['gdp_cagr_pct'],100*((value(c,'gdp_pwt',b)/value(c,'gdp_pwt',a))**(1/years)-1))
    subperiods={(1960,1989),(1989,2000),(2000,2008),(2008,2019),(2019,2023)}
    for id in ['6.T3','6.T4']:
        g=pl.read_csv(GOLD/'tablas'/(id+'.csv'))
        for c in ['CHN','ESP']:assert set(g.filter(pl.col('country')==c).select('start','end').iter_rows())==subperiods
    for c in ['CHN','ESP']:
        g=growth.filter(pl.col('country')==c)
        rows=[r for r in g.iter_rows(named=True) if (r['start'],r['end']) in subperiods]
        assert sum(r['years'] for r in rows)==63
        total=g.filter((pl.col('start')==1960)&(pl.col('end')==2023)).row(0,named=True)
        close(sum(r['years']*r['gdp_log_pp'] for r in rows)/63,total['gdp_log_pp'])
    registry=pl.read_csv(OUT/'catalogo_resultados.csv',infer_schema_length=None)
    requirements=pl.read_csv(OUT/'estado_requisitos.csv',infer_schema_length=None)
    assert set(requirements['id'])=={r['id'] for r in json.loads((ROOT/'datos/catalogo/requirements.json').read_text())}
    ids=set(registry['id']);assert registry.height==len(ids)
    figure_points=0
    for r in registry.iter_rows(named=True):
        if r['kind']=='referencia':assert r['reference'] in ids;continue
        assert (ROOT/r['path']).is_file()
        if r['kind']!='grafico':continue
        z=pl.read_csv(ROOT/r['data_path'],infer_schema_length=None)
        assert z.height>0
        for p in z.iter_rows(named=True):
            if 'metric' in p:
                close(p['original_value'],value(p['country'],p['metric'],p['year']))
                close(p['value'],p['original_value']/p['scale_divisor'])
                if p['scale_divisor']==1e6:assert p['unit']=='million_'+p['original_unit']
                elif p['scale_divisor']==1e9:assert p['unit']=='billion_'+p['original_unit']
                else:assert p['unit']==p['original_unit']
            else:
                close(p['x_value'],value(p['country'],p['x_metric'],p['year']))
                close(p['y_value'],value(p['country'],p['y_metric'],p['year']))
            assert p['year']<=2023;figure_points+=1
    assert requirements.filter(pl.col('id')=='2D.io')['status'][0]=='PARCIAL'
    assert requirements.filter(pl.col('id')=='2D.income')['status'][0]=='PARCIAL'
    notebook=nbformat.read(ROOT/'notebooks/06_datos_informe.ipynb',as_version=4);nbformat.validate(notebook)
    cells=[c for c in notebook.cells if c.cell_type=='code']
    assert cells and all(c.execution_count is not None for c in cells)
    assert not any(o.output_type=='error' for c in cells for o in c.outputs)
    summary=json.loads((OUT/'resumen.json').read_text())
    assert summary['observations']==d.height and summary['indicators']==len(data)
    result=dict(status='OK_WITH_EXPLICIT_ADAPTATIONS',input_hashes=len(lineage['inputs']),output_hashes=len(lineage['outputs']),
                source_PWT_cells=source_checks,paired_statistic_rows=statistic_checks,figure_points_checked=figure_points,
                growth_accounting_rows=growth.height,requirements=requirements.height,
                figures=summary['figures'],tables=summary['tables'],notebook_code_cells=len(cells),
                artificial_gap_filling=False,inventory_percentage_growth=False)
    write_json(OUT/'verification.json',result);print(result)

if __name__=='__main__':main()
