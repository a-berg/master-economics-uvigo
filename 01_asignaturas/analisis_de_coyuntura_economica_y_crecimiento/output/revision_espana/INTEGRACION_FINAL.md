# Integración de España — 21/10/2026

Se completa la integración pendiente: 26 series y 835 observaciones nuevas. Total: 123 series, 6.434 observaciones en `datos/silver/espana.parquet` y 125 entradas de catálogo (incluye dos códigos AMECO excluidos). La vista `espana_anual.parquet/csv` contiene 123 series y 80 años, 1946–2025; los nulos representan ausencia de cobertura. No es un panel equilibrado.

## Archivos de trabajo

- `datos/silver/espana.parquet/csv`: valores, unidad, fuente, código, hash y estado por observación.
- `datos/silver/espana_anual.parquet/csv`: vista ancha para análisis, sin previsiones ni el periodo parcial de concursos 2004.
- `output/revision_espana/catalogo_espana.csv`: definición, código, unidad, cobertura, decisión y URL por serie. `avh` es el número medio anual de horas trabajadas por persona ocupada; `emp` son millones de personas ocupadas (PWT).
- `output/revision_espana/filas_reconciliadas.csv`: correspondencia del inventario sin código con `silver_reference` e `integration_status`; las anotaciones originales no se sustituyen.
- `datos/silver/espana_periodos.parquet`: 2.544 observaciones mensuales y trimestrales; `periodos_completos_anualizacion.csv` registra inclusiones y exclusiones.
- `datos/catalogo/fuentes_recuperadas_espana.json`: manifiestos de los originales empleados, con URL, fecha de consulta, artefacto y SHA-256. SEPE conserva el archivo de procedencia por observación.
- `notebooks/03_integracion_espana.ipynb`: cobertura y exploración de los nuevos datos, con salidas guardadas.

## Límites que siguen abiertos

| Bloque | Disponible | Límite |
|---|---|---|
| EPA actual | 2006–2025 | Histórico anterior sin reconstruir; no se rellena con paro registrado. |
| Paro registrado | 2001–2025, medias de 12 meses | Falta 1981–2000; reconstrucciones SISPE y errores de campos de año del original documentados. |
| Defunciones | Residencia 1975–2024; inscripción 1960–1974 | Universos diferentes: dos series separadas. |
| Nacimientos / matrimonios | Inscripción / matrimonios de diferente sexo | No cambiar el universo por el nombre abreviado del Excel. |
| Quiebras y suspensiones | 1990–2003 anual; hasta 2004Q3 trimestral | Faltan 1985–1989; 2004 incompleto. Detalle empresarial adicional archivado. |
| Concursos | 2004–2020 | 2004 solo últimos cuatro meses, excluido de vista analítica; régimen distinto del histórico. |
| Otros impuestos netos producción | 1995–2022 | Cobertura de la tabla descargada; no prolongar automáticamente a 2024. |
| Dinero IMF/IFS vía FRED | M1/M2/M3: 1962–1998 | Alternativa documentada, no equivalencia acreditada de MOISEES. Medias y diciembre separados; pesetas. |
| Dinero histórico BdE | BM/M3 y M3/BM: cierres 1962–1997 | 1998 es octubre. Falta 1999–2001 y equivalencia exacta de MOISEES. No calcular M1/BM o M2/BM mezclando medias y cierres. |

SMI: cuantía mensual legal en 14 pagas, con media anual y diciembre separados. No equivale a salario observado. No se crea media 1980 sin enero–mayo. La retroactividad de 2023 se apoya en el BOE, con evidencia en `smi_effective_dates.csv`. El manifiesto conserva la excepción de transporte: el archivo público MITES se recuperó sin poder verificar el certificado TLS; se comprobó firma Excel y se contrastaron importes con BOE. Esta excepción no se aplica a las demás descargas.

Los errores de año en los archivos SEPE se registran en `source_anomalies.csv`: la secuencia mensual y al menos un campo de año respaldan cada corrección. Se conservan los bytes originales. Los scripts de investigación originales están en `src/adquisicion_historica/`; se ejecutaron desde el directorio padre y pueden hacer peticiones de red. No son necesarios para reconstruir los datos ya archivados. Los intentos fallidos o respuestas HTML de URLs candidatas no se usan como series.

## Reproducción desde originales archivados

Desde la raíz `trabajo_china`, sin nuevas descargas:

```sh
uv sync --locked --group analysis
uv run python src/spain_missing.py
uv run python src/spain_silver.py
uv run --group analysis python src/verify_spain_recovered.py
uv run --group analysis python src/verify_spain.py
```

Controles superados: selección por códigos y dimensiones, hashes de los originales, ausencia de duplicados y valores no finitos, 422 reconstrucciones independientes de anualizaciones, identidades EPA y producción, 56 agregados del Excel, exclusión de previsiones y parcial 2004, notebook de revisión previo y snapshot v0 inalterado. Resultado legible por máquina: `verificacion_integracion.json`.

Esta entrega cierra la integración de las fuentes recuperadas para España. Los límites anteriores permanecen explícitos; no certifica que todo el histórico del Excel esté reproducido ni completa todavía China o el informe final.
