# China: entrega de datos y decisiones — 21/10/2026

Se entrega una silver reproducible y una decisión por necesidad. **No se acredita cobertura completa ni equivalencia íntegra con España.** El estado verificable y los recuentos vigentes están en `quality.json`; los huecos no se rellenan. El informe académico final queda fuera de esta fase de datos.

Resultado: **136 series y 7.514 observaciones** en la tabla larga; **90 series y 4.542 observaciones** en la vista analítica, y 46 cand   tes. Pasan 110 comprobaciones de manifiestos, 1.760 celdas WDI y 4.306 celdas PWT contrastadas con originales, 66 identidades demográficas, 37 laborales y los 40 controles de totales IO. `verification.json` confirma también v0 y el notebook ejecutado.

## Punto de partida y conservación

- Rama: `codex/china-series-audit`. No se encontró AGENTS.md en la asignatura ni en sus directorios ascendientes inspeccionados.
- España se reconstruyó desde sus originales mediante `spain_missing.py` y `spain_silver.py`: 123 series, 6.434 observaciones. Pasaron `verify_spain_recovered.py` y `verify_spain.py`, incluidas 422 anualizaciones independientes y la comprobación de v0. La única diferencia regenerada era el orden de categorías en un JSON y se restauró; la entrega española queda intacta.
- Se recuperaron del chat de referencia las instrucciones y la plantilla originales del profesor. Están en `datos/bronze/professor_instructions_20261021/`, con hash y procedencia; no se inventa una fecha histórica de descarga.
- Se revisaron las ocho páginas de instrucciones. El tema 7 exige 1960–2023, frente al periodo provisional 1990–2023 del análisis previo. La nueva descomposición cubre 1960–2023 sin alterar la configuración histórica ni v0. Los subperiodos propuestos son 1960–1989, 1989–2000, 2000–2008, 2008–2019 y 2019–2023; pueden reutilizarse en las tablas 6.3, 6.4 y 7.1.
- Los originales anteriores, `observations.parquet`, España y el snapshot v0 se conservan. No se incorporan a China los agregados ONU AMA: solo se consulta UN MADT 2.6.

## Entrega y uso

| Archivo | Contenido |
|---|---|
| `datos/silver/china.parquet` y `.csv` | Tabla larga con valores originales y derivados explícitos, unidades, estado, dimensiones, flags y hashes. Incluye candidatas en cuarentena. |
| `datos/silver/china_anual.parquet` y `.csv` | Vista ancha de series analíticas; excluye años 2026+ y magnitudes de escala/base pendiente. No es un panel equilibrado. |
| `catalogo_china.csv` | Definiciones del proveedor, cobertura, calidad, notas, URL, fecha y cadena de procedencia. |
| `contratos.csv` | 38 necesidades: definición, universo, unidad, valoración, frecuencia, periodo, candidata, cobertura y referencia española. |
| `correspondencias_espana_china.csv` | Las 125 entradas del catálogo español, incluidas las excluidas y las adicionales. Las reglas previas son índices de búsqueda, no equivalencias acreditadas. |
| `inventario_requisitos.csv` | Inputs reutilizados entre figuras y temas; evita contarlos como nuevas descargas. |
| `inventario_filas_excel_anotadas.csv` | Conserva las 69 filas sin código reconciliadas y las notas del usuario; no vuelve a clasificar duplicados como ausencias. |
| `existing_inventory.csv`, `wdi_inventory.csv`, `ilo_inventory.csv` | Auditoría de lo ya descargado, respuesta de cada indicador WDI y todas las dimensiones OIT. |
| `provenance.json`, `acquisition_*.json` | Artefactos, URL, fecha de consulta original, SHA-256 y resultados de adquisición, incluidos fallos. |
| `source_comparisons.csv` | Contrastes anuales con niveles originales, multiplicador de contraste, diferencias y reserva de independencia. |
| `io_2023_20_sectors.csv`, `io_2023_3_sectors.csv` | Matriz de productos 20×20 y agregación 3×3; escala nativa pendiente de documentación. |
| `notebooks/04_china.ipynb` | Notebook ejecutado, siete celdas de código y seis figuras guardadas; IPython en proceso, sin iniciar kernel Jupyter. |
| `quality.json` | Controles, recuentos y estados por contrato; no se reduce la calidad a una puntuación única. |

