"""Revisión reproducible: uv run --with pandas==3.0.6 python src/validate_pwt.py.
Resultados candidatos, separados de las series certificadas de silver.
"""
import json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/revision_equivalencias'; OUT.mkdir(parents=True,exist_ok=True)
provenance={}
def artifact(id):
 m=json.loads((ROOT/f'datos/bronze/{id}/latest.json').read_text()); p=ROOT/m['artifact']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']
 provenance[id]=m
 return p
nafile=artifact('pwt110_na'); mainfile=artifact('pwt110'); laborfile=artifact('pwt110_labor_detail')
na=pd.read_excel(nafile,sheet_name='Data'); main=pd.read_excel(mainfile,sheet_name='Data')
na_legend=pd.read_excel(nafile,sheet_name='Legend')
na_legend.to_csv(OUT/'pwt_na_diccionario_original.csv',index=False)
reader=pd.io.stata.StataReader(laborfile,convert_categoricals=False)
labels=reader.variable_labels();values=reader.value_labels(); labor=reader.read()
(OUT/'pwt_labor_metadatos.json').write_text(json.dumps({'variables':labels,'categorias':{k:{str(a):b for a,b in v.items()} for k,v in values.items()}},indent=2,ensure_ascii=False))
checks=[];candidates=[]
for country in ['CHN','ESP']:
 n=na[na.countrycode.eq(country)].copy(); m=main[main.countrycode.eq(country)].copy(); l=labor[labor.countrycode.eq(country)].copy()
 combined=m.merge(l,on=['countrycode','year'],suffixes=('_main','_detail'))
 for field,scale in [('emp',1e-6),('avh',1.0),('labsh',1.0)]:
  a=combined[f'{field}_main']; b=combined[f'{field}_detail']*scale; mask=a.notna()&b.notna()
  equal=np.isclose(a[mask],b[mask],rtol=1e-6,atol=1e-6)
  checks.append(dict(country=country,test=f'{field}: main vs labor detail',n=int(mask.sum()),n_equal=int(equal.sum()),scale_detail_to_main=scale,max_abs_diff=float((a[mask]-b[mask]).abs().max()),decision='COINCIDENCIA_VECTORIAL' if equal.all() else 'DIFERENCIAS_PENDIENTES'))
 c=n.merge(l[['countrycode','year','comp_sh','i_comp_sh','i_labsh','i_emp']],on=['countrycode','year']).merge(m[['countrycode','year','emp','avh']],on=['countrycode','year'],suffixes=('_na','_main'))
 c['ra_candidate_na_units']=c.comp_sh*c.v_gdp
 c['hours_candidate_million']=c.emp_main*c.avh_main
 c['comp_sh_quality']=c.i_comp_sh.map({0:'constante_asumida_o_interpolada',1:'observada',2:'extrapolada_mixed_income'})
 c['ra_status']='CANDIDATA: cuota de asalariados, pendiente validar escala monetaria y coherencia del PIB'
 c['hours_status']='DERIVACION_ARITMETICA: millones de personas por horas anuales; no valida universo externo'
 c['monetary_unit']='unidad de PWT NA; moneda nacional; escala pendiente de certificación'
 candidates.append(c[['countrycode','year','v_gdp','comp_sh','comp_sh_quality','i_labsh','i_emp','ra_candidate_na_units','ra_status','monetary_unit','emp_main','avh_main','hours_candidate_million','hours_status']])
 checks.append(dict(country=country,test='comp_sh vs labsh (distinción conceptual obligatoria)',n=int(l.comp_sh.notna().sum()),n_equal=int(np.isclose(l.comp_sh,l.labsh,equal_nan=False).sum()),scale_detail_to_main=1.,max_abs_diff=float((l.comp_sh-l.labsh).abs().max()),decision='USAR_COMP_SH_PARA_RA; NO_LABSH_AJUSTADA'))
pd.DataFrame(checks).to_csv(OUT/'pwt_comprobaciones.csv',index=False)
pd.concat(candidates).to_csv(OUT/'pwt_derivaciones_candidatas.csv',index=False)
# CH2 es la alternativa Wu conservada en el suplemento, no otro país.
alt=na[na.countrycode.eq('CH2')][['year','q_gdp','v_gdp']].rename(columns={'q_gdp':'q_gdp_wu','v_gdp':'v_gdp_wu'})
china=na[na.countrycode.eq('CHN')][['year','q_gdp','v_gdp']].merge(alt,on='year',how='left').sort_values('year')
china['growth_official_pct']=china.q_gdp.pct_change(fill_method=None)*100
china['growth_wu_pct']=china.q_gdp_wu.pct_change(fill_method=None)*100
china.to_csv(OUT/'china_pib_oficial_alternativa_wu.csv',index=False)
(OUT/'pwt_evidencias_fuentes.json').write_text(json.dumps(provenance,indent=2,ensure_ascii=False))
print(pd.DataFrame(checks).to_string(index=False))
print('China comp_sh:',pd.concat(candidates).query("countrycode=='CHN'").groupby('comp_sh_quality').size().to_dict())
assert len(alt)>0,'CH2 no encontrado'
assert pd.concat(candidates).comp_sh.dropna().between(0,1).all()
