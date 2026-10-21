# Análisis de coyuntura de China y España

Pipeline de datos para el informe del máster. El Excel del profesor se conserva como referencia documental. Las cifras nuevas se obtienen desde fuentes oficiales y desde PWT 11.0.

## Estado vigente: integración de España (21/10/2026)

La silver contiene **123 series y 6.434 observaciones**; se han integrado las 26 series recuperadas. La vista analítica excluye previsiones AMECO y el periodo parcial de concursos de 2004. Las coberturas varían entre series: 1946–2025 es el rango conjunto, no un panel completo.

La entrega y reproducción vigente se describen en [INTEGRACION_FINAL.md](output/revision_espana/INTEGRACION_FINAL.md). El [catálogo](output/revision_espana/catalogo_espana.csv) identifica cada serie y su procedencia; [filas_reconciliadas.csv](output/revision_espana/filas_reconciliadas.csv) conecta las filas sin código del Excel con silver, conserva tus notas y distingue equivalencias de alternativas. AMGE/AXGE permanecen excluidas.

El notebook [03_integracion_espana.ipynb](notebooks/03_integracion_espana.ipynb) permite explorar la cobertura y las nuevas series. El notebook 02 conserva el contraste histórico de las ediciones AMECO y sus 31 figuras. Las instrucciones siguientes corresponden al pipeline inicial; para reconstruir esta fase utiliza las del documento de integración.

## Ejecución

```sh
uv sync --locked
uv run python src/pipeline.py all
uv run python src/pipeline.py build
uv run python src/pipeline.py download --refresh
uv run python src/verify.py
```

`all` audita el Excel, importa los archivos originales, descarga, normaliza y genera tablas y figuras. `build` trabaja sin red sobre las descargas existentes. `download` reutiliza los bytes verificados por SHA-256; `--refresh` crea una nueva instantánea. Un fallo de descarga produce estado explícito y salida 2 de `all`, aunque se generen resultados parciales. No se mezclan automáticamente versiones de un mismo proveedor.

## Estructura

- `datos/bronze/`: originales y manifiestos JSON. Cada descarga tiene instante UTC, URL, parámetros, hash y fecha de actualización si el proveedor la entrega. Las instantáneas anteriores permanecen. `latest.json` es un puntero mutable.
- `datos/silver/observations.parquet`: observaciones en formato largo, con país, año, serie, valor, unidad original, dimensiones, flags y hash de bronze. Las unidades de PWT se resuelven con sus leyendas preservadas; no asumir que todas son iguales.
- `datos/gold/`: cobertura, panel común PWT, contabilidad de crecimiento, estadísticos cíclicos, estado de descargas y de requisitos.
- `datos/catalogo/`: descargas, requisitos y parámetros analíticos.
- `output/figuras/`: figuras SVG para Typst y PNG para inspección.
- `entregas/`: borrador del informe y bibliografía. El informe sigue siendo un borrador, con requisitos pendientes identificados.

Los archivos antiguos de `datos/` no se eliminan ni se renombran. Su importación no inventa una fecha de consulta ni una URL desconocidas. La fecha del archivo no se trata como fecha de descarga.

## Criterios económicos

Eurostat proporciona una base oficial para España. PWT ofrece una base común para comparaciones con China y una versión coherente de PIB, stock de capital y empleo para contabilidad del crecimiento. Ambas bases se mantienen identificadas: no se empalman silenciosamente. PWT NA permite estudiar componentes de demanda reales sin aplicar a todos el deflactor del PIB.

`rgdpna` y `rnna` se emplean en crecimiento y contabilidad; `rgdpe/pop`, en la comparación internacional de niveles por habitante. La productividad con `rgdpna` es una magnitud a precios nacionales constantes y no una medida directa de diferencias de bienestar entre países. El residuo de Solow recoge todo lo no explicado por los inputs incluidos, no solamente tecnología.

Las contribuciones se calculan con diferencias logarítmicas anualizadas y alpha=1/3. Se presenta también CAGR, separadamente. Las correlaciones utilizan pares de años observados de las tasas anuales, desviación muestral y número de observaciones. Las tasas exigen años consecutivos y denominadores positivos. No se interpolan Gini ni otras series.

El informe final exige completar las fuentes y gráficos aún pendientes, revisar comparabilidad y añadir interpretación respaldada por datos y bibliografía. Los resultados generados no constituyen un informe terminado.

## Aplicación al repositorio original

Esta entrega se preparó en una copia porque el repositorio original era de solo lectura para la sesión. Puede inspeccionarse y ejecutarse de forma independiente. El paquete incluye los originales necesarios para reproducir el proceso.

Para incorporar los archivos a la carpeta original, revisar primero:

```sh
python aplicar_al_repositorio.py /ruta/a/la/asignatura
```

Para copiar después de esa comprobación:

```sh
python aplicar_al_repositorio.py /ruta/a/la/asignatura --apply
```

El script no elimina archivos. Rechaza sobrescrituras de archivos cambiados desde la captura original y respalda los que sustituye. La ejecución dentro de esta sesión solo realizó la comprobación; no copió al repositorio.

## Informe

```sh
typst compile --root . entregas/ensayo_final_ABerges.typ output/ensayo_final_ABerges.pdf
```

Se mantiene la dependencia de tu paquete local `@local/master-uvigo-templates:0.1.0` y la importación existente de Lilaq. El PDF se ha compilado y revisado visualmente. La bibliografía enlaza fuentes y conserva la edición consultada. `PENDIENTES.md` identifica expresamente lo que falta para una entrega académica completa.

## Versión inicial y exploración

La versión `v0_2026-10-16` contiene copias de silver, gold, catálogos y código de preparación, además de referencias y hashes de todos los originales bronze existentes. Se verifica también el manifiesto. No se sobrescribe: una futura revisión debe crear otro identificador. Esto fija los inputs y permite detectar cambios, pero no certifica ausencia de sesgos estadísticos.

```sh
uv sync --group analysis --locked
uv run --group analysis python src/snapshot.py verify v0_2026-10-16
uv run --group analysis python src/eda.py --version v0_2026-10-16
uv run --group analysis python src/verify_eda.py
```

Abrir `notebooks/01_eda.ipynb` en Jupyter o VS Code, seleccionar el Python de `.venv` y ejecutar las celdas. Para registrar un kernel local:

```sh
uv run --group analysis python -m ipykernel install --user --name coyuntura-eda --display-name 'Python (coyuntura EDA)'
```

La sesión de preparación no pudo arrancar un kernel Jupyter porque no permitía los sockets de comunicación. Las ocho celdas se ejecutaron y guardaron mediante IPython en proceso (`src/execute_notebook.py`); el notebook registra esa modalidad. Los controles interactivos requieren reejecutar con un kernel local. Como alternativa sin Jupyter, `output/eda/v0_2026-10-16/exploracion.html` contiene los gráficos interactivos con Plotly incluido, sin CDN ni conexión a datos externos.

La exploración se mantiene separada de la maquetación final con Lilaq. Las figuras del profesor conservarán su identificador, con sufijo de país si se separan, por ejemplo `2.B.1-CHN` y `2.B.1-ESP`; el catálogo reserva ese criterio sin cambiar aún las figuras del borrador.

La política de fuentes se registra en `datos/catalogo/source_policy.json`: descarga directa NBS solo como último recurso. La distribución por WDI/PWT no implica independencia de las estadísticas nacionales; revisar procedencia y método por serie.
