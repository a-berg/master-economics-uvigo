"""Transcripciones visuales revisables de tablas JPG NBS archivadas.
No OCR silencioso. Cada posición corresponde a fila/columna del original.
"""
import json
from pathlib import Path
import polars as pl
from china_silver import ROOT,OUT,manifest

def extract():
    OUT.mkdir(exist_ok=True,parents=True);records=[]
    def add(table,series,years,values,unit,note):
        m=manifest('china_nbs_'+table)
        for y,v in zip(years,values,strict=True):
            records.append(dict(table=table,series_id='NBS.'+series,year=y,value=v,unit=unit,
                artifact=m['artifact'],bronze_sha256=m['sha256'],source_url=m['url'],
                extraction='visual_transcription_from_archived_image',note=note))
    gdp=[3684.8,4107.2,4595.7,4944.7,5383.6,6032.5,7292.4,9115.9,10395.2,12196.1,15206.4,17210.0,18909.6,22070.9,27295.6,35819.7,48862.2,61649.4,72210.6,80225.0,85863.9,91378.9,101308.6,112157.3,123311.9,139377.3,164228.0,189907.5,222578.4,274179.7,324317.8,354521.6,419253.3,497507.6,547510.6,603660.4,655782.9,702511.5,761193.0,847382.9,936010.1,1005872.4,1034867.6,1173823.0,1234029.4,1294271.7,1349083.5]
    add('03_01','GDP.CURRENT',range(1978,2025),gdp,'100_million_CNY_current','PIB por producción; tabla 3-1 edición 2025; revisión quinto censo. No sustituye una tabla de producción bruta P.1.')
    add('04_01','REGISTERED_UNEMPLOYED.URBAN',range(2020,2025),[1160,1040,1203,1074,1102],'ten_thousand_persons','Registrados urbanos; no toda China ni equivalencia SEPE. Momento de referencia no explicitado en esta fila; no etiquetar como media anual.')
    add('04_01','SURVEY_UNEMPLOYMENT.URBAN.ANNUAL_MEAN',range(2020,2025),[5.6,5.1,5.6,5.2,5.1],'percent','Tasa de encuesta urbana; media anual. No nivel de desempleados nacionales.')
    add('04_01','SURVEY_UNEMPLOYMENT.URBAN.YEAR_END',range(2020,2025),[5.2,5.1,5.5,5.1,5.1],'percent','Tasa urbana al cierre; separada de media anual.')
    add('03_15','COMPENSATION.DOMESTIC.USES',[2023],[687230.1],'100_million_CNY_current','Usos de sectores domésticos: 365599.1+23690.6+104567.4+193372.9. Recursos domésticos 687736.0 incluyen flujos con resto del mundo; no confundir doméstico con nacional.')
    add('03_15','TAXES_PRODUCTION.NET',[2023],[103970.7],'100_million_CNY_current','Impuestos NETOS sobre producción; no permite separar D2 y D3.')
    add('03_15','GFCF.CURRENT',[2023],[523590.3],'100_million_CNY_current','Tabla de flujos de fondos; nominal. No CCF ni volumen.')
    add('03_15','INVENTORIES.CURRENT',[2023],[8740.0],'100_million_CNY_current','Variación de existencias nominal; no deflactar con PIB.')
    add('03_15','GCF.CURRENT',[2023],[532330.2],'100_million_CNY_current','FBC nominal; diferencia de 0.1 respecto a suma componentes por redondeo.')
    # Money: year-end, old M1 definition. Breaks explicitly retained in catalogue.
    add('18_01','M2.YEAR_END',range(1990,2025),[15293.4,19349.9,25402.2,34879.8,46923.5,60750.5,76094.9,90995.3,104498.5,119897.9,134610.3,158301.9,185007.0,221222.8,253207.7,298755.5,345577.9,403401.3,475166.6,610224.5,725851.8,851590.9,974148.8,1106525.0,1228374.8,1392278.1,1550066.7,1690235.3,1826744.2,1986488.8,2186795.9,2382899.6,2664320.8,2922713.3,3135322.3],'100_million_CNY_year_end','PBC vía NBS. Rupturas 1997, junio 2001, 2009/2010, octubre 2011, enero 2018. No BM; no M3.')
    pl.DataFrame(records).write_csv(OUT/'nbs_transcription.csv')
    # IO rows supply products, columns use products. 1 agriculture; 2–12 industry incl construction; 13–20 services.
    matrix='''22600.7 56.0 42072.1 4133.0 6215.8 6198.0 111.3 200.4 574.3 321.1 488.3 842.3 120.6 126.9 10294.9 234.2 100.0 316.6 2228.4 4304.4
113.7 11202.4 307.2 107.5 434.4 47406.8 7877.3 30718.7 307.2 151.0 20714.4 1631.1 23.6 39.5 47.5 0.0 3.5 106.4 54.5 457.0
15881.6 173.5 17066.7 419.7 253.3 2510.5 214.1 1104.9 2347.9 63.8 617.6 1085.6 319.6 942.4 16798.2 793.6 342.0 365.0 1801.4 5490.4
19.5 143.0 385.5 20342.6 1518.4 999.7 292.7 268.0 1094.8 161.8 72.6 357.5 53.6 262.6 541.6 51.3 91.1 111.0 995.1 3945.1
251.0 643.5 1458.2 498.3 16962.0 1487.0 925.2 808.6 2769.4 193.0 134.4 7534.8 714.9 1597.3 382.7 2752.8 1640.2 174.3 5958.5 6966.8
11251.7 3097.4 2374.9 8323.1 6507.7 77236.5 7423.6 12452.7 25633.3 1188.5 1950.9 11538.9 537.4 16833.5 834.1 363.7 61.3 255.3 4484.6 22998.6
84.6 264.4 339.0 69.9 290.1 1346.9 14490.1 2910.5 8984.6 85.1 52.5 38658.3 49.9 36.9 65.4 39.4 23.7 1903.9 49.4 1056.6
313.8 2334.5 304.5 298.6 5444.1 2730.4 4389.0 77696.6 64845.6 1161.7 195.0 44123.6 14.5 87.7 146.3 233.1 0.7 355.7 587.2 4541.3
970.2 2214.7 415.2 642.2 1489.5 1947.1 2341.1 4935.8 222602.0 1754.5 3974.2 25785.6 3146.4 15562.3 272.0 23238.2 374.3 1711.8 13522.8 20160.0
150.9 131.5 82.8 265.9 1460.2 887.5 951.7 9860.5 1023.6 2714.5 681.7 272.1 99.5 502.0 103.7 28.9 9.9 611.5 475.1 1378.3
2756.5 2747.3 1136.0 1596.3 1467.1 9588.4 4221.1 14041.3 5522.9 697.8 51164.2 1203.1 2547.2 3496.4 1496.5 1025.4 271.9 1172.0 710.3 4038.7
51.6 179.2 63.6 44.3 66.3 153.7 48.2 78.8 466.5 25.0 219.4 10032.2 263.3 180.3 121.9 33.4 79.8 5947.5 77.8 1299.7
3620.3 1218.7 4892.8 4099.4 5496.9 8769.3 3232.9 5324.4 29043.0 449.7 1288.2 12754.6 2501.5 5868.4 3422.1 3593.7 667.2 928.1 4791.2 12572.1
2634.1 2073.8 3350.5 2235.5 3351.1 8865.9 4671.3 9622.4 15990.2 445.7 2935.8 11984.3 11878.3 26161.7 1770.0 1988.5 1756.1 549.2 6590.9 11782.1
87.0 99.8 218.5 134.0 194.6 705.3 208.9 645.2 1323.6 35.5 82.5 1657.2 1217.7 2387.3 313.3 1248.3 2263.7 111.4 7030.0 10758.6
30.6 33.4 123.2 71.5 88.2 142.7 36.5 73.3 2946.7 13.4 120.0 1670.2 5772.9 4492.1 515.2 50589.4 2302.7 891.1 8826.2 12248.3
2055.8 1743.3 591.1 461.7 548.4 2110.4 1133.7 4078.6 2241.0 147.5 3891.6 6554.9 7813.7 11281.4 583.5 2412.7 13307.9 5751.1 7947.4 5386.0
3.3 20.0 37.5 46.2 51.6 60.2 45.6 40.2 238.2 14.7 33.6 131.1 6899.4 493.5 955.0 3228.9 2812.6 8393.7 2662.4 5476.3
720.9 1610.4 2712.7 1157.8 1580.9 4793.7 1587.7 4536.9 13459.8 435.0 3579.1 7215.4 17523.9 4112.6 1485.2 14860.6 5745.0 9074.4 23322.4 16620.1
950.5 1082.2 887.2 585.2 720.3 2449.9 829.7 1888.1 6213.5 210.4 1946.7 30754.1 3065.6 6410.2 1133.7 2459.5 1347.1 1307.2 2618.0 26503.4'''
    a=[[float(v) for v in line.split()] for line in matrix.splitlines()]
    assert len(a)==20 and all(len(r)==20 for r in a)
    expected_rows=[101539.5,121703.8,68591.7,31707.6,53852.9,215347.7,70801.2,209803.9,347059.8,21691.8,110900.3,19432.5,114534.6,130637.2,30722.1,90987.7,80041.8,31644.1,136134.3,93362.6]
    expected_cols=[64548.2,31069.0,78819.0,45532.6,54140.9,180389.9,55031.9,181285.9,407628.3,10269.7,94142.8,215786.8,64563.6,100875.1,41282.8,109175.5,33200.7,40037.2,94733.4,177983.9]
    checks=[]
    for i in range(20):
        checks.append(dict(axis='row',index=i+1,calculated=sum(a[i]),published=expected_rows[i],difference=sum(a[i])-expected_rows[i]))
        checks.append(dict(axis='column',index=i+1,calculated=sum(r[i] for r in a),published=expected_cols[i],difference=sum(r[i] for r in a)-expected_cols[i]))
    # 20 rounded cells and one rounded total: worst-case rounding tolerance 1.05 native units.
    assert all(abs(r['difference'])<=1.051 for r in checks),[r for r in checks if abs(r['difference'])>1.051]
    pl.DataFrame(checks).write_csv(OUT/'io_transcription_checks.csv')
    groups=['agriculture']+['industry']*11+['services']*8
    m=manifest('china_nbs_03_21')
    cells=[dict(year=2023,supplying_product=i+1,using_product=j+1,supplying_sector=groups[i],using_sector=groups[j],value=a[i][j],unit='native_IO_table_unit_scale_not_explicit_in_image',bronze_sha256=m['sha256']) for i in range(20) for j in range(20)]
    d=pl.DataFrame(cells);d.write_csv(OUT/'io_2023_20_sectors.csv')
    d.group_by('year','supplying_sector','using_sector','unit','bronze_sha256').agg(pl.col('value').sum()).sort('supplying_sector','using_sector').write_csv(OUT/'io_2023_3_sectors.csv')
    return records

if __name__=='__main__':extract();print('NBS transcription and IO checks OK')
