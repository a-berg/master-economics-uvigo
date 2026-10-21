"""Exploración descriptiva sobre un snapshot fijo. No descarga ni modifica los datos de entrada."""
from __future__ import annotations
import argparse,html,json,math,statistics
from pathlib import Path
import polars as pl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from snapshot import ROOT,verify

LABELS={'CHN':'China','ESP':'España'}

def load(version='v0_2026-10-16',root=ROOT):
    verify(version,root)
    base=root/'datos/snapshots'/version/'frozen'
    return pl.read_parquet(base/'datos/silver/observations.parquet'),base

def select(df,country,source,series):
    return df.filter((pl.col('country')==country)&(pl.col('source')==source)&(pl.col('series')==series)).select('year','value').sort('year')

def coverage(df):
    rows=[]
    for group,d in df.group_by(['country','source','series','unit'],maintain_order=True):
        years=sorted(d['year'].to_list());observed=set(years)
        gaps=sorted(set(range(years[0],years[-1]+1))-observed)
        rows.append(dict(zip(['country','source','series','unit'],group))|dict(first=years[0],last=years[-1],n=len(years),internal_missing=len(gaps),missing_years=','.join(map(str,gaps)),zeros=d.filter(pl.col('value')==0).height,negative=d.filter(pl.col('value')<0).height,nonempty_flags=d.filter(pl.col('flag').is_not_null()&(pl.col('flag')!='')).height))
    return pl.DataFrame(rows,infer_schema_length=None).sort(['country','source','series'])

def change(d,mode,base_year=2008):
    rows=list(d.iter_rows(named=True));out=[]
    if mode=='index':
        base=next((r['value'] for r in rows if r['year']==base_year),None)
        if base is None or base==0:raise ValueError(f'No hay base válida en {base_year}; no se sustituye por otro año.')
        return [(r['year'],100*r['value']/base) for r in rows]
    if mode=='growth':
        # No unir dos años no consecutivos ni calcular crecimiento ordinario sobre valores no positivos.
        for prev,row in zip(rows,rows[1:]):
            if row['year']==prev['year']+1 and prev['value']>0 and row['value']>0:
                out.append((row['year'],100*(row['value']/prev['value']-1)))
        return out
    return [(r['year'],r['value']) for r in rows]

def explorer(df,source='pwt110_na',series='q_gdp',mode='index',start=1990,end=2023,base_year=2008):
    # Los niveles se separan por país: no superponer yuanes y euros sobre un único eje.
    fig=make_subplots(rows=1,cols=2,subplot_titles=['China','España']) if mode=='level' else go.Figure()
    colors={'CHN':'#276b9c','ESP':'#c46834'}
    for i,country in enumerate(LABELS,1):
        data=select(df,country,source,series)
        if not data.height:continue
        pairs=change(data,mode,base_year)
        # Insertar None en huecos: evitar unir años sin observación.
        lookup={y:v for y,v in pairs};years=list(range(start,end+1));values=[lookup.get(y) for y in years]
        trace=go.Scatter(x=years,y=values,name=LABELS[country],mode='lines+markers',marker_size=3,line_color=colors[country],connectgaps=False,
            hovertemplate='%{x}: %{y:.4g}<extra>'+LABELS[country]+'</extra>')
        if mode=='level':fig.add_trace(trace,row=1,col=i)
        else:fig.add_trace(trace)
    ylabel={'index':f'Índice {base_year}=100','growth':'Variación anual (%)','level':'Unidad original; consultar metadatos de la serie'}[mode]
    fig.update_layout(title=f'{source} · {series} · {mode}',template='plotly_white',height=440,yaxis_title=ylabel,
       legend=dict(orientation='h'),margin=dict(l=60,r=30,t=75,b=60))
    fig.update_xaxes(title='Año',rangeslider_visible=True)
    return fig

def rates(df,country,source,series):
    return dict(change(select(df,country,source,series),'growth'))

