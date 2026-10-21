"""Notebook legible con controles y salida estática para las 31 series pendientes."""
import json
from pathlib import Path
import nbformat as nb
import polars as pl
R=Path(__file__).resolve().parents[1]
md=nb.v4.new_markdown_cell; code=nb.v4.new_code_cell
pending=pl.read_csv(R/'output/revision_espana/catalogo_espana.csv').filter(pl.col('initial_status').is_in(['COMPATIBLE_CODIGO_DIFERENCIAS_PENDIENTES','PENDIENTE_UNIDADES','PENDIENTE_DISCREPANCIAS_NUMERICAS'])&(pl.col('n')>0)&(pl.col('source')=='ameco_spring2026'))
cells=[md('''# España: revisión de las diferencias con el Excel

**Corte: 20/10/2026.** Se conservan para diagnóstico las 26 series de código compatible con diferencias, las tres de unidades y las dos de discrepancias numéricas: **31 series españolas**. Las diez con cambio de base se aceptan por decisión del alumno usando íntegramente la edición AMECO actual. Los cuatro códigos de EE. UU. son referencias auxiliares y no entran en silver de España.

Las 31 series quedaron aceptadas tras la revisión del alumno del 20/10/2026, adoptando los datos publicados vigentes sin afirmar una causa concreta de discrepancia. El notebook no descarga, reescala ni modifica las series. La vista interactiva requiere ejecutar las celdas en un kernel local; el apéndice deja una figura por serie visible también sin kernel.

```sh
uv sync --group analysis --locked
uv run --group analysis jupyter notebook notebooks/02_revision_espana.ipynb
```

Si no tienes la interfaz de Jupyter instalada, abre este archivo en VS Code con el intérprete `.venv/bin/python` o ejecuta `uv run --with notebook --group analysis jupyter notebook notebooks/02_revision_espana.ipynb`.
'''),code('''from pathlib import Path
import sys, json
import polars as pl
from IPython.display import display, Markdown
root = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'src/spain_silver.py').exists())
sys.path.insert(0, str(root / 'src'))
from review_spain import load, summary, annual, show, explorer
from snapshot import verify
verify('v0_2026-10-16')
cat, pending, pairs = load()
print(f"España: {cat.height} entradas de catálogo; {pending.height} series para revisión.")
assert pending.height == 31
'''),md('''## 1. Decisiones vigentes y catálogo

La política está en `datos/catalogo/decisiones_espana.json`. Tras revisar las anotaciones del alumno, hay 84 series AMECO españolas: las 74 explícitas recuperadas y diez localizadas por concepto. Se conservan las decisiones sobre edición vigente y cambios de base. Las 31 comparaciones se conservan como diagnóstico histórico, sin bloquear su inclusión en la vista anual. AMGE/AXGE se excluyen de los objetivos actuales; la fecha exacta de su retirada no se ha acreditado.

No se mezclan bases del Excel y de AMECO en una misma serie. Los años 2026–2027 se conservan como horizonte de previsión en la tabla larga y se excluyen de la vista analítica. Esto no convierte automáticamente los años anteriores en definitivos.
'''),code('''display(cat.group_by('status').len().sort('status'))
display(cat.filter(pl.col('status') == 'ACEPTADA_BASE_EDICION_ACTUAL').select('series_id','name','unit','decision_note'))
'''),md('''## 2. Lista de revisión

La razón es **AMECO/Excel**, la diferencia relativa se divide por el valor absoluto del Excel y se deja vacía cuando ese valor es cero. El crecimiento solo se calcula entre años consecutivos, con valores positivos. Para cuotas, ratios o series con ceros o negativos, el gráfico muestra cambios en unidades de la serie en lugar de tasas; la MAE de crecimiento queda vacía. Una razón constante puede sugerir una escala; no demuestra su causa. No se aplica ninguna corrección automáticamente.
'''),code('''diagnostics = summary()
display(diagnostics)
'''),md('''## 3. Explorador

El selector permite ver niveles, razón, diferencias relativas y tasas anuales. El factor de escala es una **hipótesis visual** que solo modifica la línea del Excel en el panel de niveles. Los demás paneles mantienen los valores originales. No afecta a silver ni acepta la serie.
'''),code('''controls = explorer()
'''),md('''Para inspeccionar por código, sin widgets:

```python
show('ESP.1.0.0.0.URTG', start=1995, end=2025, factor_excel=1e-4)
annual('ESP.1.0.0.0.URTG')  # todas las diferencias y tasas
```

Prioridad de revisión: URTG/UUTG (escala y unidad), UVG4 (niveles), AMGT/AXGT (unidad antigua vacía), después las 26 compatibles. No se atribuyen todas las diferencias a revisiones estadísticas sin evidencia.
'''),md('''## 4. EPA: fila de procedencia desconocida

La anotación literal está en `mercado traballo`, **I29**, junto a una fila rotulada INE/EPA con datos de 1981–2011. No se ha reconstruido la procedencia exacta ni se usa esa fila para producir datos.

Se descargan tres series oficiales de medias de los cuatro trimestres: activos, ocupados y parados, total nacional, ambos sexos, 16 y más años. Tablas INE 65949, 65962 y 65994; identificadores EPA634675/6/7. Los valores están en miles de personas. La tabla actual ofrece **2006–2025**: los años anteriores quedan sin rellenar, no desaparecen del inventario pendiente.

La publicación actual utiliza base poblacional 2011 hasta 2020 y 2021 desde 2021. Es una diferencia metodológica que se conserva por año; no es un cambio de base de precios. EPA, empleo de cuentas nacionales y paro registrado permanecen separados.

Fuentes: [EPA anual](https://www.ine.es/dynt3/inebase/index.htm?capsel=10993&padre=10989), [tabla de parados](https://www.ine.es/jaxiT3/Tabla.htm?t=65994), [metadatos API](https://www.ine.es/dyngs/DAB/index.htm?cid=1102).
'''),code('''labor_comparison = pl.read_csv(root / 'output/revision_espana/epa_comparacion_excel.csv')
display(labor_comparison)
silver = pl.read_parquet(root / 'datos/silver/espana.parquet')
display(silver.filter(pl.col('source').str.starts_with('ine_epa_annual')).group_by(['series_id','population_basis']).agg(pl.col('year').min().alias('first'),pl.col('year').max().alias('last'),pl.len().alias('n')))
epa = silver.filter(pl.col('source').str.starts_with('ine_epa_annual')).pivot(on='series_id',index='year',values='value')
residual = epa.with_columns((pl.col('INE.EPA.ANNUAL.ACTIVOS')-pl.col('INE.EPA.ANNUAL.OCUPADOS')-pl.col('INE.EPA.ANNUAL.PARADOS')).alias('residuo_miles'))
display(residual)
assert residual['residuo_miles'].abs().max() < .11  # cada nivel se publica con un decimal
'''),md('''## 5. Estado de silver

`datos/silver/espana.parquet` es la tabla larga de procedencia y valores: conserva las 74 series AMECO recuperadas y las tres nuevas del INE, con estado de aceptación por serie. `espana_anual.parquet` es la vista ancha de las **97 series aceptadas**, sin horizonte de previsión; sus celdas nulas reflejan coberturas distintas. El catálogo es `espana_catalogo.parquet`.

No es todavía toda fila base del Excel: las filas sin código se enumeran en `output/revision_espana/filas_sin_codigo_inventario.csv`. Se conserva ese inventario para evitar que 76 identificadores se confundan con una auditoría completa de producción, demografía, quiebras, dinero u otras referencias no codificadas.
'''),code('''display(silver.group_by(['source','status','apta_analisis']).agg(pl.len().alias('observaciones')))
wide = pl.read_parquet(root / 'datos/silver/espana_anual.parquet')
print('Vista anual:', wide.shape, 'columnas:', wide.columns)
assert not silver.select(pl.struct(['series_id','year']).is_duplicated().any()).item()
assert silver['value'].is_finite().all()
'''),md('''## 6. Mantener el registro de decisiones

Edita únicamente las decisiones que quieras aceptar. Se adopta el valor publicado actual completo, no el del Excel ni el reescalado diagnóstico. La celda siguiente solo previsualiza; para persistir hay instrucciones explícitas debajo. Puedes mantener el resto pendiente.
'''),code('''# Ejemplo de formato; vacío para añadir decisiones futuras; las 31 aceptaciones actuales ya están en el JSON:
manual_decisions = {
    # 'ESP.1.0.0.0.AMGT': {
    #     'action': 'accept_current_edition',
    #     'note': 'Explicar unidad, denominador y evidencia consultada.'
    # }
}
assert set(manual_decisions) <= set(pending['series_id'])
assert all(v.get('note') and v.get('action') in ['accept_current_edition','keep_pending'] for v in manual_decisions.values())
display(manual_decisions)
'''),md('''Cuando termines, guarda las decisiones en `datos/catalogo/decisiones_espana.json`, campo `manual_decisions`, y ejecuta `uv run python src/spain_silver.py`. O ejecuta expresamente este bloque:

```python
policy_path = root / 'datos/catalogo/decisiones_espana.json'
policy = json.loads(policy_path.read_text())
policy['manual_decisions'].update(manual_decisions)
policy_path.write_text(json.dumps(policy, ensure_ascii=False, indent=2) + '\\n')
from spain_silver import build
build()
```

Las 31 series del explorador se mantienen como cohorte de revisión incluso tras aceptar alguna, para conservar su comparación. El estado original de la auditoría permanece en `initial_status`. La tabla de revisión fechada 19/10 es evidencia histórica; el catálogo vigente de España está en `output/revision_espana/catalogo_espana.csv`.

## 7. Apéndice: las 31 comparaciones

Las salidas guardadas permiten revisar todas las figuras sin un kernel. Para datos anuales completos usa `annual(codigo)` o el CSV de comparación anual.
''')]
for r in pending.sort('series_id').iter_rows(named=True):
 cells.append(code(f"show({r['series_id']!r}, detail=False)"))
