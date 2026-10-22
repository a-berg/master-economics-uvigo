"""Adquisición China: bytes inmutables, errores explícitos y reutilización por hash.

uv run python src/china_acquire.py priority|nbs
NBS solo después de examinar output/revision_china/contratos.csv.
"""
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from pipeline import download_one, write_json

ROOT = Path(__file__).resolve().parents[1]
INDICATORS = '''NY.GDP.MKTP.CN NY.GDP.MKTP.KN NE.CON.PRVT.CN NE.CON.PRVT.KN
NE.CON.GOVT.CN NE.CON.GOVT.KN NE.GDI.TOTL.CN NE.GDI.TOTL.KN
NE.GDI.FTOT.CN NE.GDI.FTOT.KN NE.GDI.STKB.CN NE.GDI.STKB.KN NE.EXP.GNFS.CN NE.EXP.GNFS.KN
NE.IMP.GNFS.CN NE.IMP.GNFS.KN FP.CPI.TOTL SP.POP.TOTL SP.POP.0014.TO
SP.POP.1564.TO SP.POP.65UP.TO SL.TLF.TOTL.IN SL.UEM.TOTL.ZS
SL.TLF.CACT.ZS SL.EMP.TOTL.SP.ZS SI.POV.GINI FM.LBL.BMNY.CN
FM.LBL.MQMY.CN FM.LBL.MONY.CN PA.NUS.FCRF FR.INR.LEND FR.INR.DPST
NY.GNS.ICTR.CN NY.GNP.MKTP.CN NY.ADJ.DKAP.CN NY.TAX.NIND.CN
NV.AGR.TOTL.CN NV.IND.TOTL.CN NV.SRV.TOTL.CN SP.DYN.CBRT.IN SP.DYN.CDRT.IN'''.split()

def specs(stage):
    def item(id, url, fmt):
        return dict(id='china_'+id, provider=id.split('_')[0], url=url, format=fmt,
                    purpose='China audit; no automatic equivalence', publication_date=None)
    if stage == 'expanded':
        return [item('oecd_icio','https://www.oecd.org/en/data/datasets/inter-country-input-output-tables.html','html'),
                item('adb_io','https://data.adb.org/dataset/peoples-republic-china-input-output-economic-indicators','html'),
                item('pbc_m1_method','https://www.pbc.gov.cn/en/3688247/3688978/3709137/2025080817512723397/index.html','html'),
                item('imf_accounts_method','https://dsbb.imf.org/sdds/dqaf-base/country/CHN/category/NAG00','html')]
    if stage == 'priority':
        result=[]
        for code in INDICATORS:
            result.append(item('wdi_data_'+code.lower().replace('.','_'),f'https://api.worldbank.org/v2/country/CHN/indicator/{code}?source=2&format=json&per_page=20000','json'))
            result.append(item('wdi_meta_'+code.lower().replace('.','_'),f'https://api.worldbank.org/v2/indicator/{code}?format=json','json'))
        base='https://rplumber.ilo.org/'
        result += [item('ilo_chn_annual',base+'data/ref_area?format=.csv.gz&id=CHN_A','gz')]
        for dic in ['indicator','source','classif1','classif2','sex','obs_status','note_source','note_indicator','note_classif']:
            result.append(item('ilo_dic_'+dic,base+'metadata/dic?format=.csv&lang=en&var='+dic,'csv'))
        result.append(item('un26_presence','https://data.un.org/Data.aspx?d=SNA&f=group_code%3A206%3Bcountry_code%3A156','html'))
        return result
    result=[item('nbs_index','https://www.stats.gov.cn/sj/ndsj/2025/left_.htm','html'),
            item('nbs_accounts_method','https://www.stats.gov.cn/sj/ndsj/2025/html/sme03.htm','html')]
    for table in ['03-01','03-10','03-15','03-21','03-22','04-01','18-01']:
        result.append(item('nbs_'+table.replace('-','_'),'https://www.stats.gov.cn/sj/ndsj/2025/html/E'+table+'.jpg','jpg'))
    return result

def acquire(spec):
    result=download_one(spec)
    if result['status']!='failed' and spec['id'].startswith('china_wdi_'):
        obj=json.loads((ROOT/result['artifact']).read_text())
        if not isinstance(obj,list) or len(obj)!=2 or not isinstance(obj[1],list):
            return {**result,'status':'failed','error':'WDI response has no data array; original response preserved'}
        if int(obj[0].get('pages',1))!=1:
            return {**result,'status':'failed','error':'Pagination incomplete; do not normalize'}
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['priority','nbs','expanded']);args=p.parse_args()
    with ThreadPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(acquire,specs(args.stage)))
    write_json(ROOT/f'output/revision_china/acquisition_{args.stage}.json',results)
    for r in results:print(r['id'],r['status'],r.get('error',''))
    if any(r['status']=='failed' for r in results):raise SystemExit(2)

if __name__=='__main__':main()
