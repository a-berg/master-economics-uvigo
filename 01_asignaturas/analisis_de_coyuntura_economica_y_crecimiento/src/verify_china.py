"""Verify delivery contracts, analytical exclusions, IO and notebook outputs."""
import hashlib,json,math
from pathlib import Path
import nbformat
import polars as pl
from china_silver import ROOT,OUT,CONCEPTS
from snapshot import verify
from pipeline import write_json

def main():
    verify('v0_2026-10-16')
    q=json.loads((OUT/'quality.json').read_text())
    d=pl.read_parquet(ROOT/'datos/silver/china.parquet')
    c=pl.read_csv(OUT/'contratos.csv',infer_schema_length=None)
    required={i for r in json.loads((ROOT/'datos/catalogo/requirements.json').read_text()) for i in r['inputs']}
    assert required<=set(c['concept'])
    assert c.height==len(CONCEPTS) and c['concept'].n_unique()==c.height
    assert c['required_unit'].null_count()==c['universe'].null_count()==0
    sp=pl.read_csv(ROOT/'output/revision_espana/catalogo_espana.csv',infer_schema_length=None)
    cross=pl.read_csv(OUT/'correspondencias_espana_china.csv',infer_schema_length=None)
    assert set(sp['series_id'])==set(cross['spain_series']) and cross.height==sp.height
    wide=pl.read_parquet(ROOT/'datos/silver/china_anual.parquet')
    analytic=d.filter(pl.col('analytic'))
    assert set(wide.columns)-{'year'}==set(analytic['series_id'])
    assert wide['year'].max()<=2025
    for row in wide.iter_rows(named=True):
        original={r['series_id']:r['value'] for r in analytic.filter(pl.col('year')==row['year']).iter_rows(named=True)}
        assert {k:v for k,v in row.items() if k!='year' and v is not None}==original
    # Check all pure derived outputs, including chained provenance and index baseline.
    by={s:{r['year']:r['value'] for r in d.filter(pl.col('series_id')==s).iter_rows(named=True)} for s in d['series_id'].unique()}
    for r in d.filter(pl.col('source')=='derived').iter_rows(named=True):
        s,y,v=r['series_id'],r['year'],r['value'];get=lambda key:by[key][y]
        if s.startswith('INDEX.NA.'):
            src=s.removeprefix('INDEX.');expected=100*get(src)/by[src][2008]
        else:
            expected={'DER.gdp_deflator':lambda:100*get('WDI.NY.GDP.MKTP.CN')/get('WDI.NY.GDP.MKTP.KN'),
                'DER.pop_15plus':lambda:get('WDI.SP.POP.TOTL')-get('WDI.SP.POP.0014.TO'),
                'DER.hours_total':lambda:get('PWT.emp')*get('PWT.avh'),
                'DER.equivalent_employment':lambda:get('DER.hours_total')*1e6/1760,
                'DER.gdp_per_worker':lambda:get('PWT.rgdpna')/get('PWT.emp'),
                'DER.capital_output':lambda:get('PWT.rnna')/get('PWT.rgdpna'),
                'DER.gdp_pc_ppp':lambda:get('PWT.rgdpe')/get('PWT.pop')}[s]()
        assert math.isclose(v,expected,rel_tol=1e-12,abs_tol=1e-9)
    raw=pl.read_csv(OUT/'io_2023_20_sectors.csv');agg=pl.read_csv(OUT/'io_2023_3_sectors.csv')
    assert raw.height==400 and agg.height==9
    recomputed=raw.group_by('supplying_sector','using_sector').agg(pl.col('value').sum()).sort('supplying_sector','using_sector')
    assert recomputed.equals(agg.select('supplying_sector','using_sector','value').sort('supplying_sector','using_sector'))
    io_checks=pl.read_csv(OUT/'io_transcription_checks.csv');assert io_checks.height==40 and io_checks['difference'].abs().max()<=1.051
    # Preserve imported documents exactly.
    imported=ROOT/'datos/bronze/professor_instructions_20261021/manifest.json'
    for m in json.loads(imported.read_text()):assert hashlib.sha256((ROOT/m['artifact']).read_bytes()).hexdigest()==m['sha256']
    notebook=nbformat.read(ROOT/'notebooks/04_china.ipynb',as_version=4);nbformat.validate(notebook)
    cells=[c for c in notebook.cells if c.cell_type=='code']
    assert len(cells)==7 and all(c.execution_count and c.outputs for c in cells)
    assert not any(o.output_type=='error' for c in cells for o in c.outputs)
    assert len(list((OUT/'figuras').glob('*.png')))==6
    assert q['observations']==d.height and q['series']==d['series_id'].n_unique()
    result=dict(status='OK_WITH_DOCUMENTED_GAPS',snapshot_v0='VERIFIED',contracts=c.height,spanish_catalogue_rows=cross.height,
        observation_count=d.height,analytic_series=analytic['series_id'].n_unique(),io_cells=raw.height,io_sum_checks=io_checks.height,
        notebook_code_cells=len(cells),notebook_figures=6,filled_missing_values=False,silent_source_splices=False)
    write_json(OUT/'verification.json',result);print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
