"""Crea el explorador de la integración actual; los controles se comparten con CLI."""
from pathlib import Path
import nbformat as n
R=Path(__file__).resolve().parents[1]
md=n.v4.new_markdown_cell;code=n.v4.new_code_cell
nb=n.v4.new_notebook(cells=[md('''# España: integración y cobertura

123 series integradas; cada una conserva su periodo, unidad y procedencia. Consulta `../output/revision_espana/INTEGRACION_FINAL.md` para límites y reproducción. Este notebook complementa el contraste AMECO del notebook 02; no certifica equivalencia numérica con MOISEES.'''),code('''from pathlib import Path
import sys
import polars as pl
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
R=Path.cwd().parent if Path.cwd().name=='notebooks' else Path.cwd()
sys.path.insert(0,str(R/'src'))
from verify_spain_recovered import verify
verify()
a=pl.read_parquet(R/'datos/silver/espana.parquet')
c=pl.read_parquet(R/'datos/silver/espana_catalogo.parquet')
r=pl.read_parquet(R/'datos/silver/espana_fuentes_recuperadas.parquet')
display(c.select('series_id','name','unit','first','last','n','status'))'''),md('## Cobertura de las 26 series nuevas'),code('''coverage=r.group_by('series_id').agg(pl.col('year').min().alias('first'),pl.col('year').max().alias('last'),pl.len().alias('n')).sort('series_id')
display(coverage)
fig,ax=plt.subplots(figsize=(11,9))
for i,row in enumerate(coverage.iter_rows(named=True)):
    ax.plot([row['first'],row['last']],[i,i],linewidth=4)
ax.set_yticks(range(coverage.height),coverage['series_id'].to_list(),fontsize=8)
ax.set_xlabel('Año; el rango no implica igualdad de universo entre series')
ax.grid(axis='x',alpha=.3)
fig.tight_layout()
display(fig)
plt.close(fig)'''),md('''## Explorar una serie

Se muestran también los indicadores de dato parcial, la transformación y la fuente por año. Para explorar interactivamente, ejecuta las celdas con un kernel local.'''),code('''def inspect(series):
    d=a.filter(pl.col('series_id')==series).sort('year')
    display(d.select('year','value','unit','source','apta_analisis','source_flag','transformation'))
    fig,ax=plt.subplots(figsize=(10,3))
    ax.plot(d['year'],d['value'],marker='.',linewidth=1)
    ax.set_title(d['name'][0]);ax.set_ylabel(d['unit'][0]);ax.grid(alpha=.3)
    display(fig);plt.close(fig)
selector=widgets.Dropdown(options=sorted(r['series_id'].unique().to_list()),description='Serie:',layout=widgets.Layout(width='95%'))
widgets.interact(inspect,series=selector)
inspect('SEPE.REGISTERED.UNEMPLOYED.ANNUAL_MEAN')'''),md('## Periodos incompletos y anomalías de los originales'),code('''display(pl.read_csv(R/'output/revision_espana/periodos_completos_anualizacion.csv').filter(~pl.col('included')))
display(pl.read_csv(R/'output/revision_espana/source_anomalies.csv'))
display(r.filter(pl.col('source_flag').is_not_null()).select('series_id','year','value','source_flag','apta_analisis'))''')])
nb.metadata['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}
n.write(nb,R/'notebooks/03_integracion_espana.ipynb')
if __name__=='__main__':
 from execute_notebook import execute
 execute(R/'notebooks/03_integracion_espana.ipynb')
