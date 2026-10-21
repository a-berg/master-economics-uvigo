# Reconciliación de las anotaciones y actualización de España

20/10/2026, tras recibir el CSV anotado por el alumno.

El problema del inventario anterior era de extracción y clasificación: ausencia de identificador escrito en una fila se estaba tratando como ausencia de correspondencia. Se ha reemplazado ese criterio por búsqueda en todo AMECO, lectura de `Source`, conservación de referencias y clasificación explícita de cálculos y duplicados.

## Resultado integrado

La tabla larga `datos/silver/espana.parquet` contiene **5.599 observaciones de 97 series**, sin duplicados de serie/año. La vista anual tiene 97 columnas de series, además de país y año; el rango total es 1950–2025, con coberturas distintas y nulos. Las previsiones de AMECO se mantienen solo en la tabla larga.

| Origen | Series integradas |
|---|---:|
| AMECO vigente: 74 identificadores explícitos y diez hallados por concepto | 84 |
| INE/EPA: activos, ocupados y parados | 3 |
| PWT 11: empleo y horas medias | 2 |
| INE/cuentas integradas: cinco niveles publicados y VAB derivado | 6 |
| Eurostat: sueldos y salarios D11, cotizaciones D12 | 2 |
| Total | 97 |

No se promete una única edición homogénea para fuentes distintas. Los datos INE ya descargados se integran conservando su edición y hash; no se presentan como última revisión 2026 sin comprobarlo. Las identidades de producción se calculan dentro de la misma descarga INE, no mezclando el PIB AMECO con el consumo intermedio INE.

## Las diez series AMECO recuperadas

| Fila del Excel | Concepto confirmado | Código seleccionado |
|---|---|---|
| REAL!43 | VAB real de manufacturas | ESP.1.1.0.0.OVGM |
| REAL!44 | VAB real total | ESP.1.1.0.0.OVG0 |
| REAL!45 | VAB real agricultura | ESP.1.1.0.0.OVG1 |
| REAL!46 | VAB real industria sin construcción | ESP.1.1.0.0.OVG2 |
| REAL!48 | VAB real construcción | ESP.1.1.0.0.OVG4 |
| REAL!49 | VAB real servicios | ESP.1.1.0.0.OVG5 |
| NOMINAL!7 | FBCF nominal gobierno | ESP.1.0.0.0.UIGG |
| NOMINAL!8 | FBCF nominal sector privado | ESP.1.0.0.0.UIGP |
| NOMINAL!22 | Consumo de capital fijo nominal gobierno | ESP.1.0.0.0.UKCG |
| NOMINAL!24 | Excedente ajustado por remuneración imputada de autónomos | ESP.1.0.0.0.UQGD |

Las dos correcciones conceptuales de las notas se conservan junto al texto original del alumno:

- `OKCT` es real y total economía; para el título nominal del gobierno de NOMINAL!22 corresponde `UKCG`.
- Los alias breves Private/Government de las filas 7/8 contradicen los títulos largos. Se sigue el título y el agregado: 7 gobierno, 8 privado.

Para UQGD se selecciona la variante `EURO-ESP`, coherente con la unidad de la fila. La variante `ESP.1.0.99.0.UQGD` anotada también existe, pero usa ECU/EUR: no se confunden las valoraciones históricas anteriores a 1999. El catálogo deja la alternativa explícita.

El archivo `datos/catalogo/ameco_completo.csv/parquet` contiene 35.173 entradas (35.013 códigos únicos) de toda la edición, con capítulo y miembro del ZIP. Algunos códigos aparecen en varios capítulos; no se impone un único subcapítulo artificial. La extracción de valores comprueba que las repeticiones de los códigos seleccionados no tengan valores/unidades incompatibles.

Ejemplo de búsqueda Python equivalente a la realizada por el alumno con nushell:

```python
from ameco_full_catalogue import search
search(r'(?:capital consumption|consumption of fixed capital).*current prices')
```

## Anotaciones, fuentes y granularidad

Se han preservado las **56 filas del CSV anotado** como original con hash. El archivo contiene UTF-8 y algunas notas Windows-1252: se mantiene el original byte a byte y se normaliza únicamente la lectura. `filas_reconciliadas.csv` añade las 13 filas de producción que no estaban en aquella versión del inventario: 69 filas clasificadas en total. Son filas de referencia, no 69 datasets independientes.

