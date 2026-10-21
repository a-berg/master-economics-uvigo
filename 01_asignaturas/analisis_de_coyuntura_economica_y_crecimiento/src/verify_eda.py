"""Controles de la versión congelada y de los productos exploratorios."""
import hashlib,json,tempfile
from pathlib import Path
import polars as pl
from snapshot import ROOT,create,verify
from eda import change
VERSION='v0_2026-10-16'
m=verify(VERSION)
try:create(VERSION)
except FileExistsError:pass
else:raise AssertionError('Se permitió sobrescribir la versión')
assert change(pl.DataFrame({'year':[2000,2002],'value':[100.,130.]}),'growth')==[]
assert change(pl.DataFrame({'year':[2000,2001],'value':[0.,130.]}),'growth')==[]
try:change(pl.DataFrame({'year':[2000],'value':[100.]}),'index',2008)
except ValueError:pass
else:raise AssertionError('Se sustituyó una base ausente')
with tempfile.TemporaryDirectory() as temp:
    root=Path(temp)
    silver=root/'datos/silver';silver.mkdir(parents=True)
    (silver/'test.csv').write_text('year,value\n2000,100\n')
    create('test',root)
    copied=root/'datos/snapshots/test/frozen/datos/silver/test.csv'
    copied.write_text('year,value\n2000,999\n')
    try:verify('test',root)
    except ValueError:pass
    else:raise AssertionError('La alteración no fue detectada')
nb=json.loads((ROOT/'notebooks/01_eda.ipynb').read_text())
code=[c for c in nb['cells'] if c['cell_type']=='code']
assert all(c['execution_count'] is not None for c in code)
assert all(o['output_type']!='error' for c in code for o in c['outputs'])
assert nb['metadata']['execution_mode']=='in_process_ipython_no_jupyter_kernel'
out=ROOT/'output/eda'/VERSION
text=(out/'exploracion.html').read_text()
from html.parser import HTMLParser
class ScriptSources(HTMLParser):
    def __init__(self):super().__init__();self.external=[]
    def handle_starttag(self,tag,attrs):
        if tag=='script':self.external.extend(v for k,v in attrs if k=='src')
parser=ScriptSources();parser.feed(text)
assert not parser.external, parser.external
cross=pl.read_csv(out/'gdp_source_differences.csv')
assert cross['difference_pp'].is_finite().all()
assert set(cross['country'])=={'CHN','ESP'}
print(f'OK: snapshot verificado; sobrescritura y alteración rechazadas; huecos y base ausente controlados; {len(code)} celdas sin errores; HTML sin CDN; diferencias entre fuentes finitas.')
