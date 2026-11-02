"""Execute a short review notebook for report data, without repeating acquisition."""
from pathlib import Path
import nbformat as nb
from execute_notebook import execute

ROOT=Path(__file__).resolve().parents[1]

def main():
    cells=[]
    def md(s):cells.append(nb.v4.new_markdown_cell(s))
    def code(s):cells.append(nb.v4.new_code_cell(s))
    md('''# Datos listos para redactar: China–España

Comparación principal 1990–2023 y contabilidad del crecimiento 1960–2023. Esta es la capa gold del informe: indicadores, tablas y gráficos con fórmulas y notas. Las entregas silver anteriores se conservan. La guía completa está en `output/preparacion_informe/GUIA_PARA_REDACTAR.md`.

Las alternativas permiten analizar evolución y estructura. No acreditan equivalencia exacta de todos los conceptos; dos bloques siguen parciales: rentas completas e input-output bilateral.''')
    code('''from pathlib import Path
import json
import polars as pl
from IPython.display import display, Image, Markdown
ROOT=Path.cwd() if (Path.cwd()/'datos').exists() else Path.cwd().parent
OUT=ROOT/'output/preparacion_informe'
GOLD=ROOT/'datos/gold/informe'
d=pl.read_parquet(GOLD/'indicadores.parquet')
catalogue=pl.read_csv(GOLD/'diccionario.csv',infer_schema_length=None)
registry=pl.read_csv(OUT/'catalogo_resultados.csv',infer_schema_length=None)
display(json.loads((OUT/'resumen.json').read_text()))
display(pl.read_csv(OUT/'estado_requisitos.csv').select('id','title','status','artifacts'))''')
    md('''## Crecimiento: mismos subperiodos y dos medidas distintas

Las tasas compuestas (CAGR) describen variaciones acumulativas. Las contribuciones de capital, empleo y residuo se suman al crecimiento logarítmico anualizado. Las tablas 6.3–6.4 y 7.1 comparten subperiodos. El residuo de Solow incluye todo lo no explicado por estos dos inputs; no es una medición exclusiva de tecnología.''')
    code('''display(pl.read_csv(GOLD/'tablas/6.T3.csv'))
display(pl.read_csv(GOLD/'tablas/7.T1.csv'))''')
    md('''## Demanda y productividad

Los componentes reales se estudian como índices y tasas de la misma edición PWT NA. Las participaciones son nominales. La productividad usa PIB y empleo PWT; las horas son totales, calculadas como ocupados por horas medias. Los gráficos conservan paneles separados para ambos países.''')
    code('''for id in ['2B.4','2C.8']:
    display(Image(filename=str(OUT/'figuras'/(id+'.png'))))
display(pl.read_csv(GOLD/'tablas/2B.T1.csv').filter((pl.col('start')==1990)&(pl.col('end')==2023)))''')
    md('''## Muestras comparables para los estadísticos

Cada correlación usa exactamente los mismos años para China y España dentro del par y ventana. Las muestras pueden diferir entre variables. Se muestra n y se conserva la lista de años y cada observación utilizada. Las existencias usan cambios de un índice del flujo, no tasas porcentuales; por ello se omite su desviación relativa frente al PIB.''')
    code('''display(pl.read_csv(GOLD/'tablas/2B.T3.csv').select('country','window_start','window_end','metric','n','mean','correlation','relative_sd'))
display(pl.read_csv(GOLD/'tablas/2C.T2.csv').filter(pl.col('metric')=='change_inventories').select('country','window_start','window_end','n','actual_last','correlation','relative_sd','note'))''')
    md('''## Remuneración por ocupado y mercado laboral

El indicador docente D1/ocupados no es salario por asalariado. Se combina D1 nacional con empleo PWT y se utiliza el deflactor del PIB nacional. La comparación laboral principal emplea modelos OIT/WDI en ambos países; registros y encuestas nacionales mantienen sus coberturas propias.''')
    code('''for id in ['3.5','4.5']:
    display(Image(filename=str(OUT/'figuras'/(id+'.png'))))
display(pl.read_csv(GOLD/'tablas/3.T4.csv').select('country','window_start','window_end','metric','n','correlation'))''')
    md('''## Limitaciones que hay que llevar al texto

Las notas distinguen restricciones de acceso, falta de cobertura y diferencias económicas. Las aproximaciones aceptadas deben acompañarse de su interpretación; no es necesario enumerar detalles técnicos que no afectan a las conclusiones. La matriz española IO y las referencias históricas docentes adicionales siguen pendientes de incorporación. El borrador Typst anterior aún no refleja esta capa de datos.''')
    code('''display(pl.read_csv(OUT/'limitaciones.csv'))
display(registry.filter(pl.col('status')=='PARCIAL').select('id','title','note','missing'))
display(Markdown('El índice visual completo está en **output/preparacion_informe/index.html**. Cada figura conserva sus datos exportados en **datos/gold/informe/figuras_datos/**.'))''')
    n=nb.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python (coyuntura)','language':'python','name':'python3'}})
    p=ROOT/'notebooks/06_datos_informe.ipynb';nb.write(n,p);execute(p)
    n=nb.read(p,as_version=4);n.metadata['execution_note']='Ejecución deliberada con IPython en proceso, sin iniciar kernel Jupyter.';nb.write(n,p)

if __name__=='__main__':main()
