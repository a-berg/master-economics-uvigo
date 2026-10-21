# Revisión de equivalencias — 19 de octubre de 2026

Se ha contrastado el Excel del profesor con AMECO Spring 2026, revisado el detalle laboral de PWT 11 y comprobado la presencia de países en UN MADT 2.6. Esta revisión no certifica todavía una correspondencia completa España–China: distingue identidad de códigos, coincidencia numérica y compatibilidad conceptual. Las derivaciones nuevas siguen como candidatas, sin incorporarse automáticamente a silver.

## Excel y AMECO

80 códigos distintos de las diez hojas base: 76 de España y cuatro de Estados Unidos (referencias auxiliares). Se recuperaron 78: 74 españoles y cuatro estadounidenses. La comparación usa años comunes, sin rellenar huecos ni ajustar escalas. La tolerancia numérica es relativa 1e-10 y absoluta 1e-8. La edición descargada incluye previsiones; los años 2026–2027 no se deben presentar como observaciones realizadas.

| Resultado | Códigos |
|---|---:|
| ACEPTADA_COINCIDENCIA_NUMERICA | 37 |
| COMPATIBLE_CODIGO_DIFERENCIAS_PENDIENTES | 26 |
| PENDIENTE_BASE_PRECIOS_O_INDICE | 10 |
| PENDIENTE_CODIGO_NO_RECUPERADO | 2 |
| PENDIENTE_DISCREPANCIAS_NUMERICAS | 2 |
| PENDIENTE_UNIDADES | 3 |

`ESP.1.1.0.0.OITT`, `OCPH`, `OVGD`, `ESP.1.0.0.0.OIST` y `OKND` coinciden en los 66 años comunes, 1960–2025. Esto valida la reproducción de la referencia española, no la equivalencia con China.

Excepciones relevantes:

- La variante de capital `ESP.1.0.99.0.OKND` y varios índices usan bases distintas. La variante principal de capital sí coincide. Los índices pueden normalizarse a una base común; un cambio de referencia de volumen encadenado necesita una revisión adicional.
- `URTG` muestra una razón mediana nueva/original cercana a 0,0001 pese a declarar la misma unidad. `UUTG` añade una discrepancia de unidades. No se ha aplicado un factor corrector sin resolver la causa.
- `UVG4` presenta discrepancias numéricas que requieren revisar el VAB de construcción.
- No se recuperaron `AMGE` y `AXGE`; no se han sustituido por cuotas comerciales con otro denominador.
- Los 26 códigos compatibles con diferencias siguen pendientes de explicación numérica. La igualdad del identificador no prueba igualdad de valores ni que las diferencias procedan de una revisión estadística.

El registro contiene título, unidad, hoja y fila de origen, años comunes, razón mediana, diferencias de nivel y crecimiento, estado y revisión necesaria. El CSV anual permite localizar cada discrepancia. Las repeticiones de un mismo código con valores distintos en el Excel se registran aparte.

## PWT: empleo, horas y remuneración

`avh` significa horas anuales medias trabajadas por persona ocupada. El empleo `emp` del archivo principal está en millones de personas; el detalle laboral usa personas. Tras convertir esa escala, empleo y horas coinciden entre ambos archivos para 72 años chinos y 74 españoles (tolerancia relativa y absoluta 1e-6). La participación laboral también coincide entre archivos.

Esto verifica coherencia entre archivos de PWT. **Compartir universo** exige además que numerador y denominador cubran la misma población, territorio, actividad y periodo: asalariados frente a todos los ocupados; empleo doméstico frente a residentes; horas efectivamente trabajadas frente a horas pagadas; media anual frente a cierre de año. La coincidencia de los vectores no resuelve por sí sola esas diferencias con AMECO o ILOSTAT.

