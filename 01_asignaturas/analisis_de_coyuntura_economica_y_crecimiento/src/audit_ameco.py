"""Contraste numérico España/USA: diez hojas base del Excel y AMECO Spring 2026."""
from __future__ import annotations
import json,math,statistics,re
from collections import defaultdict
from pathlib import Path
import polars as pl
from catalogue import read_excel
from diagnose_core import BASE
from snapshot import ROOT,verify

def audit():
    m=verify('v0_2026-10-16')
    excel=next(ROOT/x['path'] for x in m['bronze_files'] if x['path'].endswith('.xls'))
    inv,occ,_=read_excel(excel)
    obs=pl.read_parquet(ROOT/'datos/silver/ampliacion_20261019/ameco_reference_codes.parquet')
    records=[];details=[];dups=[]
    groups=defaultdict(list)
    for r in occ:
        if r['sheet'] in BASE:groups[r['code']].append(r)
    priority={s:i for i,s in enumerate(['REAL','NOMINAL','POP','K','mercado traballo','Indices Prezos','i-e'])}
    for code,items in sorted(groups.items()):
        item=min(items,key=lambda x:(priority.get(x['sheet'],100),-x['n']))
        d=obs.filter(pl.col('code')==code).sort('year')
        orig={int(y):float(v) for y,v in item['years'].items()}
        new={r['year']:r['value'] for r in d.iter_rows(named=True)}
        overlap=sorted(set(orig)&set(new));pairs=[]
        for year in overlap:
            old=orig[year];value=new[year];diff=value-old
            pct=100*diff/abs(old) if old else None
            same=math.isclose(old,value,rel_tol=1e-10,abs_tol=1e-8)
            pairs.append(dict(code=code,year=year,excel=old,ameco=value,difference=diff,difference_pct=pct,ratio=value/old if old else None,equal_with_rounding=same))
        details.extend(pairs)
        ratios=[p['ratio'] for p in pairs if p['ratio'] is not None]
        equal=sum(p['equal_with_rounding'] for p in pairs)
        grow=[]
        for year in overlap:
            if year-1 in orig and year-1 in new and min(orig[year],orig[year-1],new[year],new[year-1])>0:
                grow.append(abs(100*((new[year]/new[year-1])-(orig[year]/orig[year-1]))))
        original_units=item['unit'].strip();new_units=str(d['unit'][0]).strip() if d.height else ''
        old_base=re.findall(r'(?:at|reference levels|=)\s*(20\d{2}|19\d{2})|((?:20|19)\d{2})\s*(?:prices|reference|=)',item['title']+' '+original_units)
        new_base=re.findall(r'(?:at|reference levels|=)\s*(20\d{2}|19\d{2})|((?:20|19)\d{2})\s*(?:prices|reference|=)',str(d['title'][0])+' '+new_units) if d.height else []
        old_b={v for pair in old_base for v in pair if v};new_b={v for pair in new_base for v in pair if v}
        if not overlap:status='PENDIENTE_CODIGO_NO_RECUPERADO'
        elif old_b and new_b and old_b!=new_b:status='PENDIENTE_BASE_PRECIOS_O_INDICE'
        elif original_units!=new_units:status='PENDIENTE_UNIDADES'
        elif equal==len(overlap):status='ACEPTADA_COINCIDENCIA_NUMERICA'
        elif ratios and not 0.8<=statistics.median(ratios)<=1.2:status='PENDIENTE_DISCREPANCIAS_NUMERICAS'
        else:status='COMPATIBLE_CODIGO_DIFERENCIAS_PENDIENTES'
        records.append(dict(code=code,country=code[:3],sheet=item['sheet'],row=item['row'],original_title=item['title'],new_title=d['title'][0] if d.height else '',
            original_units=original_units,new_units=new_units,n_original=len(orig),n_downloaded=len(new),n_overlap=len(overlap),equal_values=equal,
            first_overlap=min(overlap) if overlap else None,last_overlap=max(overlap) if overlap else None,
            missing_original_years=','.join(map(str,sorted(set(orig)-set(new)))),max_abs_diff=max((abs(p['difference']) for p in pairs),default=None),
            median_ratio=statistics.median(ratios) if ratios else None,max_abs_relative_diff_pct=max((abs(p['difference_pct']) for p in pairs if p['difference_pct'] is not None),default=None),
            mean_abs_growth_difference_pp=statistics.mean(grow) if grow else None,status=status,
            decision_basis='Identificador, título y unidad; contraste numérico por año. Diferencias no se atribuyen automáticamente a revisión. No demuestra exactitud externa ni estado observado/estimado.',
            source_edition='AMECO Spring 2026, publicación 2026-06-03'))
        for other in items:
            if other is item:continue
            common=set(item['years'])&set(other['years'])
            ne=sum(not math.isclose(item['years'][y],other['years'][y],rel_tol=1e-10,abs_tol=1e-8) for y in common)
            if ne:dups.append(dict(code=code,primary=f"{item['sheet']}:{item['row']}",other=f"{other['sheet']}:{other['row']}",n_common=len(common),n_different=ne,primary_unit=item['unit'],other_unit=other['unit']))
    dest=ROOT/'output/revision_equivalencias';dest.mkdir(parents=True,exist_ok=True)
    pl.DataFrame(records,infer_schema_length=None).write_csv(dest/'ameco_decisiones.csv')
    pl.DataFrame(details,infer_schema_length=None).write_parquet(dest/'ameco_comparacion_anual.parquet')
    pl.DataFrame(details,infer_schema_length=None).write_csv(dest/'ameco_comparacion_anual.csv')
    (dest/'excel_repeticiones_discrepantes.json').write_text(json.dumps(dups,ensure_ascii=False,indent=2)+'\n')
    print(pl.DataFrame(records).group_by('status').len())
    print('Ejemplos principales:')
    print(pl.DataFrame(records).filter(pl.col('code').str.contains(r'\.(OITT|OCPH|OVGD|OKND|NETN|UWCD|OIST)$')).select('code','n_overlap','equal_values','median_ratio','mean_abs_growth_difference_pp','status'))
    return records
if __name__=='__main__':audit()
