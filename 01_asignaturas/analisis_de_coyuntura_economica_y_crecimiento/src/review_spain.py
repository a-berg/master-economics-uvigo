"""Diagnósticos y gráficos del notebook 02; lectura sin descargas ni cambios de decisiones."""
from pathlib import Path
import json,math,statistics,io
import polars as pl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from IPython.display import display,Image,Markdown
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/revision_espana'

def load():
 cat=pl.read_csv(OUT/'catalogo_espana.csv')
 pending=cat.filter(pl.col('initial_status').is_in(['COMPATIBLE_CODIGO_DIFERENCIAS_PENDIENTES','PENDIENTE_UNIDADES','PENDIENTE_DISCREPANCIAS_NUMERICAS'])&(pl.col('n')>0)&(pl.col('source')=='ameco_spring2026')).sort('series_id')
 pairs=pl.read_parquet(ROOT/'output/revision_equivalencias/ameco_comparacion_anual.parquet').filter(pl.col('code').is_in(pending['series_id'].implode()))
 return cat,pending,pairs

def annual(code):
 _,_,pairs=load();rows=pairs.filter(pl.col('code')==code).sort('year').to_dicts();prev=None
 for r in rows:
  for source in ['excel','ameco']:
   r['growth_'+source+'_pct']=100*(r[source]/prev[source]-1) if prev and r['year']==prev['year']+1 and prev[source]>0 and r[source]>0 else None
  for source in ['excel','ameco']:
   r['change_'+source]=r[source]-prev[source] if prev and r['year']==prev['year']+1 else None
  r['growth_diff_pp']=r['growth_ameco_pct']-r['growth_excel_pct'] if r['growth_excel_pct'] is not None and r['growth_ameco_pct'] is not None else None
  prev=r
 return pl.DataFrame(rows,infer_schema_length=None)

NOTES={
'URTG':'La razón AMECO/Excel está cerca de 0,0001. Probar factor_excel=1e-4 solo como hipótesis visual. Silver conserva AMECO sin escalar; falta explicar la escala de la referencia.',
'UUTG':'La razón está cerca de 0,0001 y la unidad literal cambia. Revisar también el título y los ajustes UMTS; no aceptar por parecido tras reescalar.',
'AMGT':'La unidad antigua está vacía. La actual dice Share. Comprobar denominador y si se expresa en porcentaje antes de aceptar.',
'AXGT':'La unidad antigua está vacía. La actual dice Share. No confundir con AXGE (excluye comercio intra-UE).',
'UVG4':'El VAB nominal de construcción presenta diferencias de nivel relevantes. Examinar fechas y alcance de revisión; no es un cambio de base de volumen.',
'NETN':'Empleo de contabilidad nacional. La comparación EPA se mantiene separada: no son universos intercambiables.',
'UWCD':'Remuneración de asalariados: revisar los años discrepantes y preservar el agregado D.1.'}
def explain(code):
 cat,_,_=load();r=cat.filter(pl.col('series_id')==code).row(0,named=True)
 audit=pl.read_csv(ROOT/'output/revision_equivalencias/ameco_decisiones.csv').filter(pl.col('code')==code).row(0,named=True)
 display(Markdown(f"### `{code}`\n\n{r['name']}\n\n**Estado:** {r['status']} · **Referencia:** {r['excel_sheet']}, fila {r['excel_row']}\n\n**Unidad Excel:** `{audit['original_units'] or '(vacía)'}` · **Unidad actual:** `{r['unit']}`\n\n{NOTES.get(code.split('.')[-1], 'Comparar fechas, magnitud y patrón de diferencias. La revisión de edición es una hipótesis, no una causa demostrada.')}"))
 display({k:audit[k] for k in ['original_title','new_title','n_overlap','equal_values','median_ratio','max_abs_relative_diff_pct','mean_abs_growth_difference_pp']})

