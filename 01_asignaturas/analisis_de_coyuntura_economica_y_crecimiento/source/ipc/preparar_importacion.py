"""Normaliza identificadores de ejes negativos que bloquean el importador."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import re

source=Path('/home/xylon/Documents/Master_Economia/Analisis de Coyuntura y Crecimiento/entregable_ipc/IPC-ADRIAN BERGES.xlsx')
Path('tmp/ipc').mkdir(parents=True,exist_ok=True)
with ZipFile(source) as original, ZipFile('tmp/ipc/importable.xlsx','w',ZIP_DEFLATED) as target:
    for entry in original.infolist():
        data=original.read(entry.filename)
        if entry.filename.startswith('xl/charts/') and entry.filename.endswith('.xml'):
            data=re.sub(rb'(<c:(?:axId|crossAx)\b[^>]*\bval=")-(\d+)(")',rb'\1\2\3',data)
        target.writestr(entry,data)
