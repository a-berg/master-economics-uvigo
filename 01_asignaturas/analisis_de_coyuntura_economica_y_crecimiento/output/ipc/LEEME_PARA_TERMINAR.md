# Para terminar hoy

Archivo de trabajo: `IPC-ADRIAN BERGES-revisado.xlsx`, en esta misma carpeta.

## Supermercados ya cargados

Se han completado las 222 celdas de 74 productos. El origen de cada semana consta en la hoja `Fuentes precios`: 14 valores proceden de históricos, catálogos o una referencia equivalente de folleto; uno se arrastra de una observación de la semana anterior y 207 conservan el precio base como estimación sin cambios. Los colores permiten distinguirlos.

## Cuotas mensuales y columnas de gasto

Netflix (8 €/mes), Spotify Duo (16,99 €/mes) e hipoteca (648 €/mes) conservan la tarifa confirmada por Adrián en las tres semanas. No se prorratean: cada columna semanal revaloriza las cantidades de la misma cesta base. Los pagos originales se mantienen. La base contiene dos cuotas de cada servicio; sus costes comparables son 16 €, 33,98 € y 1.296 €, respectivamente, en cada observación. No son nuevos desembolsos semanales.

Las columnas CO, CQ y CS son fórmulas, no un diario de nuevas compras. Se han restaurado las fórmulas sustituidas por ceros en pijama e hipoteca y la borrada en CO93. También se ha corregido la «s» de CP116 a 35 €/kg, coincidente con la base y las otras semanas. La hipoteca sigue teniendo un peso elevado en la cesta original; este ajuste no cambia las ponderaciones.

## Seguimiento completo

Las 104 partidas tienen precios en las tres semanas. No quedan celdas de precio pendientes. Se conservan los precios base de bombilla (4,95 €), spray (15 €) y ceras (3,99 €/unidad) como estimaciones sin cambios, autorizadas por Adrián.

| Semana | Coste de la cesta (€) | Índice (base 100) | Variación (%) |
| --- | ---: | ---: | ---: |
| 12–18/10/2026 | 1752.0079 | 100.004447 | 0.004447 |
| 19–25/10/2026 | 1752.0079 | 100.004447 | 0.000000 |
| 26/10–01/11/2026 | 1751.6491 | 99.983966 | -0.020479 |

La primera variación compara con la base; las otras dos comparan semanas consecutivas. El resultado incorpora los supuestos de estabilidad documentados.


## Actualizar el informe

Desde la raíz de la asignatura:

```bash
uv run python source/ipc/actualizar_informe.py
```

Este comando lee el Excel, actualiza los datos del Typst y compila el PDF. No modifica el Excel. Si has guardado la copia editada en otra ruta, usa `--workbook "/ruta/al/archivo.xlsx"`.

El archivo original de Documentos se mantiene intacto. No vuelvas a ejecutar el constructor antiguo `completar_excel.mjs`, porque reconstruye desde el original.
