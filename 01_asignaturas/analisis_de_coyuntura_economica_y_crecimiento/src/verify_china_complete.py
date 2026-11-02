"""Meaningful source, formula, missingness, preservation and notebook checks."""
import hashlib
import json
import math
from pathlib import Path
import nbformat
import polars as pl
from openpyxl import load_workbook
from pipeline import write_json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/revision_china/complecion'

def main():
    protected=json.loads((OUT/'preservacion_inicio.json').read_text())
    changed=[p for p,h in protected.items() if not (ROOT/p).is_file() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    assert not changed,changed
    manifests=json.loads((OUT/'provenance.json').read_text())
    for m in manifests:assert hashlib.sha256((ROOT/m['artifact']).read_bytes()).hexdigest()==m['sha256']
    by_id={m['id']:m for m in manifests}
    old=pl.read_parquet(ROOT/'datos/silver/china.parquet')
    new=pl.read_parquet(ROOT/'datos/silver/china_suplemento.parquet')
    all_data=pl.read_parquet(ROOT/'datos/silver/china_completada.parquet')
    assert all_data.filter(pl.col('series_id').is_in(old['series_id'].unique().implode())).equals(old.sort('series_id','year'))
    assert not all_data.select(pl.struct('series_id','year').is_duplicated().any()).item()
    assert new['value'].is_finite().all()
    series={sid:dict(zip(d['year'],d['value'])) for (sid,),d in new.group_by('series_id')}
    def close(a,b):assert math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-7),(a,b)
    m=by_id['china_complete_oecd_table1_20261102']
    raw=pl.read_csv(ROOT/m['artifact'],infer_schema_length=None)
    raw=raw.filter((pl.col('PRICE_BASE')=='V')&(pl.col('UNIT_MEASURE')=='XDC')&
                   (pl.col('TABLE_IDENTIFIER')=='T0103')&pl.col('TRANSACTION').is_in(['D1','D2','B1GQ','B2A3G']))
    assert raw.height==sum(len(series['OECD.INCOME.'+x]) for x in ['D1','D2','B1GQ','B2A3G'])
    for r in raw.iter_rows(named=True):
        close(series['OECD.INCOME.'+r['TRANSACTION']][r['TIME_PERIOD']],r['OBS_VALUE'])
        assert r['UNIT_MULT']==6 and r['CURRENCY']=='CNY'
    # Different GDP vintages/components must NOT be forced to match.
    for y,g in series['ALT.gdp_factor_cost'].items():
        close(g,series['OECD.INCOME.B1GQ'][y]-series['OECD.INCOME.D2'][y])
        close(series['ALT.gross_surplus_residual'][y],g-series['OECD.INCOME.D1'][y])
    assert abs(series['OECD.INCOME.D1'][2023]-687230.1*100)<5
    assert abs(series['OECD.INCOME.D2'][2023]-103970.7*100)<5
    assert 2023 not in series['OECD.INCOME.B2A3G']
    # Recompute CCF from original Excel cells (not intermediate CSV).
    m=by_id['pwt110_capital'];b=load_workbook(ROOT/m['artifact'],read_only=True,data_only=True)
    s=b['Data'];s.reset_dimensions();it=s.iter_rows(values_only=True);header=next(it);calc={}
    for row in it:
        r=dict(zip(header,row))
        if r['countrycode']!='CHN':continue
        assets=['Struc','Mach','TraEq','Other']
        if any(r.get(k+'_'+a) is None for k in ['Dc','Np','Ip'] for a in assets):continue
        calc[int(r['year'])]={p:sum(r['Dc_'+a]/r[p+'_'+a] for a in assets) for p in ['Np','Ip']}
    b.close()
    assert set(calc)==set(series['ALT.CCF_REAL_INDEX_NP'])==set(range(1952,2024))
    for y,v in calc.items():
        close(series['ALT.CCF_REAL_INDEX_NP'][y],v['Np']/calc[2021]['Np']*100)
        close(series['ALT.CCF_REAL_INDEX_IP'][y],v['Ip']/calc[2021]['Ip']*100)
    cap=pl.read_csv(OUT/'ccf_calculo_y_sensibilidad.csv')
    assert (cap['investment_scale_ratio'].drop_nulls()-1).abs().max()<1e-6
    m=by_id['china_inventory_search_fred_table_extract_20261102']
    fred=json.loads((ROOT/m['artifact']).read_text())['observations'];base=next(r['value'] for r in fred if r['date'].startswith('2008'))
    assert len(series['ALT.INVENTORIES_REAL_INDEX'])==len(fred)==40
    for r in fred:close(series['ALT.INVENTORIES_REAL_INDEX'][int(r['date'][:4])],100*r['value']/base)
    assert set(series['ALT.NBS.PRICE_SUBSIDIES'])=={1978,1980,1985,*range(1990,2007)}
    close(series['ALT.NBS.PRICE_SUBSIDIES'][2006],1387.52*100)
    assert series['ALT.IMF.CASH_SUBSIDIES']=={2023:2.0}
    # Coefficients denominator is gross output; column sums are below one.
    tech=pl.read_csv(OUT/'io_2023_coeficientes_tecnicos.csv')
    totals=pl.read_csv(OUT/'io_produccion_transcrita.csv').group_by('sector').agg(pl.col('gross_output_native').sum())
    gross=dict(zip(totals['sector'],totals['gross_output_native']))
    assert tech.height==9
    for r in tech.iter_rows(named=True):close(r['technical_coefficient'],r['value']/gross[r['using_sector']])
    assert tech.group_by('using_sector').agg(pl.col('technical_coefficient').sum())['technical_coefficient'].max()<1
    assert abs(sum(tech['value'])-2080497.0)<=1.051
    wide=pl.read_parquet(ROOT/'datos/silver/china_completada_anual.parquet')
    expected=all_data.filter(pl.col('analytic')).select('year','series_id','value').sort('series_id','year')
    actual=wide.unpivot(index='year',variable_name='series_id').drop_nulls('value').sort('series_id','year')
    assert actual.equals(expected)
    selection=pl.read_csv(OUT/'seleccion_conceptos.csv',infer_schema_length=None)
    panel=pl.read_parquet(ROOT/'datos/silver/china_seleccion.parquet')
    assert selection.height==38 and panel['concept'].n_unique()==37
    for r in panel.iter_rows(named=True):
        d=all_data.filter((pl.col('series_id')==r['series_id'])&(pl.col('year')==r['year']))
        assert d.height==1;close(r['value'],d['value'][0]);assert r['unit']==d['unit'][0]
    n=nbformat.read(ROOT/'notebooks/05_china_alternativas.ipynb',as_version=4);nbformat.validate(n)
    cells=[c for c in n.cells if c.cell_type=='code']
    assert cells and all(c.execution_count is not None for c in cells)
    assert not any(o.output_type=='error' for c in cells for o in c.outputs)
    result=dict(status='OK_WITH_DOCUMENTED_ALTERNATIVES',protected_files=len(protected),source_hashes=len(manifests),
                OECD_source_cells=raw.height,CCF_asset_derived_observations=len(calc)*2,FRED_index_observations=len(fred),
                io_coefficients=tech.height,subsidies_partial_years=20,notebook_code_cells=len(cells),
                exact_D3_recovered=False,own_gap_filling=False,spain_and_originals_unchanged=True)
    write_json(OUT/'verification.json',result);print(result)

if __name__=='__main__':main()