`analytic=true` permite exploración con las reservas del catálogo. **No significa equivalencia acreditada con España ni observación directa sin estimación.** No se comparan niveles en CNY con EUR. Los niveles PWT a precios nacionales sirven para crecimiento; bienestar exige PPA y población compatibles. Los índices PWT NA no son niveles de moneda nacional.

## Resultado de la búsqueda prioritaria

1. **World Bank:** se consultaron 41 códigos, con datos y metadatos por separado. En esta consulta hay valores para PIB, consumo nominal, inversión nominal, algunos volúmenes, población, precios, Gini y variables financieras/laborales. No hay valores chinos para G, FBCF, X, IM y existencias reales en los códigos consultados. MQMY y MONY no son aceptados como datos en source=2; DKAP.CN devuelve código inválido. Se preservan respuestas, sin convertirlas en series vacías pretendidamente observadas. Las respuestas por lotes inicialmente intentadas también se archivan; no alimentan la silver.
2. **PWT 11:** se releen los tres Excel originales (principal, NA y capital), no la silver antigua. El archivo principal proporciona PIB, capital, empleo y horas para el tramo largo. Los niveles NA/CAP de escala pendiente se mantienen en cuarentena. Los índices de precios de CAP tienen base pendiente; las cuotas de servicios de capital son adimensionales. Se generan índices 2008=100 de los volúmenes NA: una escala multiplicativa constante se cancela, pero sigue pendiente confirmar el alcance de inversión/FBC y hogares/ISFLSH.
3. **ILOSTAT:** las antiguas rutas webapps devuelven 404. El portal oficial identifica el servidor vigente rplumber, del que se archivan China anual y nueve diccionarios. Se seleccionan ambos sexos, edad `AGE_YTHADULT_YGE15`, sin segunda clasificación, separando cada fuente. El censo de 2000, las estimaciones oficiales históricas, la encuesta nacional y los modelos nunca se empalman. Los niveles modelizados son directos; no se multiplican activos WDI por otra edición de tasa de paro.
4. **UN MADT 2.6:** la consulta de China continental, código 156, grupo 206, ISIC Rev.4, devuelve cero registros con contador y mensaje explícito de ausencia. Se conserva el HTML nuevo y se limita la conclusión a esa consulta/variante. No se usa Hong Kong ni otra tabla ONU como sustitución.

El documento `BUSQUEDA_Y_BLOQUEOS.md` explica la evaluación previa a NBS, el recurso dirigido al anuario y la búsqueda ampliada.

## NBS y coherencia entre fuentes

Solo tras detectar los huecos se archivaron el índice del anuario 2025, la metodología y siete tablas. El formato de publicación accesible es JPG. Las cifras incorporadas se transcriben de forma explícita en `src/china_nbs_extract.py`, con tabla, fila conceptual, unidad, URL y hash. No se emplea OCR automático para aceptar valores.

La tabla 3-1 proporciona 47 años de PIB nominal para contraste. La diferencia relativa absoluta máxima respecto a WDI es aproximadamente **0,3631%**, con mediana cero. Bajo la hipótesis de que NA está en millones de CNY, el contraste con PWT NA tiene diferencia máxima aproximada **2,6725%**: se conserva como diagnóstico de escala y edición, sin corregir la serie. El documento NBS informa de revisiones históricas por el quinto censo económico. Eso hace plausible una explicación por revisión; **no demuestra por sí solo la causa de cada discrepancia**.

