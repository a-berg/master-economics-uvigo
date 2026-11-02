# Búsqueda dirigida de existencias reales — 02/11/2026

## Resultado

**Se ha localizado una candidata real de China para 1980–2019: FMI/IFS vía FRED, `NINVRXDCCNA`, “Real Changes in Inventories for China”.** No se acepta todavía como equivalente a OIST: la ficha pública no explicita año de referencia, multiplicador monetario ni código contable que permita acreditar la inclusión/exclusión de objetos valiosos.

La búsqueda se hizo en el orden solicitado: primero P.52+P.53, después P.52. Se archivan candidatos y evidencia en esta carpeta, separados de la silver aceptada. El estado `NO_RECUPERADA` del inventario del 21/10 debe leerse ahora junto a este suplemento: **hay candidata real localizada, pero no equivalencia acreditada**. No se modificó `contratos.csv`, que tiene un archivo de bloqueo de LibreOffice activo durante esta revisión.

## 1. P.52+P.53: resultado OCDE

Se obtuvo la estructura oficial de `OECD.SDD.NAD / DSD_NAMAIN10@DF_TABLE1_EXPENDITURE / 2.0`. El código que corresponde al agregado buscado es **P5M**, definido como cambios de existencias y adquisiciones menos cesiones de objetos valiosos.

La consulta anual de China devuelve 275 observaciones: cinco variantes monetarias de 55 años, **1970–2024**. Sin embargo, todas tienen valoración `V` o `VQ`:

- `V`: precios corrientes.
- `VQ`: precios corrientes con conversor constante; NO precios constantes.
- Los códigos de volumen definidos en la propia estructura son, entre otros, `L` (volumen encadenado) y `Q` (precios constantes). No aparecen en la respuesta de esta consulta china.

La variante `XDC / V` está expresada en **millones de CNY** (`UNIT_MULT=6`, `CURRENCY=CNY`). Es un agregado nominal útil como referencia, pero no resuelve `inventories_real`. Las variantes USD con PPA o cambio constante tampoco se transforman en reales por fijar el conversor monetario.

[Consulta oficial P5M](https://sdmx.oecd.org/public/rest/v1/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_EXPENDITURE,2.0/A.CHN...P5M.......?format=csvfile).

## 2. P.52 por separado

### OCDE

La consulta del código `P52` devuelve otras 275 observaciones con las mismas cinco variantes y el mismo periodo. De nuevo son `V` y `VQ`, sin volumen real. P52 y P5M nominales en moneda nacional coinciden numéricamente en los 55 años; `oecd_combined_vs_p52.csv` registra la comprobación. **Esa coincidencia no prueba que los objetos valiosos hayan sido medidos separadamente y sean cero.** Tampoco permite reconstruir un agregado real.

[Consulta oficial P52](https://sdmx.oecd.org/public/rest/v1/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE1_EXPENDITURE,2.0/A.CHN...P52.......?format=csvfile).

### FMI/IFS vía FRED: candidata nueva

La [tabla oficial de FRED](https://fred.stlouisfed.org/data/NINVRXDCCNA) publica **40 observaciones anuales consecutivas, 1980–2019**, atribuidas a International Monetary Fund / International Financial Statistics. Se identifica como real y no desestacionalizada. La última actualización de los valores indicada por la tabla es **22/06/2021**; una fecha futura de publicación del conjunto IFS no significa que esta serie tenga observaciones nuevas.

Su unidad pública es únicamente `Domestic Currency`. No se supone que las cifras estén en yuanes, millones o miles de millones sin acreditar el multiplicador; tampoco se asigna una base 2015 o 2020. Por ejemplo, los valores originales publicados son 785627.905080997 en 2015 y 580944.206221771 en 2019. Se conservan sin convertirlos.

La descripción se corresponde por título con variación de existencias, pero FRED no muestra aquí un código SNA P52 ni información suficiente para certificar el tratamiento de objetos valiosos. Por ello se registra como **P52-like**, sin afirmar equivalencia exacta ni adoptar la cobertura más amplia de España.

Las descargas directas HTML/CSV con Python agotaron el tiempo de espera. La tabla sí fue accesible mediante la herramienta web. Se preservaron sus 40 cifras y metadatos como **extracción estructurada de la tabla primaria**, con URL, fecha, método y hash. El manifiesto declara expresamente que ese archivo no son los bytes HTML originales. No se presenta una transcripción como descarga CSV del proveedor.

El origen declarado es FMI; la cadena desde estadísticas nacionales o estimaciones hasta IFS queda pendiente de documentar por serie. Distribución FRED no significa medición independiente.

### World Bank

Se repitió la consulta de `NE.GDI.STKB.KN` para China con `source=2`: devuelve cero valores no nulos. Se conserva la respuesta nueva. No demuestra que nunca hubiera datos en ediciones históricas ni que no existan en otra fuente.

## Decisión y siguiente comprobación

| Necesidad | Decisión actual |
|---|---|
| P52+P53 en volumen | No recuperada en la consulta OCDE revisada; solo nominales. |
| P52 en volumen | Candidata FMI/FRED localizada para 1980–2019; base, multiplicador y alcance contable pendientes. |
| P52/P52+P53 nominal | OCDE recuperada para 1970–2024; conserva unidades y flags. No sustituye la magnitud real. |

El siguiente paso para aceptar la candidata es obtener metadatos originales IFS que acrediten base de precios, escala, método y tratamiento de objetos valiosos. Aun aceptándola como alternativa P52, **no cubre 1960–1979 ni 2020–2023**. No se prolonga con nominales, con un deflactor del PIB ni con la diferencia de componentes reales PWT sin validar aditividad y bases.

La tabla española OIST (P52+P53, miles de millones EUR de 2020) sigue intacta. Tampoco se modificaron la silver china principal ni las decisiones de aceptación previas.

## Archivos y reproducción

- `candidate_summary.csv`: resultado por variante, cobertura y reserva metodológica.
- `inventories_candidates.csv/parquet`: 550 observaciones OCDE nominales y 40 cifras de la candidata real FRED; todas con `accepted_for_inventories_real=false`.
- `oecd_codes.csv`: definiciones extraídas de la estructura oficial, incluido VQ.
- `oecd_combined_vs_p52.csv`: contraste nominal del agregado frente a P52.
- `provenance.json`: URL, fechas, hashes y método de adquisición/extracción.
- `acquisition*.json`: resultados de las solicitudes, incluidos timeouts.
- `verification.json`: integridad, dimensiones, número de observaciones y exclusiones.

Normalización y comprobación sin red:

```sh
uv run --offline python src/review_china_inventories.py
```

Las consultas de red son `src/search_china_inventories.py --stage initial`, `--stage combined` y `--stage p52`. La extracción FRED ya archivada se verifica por hash al reconstruir; no se vuelve a inventar desde un script ni se confunde con una descarga HTTP.
