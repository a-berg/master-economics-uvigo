# Mi IPC: primer borrador

**Organización del 9 de noviembre:** los scripts de preparación, actualización y
verificación están en `../../source/ipc/`. En esta carpeta permanecen el Typst,
la bibliografía y los JSON que utiliza el documento. Las instrucciones de
ejecución están en `../../source/ipc/README.md`; los apartados históricos de esta
guía describen las etapas iniciales del trabajo.

**Actualización del 7 de noviembre:** el Excel revisado ya tiene los 222 precios de supermercado cargados, con sus fuentes y estimaciones identificadas en la hoja `Fuentes precios`. Quedan 30 partidas fuera de supermercados. La guía vigente para terminar es `../../output/ipc/LEEME_PARA_TERMINAR.md`. Después de editarlas, ejecutar `uv run python source/ipc/actualizar_informe.py` para regenerar las tablas, gráficos y resultados del informe. Los constructores de la corrección inicial descritos más abajo no deben volver a ejecutarse sobre el archivo rellenado.

El informe está en `mi_ipc_ABerges.typ` y utiliza el paquete local habitual `@local/master-uvigo-templates:0.1.0`, con `essay`, `base-styles` y los tamaños de letra compartidos. Los datos de la tabla 1 proceden de `datos_ipc.json`. La bibliografía está en `referencias.bib`.

Los resultados para revisar se guardan en `../../output/ipc/`:

- `IPC-ADRIAN BERGES-revisado.xlsx`: copia corregida. El archivo original de Documentos se conserva intacto.
- `mi_ipc_ABerges.pdf`: informe compilado.

## Qué se ha corregido

El subtotal de ocio omitía la fila 98 (Spotify). El gasto de ocio pasa de 16,00 a 49,98 euros y el total de 1.717,95 a 1.751,93 euros. Se corrige el subtotal de la base y el de las tres semanas. Las ponderaciones personales se recalculan.

Los índices 101, 102 y 103 eran ejemplos escritos como valores. Ahora se calculan como el coste de la cesta a precios de cada semana dividido entre su coste base, por 100. Los resultados quedan vacíos cuando falta un precio de un bien con cantidad base positiva. Los grupos sin compras tienen gasto cero. La presencia de un precio en otra fila no suple el que falta.

Se actualizan las fechas de las cabeceras, las etiquetas y los títulos de los dos gráficos nativos. Se mantienen las dos hojas, los registros diarios, las cantidades, las descripciones y los valores de referencia para España y Galicia. Los totales de ponderaciones pasan a ser fórmulas. Los gráficos toman datos del auxiliar J16:L20 de `Tablas e Gráficos`: los `#N/A` de ese auxiliar son intencionados y hacen que se omitan los valores pendientes, en lugar de dibujarlos como cero.

La base efectiva es **08/09–06/10/2026**, no el mes natural de septiembre. El seguimiento termina el **01/11/2026**. Las referencias antiguas a febrero-marzo de 2024 y septiembre de 2024 no describían estos datos.

## Qué pide el profesor y qué está disponible

| Requisito | Situación del borrador |
| --- | --- |
| Resumen de menos de 200 palabras | Incluido, con objetivo, método y resultados disponibles |
| Introducción: interés, objetivo, método, resultados y estructura | Incluida |
| Metodología sin adelantar resultados | Incluida: base, cantidades, ponderaciones, Laspeyres y tasas |
| Comparación de ponderaciones con España y Galicia | Tabla 1 y comentario incluidos, con referencia histórica de 2024 |
| IPC semanal | Fórmulas listas; precios todavía pendientes |
| Inflación semanal | Fórmulas listas; precios todavía pendientes |
| Conclusiones y extensiones breves | Incluidas |
| Bibliografía solo de fuentes usadas | Incluida |
| Tablas y gráficos en apéndice, citados desde el texto | Dos tablas y dos gráficos incluidos. Los gráficos no simulan observaciones ausentes |

## Por dónde continuar

