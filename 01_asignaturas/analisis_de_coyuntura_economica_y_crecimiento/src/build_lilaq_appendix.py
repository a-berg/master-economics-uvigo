"""Export the verified figure points for native Lilaq plots; never embeds Matplotlib images."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import polars as pl
from prepare_report import ReportData

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/apendice_lilaq'
COLORS=['24598A','C67430','31745B','86649C','B74B50','328798']

class FigureSpecs:
    def __init__(self):self.items=[]
    def figure(self,id,title,**kw):self.items.append(dict(id=id,title=title,**kw))
    def register(self,*args,**kwargs):pass

def ticks(lo,hi,year=False):
    if year:
        step=1 if hi-lo<5 else 5 if hi-lo<26 else 10
    else:
        rough=(hi-lo)/5
        power=10**math.floor(math.log10(rough))
        step=next(s*power for s in [1,2,2.5,5,10] if s*power>=rough)
    start=math.ceil(lo/step)*step
    result=[]
    for i in range(12):
        v=round(start+i*step,10)
        if v>hi+1e-9:break
        decimals=next((d for d in range(7) if math.isclose(step*10**d,round(step*10**d),abs_tol=1e-9)),6)
        label=str(int(v)) if year else f'{v:,.{decimals}f}'.replace(',',' ').replace('.',',')
        result.append([v,label])
    return result

def bounds(values,include_zero=False,year=False):
    lo=min(values);hi=max(values)
    if include_zero:lo=min(lo,0);hi=max(hi,0)
    if lo==hi:
        pad=1 if year else max(abs(lo)*.12,1)
    else:pad=(hi-lo)*(.025 if year else .08)
    return [lo-pad,hi+pad]

def runs(points):
    groups=[]
    for y,x,v in sorted(points):
        if not groups or y!=groups[-1][-1][0]+1:groups.append([])
        groups[-1].append((y,x,v))
    return [dict(years=[p[0] for p in g],x=[p[1] for p in g],y=[p[2] for p in g]) for g in groups]

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    registry=pl.read_csv(ROOT/'output/preparacion_informe/catalogo_resultados.csv',infer_schema_length=None)
    dictionary=pl.read_csv(ROOT/'datos/gold/informe/diccionario.csv',infer_schema_length=None)
    specs=FigureSpecs();ReportData.figures(specs)
    metric_meta={(r['country'],r['metric']):r for r in dictionary.iter_rows(named=True)}
    hashes={};figures=[];points=0
    def providers(c,m,seen=None):
        seen=set() if seen is None else seen
        if m in seen:return set()
        seen.add(m);row=metric_meta[c,m];parents=row['input_metrics'] or ''
        if parents:return set.union(*(providers(c,k,seen.copy()) for k in parents.split(';')))
        s=row['source']
        if s.startswith('pwt110'):return {'PWT 11'}
        if s.startswith('WDI.'):return {'Banco Mundial (WDI)'}
        if s.startswith('OECD.') or s in ['ALT.gdp_factor_cost','ALT.tax_net_oecd']:return {'OCDE'}
        if 'NBS' in s:return {'NBS'}
        if 'INVENTORIES' in s:return {'FMI/IFS vía FRED'}
        if s.startswith('ESP.'):return {'AMECO'}
        if s.startswith('INE.'):return {'INE'}
        if s.startswith('ILO.'):return {'OIT'}
        if s.startswith('SEPE.'):return {'SEPE'}
        raise ValueError(('Unmapped source',s))
    for spec in specs.items:
        id=spec['id'];entry=registry.filter(pl.col('id')==id).row(0,named=True)
        path=ROOT/entry['data_path'];hashes[entry['data_path']]=hashlib.sha256(path.read_bytes()).hexdigest()
        data=pl.read_csv(path,infer_schema_length=None)
        scatter='x' in spec
        labels=spec['ys'] if scatter else spec['metrics']
        # Fixed series colors across the two countries and all panels of this figure.
        color={m:COLORS[i%len(COLORS)] for i,(m,label) in enumerate(labels)}
        legend=[dict(label=label,color=color[m]) for m,label in labels]
        panels=[];sources=set();coverage=[]
        for c,name in [('CHN','China'),('ESP','España')]:
            z=data.filter(pl.col('country')==c);years=z['year'].unique().sort().to_list()
            spans={}
            for metric,label in labels:
                sub=z.filter(pl.col('y_metric' if scatter else 'metric')==metric)
                if not sub.height:continue
                ys=sub['year'].unique().sort().to_list()
                span=str(ys[0]) if ys[0]==ys[-1] else str(ys[0])+'-'+str(ys[-1])
                if scatter:span+=' (n='+str(len(ys))+')'
                spans.setdefault(span,[]).append(label)
            if len(spans)==1:coverage.append(name+': '+next(iter(spans)))
            else:coverage.append(name+': '+', '.join('/'.join(ls)+' '+span for span,ls in spans.items()))
            subsets=[('Índices de inversión y CCF',[v for v in labels if v[0]!='inventories_index']),('Existencias (flujo)',[v for v in labels if v[0]=='inventories_index'])] if id=='2C.1' else [('',labels)]
            for sublabel,selected in subsets:
                series=[];xx=[];yy=[];xlabel='Año';ylabel=spec.get('unit','')
                for m,label in selected:
                    points_data=z.filter(pl.col('y_metric' if scatter else 'metric')==m).sort('year')
                    if not points_data.height:continue
                    sources|=providers(c,m)
                    if scatter:sources|=providers(c,spec['x'])
                    xfactor=1;yfactor=1
                    if scatter:
                        xlabel={'employment_pwt':'Ocupados (millones)','hours_total':'Horas totales (miles de millones)',
                                'growth_gdp_pwt':'Crecimiento del PIB (%)','capital_worker':'Capital por ocupado (miles de USD de 2021)',
                                'growth_wage_real':'Crecimiento de remuneración real (%)','gdp_pc_ppp':'PIB por habitante (miles de USD PPA de 2021)'}[spec['x']]
                        xfactor={'employment_pwt':1e6,'hours_total':1e9,'capital_worker':1e3,'gdp_pc_ppp':1e3}.get(spec['x'],1)
                        if m=='gdp_pwt':yfactor=1e3;ylabel='PIB real (miles de millones de USD de 2021)'
                        if m=='productivity_worker':yfactor=1e3;ylabel='PIB por ocupado (miles de USD de 2021)'
                        pts=[(r['year'],r['x_value']/xfactor,r['y_value']/yfactor) for r in points_data.iter_rows(named=True)]
                    else:
                        if spec.get('scale')==1e9:ylabel='Miles de millones de '+('CNY' if c=='CHN' else 'EUR')
                        if id=='3.4':yfactor=1000;ylabel='Miles de '+('CNY' if c=='CHN' else 'EUR')+' por ocupado y año'
                        if id=='2C.1':ylabel='Escala |valor 2008| = 100' if m=='inventories_index' else '2008 = 100'
                        pts=[(r['year'],r['year'],r['value']/yfactor) for r in points_data.iter_rows(named=True)]
                    points+=len(pts);xx.extend(p[1] for p in pts);yy.extend(p[2] for p in pts)
                    series.append(dict(metric=m,label=label,color=color[m],xfactor=xfactor,yfactor=yfactor,
                                       runs=[dict(years=[p[0] for p in pts],x=[p[1] for p in pts],y=[p[2] for p in pts])] if scatter else runs(pts)))
                assert xx and yy,(id,c)
                zero=(not scatter and ('growth_' in selected[0][0] or 'inventories' in selected[0][0]))
                xlim=bounds(xx,year=not scatter);ylim=bounds(yy,include_zero=zero)
                xticks=[[xx[0],str(int(xx[0]))]] if not scatter and len(set(xx))==1 else ticks(*xlim,year=not scatter)
                panels.append(dict(country=c,title=name if not sublabel else name+' · '+sublabel,kind='scatter' if scatter else 'line',
                                   xlabel=xlabel,ylabel=ylabel,xlim=xlim,ylim=ylim,xticks=xticks,yticks=ticks(*ylim),
                                   series=series,show_zero=zero))
        # In the four-panel investment page, countries form columns and concepts form rows.
        if id=='2C.1':panels=[panels[i] for i in [0,2,1,3]]
        figures.append(dict(id=id,title=spec['title'],status=entry['status'],note=entry['note'],
                            source='Elaboración propia con '+', '.join(sorted(sources))+'.',coverage='; '.join(coverage)+'.',
                            legend=legend,panels=panels))
    payload=dict(figures=figures,count=len(figures),point_count=points,renderer='Lilaq 0.6.0; native vector plots',
                 instructions='Gráficas únicamente. Sin tablas ni texto principal; notas relevantes bajo cada figura.')
    path=OUT/'graficas.json';path.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    hashes['datos/gold/informe/diccionario.csv']=hashlib.sha256((ROOT/'datos/gold/informe/diccionario.csv').read_bytes()).hexdigest()
    hashes['output/preparacion_informe/catalogo_resultados.csv']=hashlib.sha256((ROOT/'output/preparacion_informe/catalogo_resultados.csv').read_bytes()).hexdigest()
    (OUT/'manifest.json').write_text(json.dumps(dict(input_sha256=hashes,json_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                                   figures=len(figures),points=points,renderer=payload['renderer']),ensure_ascii=False,indent=2)+'\n')
    print(dict(figures=len(figures),points=points,output=str(path.relative_to(ROOT))))

if __name__=='__main__':main()
