import sys,json,urllib.request,ssl
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,'trabajo_china/src')
from acquire_core import fetch
specs=[]
for label,file in [('2001_2016','evolparoseries2001.xls'),('2017_current','evolparoseries.xls'),('evolution','parosexedasect.xls')]:
 specs.append(dict(id='sepe_registered_'+label+'_20261020',url='https://www.sepe.es/SiteSepe/contenidos/que_es_el_sepe/estadisticas/datos_avance/xls/empleo/'+file,extension='xls',publication_date=None,landing_url='https://www.sepe.es/HomeSepe/que-es-el-sepe/estadisticas/datos-avance/paro.html'))
specs.append(dict(id='bde_money_history_landing',url='https://repositorio.bde.es/handle/123456789/15431',extension='html',publication_date=None,landing_url='https://www.bde.es/webbe/es/estadisticas/otras-estadisticas/historicas/bloques/magnitudes-monetarias-financieras.html'))
for file in ['0906001a','0906003a']:
 specs.append(dict(id='ine_'+file+'_landing',url='https://www.ine.es/jaxi/Tabla.htm?path=/t38/bme2/t30/p148/l0/&file='+file+'.px&L=0',extension='html',publication_date=None,landing_url='https://www.ine.es/jaxi/Tabla.htm?path=/t38/bme2/t30/p148/l0/&file='+file+'.px&L=0'))
with ThreadPoolExecutor(max_workers=4) as pool:
 jobs={pool.submit(fetch,s):s for s in specs}
 for f in as_completed(jobs):
  try:m=f.result();print(m['id'],m['bytes'],flush=True)
  except Exception as e:print(jobs[f]['id'],repr(e),flush=True)
