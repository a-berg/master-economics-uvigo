"""Check exported Lilaq points and the compiled appendix without altering source data."""
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import polars as pl

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/apendice_lilaq'
PDF=ROOT/'output/pdf/apendice_graficas_revision.pdf'

def main():
    manifest=json.loads((OUT/'manifest.json').read_text())
    for p,h in manifest['input_sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
    assert hashlib.sha256((OUT/'graficas.json').read_bytes()).hexdigest()==manifest['json_sha256']
    data=json.loads((OUT/'graficas.json').read_text())
    registry=pl.read_csv(ROOT/'output/preparacion_informe/catalogo_resultados.csv',infer_schema_length=None).filter(pl.col('kind')=='grafico')
    assert set(registry['id'])=={f['id'] for f in data['figures']}
    points=0
    for f in data['figures']:
        original=pl.read_csv(ROOT/registry.filter(pl.col('id')==f['id'])['data_path'][0],infer_schema_length=None)
        checked=set()
        for p in f['panels']:
            for value,label in p['xticks']+p['yticks']:
                assert math.isclose(value,float(label.replace(' ','').replace(',','.')),rel_tol=1e-8,abs_tol=1e-8)
            for s in p['series']:
                for run in s['runs']:
                    if p['kind']=='line':assert all(b==a+1 for a,b in zip(run['years'],run['years'][1:]))
                    assert len(run['x'])==len(run['y'])==len(run['years'])
                    for y,x,v in zip(run['years'],run['x'],run['y']):
                        scatter=p['kind']=='scatter'
                        key=(p['country'],s['metric'],y);assert key not in checked;checked.add(key)
                        r=original.filter((pl.col('country')==p['country'])&(pl.col('year')==y)&
                                          (pl.col('y_metric' if scatter else 'metric')==s['metric'])).row(0,named=True)
                        expected_x=r['x_value']/s['xfactor'] if scatter else y
                        expected_y=r['y_value']/s['yfactor'] if scatter else r['value']/s['yfactor']
                        assert math.isclose(x,expected_x,rel_tol=1e-12,abs_tol=1e-10)
                        assert math.isclose(v,expected_y,rel_tol=1e-12,abs_tol=1e-10)
                        assert p['xlim'][0]<=x<=p['xlim'][1] and p['ylim'][0]<=v<=p['ylim'][1]
                        points+=1
        assert len(checked)==original.height,(f['id'],len(checked),original.height)
    pages=[s for s in subprocess.check_output(['pdftotext','-layout',str(PDF),'-'],text=True).split('\f') if s.strip()]
    assert len(pages)==len(data['figures'])==38
    for text,f in zip(pages,data['figures']):
        ids=re.findall(r'GRÁFICO\s+([0-9A-Za-z._]+)',text)
        assert ids==[f['id']],(ids,f['id'])
        assert all(label in text for label in ['Fuente:','Cobertura:','Nota:'])
    images=subprocess.check_output(['pdfimages','-list',str(PDF)],text=True).strip().splitlines()
    assert len(images)==2,'Expected native vector graphics without embedded raster images'
    source=(ROOT/'entregas/apendice_graficas_lilaq.typ').read_text()
    assert 'lq.plot(' in source and 'image(' not in source
    assert points==data['point_count']==6479
    result=dict(status='OK',figures=len(data['figures']),pages=len(pages),points_verified=points,
                input_hashes=len(manifest['input_sha256']),renderer='Lilaq 0.6.0',embedded_raster_images=0,
                source_points_changed=False,pdf_sha256=hashlib.sha256(PDF.read_bytes()).hexdigest())
    (OUT/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(result)

if __name__=='__main__':main()
