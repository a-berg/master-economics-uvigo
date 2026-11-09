"""Lee la copia de trabajo y actualiza tablas, gráficos y resultados del Typst.

No escribe en Excel. Ejecutar otra vez después de la edición manual.
"""
from pathlib import Path
import argparse
import json
import subprocess
import openpyxl

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=ROOT/'entregas/ipc'
DEFAULT=ROOT/'output/ipc/IPC-ADRIAN BERGES-revisado.xlsx'

def update(path):
    formulas=openpyxl.load_workbook(path,data_only=False)
    values=openpyxl.load_workbook(path,data_only=True)
    s=values['Mis Gastos']
    f=formulas['Mis Gastos']
    base=json.loads((DATA/'datos_ipc.json').read_text())
    plan=json.loads((DATA/'plan_precios.json').read_text())
    weeks=[]
    for k,col in enumerate((94,96,98)):
        missing=[]
        cost=0
        for item in base['items']:
            price=s.cell(item['row'],col).value
            expression=f.cell(item['row'],col).value
            if expression==f'=$CK{item["row"]}/$CL{item["row"]}':
                price=item['base_price']
            if not isinstance(price,(int,float)):
                missing.append(dict(row=item['row'],name=item['name'],base_price=item['base_price']))
            else:
                cost+=price*item['quantity']
        index=None if missing else cost/base['total']*100
        prev=100 if not weeks else weeks[-1]['index']
        rate=None if index is None or prev is None else (index/prev-1)*100
        weeks.append(dict(label=('12–18/10/2026','19–25/10/2026','26/10–01/11/2026')[k],cost=None if missing else cost,index=index,rate=rate,missing=missing))
    result=dict(complete=all(w['index'] is not None for w in weeks),weeks=weeks,counts=plan['counts'],supermarket_products=len(plan['items']),manual_products=len(plan['manual']),missing_count=len(weeks[0]['missing']),base=base['total'])
    (DATA/'seguimiento_ipc.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    pending=ROOT/'output/ipc/LEEME_PARA_TERMINAR.md'
    lines=['# Para terminar hoy','','Archivo de trabajo: `IPC-ADRIAN BERGES-revisado.xlsx`, en esta misma carpeta.','','## Supermercados ya cargados','','Se han completado las 222 celdas de 74 productos. El origen de cada semana consta en la hoja `Fuentes precios`: 14 valores proceden de históricos, catálogos o una referencia equivalente de folleto; uno se arrastra de una observación de la semana anterior y 207 conservan el precio base como estimación sin cambios. Los colores permiten distinguirlos.','','## Cuotas mensuales y columnas de gasto','','Netflix (8 €/mes), Spotify Duo (16,99 €/mes) e hipoteca (648 €/mes) conservan la tarifa confirmada por Adrián en las tres semanas. No se prorratean: cada columna semanal revaloriza las cantidades de la misma cesta base. Los pagos originales se mantienen. La base contiene dos cuotas de cada servicio; sus costes comparables son 16 €, 33,98 € y 1.296 €, respectivamente, en cada observación. No son nuevos desembolsos semanales.','','Las columnas CO, CQ y CS son fórmulas, no un diario de nuevas compras. Se han restaurado las fórmulas sustituidas por ceros en pijama e hipoteca y la borrada en CO93. También se ha corregido la «s» de CP116 a 35 €/kg, coincidente con la base y las otras semanas. La hipoteca sigue teniendo un peso elevado en la cesta original; este ajuste no cambia las ponderaciones.','','## Precios pendientes de revisión','','Introduce únicamente precios unitarios en **CP, CR y CT** de `Mis Gastos`. Una partida que no se ha vuelto a comprar también necesita precio para revalorizar la cesta. Los blancos no equivalen a tarifa constante.','','| Fila | Partida | Precio base por unidad |','| --- | --- | ---: |']
    for item in weeks[0]['missing']:
        lines.append(f'| {item["row"]} | {item["name"]} | {item["base_price"]:.3f} |')
    if result['complete']:
        lines=lines[:lines.index('## Precios pendientes de revisión')]+[
            '## Seguimiento completo','',
            'Las 104 partidas tienen precios en las tres semanas. No quedan celdas de precio pendientes. Se conservan los precios base de bombilla (4,95 €), spray (15 €) y ceras (3,99 €/unidad) como estimaciones sin cambios, autorizadas por Adrián.','',
            '| Semana | Coste de la cesta (€) | Índice (base 100) | Variación (%) |',
            '| --- | ---: | ---: | ---: |',
            *[f'| {w["label"]} | {w["cost"]:.4f} | {w["index"]:.6f} | {w["rate"]:.6f} |' for w in weeks],
            '',
            'La primera variación compara con la base; las otras dos comparan semanas consecutivas. El resultado incorpora los supuestos de estabilidad documentados.','',
        ]
    lines+=['','Para dejar toda la restauración igual: escribe `=$CK103/$CL103` en **CP103**, copia hacia abajo hasta **CP125** y pega ese bloque también en **CR103:CR125** y **CT103:CT125**. Los signos `$` fijan las columnas de la base. Revisa cualquier precio que haya cambiado.','','Cuando todos los precios estén completos, el resumen y los gráficos del Excel se calcularán. Guarda el archivo antes de actualizar el informe.','','## Actualizar el informe','','Desde la raíz de la asignatura:','','```bash','uv run python source/ipc/actualizar_informe.py','```','','Este comando lee el Excel, actualiza los datos del Typst y compila el PDF. No modifica el Excel. Si has guardado la copia editada en otra ruta, usa `--workbook "/ruta/al/archivo.xlsx"`.','','El archivo original de Documentos se mantiene intacto. No vuelvas a ejecutar el constructor antiguo `completar_excel.mjs`, porque reconstruye desde el original.']
    if result['complete']:
        first=lines.index('Para dejar toda la restauración igual: escribe `=$CK103/$CL103` en **CP103**, copia hacia abajo hasta **CP125** y pega ese bloque también en **CR103:CR125** y **CT103:CT125**. Los signos `$` fijan las columnas de la base. Revisa cualquier precio que haya cambiado.')
        last=lines.index('## Actualizar el informe')
        del lines[first:last]
    pending.write_text('\n'.join(lines)+'\n')
    print('Precios pendientes por semana:',[len(w['missing']) for w in weeks])
    print('Índices:',[w['index'] for w in weeks])
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--workbook',type=Path,default=DEFAULT)
    p.add_argument('--no-compile',action='store_true')
    a=p.parse_args()
    update(a.workbook)
    if not a.no_compile:
        subprocess.run(['typst','compile','--root',str(ROOT),str(DATA/'mi_ipc_ABerges.typ'),str(ROOT/'output/ipc/mi_ipc_ABerges.pdf')],check=True,cwd=ROOT)