- Las nueve filas marcadas «Ignorar» dejan de considerarse inputs independientes.
- Las siete referencias/duplicados AMECO apuntan a su serie canónica, sin generar columnas nuevas.
- Los multiplicadores M1/BM, M2/BM y M3/BM se identifican como derivados.
- Las celdas de `Source` y sus hipervínculos se preservan en `excel_hoja_source.json`, con fila de origen.
- Para población, `Source!73–85` enlaza defunciones por residencia, nacimientos por inscripción y matrimonios de diferente sexo. Las fuentes ya están identificadas; sus descargas y selección siguen pendientes.
- Para trabajo, `Source!41–69` distingue paro registrado SEPE/INEM, EPA y salario mínimo del Ministerio. EPA no sustituye automáticamente al paro registrado. Los periodos históricos de origen incierto siguen identificados como tales.
- `Source!35` y `mercado traballo!21` dicen PWT 10.0/100; para el proyecto se adopta PWT 11 como ya estaba acordado, sin atribuir 11 al original.

### Empresas

El lector anterior reutilizaba el encabezado anual anterior al encontrar `1990Q1`, lo que desplazaba años y coberturas. Ahora reconoce el encabezado trimestral y preserva los periodos reales. Las filas de detalle tienen 59 trimestres, 1990Q1–2004Q3, no los años que figuraban en el inventario defectuoso.

Las cuatro filas de agregados anuales (23, 24, 25 y 51) contienen 14 años completos, 1990–2003. Se han contrastado **56 agregados** con sus cuatro trimestres: todos coinciden exactamente. El año parcial 2004 no se completa ni se confunde con un año entero. La fila 50 tiene su propia cobertura; no se fuerza a la del total.

`excel_empresas_periodos.parquet` conserva los valores con su periodo y fila de origen; `excel_empresas_comprobacion_anual.csv` contiene las verificaciones. Son evidencia del Excel, no nuevas descargas oficiales. Los enlaces de suspensiones, declaraciones de quiebra y empresas concursadas en `Source!88–102` permiten seguir el trabajo sin confundir los conceptos históricos con el procedimiento concursal moderno.

## AMGE, AXGE y la edición del Excel

AMGE y AXGE pasan a `EXCLUIDA_NO_PUBLICADA_EDICION_ACTUAL`, sin bloquear el cierre de AMECO. La fecha exacta de retirada no se ha certificado. La búsqueda en el archivo oficial **Autumn 2021** tampoco encuentra esos dos códigos; el resultado está en `ameco_series_excluidas.json`. Esto es más limitado que afirmar una retirada posterior a 2021.

La nota `Source!128` mezcla «Autumn 2021 Economic Forecast» con «15/11/2023», mientras otras hojas contienen actualizaciones posteriores. Se preserva la nota como indicio de procedencia, no como prueba de que todo el libro sea una sola edición 2021.

El enlace compartido de Google no se pudo leer. Para la comprobación se descargó el archivo oficial 2021 desde el archivo de AMECO, conservando URL y hash. Fuente: https://economy-finance.ec.europa.eu/economic-research-and-databases/economic-databases/ameco-database/ameco-archive_en.

## Pendiente real

Las fuentes están identificadas para población, paro registrado, SMI y empresas; falta completar sus descargas, selecciones y coberturas. En dinero sigue pendiente acreditar la descarga histórica y resolver la continuidad monetaria; los cocientes no requieren otra descarga. Para tipo de cambio está identificado `PA.NUS.FCRF`, pero deben mantenerse explícitas peseta/EUR y España/zona euro.

El bloque de otros impuestos netos sobre producción necesita selección específica; conocer el enlace de las cuentas no significa haber integrado todos sus conceptos. Las versiones antiguas de fuentes ya descargadas tampoco sustituyen una revisión de actualidad.

## Reproducción de esta fase

```sh
uv run python src/ameco_full_catalogue.py
uv run python src/reconcile_annotations.py
uv run python src/audit_ameco_retired.py
uv run python src/spain_silver.py
uv run --group analysis python src/verify_spain.py
```

La reconciliación reutiliza la copia original anotada archivada en bronze. No modifica el CSV del alumno. El notebook 02 incluye la búsqueda por concepto, la clasificación reconciliada y la verificación de los agregados de empresas.