def cross_sources(df):
    rows=[]
    for country in LABELS:
        ref=rates(df,country,'wdi_common','NY.GDP.MKTP.KN')
        for source,series in [('pwt110','rgdpna'),('pwt110_na','q_gdp')]+([('estat_nama_10_gdp','A|CLV20_MEUR|B1GQ|ES')] if country=='ESP' else []):
            other=rates(df,country,source,series)
            for year in sorted(set(ref)&set(other)):
                if 1990<=year<=2023:rows.append(dict(country=country,year=year,source=source,series=series,wdi_growth=ref[year],other_growth=other[year],difference_pp=other[year]-ref[year]))
    return pl.DataFrame(rows)

def shocks(df):
    rows=[]
    # Umbral de cribado explícito. Un salto puede ser real (p. ej., una crisis); no se elimina.
    for source,series in [('pwt110','rgdpna'),('pwt110','emp'),('pwt110','avh'),('pwt110_na','q_i'),('wdi_common','NY.GDP.MKTP.KN')]:
        for country in LABELS:
            pairs=change(select(df,country,source,series),'growth')
            if not pairs:continue
            vals=[v for y,v in pairs];median=statistics.median(vals);mad=statistics.median(abs(v-median) for v in vals)
            for year,v in pairs:
                score=abs(v-median)/(1.4826*mad) if mad else None
                if 1990<=year<=2023 and (abs(v)>15 or (score is not None and score>6)):
                    rows.append(dict(country=country,source=source,series=series,year=year,growth_pct=v,robust_score=score,meaning='review_only_not_error'))
    return pl.DataFrame(rows,infer_schema_length=None)

def demand_residuals(base):
    p=pl.read_csv(base/'datos/gold/comparison.csv')
    return p.select('country','year',*[pl.col(x) for x in ['share_c','share_i','share_g','share_x','share_m']]).with_columns(
       (100*(1-pl.col('share_c')-pl.col('share_i')-pl.col('share_g')-pl.col('share_x')+pl.col('share_m'))).alias('nominal_residual_pct_gdp'))

