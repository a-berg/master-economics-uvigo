"""Targeted P52+P53 then P52 research. Preserve all responses; no automatic integration."""
import argparse,json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
from pipeline import download_one,write_json
ROOT=Path(__file__).resolve().parents[1]
SPECS=[
 ('oecd_structure','https://sdmx.oecd.org/public/rest/v1/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE1_EXPENDITURE/2.0?references=all','xml'),
 ('fred_real_page','https://fred.stlouisfed.org/series/NINVRXDCCNA','html'),
 ('fred_real_csv','https://fred.stlouisfed.org/graph/?g=1&id=NINVRXDCCNA&cosd=1900-01-01&coed=2026-11-02','html'),
 ('fred_real_download','https://fred.stlouisfed.org/graph/graph.csv?id=NINVRXDCCNA','csv'),
 ('fred_nominal_download','https://fred.stlouisfed.org/graph/graph.csv?id=NINVXDCCNA','csv'),
 ('imf_method','https://dsbb.imf.org/sdds/dqaf-base/country/CHN/category/NAG00','html'),
 ('wdi_real','https://api.worldbank.org/v2/country/CHN/indicator/NE.GDI.STKB.KN?source=2&format=json&per_page=20000','json')]
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--stage',choices=['initial','combined','p52'],default='initial');args=parser.parse_args()
 specs=SPECS
 if args.stage!='initial':
  transaction='P5M' if args.stage=='combined' else 'P52'
  key='.'.join(['A','CHN','','',transaction,'','','','','','',''])
  specs=[('oecd_'+transaction.lower(),'https://sdmx.oecd.org/public/rest/v1/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_EXPENDITURE,2.0/'+key+'?format=csvfile','csv')]
 def acquire(s):
  id,url,fmt=s
  result=download_one(dict(id='china_inventory_search_'+id+'_20261102',url=url,format=fmt,provider='research',publication_date=None,purpose='P52+P53 before P52; candidate only'))
  return dict(**result,url=url,checked_at_utc=datetime.now(timezone.utc).isoformat())
 with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(acquire,specs))
 write_json(ROOT/('output/revision_china/inventories_search/acquisition_'+args.stage+'.json'),results)
 for r in results:print(r['id'],r['status'],r.get('error',''))
 if any(r['status']=='failed' for r in results):raise SystemExit(2)
if __name__=='__main__':main()
