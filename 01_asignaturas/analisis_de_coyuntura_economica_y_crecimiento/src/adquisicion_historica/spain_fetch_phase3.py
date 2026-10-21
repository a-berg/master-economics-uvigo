import sys
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,'trabajo_china/src')
from acquire_core import fetch
specs=[dict(id='bde_money_method_2018',url='https://www.bde.es/f/webbde/SES/Secciones/Publicaciones/PublicacionesSeriadas/DocumentosTrabajo/18/Files/dt1806e.pdf',extension='pdf',publication_date='2018-02-19',landing_url='https://www.bde.es/wbe/es/publicaciones/analisis-economico-investigacion/documentos-trabajo/money-spain--new-historical-statistics-18301998.html')]
for code in ['FM.LBL.MQMY.CN','FM.LBL.MONY.CN','FM.LBL.BMNY.CN']:
 specs.append(dict(id='wdi_money_'+code.lower().replace('.','_'),url=f'https://api.worldbank.org/v2/country/ESP/indicator/{code}?format=json&per_page=20000',extension='json',publication_date=None,landing_url=f'https://data.worldbank.org/indicator/{code}'))
with ThreadPoolExecutor(max_workers=4) as pool:
 jobs={pool.submit(fetch,s):s for s in specs}
 for f in as_completed(jobs):
  try:m=f.result();print(m['id'],m['bytes'],flush=True)
  except Exception as e:print(jobs[f]['id'],repr(e),flush=True)