def build(version='v0_2026-10-16',root=ROOT):
    df,base=load(version,root);out=root/'output/eda'/version;out.mkdir(parents=True,exist_ok=True)
    cov=coverage(df);cov.write_csv(out/'coverage_gaps_flags.csv')
    cross=cross_sources(df);cross.write_csv(out/'gdp_source_differences.csv')
    stats=cross.group_by(['country','source']).agg(pl.len().alias('n'),pl.col('difference_pp').abs().mean().alias('mean_abs_difference_pp'),pl.col('difference_pp').abs().max().alias('max_abs_difference_pp'))
    stats.sort(['country','source']).write_csv(out/'gdp_source_summary.csv')
    events=shocks(df);events.write_csv(out/'review_events.csv')
    residuals=demand_residuals(base);residuals.write_csv(out/'nominal_demand_residuals.csv')
    flags=df.filter(pl.col('flag').is_not_null()&(pl.col('flag')!='')).group_by(['source','flag']).len().sort(['source','flag'])
    flags.write_csv(out/'flags_summary.csv')
    # Autocontenido: Plotly se incluye una vez; no usa CDN ni peticiones de datos.
    fragments=[]
    for i,(source,series,mode) in enumerate([('pwt110_na','q_gdp','index'),('pwt110_na','q_gdp','growth'),('pwt110','emp','index'),('pwt110','avh','level'),('pwt110_na','q_i','index'),('wdi_common','NY.GDP.MKTP.KN','index')]):
        fig=explorer(df,source,series,mode)
        fragments.append(fig.to_html(full_html=False,include_plotlyjs=True if i==0 else False))
    fig=go.Figure()
    for group,d in cross.group_by(['country','source'],maintain_order=True):
        d=d.sort('year');fig.add_trace(go.Scatter(x=d['year'].to_list(),y=d['difference_pp'].to_list(),mode='lines',name=' / '.join(group)))
    fig.update_layout(title='Diferencia de crecimiento frente a WDI (puntos porcentuales)',template='plotly_white',height=450,yaxis_title='p.p.')
    fig.update_xaxes(rangeslider_visible=True)
    fragments.append(fig.to_html(full_html=False,include_plotlyjs=False))
    covsmall=cov.filter((pl.col('source').is_in(['pwt110','pwt110_na','wdi_common']))&(pl.col('series').is_in(['rgdpna','rnna','emp','avh','q_gdp','q_c','q_i','q_g','q_x','q_m','SI.POV.GINI'])))
    def table(frame):
        return '<table><thead><tr>'+''.join('<th>'+html.escape(x)+'</th>' for x in frame.columns)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in r)+'</tr>' for r in frame.iter_rows())+'</tbody></table>'
    doc='''<!doctype html><html lang="es"><meta charset="utf-8"><title>Exploración inicial China y España</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:0 20px;color:#222}table{border-collapse:collapse;font-size:12px;display:block;overflow:auto}td,th{padding:6px 8px;border:1px solid #ddd}h2{margin-top:40px}</style><h1>Exploración inicial de China y España</h1>'''
    doc+=f'<p>Versión fija: <b>{html.escape(version)}</b>. Datos cargados de una instantánea verificada. Los gráficos permiten zoom, consulta de valores y selección de series mediante la leyenda.</p>'
    doc+='<p>La procedencia nacional subyacente de algunas series de China está pendiente de documentar. Coincidencia entre distribuidores no demuestra independencia ni ausencia de sesgos. Los indicadores de revisión no se interpretan como pruebas de manipulación.</p>'
    doc+='<h2>Cobertura y huecos</h2>'+table(covsmall)+'<h2>Series exploratorias</h2>'+''.join(fragments)+'<h2>Diferencias entre fuentes</h2>'+table(stats)+'<h2>Observaciones para revisar</h2>'+table(events)+'</html>'
    (out/'exploracion.html').write_text(doc)
    notes=['# Exploración preliminar de la versión '+version,'',
      '## Alcance','',
      f'- {df.height:,} observaciones almacenadas; se conservan variantes, países, conceptos y unidades por separado.',
      '- Los gráficos principales emplean índices y tasas. Los niveles originales se separan por país.',
      '- No se han descargado datos directos del NBS. Su utilización queda como último recurso.',
      '- Esta exploración no demuestra ni refuta inflación estadística. Tampoco acredita independencia entre WDI y PWT.','',
      '## Diferencias de crecimiento del PIB frente a WDI','']
    for r in stats.sort(['country','source']).iter_rows(named=True):
        notes.append(f"- {r['country']} / {r['source']}: {r['n']} años; diferencia absoluta media {r['mean_abs_difference_pp']:.4f} p.p.; máxima {r['max_abs_difference_pp']:.4f} p.p.")
    notes+=['','## Revisión prioritaria','',f'- {events.height} eventos marcados con reglas de cribado explícitas. Revisar crisis, cambios de definición y revisiones; no corregir automáticamente.',
       '- Las diferencias entre fuentes pueden reflejar distintas ediciones y métodos; no constituyen errores por sí mismas.',
       '- Los residuos de la identidad nominal se calculan en puntos de PIB; no se impone aditividad a los volúmenes encadenados.',
       '- Las variables con huecos no se interpolan. Los flags de Eurostat se conservan y se consultan en su respuesta original.',
       '- Antes de cerrar el informe faltan: cadena de procedencia CHN, validación de universos laborales, existencias/CCF reales, rentas y tablas input-output.','',
       '## Archivos','',
       '- coverage_gaps_flags.csv: cobertura efectiva, huecos internos, ceros, negativos y flags por serie.',
       '- gdp_source_differences.csv y gdp_source_summary.csv: comparación de tasas sin igualar niveles de moneda.',
       '- review_events.csv: revisión de saltos; no identifica automáticamente errores.',
       '- nominal_demand_residuals.csv: identidad de demanda corriente.',
       '- exploracion.html: gráficos interactivos autocontenidos.']
    (out/'HALLAZGOS.md').write_text('\n'.join(notes)+'\n')
    return dict(version=version,observations=df.height,series=cov.height,events=events.height,output=str(out))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--version',default='v0_2026-10-16');a=p.parse_args();print(build(a.version))
