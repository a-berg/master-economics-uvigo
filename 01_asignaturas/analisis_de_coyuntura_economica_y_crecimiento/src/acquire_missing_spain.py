"""Adquisición de fuentes identificadas: originales y fallos explícitos, sin fabricar series."""
import json
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from acquire_core import fetch
R=Path(__file__).resolve().parents[1]
SPECS=[]
for table,name in [('6545','deaths_residence'),('6554','deaths_historical'),('6518','births_registration'),('6529','marriages_different_sex'),('3169','insolvency'),('3184','insolvency_turnover'),('32449','sector_accounts')]:
 SPECS.append(dict(id='ine_'+name+'_20261020',url=f'https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{table}',extension='json',publication_date=None,landing_url=f'https://www.ine.es/jaxiT3/Tabla.htm?t={table}'))
SPECS += [dict(id='mites_smi_20261020',url='https://www.mites.gob.es/estadisticas/bel/SMI/smi1.xls',extension='xls',publication_date=None,landing_url='https://www.mites.gob.es/es/Guia/texto/guia_6/contenidos/guia_6_13_2.htm'),dict(id='wdi_fx_esp_emu_20261020',url='https://api.worldbank.org/v2/country/ESP;EMU/indicator/PA.NUS.FCRF?format=json&per_page=20000',extension='json',publication_date=None,landing_url='https://data.worldbank.org/indicator/PA.NUS.FCRF')]
def main():
 records=[]
 with ThreadPoolExecutor(max_workers=4) as pool:
  jobs={pool.submit(fetch,s):s for s in SPECS}
  for f in as_completed(jobs):
   s=jobs[f]
   try:m=f.result();rec={'id':s['id'],'status':'ARCHIVED','bytes':m['bytes'],'artifact':m['artifact']}
   except Exception as e:rec={'id':s['id'],'status':'FAILED','error':str(e),'url':s['url']}
   records.append(rec);print(rec,flush=True)
 dest=R/'output/revision_espana';dest.mkdir(exist_ok=True)
 (dest/'missing_sources_acquisition.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
