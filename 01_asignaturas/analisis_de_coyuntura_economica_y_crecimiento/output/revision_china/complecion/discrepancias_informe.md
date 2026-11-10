# Datos utilizables y diferencias para el informe

Actualización de 02/11/2026. La estrategia se ha ejecutado buscando primero el concepto solicitado y después una alternativa útil. Se añaden **29 series y 934 observaciones**: la vista ampliada reúne **165 series y 8.448 observaciones**. Los 38 conceptos tienen una selección: 37 cuentan con datos numéricos y el restante es la matriz input-output. Esto no equivale a un panel completo ni a 38 equivalencias exactas.

## Qué utilizar

| Necesidad | Selección | Cobertura | Diferencia que debe aparecer en el informe |
|---|---|---|---|
| Existencias reales | Índice FMI/IFS vía FRED, 2008=100 | 1980–2019 | España incluye P52+P53; la inclusión de objetos valiosos en China no está acreditada. Sirve para evolución, no para comparar niveles monetarios. |
| CCF real | Estimación con detalle de capital PWT, índice 2021=100 | 1952–2023 | CCF nominal por activo dividido por precios del stock: aproximación propia, no serie oficial de CCF en volumen. |
| Remuneración | D1 OCDE | 1992–2023 | Tratamiento nacional de trabajadores por cuenta propia potencialmente distinto; no sustituir por `labsh × PIB`. |
| Excedente bruto | B2A3G OCDE | 1992–2021 | Incluye renta mixta. El residuo calculado con el PIB disponible es otra serie, 1992–2023, y no se empalma con la publicada. |
| Impuestos | Serie D2 OCDE interpretada como neta | 1992–2023 | Coincide en 2023 con los impuestos **netos** NBS. No se ha recuperado D2 bruto separado de D3. |
| Subvenciones | Gasto NBS en subvenciones a precios | 1978, 1980, 1985 y 1990–2006 | Categoría fiscal parcial; puede incluir ayudas a consumidores. No equivale a D3 de toda la economía. |
| Subvenciones recientes | Estimación FMI: 2% del PIB | 2023 | Subvenciones monetarias a empresas no financieras, estimadas a partir de cotizadas; dato puntual separado del histórico NBS. |
| PIB a coste de factores | PIB OCDE menos serie tributaria anterior | 1992–2023 | Aproximación condicionada a interpretar los tributos como netos. No sumar además subvenciones FMI/NBS. |
| Producción e intermedios | Tabla IO NBS | 2023 | Precios de productor. Escala monetaria inferida por coincidencia con D1 de la tabla de flujos de fondos; cocientes disponibles sin esa hipótesis. |
| Input-output | Coeficientes técnicos 3×3 NBS | 2023 | Cada flujo se divide por la producción bruta del sector usuario. No son porcentajes sobre el total de consumos intermedios. |
| C, G, inversión, X y M reales | Índices PWT NA, 2008=100 | 1952–2023 | Válidos para evolución. No sumar componentes encadenados ni comparar directamente sus niveles con euros de 2020. |
| FBCF real | Índice PWT NA, 2008=100 | 1970–2023 | Mismo criterio; mantener diferenciada de inversión total. |

Para el mercado laboral, se mantienen las alternativas previas: paro registrado urbano NBS, encuesta nacional vía OIT y estimaciones modelizadas OIT en series separadas. Sus coberturas se consultan en `seleccion_conceptos.csv`.

## Tres decisiones que afectan al análisis