cells.extend([md("""## 8. Anotaciones del alumno y búsqueda por concepto

Se preservan las 56 anotaciones originales y se clasifican 69 filas sin código, incluidas 13 de producción que no estaban en el CSV anotado. El catálogo completo permite buscar sin depender de que el código esté escrito en una fila del Excel. La clasificación distingue cálculo, duplicado, fuente disponible, fuente documentada y estado de integración.

Se corrige `NOMINAL!22` a **UKCG** (nominal, gobierno); OKCT es real y total economía. Para empresas se reconocen los encabezados trimestrales: se han comprobado 56 agregados anuales (1990–2003) contra los cuatro trimestres correspondientes, sin diferencias.

Las nuevas integraciones conservan ediciones distintas de INE, Eurostat y PWT; tenerlas en una misma tabla no autoriza a sustituir sus universos o a mezclar ediciones en identidades contables.
"""),code("""from ameco_full_catalogue import search
print('Búsqueda equivalente a la realizada con nushell:')
display(search('(?:capital consumption|consumption of fixed capital).*current prices'))
reconciled = pl.read_csv(root / 'output/revision_espana/filas_reconciliadas.csv')
display(reconciled.select('sheet','row','user_note','status','source_reference','integration_status'))
"""),code("""business_checks = pl.read_csv(root / 'output/revision_espana/excel_empresas_comprobacion_anual.csv')
display(business_checks.group_by('derived_row').agg(pl.len().alias('anios'),pl.col('quarters_available').min().alias('trimestres_min'),pl.col('difference').abs().max().alias('diferencia_max')))
assert business_checks.height == 56 and business_checks['difference'].abs().max() == 0
""")])
notebook=nb.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'Python (uv: analysis)','language':'python','name':'python3'},'language_info':{'name':'python'},'review_version':'2026-10-20'})
nb.write(notebook,R/'notebooks/02_revision_espana.ipynb')
print('Notebook creado con',len(cells),'celdas; apéndice:',pending.height,'series')
if __name__=='__main__':pass
