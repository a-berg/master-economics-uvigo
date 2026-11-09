"""Completa opciones/cachés de gráficos no expuestas por artifact-tool.

Conserva referencias dinámicas a las celdas y omite los puntos pendientes.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
import openpyxl
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('--workbook',type=Path,default=Path('output/ipc/IPC-ADRIAN BERGES-revisado.xlsx'))
path=parser.parse_args().workbook
w=openpyxl.load_workbook(path,data_only=True)
s=w['Tablas e Gráficos']
ns={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
tag=lambda name:'{'+ns['c']+'}'+name

with ZipFile(path) as source:
    entries=[(info,source.read(info.filename)) for info in source.infolist()]
with ZipFile(path,'w',ZIP_DEFLATED) as target:
    for info,data in entries:
        if '/charts/chart' in info.filename and info.filename.endswith('.xml'):
            root=E.fromstring(data)
            for el in root.findall('.//c:dispBlanksAs',ns):
                el.set('val','gap')
            for series in root.findall('.//c:ser',ns):
                ref=series.find('c:val/c:numRef',ns)
                is_rate='$L$' in ref.find('c:f',ns).text
                cache=ref.find('c:numCache',ns)
                if cache is None:
                    cache=E.SubElement(ref,tag('numCache'))
                cache.clear()
                E.SubElement(cache,tag('formatCode')).text='0.00'
                E.SubElement(cache,tag('ptCount'),val='4')
                for idx,row in enumerate(range(17,21)):
                    value=s.cell(row,12 if is_rate else 11).value
                    if isinstance(value,(int,float)):
                        point=E.SubElement(cache,tag('pt'),idx=str(idx))
                        E.SubElement(point,tag('v')).text=str(value)
                cat=series.find('c:cat/c:strRef',ns)
                cache=cat.find('c:strCache',ns)
                if cache is None:
                    cache=E.SubElement(cat,tag('strCache'))
                cache.clear()
                E.SubElement(cache,tag('ptCount'),val='4')
                for idx,row in enumerate(range(17,21)):
                    point=E.SubElement(cache,tag('pt'),idx=str(idx))
                    E.SubElement(point,tag('v')).text=str(s.cell(row,10).value)
                marker=series.find('c:marker',ns)
                if marker is not None:
                    symbol=marker.find('c:symbol',ns)
                    if symbol is not None:
                        symbol.set('val','circle')
            data=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
        target.writestr(info,data)
print('Gráficos: huecos y cachés sin ceros ficticios; referencias conservadas.')
