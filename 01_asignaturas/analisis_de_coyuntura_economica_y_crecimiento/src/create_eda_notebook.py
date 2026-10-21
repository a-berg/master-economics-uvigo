"""Genera el notebook de exploración (sin ejecutar ni descargar)."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def md(s):return dict(cell_type='markdown',metadata={},source=s.splitlines(keepends=True))
def code(s):return dict(cell_type='code',metadata={},source=s.splitlines(keepends=True),execution_count=None,outputs=[])
cells=[md('''# Exploración inicial de China y España

Versión fija **v0_2026-10-16**. Se examinan cobertura, huecos, flags, tasas y diferencias entre fuentes. No se descarga nada ni se modifican bronze/silver/gold.

**Criterio de fuentes:** NBS directo como último recurso. Un distribuidor internacional puede reutilizar estadísticas nacionales; la coincidencia entre fuentes no prueba independencia ni descarta sesgos. Los saltos marcados son observaciones para revisar, no pruebas de manipulación.

Ejecutar con el entorno `uv sync --group analysis --locked`; seleccionar su kernel Python en Jupyter o VS Code. El notebook ejecutado conserva tablas y gráficos; para usar los controles, volver a ejecutar las celdas con un kernel activo.'''),code('''from pathlib import Path
import sys, json
import polars as pl
from IPython.display import display, Markdown, clear_output
root = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / "src/eda.py").exists())
sys.path.insert(0, str(root / "src"))
from snapshot import verify
from eda import load, coverage, explorer, cross_sources, shocks, demand_residuals, build
VERSION = "v0_2026-10-16"
manifest = verify(VERSION, root)
df, frozen = load(VERSION, root)
print(f"{VERSION}: {df.height:,} observaciones; {len(manifest['bronze_files'])} originales verificados")
'''),md('''## 1. Procedencia y versión

Los metadatos distinguen proveedor, URL, fecha de acceso, fecha de actualización y hash. Una versión congelada garantiza que repetimos los mismos cálculos con los mismos bytes; no certifica la veracidad de la medición económica.'''),code('''display(pl.DataFrame([{
    "dataset": x["metadata"].get("id", x["metadata"].get("dataset_id")),
    "provider": x["metadata"].get("provider"),
    "accessed": x["metadata"].get("accessed_at_utc"),
    "updated": x["metadata"].get("provider_updated_at"),
    "sha256": x["sha256"]
} for x in manifest["bronze_files"]], infer_schema_length=None))
policy = json.loads((frozen / "datos/catalogo/source_policy.json").read_text())
print(policy["upstream_origin"])
'''),md('''## 2. Cobertura y calidad técnica

La cobertura efectiva se calcula por serie y país, no por las columnas anunciadas en un CSV. Se detectan huecos internos y se conservan ceros, valores negativos y flags. Estos últimos no se convierten automáticamente en errores.'''),code('''cov = coverage(df)
keys = ["rgdpna", "rnna", "emp", "avh", "q_gdp", "q_c", "q_i", "q_g", "q_x", "q_m", "SI.POV.GINI"]
display(cov.filter(pl.col("source").is_in(["pwt110", "pwt110_na", "wdi_common"]) & pl.col("series").is_in(keys)))
assert df["value"].is_finite().all()
assert not df.select(pl.struct(["country", "year", "series", "source"]).is_duplicated().any()).item()
print("Claves únicas y valores numéricos finitos.")
'''),md('''## 3. Exploración de series

Se empieza con índices 2008=100. Las tasas requieren años consecutivos y niveles positivos. Si falta la base elegida, se informa; no se sustituye silenciosamente. Los niveles se muestran en paneles separados por país para evitar superponer euros y yuanes.

El selector permite escoger proveedor, serie, transformación y período. PWT contiene variables a PPA y otras a precios nacionales; consultar la leyenda conservada antes de interpretar niveles.'''),code('''explorer(df, "pwt110_na", "q_gdp", "index").show(renderer="plotly_mimetype")
'''),code('''import ipywidgets as widgets
sources = [s for s in ["pwt110_na", "pwt110", "wdi_common", "estat_nama_10_gdp"] if s in df["source"].unique()]
source = widgets.Dropdown(options=sources, value="pwt110_na", description="Proveedor")
series = widgets.Dropdown(description="Serie", layout=widgets.Layout(width="650px"))
mode = widgets.Dropdown(options=[("Índice", "index"), ("Crecimiento anual", "growth"), ("Nivel por país", "level")], value="index", description="Medida")
years = widgets.IntRangeSlider(value=[1990, 2023], min=1960, max=2025, description="Años", continuous_update=False)
base_year = widgets.IntSlider(value=2008, min=1960, max=2023, description="Base", continuous_update=False)
out = widgets.Output()
def render(*_):
    with out:
        clear_output(wait=True)
        if not series.value:
            return
        print("Unidad almacenada:", df.filter((pl.col("source") == source.value) & (pl.col("series") == series.value))["unit"].unique().to_list())
        try:
            explorer(df, source.value, series.value, mode.value, *years.value, base_year.value).show(renderer="plotly_mimetype")
        except ValueError as error:
            print(error)
def update_series(*_):
    options = sorted(df.filter(pl.col("source") == source.value)["series"].unique().to_list())
    series.options = options
    series.value = "q_gdp" if "q_gdp" in options else options[0]
    render()
source.observe(update_series, names="value")
for control in [series, mode, years, base_year]:
    control.observe(render, names="value")
update_series()
display(widgets.VBox([source, series, mode, years, base_year, out]))
'''),md('''## 4. Diferencias entre fuentes

Se comparan tasas de crecimiento del PIB real durante 1990–2023, no niveles de monedas distintas. La referencia WDI no se considera verdad observada. Diferencias entre ediciones y ajustes metodológicos pueden explicar divergencias; el acuerdo entre fuentes también puede proceder de inputs comunes.'''),code('''cross = cross_sources(df)
summary = cross.group_by(["country", "source"]).agg(
    pl.len().alias("n"),
    pl.col("difference_pp").abs().mean().alias("mean_abs_difference_pp"),
    pl.col("difference_pp").abs().max().alias("max_abs_difference_pp")
).sort(["country", "source"])
display(summary)
display(cross.sort(pl.col("difference_pp").abs(), descending=True).head(12))
'''),md('''## 5. Saltos e identidades

Se marcan crecimientos de magnitud superior al 15 % o desviaciones robustas superiores a seis, calculadas con mediana y MAD de la serie. Es un cribado descriptivo: las crisis y rebotes pueden ser auténticos. No se elimina ni corrige ninguna observación.

La identidad de demanda se comprueba a precios corrientes. No se exige aditividad a los volúmenes encadenados.'''),code('''events = shocks(df)
display(events)
residuals = demand_residuals(frozen)
display(residuals.filter(pl.col("year").is_between(1990, 2023)).group_by("country").agg(
    pl.col("nominal_residual_pct_gdp").abs().max().alias("max_abs_residual_pct_gdp")
))
'''),md('''## 6. Resultados de la exploración

Los productos EDA se escriben en un directorio separado por versión. No sustituyen los archivos congelados. La numeración del informe se pospone: se conservará el identificador del profesor, con sufijos de país como `2.B.1-CHN` y `2.B.1-ESP`, o paneles dentro de una misma figura.'''),code('''result = build(VERSION, root)
print(result)
display(Markdown((Path(result["output"]) / "HALLAZGOS.md").read_text()))
''')]
nb=dict(nbformat=4,nbformat_minor=5,metadata=dict(kernelspec=dict(display_name='Python (coyuntura EDA)',language='python',name='coyuntura-eda'),language_info=dict(name='python',version='3.14')),
        cells=[dict(c, id=f'eda-{i:03d}') for i,c in enumerate(cells)])
folder=ROOT/'notebooks';folder.mkdir(exist_ok=True)
(folder/'01_eda.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n')
print(folder/'01_eda.ipynb')