**Rentas.** Los componentes OCDE no cierran exactamente con el PIB de la descarga. La diferencia máxima equivale al 2,19% del PIB en el periodo compartido. Se muestra como discrepancia, sin convertirla en subvenciones ni ajustar el excedente publicado. Para comparar estructura de rentas conviene presentar cuotas del PIB con una nota de alcance; para una identidad contable exacta, utilizar una sola tabla y su discrepancia explícita. [Datos y códigos OCDE](https://sdmx.oecd.org/public/rest/v1/dataflow/OECD.SDD.NAD/DSD_NAMAIN10@DF_TABLE1/2.0?references=all).

**CCF.** La fórmula de trabajo es `Σ(Dc_activo / Np_activo)`, normalizada a 2021=100. Se conservan cuatro grupos de activos y la sensibilidad usando `Ip` en lugar de `Np`. La diferencia máxima entre ambos índices es 10,78% en toda la historia: es sensibilidad a una decisión metodológica, no un intervalo de confianza. PWT construye estas magnitudes mediante estimaciones de capital; ninguna es una medición independiente del CCF chino. El cociente nominal CCF/PIB de PWT y el CCF/RNB de WDI quedan como referencias adicionales, con denominadores y métodos distintos. [PWT 11](https://www.rug.nl/ggdc/productivity/pwt/).

**Subvenciones.** El histórico de precios NBS permite describir una política concreta y su evolución, pero no calcular D3 total. El cambio de registro de ingreso negativo a gasto en 1986 se conserva; los años sin observación quedan vacíos. No se enlaza con la estimación FMI de 2023. [Tabla NBS 8-9](https://www.stats.gov.cn/sj/ndsj/2007/html/H0809e.htm), [investigación FMI 2025/155](https://www.elibrary.imf.org/abstract/journals/001/2025/155/article-A001-en.xml).

Texto breve reutilizable en el informe:

> Ante la falta de algunas series plenamente comparables, se emplean alternativas explícitas: índices para la demanda y las existencias reales, una aproximación del consumo de capital fijo con datos PWT y agregados de rentas que pueden incluir renta mixta o impuestos netos. Las subvenciones se estudian con una serie fiscal parcial. Estas diferencias limitan la comparación de niveles y el cierre de identidades, pero permiten analizar evolución y estructura sin completar artificialmente los años ausentes.

## Archivos de trabajo y reproducción

- `datos/silver/china_completada.parquet` y `.csv`: entrega original más suplemento, con unidades, estados y trazabilidad.
- `datos/silver/china_completada_anual.parquet/csv`: vista ancha de series utilizables, incluidas aproximaciones identificadas por sus códigos.
- `datos/silver/china_seleccion.parquet/csv` y `china_seleccion_anual.csv`: una elección por concepto. **Las columnas tienen unidades diferentes**, detalladas en el mapa de selección.
- `seleccion_conceptos.csv`: selección efectiva, cobertura, unidad, uso y estado anterior. Las anotaciones originales de `../contratos.csv` permanecen intactas.
- `catalogo_suplemento.csv`, `provenance.json`, `acquisition_*.json`: definiciones, fórmulas, originales, URLs, instantes UTC, hashes y consultas fallidas.
- `notebooks/05_china_alternativas.ipynb`: exploración ejecutada con cinco figuras, incluida la sensibilidad del CCF.

```sh
uv run --offline python src/china_complete.py
uv run --offline --group analysis python src/create_china_complete_notebook.py
uv run --offline --group analysis python src/verify_china_complete.py
```

Estos comandos leen la entrega anterior; no regeneran sus contratos ni sobreescriben España. Los originales anteriores y v0 se comprueban mediante hashes.

## Bloqueos reales y criterio de cierre

Se consultó la tabla 1 completa de OCDE para China: no hay P51C ni D3 en la respuesta archivada; esto describe esa consulta, no una inexistencia universal. La tabla 6 devolvió 404 en las versiones probadas, aunque su estructura 1.0 fue accesible. WDI no devolvió CCF en moneda local ni subvenciones chinas en los códigos consultados; CCF/RNB sí tiene 1970–2021. Las notas NBS de 2025 devolvieron 404 y se archivó la edición 2020.

Se localizó el [Excel del capítulo 3 del WEO de octubre de 2025](https://www.imf.org/-/media/files/publications/weo/2025/october/data/ch3data.xlsx), que acompaña el análisis de política industrial china. Las rutas PDF/XLSX y las variantes oficiales de descarga devolvieron 403, también con cabeceras de navegador. La cifra FMI 2023 se conserva como **extracción estructurada del texto publicado**, con manifiesto propio; no se afirma haber descargado ese Excel ni se digitaliza la gráfica para inventar una precisión anual.

Se cierra esta ronda con una alternativa documentada para cada hueco. Quedan sin equivalencia exacta D3 y D2 bruto por separado, y sin histórico anual reciente de subvenciones incorporado. Recuperar el Excel FMI mejoraría esa alternativa, pero no resolvería por sí solo la equivalencia con D3.