def figure(code,start=1960,end=2025,factor_excel=1.,save=None):
 d=annual(code).filter(pl.col('year').is_between(start,end));r=d.to_dicts()
 fig,ax=plt.subplots(2,2,figsize=(11,6.8));years=[x['year'] for x in r]
 ax[0,0].plot(years,[x['excel']*factor_excel for x in r],label=f'Excel × {factor_excel:g}')
 ax[0,0].plot(years,[x['ameco'] for x in r],label='AMECO vigente',ls='--')
 ax[0,0].set_title('Niveles en unidades de cada fuente');ax[0,0].legend(fontsize=8)
 ax[0,1].plot(years,[x['ratio'] for x in r]);ax[0,1].axhline(1,color='gray',ls=':');ax[0,1].set_title(f'Razón AMECO / Excel · mediana {d["ratio"].median():.6g}')
 ax[1,0].plot(years,[x['difference_pct'] for x in r]);ax[1,0].axhline(0,color='gray',ls=':');ax[1,0].set_title('Diferencia / |Excel| (%) — sin ajuste')
 unit=load()[0].filter(pl.col('series_id')==code)['unit'][0]
 delta=unit in ['Share','Rate','capital output ratio','Marginal efficiency of capital'] or any(x['excel']<=0 or x['ameco']<=0 for x in r)
 field='change_' if delta else 'growth_'
 for source,label in [('excel','Excel'),('ameco','AMECO')]:
  key=field+source+('' if delta else '_pct')
  ax[1,1].plot(years,[x[key] for x in r],label=label,ls='--' if source=='ameco' else '-')
 ax[1,1].set_title('Cambio anual (unidades de la serie)' if delta else 'Variación anual (%) — años consecutivos');ax[1,1].legend(fontsize=8)

 for a in ax.flat:a.grid(alpha=.22);a.set_xlabel('Año');a.ticklabel_format(axis='y',style='plain',useOffset=False)
 fig.suptitle(code+(' · REESCALADO HIPOTÉTICO, NO APLICADO A SILVER' if factor_excel!=1 else ''),fontsize=11);fig.tight_layout()
 if save:fig.savefig(save,dpi=110)
 return fig

def show(code,start=1960,end=2025,factor_excel=1.,detail=True):
 explain(code);fig=figure(code,start,end,factor_excel)
 b=io.BytesIO();fig.savefig(b,format='png',dpi=105);plt.close(fig);display(Image(data=b.getvalue()))
 if detail:
  d=annual(code).filter(pl.col('year').is_between(start,end))
  display(Markdown('**Diez mayores diferencias absolutas de nivel.** En unidades distintas, se revisa primero la unidad.'))
  display(d.with_columns(pl.col('difference').abs().alias('_rank')).sort('_rank',descending=True).drop('_rank').head(10))

def summary():
 _,pending,_=load();data=[]
 for r in pending.iter_rows(named=True):
  d=annual(r['series_id']);rat=d['ratio'].drop_nulls();growth=d['growth_diff_pp'].drop_nulls()
  data.append(dict(series_id=r['series_id'],name=r['name'],status=r['status'],n=d.height,median_ratio=rat.median(),max_absolute_relative_pct=d['difference_pct'].abs().max(),growth_mae_pp=growth.abs().mean() if len(growth) and d['excel'].min()>0 and d['ameco'].min()>0 and r['unit'] not in ['Share','Rate','capital output ratio','Marginal efficiency of capital'] else None,n_changed=d.filter(~pl.col('equal_with_rounding')).height,review_note=NOTES.get(r['series_id'].split('.')[-1],'Revisión visual y de edición pendiente.')))
 return pl.DataFrame(data,infer_schema_length=None)

def explorer():
 import ipywidgets as w
 _,pending,_=load()
 dropdown=w.Dropdown(options=[(r['series_id']+' · '+r['name'][:70],r['series_id']) for r in pending.iter_rows(named=True)],layout=w.Layout(width='95%'))
 years=w.IntRangeSlider(value=[1960,2025],min=1960,max=2025,description='Años',continuous_update=False,layout=w.Layout(width='80%'))
 factor=w.Dropdown(options=[('Sin ajuste',1.),('Hipótesis Excel × 0,0001',1e-4),('Hipótesis Excel × 1.000',1000.)],description='Diagnóstico',layout=w.Layout(width='70%'))
 output=w.Output()
 def draw(*_):
  with output:
   output.clear_output(wait=True);show(dropdown.value,*years.value,factor.value)
 for control in [dropdown,years,factor]:control.observe(draw,names='value')
 display(w.VBox([dropdown,years,factor,output]));draw()
 return dropdown,years,factor

def build():
 s=summary();s.write_csv(OUT/'diagnosticos_31_series.csv');dest=OUT/'figuras';dest.mkdir(exist_ok=True)
 for code in s['series_id']:
  fig=figure(code,save=dest/(code+'.png'));plt.close(fig)
 print('Diagnósticos y figuras:',s.height)
if __name__=='__main__':build()
