"""Originales oficiales EPA: medias de cuatro trimestres; no usa promedios parciales."""
from acquire_core import fetch
from concurrent.futures import ThreadPoolExecutor
TABLES={'65949':'activos','65962':'ocupados','65994':'parados'}
def main():
 specs=[dict(id='ine_epa_annual_'+label,url=f'https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{table}',extension='json',publication_date=None,landing_url=f'https://www.ine.es/jaxiT3/Tabla.htm?t={table}') for table,label in TABLES.items()]
 specs += [dict(id='ameco_edition_evidence_20261020',url='https://economy-finance.ec.europa.eu/economic-research-and-databases/economic-databases/ameco-database_en',extension='html',publication_date=None,landing_url='https://economy-finance.ec.europa.eu/economic-research-and-databases/economic-databases/ameco-database_en'),dict(id='ine_epa_annual_metadata',url='https://www.ine.es/dynt3/inebase/index.htm?capsel=10993&padre=10989',extension='html',publication_date=None,landing_url='https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=estadistica_C&cid=1254736176918&idp=1254735976595&menu=resultados&secc=1254736195128')]
 with ThreadPoolExecutor(max_workers=5) as pool:
  for m in pool.map(fetch,specs):print(m['id'],m['bytes'],flush=True)
if __name__=='__main__':main()
