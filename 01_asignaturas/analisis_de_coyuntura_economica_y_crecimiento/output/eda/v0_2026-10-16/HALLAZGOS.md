# Exploración preliminar de la versión v0_2026-10-16

## Alcance

- 88,798 observaciones almacenadas; se conservan variantes, países, conceptos y unidades por separado.
- Los gráficos principales emplean índices y tasas. Los niveles originales se separan por país.
- No se han descargado datos directos del NBS. Su utilización queda como último recurso.
- Esta exploración no demuestra ni refuta inflación estadística. Tampoco acredita independencia entre WDI y PWT.

## Diferencias de crecimiento del PIB frente a WDI

- CHN / pwt110: 34 años; diferencia absoluta media 0.0645 p.p.; máxima 0.1832 p.p.
- CHN / pwt110_na: 34 años; diferencia absoluta media 0.0645 p.p.; máxima 0.1832 p.p.
- ESP / estat_nama_10_gdp: 28 años; diferencia absoluta media 0.0036 p.p.; máxima 0.1009 p.p.
- ESP / pwt110: 34 años; diferencia absoluta media 0.0119 p.p.; máxima 0.2148 p.p.
- ESP / pwt110_na: 34 años; diferencia absoluta media 0.0119 p.p.; máxima 0.2148 p.p.

## Revisión prioritaria

- 16 eventos marcados con reglas de cribado explícitas. Revisar crisis, cambios de definición y revisiones; no corregir automáticamente.
- Las diferencias entre fuentes pueden reflejar distintas ediciones y métodos; no constituyen errores por sí mismas.
- Los residuos de la identidad nominal se calculan en puntos de PIB; no se impone aditividad a los volúmenes encadenados.
- Las variables con huecos no se interpolan. Los flags de Eurostat se conservan y se consultan en su respuesta original.
- Antes de cerrar el informe faltan: cadena de procedencia CHN, validación de universos laborales, existencias/CCF reales, rentas y tablas input-output.

## Archivos

- coverage_gaps_flags.csv: cobertura efectiva, huecos internos, ceros, negativos y flags por serie.
- gdp_source_differences.csv y gdp_source_summary.csv: comparación de tasas sin igualar niveles de moneda.
- review_events.csv: revisión de saltos; no identifica automáticamente errores.
- nominal_demand_residuals.csv: identidad de demanda corriente.
- exploracion.html: gráficos interactivos autocontenidos.
