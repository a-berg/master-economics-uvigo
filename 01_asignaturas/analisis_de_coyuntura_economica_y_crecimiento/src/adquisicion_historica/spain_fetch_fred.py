import sys
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,'trabajo_china/src')
from acquire_core import fetch
specs=[dict(id='fred_imf_spain_'+s.lower(),url=f'https://fred.stlouisfed.org/data/{s}',extension='html',publication_date=None,landing_url=f'https://fred.stlouisfed.org/series/{s}') for s in ['MYAGM1ESM189N','MYAGM2ESM189N','MYAGM3ESM189N']]
with ThreadPoolExecutor(max_workers=3) as pool:
 jobs={pool.submit(fetch,s):s for s in specs}
 for f in as_completed(jobs):
  try:m=f.result();print(m['id'],m['bytes'],flush=True)
  except Exception as e:print(jobs[f]['id'],repr(e),flush=True)