WDI identifica estadísticas nacionales, OCDE y estimaciones propias como posibles fuentes genéricas de cuentas nacionales; no determina la cadena china por año. PWT 11 sí documenta la adopción del PIB oficial chino. WDI laboral remite a OIT y WDI broad money a FMI. NBS monetario redistribuye PBC. La coincidencia entre esos canales no es validación independiente del productor nacional. No se infiere inflación estadística del PIB ni su ausencia.

M2 de NBS se contrasta con broad money WDI conservando nombres y reservas sobre definición/fecha. Las diferencias llegan aproximadamente a **5,5627%** y no se arreglan mediante un factor estimado. El anuario registra cambios de perímetro monetario; el método M1 cambió además en 2025. No se empalma M1 antiguo con nuevo, M2 con M3 ni dinero en circulación con base monetaria.

## Límites que permanecen abiertos

| Necesidad | Evidencia y decisión |
|---|---|
| Producción e intermedios anuales | ONU 2.6 sin registros en la consulta; NBS IO solo 2023, precios de productor y escala no explícita en JPG. Datos estructurales conservados, sin fabricar historia. |
| Tabla IO 3 sectores | Recuperada la matriz estructural de 2023 y agregada; filas oferentes, columnas usuarias. Industria incluye construcción. Escala monetaria pendiente; participaciones por columna sí son adimensionales. |
| CCF real y existencias reales | PWT CAP ofrece CCF nominal por activos; NBS aporta CCF y existencias nominales estructurales. No se usa el deflactor del PIB ni una resta de volúmenes encadenados. Falta serie/transformación acreditada. |
| Remuneración | NBS 2023, usos domésticos, una observación. Los recursos domésticos difieren por flujos con resto del mundo; no se sustituyen. La reconstrucción PWT anterior sigue siendo candidata y tiene años interpolados/constantes asumidos. |
| EBE, PIB coste factores, D2 y D3 separados | La tabla IO y los flujos de fondos incluyen excedente y tributos netos con valoraciones/universos específicos. No se fuerzan identidades de PIB a mercado ni se separan impuestos/subvenciones sin datos. |
| Empleo/horas | Base PWT coherente para crecimiento, con estimaciones; no equivalencia automática con EPA o cuentas nacionales españolas. |
| Paro registrado | NBS urbano 2020–2024; momento de referencia no explícito en esa fila. No equivale a media anual SEPE ni a encuesta nacional. |
| Encuesta de paro | Niveles ILO de encuesta nacional, 2016–2022, separados de censo, oficiales y modelos. No se prolonga con tasa urbana ni con otra fuente. |
| IPC y Gini | IPC WDI desde 1986. Gini publicado 1981–2022 en años concretos; falta acreditar concepto distributivo común por encuesta para comparar con España. No se interpola. |
| Complementos españoles | Dinero histórico, procedimientos concursales, SMI, impuestos desglosados y otras series adicionales no quedan acreditados por una similitud de título. Se mantienen abiertos en la matriz completa; no bloquean todos los gráficos del núcleo docente. |

## Reproducción sin red

Desde la raíz de esta asignatura:

```sh
uv sync --locked --group analysis
uv run --offline python src/china_silver.py
uv run --offline python src/china_quality.py
uv run --offline --group analysis python src/create_china_notebook.py
uv run --offline --group analysis python src/verify_china.py
```

Para adquisición nueva/caché verificada: `uv run python src/china_acquire.py priority`, después `nbs` y `expanded`, inspeccionando los contratos antes de acudir a NBS. La salida 2 indica fallos o códigos rechazados y queda registrada: no equivale a que toda la adquisición haya fallado. Los archivos existentes se reutilizan por hash y URL; no hay actualización silenciosa de edición.

El `.gitignore` local permite incluir exclusivamente los nuevos originales China, las instrucciones recuperadas y las tablas China, pese a las exclusiones generales bronze/silver del repositorio. No se ha publicado ni subido esta rama automáticamente.
