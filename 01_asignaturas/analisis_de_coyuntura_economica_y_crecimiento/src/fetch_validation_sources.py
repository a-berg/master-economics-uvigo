"""Documentación primaria para revisar las equivalencias, archivada con hashes."""
from concurrent.futures import ThreadPoolExecutor
from acquire_core import fetch
SPECS=[dict(id='pwt110_userguide',url='https://dataverse.nl/api/access/datafile/554025',extension='pdf',publication_date=None,landing_url='https://www.rug.nl/ggdc/productivity/pwt/'),dict(id='pwt110_whatsnew',url='https://dataverse.nl/api/access/datafile/554031',extension='pdf',publication_date=None,landing_url='https://www.rug.nl/ggdc/productivity/pwt/'),dict(id='pwt110_labor_detail',url='https://dataverse.nl/api/access/datafile/554028',extension='dta',publication_date=None,landing_url='https://www.rug.nl/ggdc/productivity/pwt/'),dict(id='pwt80_na_method',url='https://www.rug.nl/ggdc/docs/national_accounts_in_pwt80.pdf',extension='pdf',publication_date=None,landing_url='https://www.rug.nl/ggdc/productivity/pwt/pwt-documentation')]
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=4) as pool:
  for m in pool.map(fetch,SPECS):print(m['id'],m['artifact'],flush=True)
