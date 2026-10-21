"""Descarga AMECO y las cuentas nacionales ONU sin alterar el snapshot inicial."""
import concurrent.futures,hashlib,json,urllib.request
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPECS=[dict(id='ameco_spring2026',url='https://ec.europa.eu/economy_finance/db_indicators/ameco/documents/ameco0.zip',extension='zip',publication_date='2026-06-03',landing_url='https://economy-finance.ec.europa.eu/economic-research-and-databases/economic-databases/ameco-database/download-annual-data-set-macro-economic-database-ameco_en'),dict(id='un_ama_current_lcu',url='https://unstats.un.org/unsd/amaapi/api/file/1',extension='xlsx',publication_date=None,landing_url='https://unstats.un.org/unsd/snaama/downloads'),dict(id='un_ama_constant2020_lcu',url='https://unstats.un.org/unsd/amaapi/api/file/5',extension='xlsx',publication_date=None,landing_url='https://unstats.un.org/unsd/snaama/downloads')]
def fetch(spec):
 folder=ROOT/'datos/bronze'/spec['id'];folder.mkdir(parents=True,exist_ok=True)
 p=folder/'latest.json'
 if p.exists():
  m=json.loads(p.read_text());target=ROOT/m['artifact']
  if hashlib.sha256(target.read_bytes()).hexdigest()!=m['sha256']:raise ValueError('Hash incorrecto')
  return m
 with urllib.request.urlopen(spec['url'],timeout=100) as r:
  raw=r.read();headers=dict(r.headers)
 sha=hashlib.sha256(raw).hexdigest();date=datetime.now(timezone.utc)
 target=folder/(date.strftime('%Y%m%dT%H%M%S')+'_'+sha[:12]+'.'+spec['extension']);target.write_bytes(raw)
 m={**spec,'artifact':target.relative_to(ROOT).as_posix(),'sha256':sha,'bytes':len(raw),'accessed_at_utc':date.isoformat(),'content_type':headers.get('Content-Type'),'provider_last_modified':headers.get('Last-Modified')}
 text=json.dumps(m,ensure_ascii=False,indent=2)+'\n';p.write_text(text);(folder/(target.name+'.json')).write_text(text)
 return m
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for m in pool.map(fetch,SPECS):print(m['id'],m['bytes'],m['artifact'],flush=True)
