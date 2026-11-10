"""Directed search for remaining China concepts; preserve responses and failures."""
import argparse
import hashlib
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from pipeline import download_one, write_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/revision_china/complecion'

def specs(stage):
    if stage == 'international':
        base = 'https://sdmx.oecd.org/public/rest/v1/'
        result = [
            ('oecd_table1_structure', base+'dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE1/2.0?references=all', 'xml'),
            ('oecd_table1', base+'data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1,2.0/A.CHN..........?format=csvfile', 'csv'),
            ('oecd_table6', base+'data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE6,2.0/A.CHN..........?format=csvfile', 'csv'),
        ]
        for code in ['NY.ADJ.DKAP.CN','NY.ADJ.DKAP.GN.ZS','GC.TAX.GSRV.CN','GC.TAX.INTT.CN','GC.XPN.TRFT.CN']:
            result += [('wdi_'+code.lower().replace('.','_'),f'https://api.worldbank.org/v2/country/CHN/indicator/{code}?format=json&per_page=20000','json'),
                       ('meta_'+code.lower().replace('.','_'),f'https://api.worldbank.org/v2/indicator/{code}?format=json','json')]
        return result
    if stage == 'nbs':
        return [('nbs_notes','https://www.stats.gov.cn/sj/ndsj/2025/html/zbe03.htm','html'),
                ('nbs_notes_2020','https://www.stats.gov.cn/sj/ndsj/2020/html/zbe03.htm','html'),
                ('nbs_io_page','https://www.stats.gov.cn/sj/ndsj/2025/html/E03-21.jpg','jpg')]
    if stage == 'expanded':
        return [('oecd_table6_structure','https://sdmx.oecd.org/public/rest/v1/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE6/1.0?references=all','xml'),
                ('oecd_table6_v1','https://sdmx.oecd.org/public/rest/v1/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE6,1.0/A.CHN..........?format=csvfile','csv'),
                ('wdi_gc_xpn_trft_zs','https://api.worldbank.org/v2/country/CHN/indicator/GC.XPN.TRFT.ZS?format=json&per_page=20000','json'),
                ('imf_subsidies_paper','https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025155-source-pdf.pdf','pdf'),
                ('imf_weo_chapter','https://www.imf.org/en/Publications/WEO/Issues/2025/10/14/world-economic-outlook-october-2025','html')]
    if stage == 'imf_data':
        return [('imf_weo_ch3_data','https://www.imf.org/-/media/files/publications/weo/2025/october/data/ch3data.xlsx','xlsx'),
                ('imf_weo_ch3','https://www.imf.org/-/media/files/publications/weo/2025/october/english/ch3.pdf','pdf')]
    if stage == 'imf_legacy':
        return [('imf_weo_ch3_data_legacy','https://www.imf.org/-/media/Files/Publications/WEO/2025/October/data/ch3data.ashx','xlsx'),
                ('imf_weo_ch3_legacy','https://www.imf.org/-/media/Files/Publications/WEO/2025/October/English/ch3.ashx','pdf')]
    if stage == 'imf_browser':
        return [('imf_weo_ch3_data_browser','https://www.imf.org/-/media/files/publications/weo/2025/october/data/ch3data.xlsx?download=1','xlsx')]
    if stage == 'subsidies_history':
        return [('nbs_price_subsidies','https://www.stats.gov.cn/sj/ndsj/2007/html/H0809e.htm','html')]
    raise ValueError(stage)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage',choices=['international','nbs','expanded','imf_data','imf_legacy','imf_browser','subsidies_history'])
    args = parser.parse_args()
    def acquire(s):
        name,url,fmt=s
        if args.stage == 'imf_browser':
            # Public file, ordinary browser headers. Preserve bytes, including any non-XLSX response.
            id='china_complete_'+name+'_20261102'
            folder=ROOT/'datos/bronze'/id
            try:
                if (folder/'latest.json').exists():
                    m=json.loads((folder/'latest.json').read_text())
                    assert hashlib.sha256((ROOT/m['artifact']).read_bytes()).hexdigest()==m['sha256']
                    return dict(id=id,status='cached',url=url,artifact=m['artifact'])
                req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Accept':'*/*'})
                with urllib.request.urlopen(req,timeout=30) as response:
                    raw=response.read();ctype=response.headers.get('Content-Type')
                sha=hashlib.sha256(raw).hexdigest();stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
                folder.mkdir(exist_ok=True,parents=True);path=folder/(stamp+'_'+sha[:12]+'.'+fmt)
                path.write_bytes(raw)
                m=dict(id=id,url=url,provider='imf',artifact=str(path.relative_to(ROOT)),sha256=sha,size_bytes=len(raw),content_type=ctype,
                       accessed_at_utc=datetime.now(timezone.utc).isoformat(),request_headers=dict(req.header_items()))
                write_json(path.with_suffix(path.suffix+'.json'),m);write_json(folder/'latest.json',m)
                result=dict(id=id,url=url,status='downloaded',artifact=m['artifact'])
            except Exception as exc:result=dict(id=id,url=url,status='failed',error=f'{type(exc).__name__}: {exc}')
            print(name,result['status'],result.get('error',''),flush=True)
            return result
        result=download_one(dict(id='china_complete_'+name+'_20261102',url=url,format=fmt,
                                provider=name.split('_')[0],publication_date=None,
                                purpose='Remaining concepts; practical documented alternatives'))
        result.update(url=url,checked_at_utc=datetime.now(timezone.utc).isoformat())
        print(name,result['status'],result.get('error',''),flush=True)
        return result
    with ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(acquire,specs(args.stage)))
    write_json(OUT/('acquisition_'+args.stage+'.json'),results)
    if any(r['status']=='failed' for r in results): raise SystemExit(2)

if __name__=='__main__': main()
