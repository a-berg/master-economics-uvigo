"""Offline review of targeted inventory searches, isolated from accepted silver."""
import hashlib,json,xml.etree.ElementTree as ET
from pathlib import Path
import polars as pl
from pipeline import write_json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/revision_china/inventories_search'

def main():
    OUT.mkdir(parents=True,exist_ok=True);provenance=[]
    def load(id):
        m=json.loads((ROOT/'datos/bronze'/id/'latest.json').read_text())
        assert hashlib.sha256((ROOT/m['artifact']).read_bytes()).hexdigest()==m['sha256']
        provenance.append(m);return m
    structure=load('china_inventory_search_oecd_structure_20261102')
    ns={'s':'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure','c':'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'}
    tree=ET.parse(ROOT/structure['artifact']).getroot();codes=[]
    for cl in tree.findall('.//s:Codelist',ns):
        if cl.get('id') not in ['CL_PRICES','CL_TRANSACTION']:continue
        for c in cl.findall('s:Code',ns):
            if cl.get('id')=='CL_TRANSACTION' and c.get('id') not in ['P5M','P52','P53']:continue
            names=[n.text for n in c.findall('c:Name',ns) if n.get('{http://www.w3.org/XML/1998/namespace}lang')=='en']
            codes.append(dict(codelist=cl.get('id'),code=c.get('id'),label=names[0]))
    pl.DataFrame(codes).write_csv(OUT/'oecd_codes.csv')
    rows=[];tables={};summary=[]
    for transaction in ['P5M','P52']:
        m=load('china_inventory_search_oecd_'+transaction.lower()+'_20261102');d=pl.read_csv(ROOT/m['artifact'])
        assert d['REF_AREA'].unique().to_list()==['CHN'] and set(d['TRANSACTION'])=={transaction}
        assert not d.select(pl.struct(['FREQ','REF_AREA','SECTOR','COUNTERPART_SECTOR','TRANSACTION','INSTR_ASSET','ACTIVITY','EXPENDITURE','UNIT_MEASURE','PRICE_BASE','TRANSFORMATION','TABLE_IDENTIFIER','TIME_PERIOD']).is_duplicated().any()).item()
        assert set(d['PRICE_BASE'])=={'V','VQ'},'Unexpected real-price candidate: review before concluding absence'
        tables[transaction]=d
        for r in d.iter_rows(named=True):
            rows.append(dict(series_id='OECD.'+transaction+'.'+r['UNIT_MEASURE']+'.'+r['PRICE_BASE'],year=r['TIME_PERIOD'],value=r['OBS_VALUE'],
                provider='OECD',transaction=transaction,unit=r['UNIT_MEASURE'],price_base=r['PRICE_BASE'],currency=r['CURRENCY'],unit_multiplier=r['UNIT_MULT'],
                real_in_source=False,accepted_for_inventories_real=False,status='NOMINAL_NOT_REAL',price_reference_year=r['REF_YEAR_PRICE'],flag=r['OBS_STATUS'],
                bronze_sha256=m['sha256'],source_url=m['url'],metadata_note='V=current prices; VQ=current prices with constant currency/PPP converter, NOT constant prices'))
        for r in d.group_by('UNIT_MEASURE','PRICE_BASE').agg(pl.col('TIME_PERIOD').min().alias('first'),pl.col('TIME_PERIOD').max().alias('last'),pl.len().alias('n')).sort('UNIT_MEASURE','PRICE_BASE').iter_rows(named=True):
            summary.append(dict(source='OECD',transaction=transaction,**r,decision='RECHAZADA_COMO_REAL',reason='Precios corrientes, incluido VQ; no volumen nacional'))
    a=tables['P5M'].filter((pl.col('UNIT_MEASURE')=='XDC')&(pl.col('PRICE_BASE')=='V')).sort('TIME_PERIOD')
    b=tables['P52'].filter((pl.col('UNIT_MEASURE')=='XDC')&(pl.col('PRICE_BASE')=='V')).sort('TIME_PERIOD')
    assert a['TIME_PERIOD'].equals(b['TIME_PERIOD'])
    compare=pl.DataFrame(dict(year=a['TIME_PERIOD'],p52_p53=a['OBS_VALUE'],p52=b['OBS_VALUE'],difference=a['OBS_VALUE']-b['OBS_VALUE']))
    compare.write_csv(OUT/'oecd_combined_vs_p52.csv')
    # Empirical equality does not certify that P53 was separately measured or zero.
    m=load('china_inventory_search_fred_table_extract_20261102');obj=json.loads((ROOT/m['artifact']).read_text())
    assert len(obj['observations'])==40
    assert [int(o['date'][:4]) for o in obj['observations']]==list(range(1980,2020))
    for o in obj['observations']:
        rows.append(dict(series_id='IMF.IFS.FRED.NINVRXDCCNA',year=int(o['date'][:4]),value=o['value'],provider='IMF via FRED',transaction='P52_LIKE_TITLE_NO_SNA_CODE_IN_FRED',
            unit=obj['unit_as_published'],price_base='REAL_AS_TITLED_BASE_UNSPECIFIED',currency=None,unit_multiplier=None,real_in_source=True,
            accepted_for_inventories_real=False,status='REAL_CANDIDATE_METADATA_PENDING',price_reference_year=None,flag='',bronze_sha256=m['sha256'],source_url=m['url'],
            metadata_note='40 observations from readable FRED table. Raw HTTP download timed out; extraction explicitly marked. Scale/base/valuables scope not accredited. No splice after 2019.'))
    summary.append(dict(source='IMF via FRED',transaction='P52_LIKE',UNIT_MEASURE='Domestic Currency',PRICE_BASE='REAL_BASE_UNSPECIFIED',first=1980,last=2019,n=40,
        decision='CANDIDATA_REAL_NO_INTEGRADA',reason='Faltan base, escala y correspondencia expresa P52; histórica, no independencia acreditada'))
    w=load('china_inventory_search_wdi_real_20261102');obj=json.loads((ROOT/w['artifact']).read_text());assert len(obj)==2 and obj[0]['pages']==1
    n=sum(r['value'] is not None for r in obj[1]);assert n==0,'New WDI observations require review'
    summary.append(dict(source='WDI',transaction='NE.GDI.STKB.KN',UNIT_MEASURE='constant LCU',PRICE_BASE='constant',first=None,last=None,n=n,decision='SIN_VALORES_EN_CONSULTA',reason='No demuestra ausencia universal'))
    result=pl.DataFrame(rows,infer_schema_length=None).sort('series_id','year');result.write_csv(OUT/'inventories_candidates.csv');result.write_parquet(OUT/'inventories_candidates.parquet')
    pl.DataFrame(summary,infer_schema_length=None).write_csv(OUT/'candidate_summary.csv')
    write_json(OUT/'provenance.json',provenance)
    verification=dict(status='OK_CANDIDATE_ONLY',oecd_observations=sum(t.height for t in tables.values()),oecd_real_observations=0,
        oecd_nominal_combined_p52_equal_years=compare.filter(pl.col('difference')==0).height,fred_real_candidate_observations=40,
        fred_first=1980,fred_last=2019,wdi_real_observations=n,source_hash_checks=len(provenance),main_silver_modified=False,spain_modified=False,
        decision='Found P52-like real candidate, not accepted equivalence. No real P52+P53 series retrieved from OECD query.')
    write_json(OUT/'verification.json',verification);print(json.dumps(verification,indent=2))
if __name__=='__main__':main()
