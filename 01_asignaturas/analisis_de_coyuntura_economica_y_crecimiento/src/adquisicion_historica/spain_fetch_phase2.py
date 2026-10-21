import sys
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,'trabajo_china/src')
from acquire_core import fetch
specs=[dict(id='ine_suspensions_historical_20261020',url='https://www.ine.es/jaxi/files/_px/es/csv_bdsc/t38/bme2/t30/p148/l0/0906001a.csv_bdsc',extension='csv',publication_date=None,landing_url='https://www.ine.es/jaxi/Tabla.htm?path=/t38/bme2/t30/p148/l0/&file=0906001a.px&L=0'),dict(id='ine_bankruptcies_historical_20261020',url='https://www.ine.es/jaxi/files/_px/es/csv_bdsc/t38/bme2/t30/p148/l0/0906003a.csv_bdsc',extension='csv',publication_date=None,landing_url='https://www.ine.es/jaxi/Tabla.htm?path=/t38/bme2/t30/p148/l0/&file=0906003a.px&L=0'),dict(id='bde_money_statistical_annex_2018',url='https://www.bde.es/f/webbde/SES/Secciones/Publicaciones/PublicacionesSeriadas/DocumentosTrabajo/18/Files/Statistical_Annex.zip',extension='zip',publication_date='2018-02-19',landing_url='https://www.bde.es/wbe/es/publicaciones/analisis-economico-investigacion/documentos-trabajo/money-spain--new-historical-statistics-18301998.html'),dict(id='mites_smi_http_20261020',url='http://www.mites.gob.es/estadisticas/bel/SMI/smi1.xls',extension='xls',publication_date=None,landing_url='https://www.mites.gob.es/es/Guia/texto/guia_6/contenidos/guia_6_13_2.htm')]
with ThreadPoolExecutor(max_workers=4) as pool:
 jobs={pool.submit(fetch,s):s for s in specs}
 for f in as_completed(jobs):
  try:m=f.result();print(m['id'],m['bytes'],flush=True)
  except Exception as e:print(jobs[f]['id'],repr(e),flush=True)
