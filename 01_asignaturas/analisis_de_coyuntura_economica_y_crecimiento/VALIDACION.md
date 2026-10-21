# Validación realizada

- Diez descargas remotas registradas y disponibles; una nueva ejecución reutiliza bronze verificado.
- Auditoría de las 27 hojas del Excel de referencia, con extracción de sus celdas almacenadas y transcripción de Source.
- 88.798 observaciones normalizadas con claves únicas y valores finitos.
- Panel común de 146 registros país-año y diez descomposiciones por país y subperíodo.
- Verificados hashes de todos los archivos bronze, CAGR por reconstrucción de valores finales, identidad aditiva de contabilidad del crecimiento y decodificación JSON-stat con faltantes y flags.
- Verificadas identidades laborales derivadas y la identidad de oferta INE para 1995–2024.
- Dieciocho selecciones oficiales españolas documentadas; una (existencias y objetos valiosos en volumen encadenado) no ofrece observaciones y queda marcada como ausente.
- Catorce figuras y dos tablas integradas en el borrador Typst. PDF compilado y revisado visualmente.
- Aplicación al repositorio probada solo en modo comprobación: sin cambios en el original.

## Alcance pendiente

Consultar PENDIENTES.md. La ejecución correcta no certifica comparabilidad conceptual de todas las fuentes ni convierte el borrador en un informe académico completo. No se han reconstruido por aproximación las series de rentas, CCF real o paro registrado que faltan.

## Versión inicial y EDA

- Snapshot `v0_2026-10-16` creado sin refrescar proveedores: 15 originales bronze conservados y 38 archivos de datos, catálogo y preparación fijados por hashes.
- Verificado que no se puede sobrescribir el ID y que una alteración de una copia de prueba se detecta.
- Ocho celdas del notebook ejecutadas con IPython en proceso y guardadas sin errores. No se afirma ejecución con kernel Jupyter: el entorno bloqueó sus sockets TCP e IPC.
- Vista HTML con gráficos interactivos, Plotly incluido y sin scripts externos. Los controles con callbacks del notebook requieren un kernel local.
- Se comprobaron casos de huecos, denominadores no positivos y base de índice ausente.
- Cribado inicial: 16 eventos de revisión, que no se identifican como errores ni como pruebas de sesgo.
- Identificadores de figuras reservados con sufijos CHN/ESP. La numeración del PDF y la migración a Lilaq se aplazan para priorizar los datos.