1. **Revisar la cesta antes de recoger precios.** La hipoteca figura dos veces (648 euros cada vez), el 8 de septiembre y el 1 de octubre. Se conserva, pero representa el 73,98 % del desembolso. Una cuota de financiación no equivale a un precio de consumo. Conviene acordar con el profesor el tratamiento de esa partida y mantener un criterio coherente para todos los gastos. El borrador incluye la sensibilidad al excluirla, sin modificar los registros.
2. **Comprobar las clasificaciones y la cobertura.** Las ceras infantiles están en otros bienes y servicios, el aceite de motor en transporte y Spotify en ocio, según la hoja original. No se han reasignado sin un criterio acordado. Un grupo vacío puede responder al calendario de pagos o a la falta de registro. Se ha revisado la coherencia aritmética, no la exhaustividad de todos los gastos ni todos los justificantes.
3. **Recoger los precios históricos de seguimiento.** En `Mis Gastos`, introducir el precio unitario en **CP** (12–18/10), **CR** (19–25/10) y **CT** (26/10–01/11). Hay 104 filas con gasto base y, por tanto, 312 observaciones de precio pendientes. Las celdas de entrada correspondientes están resaltadas. Anotar la fecha, establecimiento y justificante en un registro externo. No utilizar un precio de hoy como si se hubiese observado en octubre. Si un precio histórico no puede recuperarse, decidir y documentar con el profesor cómo tratar esa ausencia.
4. **Mantener la unidad.** En productos por peso se necesita €/kg; en envases, €/envase; en suscripciones, €/servicio del mismo período. No introducir el importe total de otra compra con cantidad diferente. El coste semanal valora la cantidad acumulada de la base. Un servicio que mantenga su tarifa también requiere comprobarla; el archivo no presupone estabilidad.
5. **Consultar `Tablas e Gráficos`.** Al completar todos los precios de una semana, aparecerán el coste y el índice. La tasa de la primera semana compara con toda la base; las siguientes comparan semanas consecutivas. No comparar directamente con una inflación mensual o interanual oficial.
6. **Actualizar el texto y el apéndice del informe.** El borrador actual describe la ausencia de precios. Tras completarlos, actualizar la tabla 2, los gráficos 1–2, las secciones 3.2–3.3, el resumen y las conclusiones. Esos bloques narrativos y gráficos no se actualizan automáticamente al editar el Excel. La tabla 1 sí se construye desde el JSON.

## Referencia oficial

Se mantienen los pesos de España y Galicia identificados como 2024 en el Excel original y su enlace a la tabla INE 50952. No se han presentado como datos de 2026 ni se ha certificado de nuevo cada valor contra una descarga de INE. La suma de cada columna es 99,9999 % por redondeo. El nuevo IPC base 2025 tiene 13 grupos, por lo que sustituir los valores por los de 2026 requiere revisar las correspondencias, no pegar cifras sobre las 12 filas existentes.

## Compilación y reproducción

Desde la raíz de la asignatura:

```bash
typst compile --root . entregas/ipc/mi_ipc_ABerges.typ output/ipc/mi_ipc_ABerges.pdf
```

`analizar_ipc.py` lee el archivo original sin escribir en él y genera `datos_ipc.json`. Puede ejecutarse con `uv run python source/ipc/analizar_ipc.py`. Calcula los totales directamente a partir de los registros diarios, sin depender de las fórmulas erróneas o de su caché.

`preparar_importacion.py`, `revisar_excel.mjs` y `completar_excel.mjs` documentan la corrección inicial. `ajustar_graficos.py` aplica huecos y cachés dispersas a los gráficos tras exportar, porque la API del importador no expone esa opción del archivo original. El importador de hojas fallaba por identificadores negativos de los ejes de los gráficos del archivo original; la copia temporal normaliza esos identificadores. **No volver a ejecutar `completar_excel.mjs` sobre la copia ya rellenada:** reconstruye el archivo revisado desde el original. Para el trabajo cotidiano basta con editar el Excel revisado y compilar el Typst al actualizar el texto.

`verificar_excel.mjs` prueba en memoria una cesta sin cambios (índice 100), un aumento de precio, las tasas resultantes y la ausencia de un precio necesario. No exporta ni conserva datos de prueba. Estos scripts JavaScript usan `@oai/artifact-tool` del runtime de Codex; `node_modules` es un enlace local ignorado por Git.

## Validaciones realizadas

Se han contrastado los totales con la suma directa de los registros, las ponderaciones y su suma. Se han comprobado las fórmulas con datos temporales y revisado la conservación de registros, hojas, combinaciones de celdas y gráficos. Se ha compilado el Typst y revisado visualmente el PDF. No se ha probado en Microsoft Excel de escritorio.