La remuneración de asalariados candidata se calcula con `comp_sh × v_gdp`. `comp_sh` es la cuota de ingresos laborales de asalariados en el PIB; `labsh` puede incorporar ajustes por autónomos. En España difieren en todos los años disponibles. En China coinciden numéricamente, pero esa coincidencia no hace intercambiables sus definiciones.

De los 72 años chinos de `comp_sh`, 30 están marcados como observados y 42 como constantes asumidas o interpolados; 2023 pertenece al segundo grupo. El CSV de candidatos conserva la calidad de cada año. La escala monetaria y la compatibilidad del PIB empleado para reconstruir remuneración siguen pendientes de certificación. Las horas totales candidatas son `emp × avh`, en millones de horas, y no sustituyen una serie observada independiente.

El suplemento NA expresa sus niveles en moneda nacional y sus volúmenes `q_*` en precios nacionales de 2021 (según su leyenda; la definición de `q_gfcf` no explicita el año). No deben confundirse con las variables en dólares del archivo principal. La correspondencia inversión/FBC requiere atender a la definición de formación bruta total; para FBCF existen `v_gfcf` y `q_gfcf`. La cobertura de consumo de hogares e ISFLSH y las escalas monetarias necesitan metadatos específicos antes de cerrar equivalencias.

## Procedencia del PIB chino

El documento oficial *What's new in PWT 11.0*, páginas PDF 8–10, explica el paso al PIB oficial de China. La alternativa de Wu queda en el suplemento NA con código `CH2`, hasta 2021. Se ha extraído una comparación de crecimientos como sensibilidad: no se sustituye silenciosamente `CHN` por `CH2`. La procedencia del empleo se conserva por separado en `i_emp`. Usar PWT no elimina automáticamente la dependencia de datos oficiales chinos. Esto tampoco demuestra que estén inflados.

## UN MADT 2.6

La consulta archivada de UNdata, grupo 206, ISIC Rev.4, devuelve cero registros para China continental (156) y 6.908 para España (724), con actualización declarada 14/10/2026. Es una comprobación de presencia de esa tabla y variante, no una descarga completa española ni una prueba de ausencia en cualquier otra fuente. Hong Kong no sustituye a China continental.

Por tanto, output y consumo intermedio chinos no quedan resueltos dentro de esta consulta de la tabla exigida. El suplemento UN AMA descargado anteriormente no equivale a MADT 2.6 y no llena por sí solo ese hueco. Si no se obtiene la tabla china en otra distribución de MADT, habrá que documentar la ausencia y evaluar una fuente alternativa o una adaptación del apartado; no se inventará consumo intermedio a partir del PIB.

## Archivos y reproducción

- `registro_equivalencias.csv/json`: decisión y tarea pendiente por código del Excel.
- `ameco_comparacion_anual.csv/parquet`: evidencia numérica por año.
- `excel_repeticiones_discrepantes.json`: discrepancias dentro del propio Excel.
- `pwt_comprobaciones.csv`: contraste entre archivos PWT.
- `pwt_derivaciones_candidatas.csv`: remuneración y horas con indicadores de calidad.
- `pwt_labor_metadatos.json` y `pwt_na_diccionario_original.csv`: definiciones originales.
- `china_pib_oficial_alternativa_wu.csv`: sensibilidad de crecimiento.
- `un26_presencia.json`: consulta, resultado, ruta original, fecha y SHA-256.

Desde la raíz del proyecto:

```sh
uv run python src/fetch_validation_sources.py
uv run python src/check_un26.py
uv run python src/audit_ameco.py
uv run --with pandas==3.0.6 python src/validate_pwt.py
uv run python src/build_review.py
uv run python src/verify_review.py
```

Los pasos de adquisición reutilizan los originales archivados cuando su hash coincide. No se ha modificado el snapshot v0. Las nuevas comprobaciones documentan el avance; aún falta cerrar la revisión semántica completa entre AMECO y las series internacionales de China, especialmente capital, universo laboral y cuentas sectoriales.
