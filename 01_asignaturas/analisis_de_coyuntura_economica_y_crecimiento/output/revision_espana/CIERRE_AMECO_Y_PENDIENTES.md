# Cierre de diferencias AMECO y alcance pendiente

20/10/2026, después de la revisión del alumno.

Se aceptan los 74 códigos AMECO españoles recuperados de la edición vigente y las tres series EPA añadidas. La vista anual pasa a 77 columnas de series. Las 31 comparaciones se mantienen como diagnóstico, sin bloquear su selección; no se certifica la causa particular de cada discrepancia. Se adoptan los valores actuales sin aplicar factores deducidos del Excel.

## Interpretación de diferencias

- AMECO incorpora previsiones. La concentración de diferencias al final es compatible con cambios de previsión y su sustitución por estimaciones posteriores, pero hace falta conocer la edición antigua para demostrarlo.
- Los precios corrientes valoran cada periodo a sus propios precios; no tienen un año base de precios. Sus revisiones históricas pueden proceder de nuevas fuentes, estimaciones y revisiones metodológicas. Un cambio de referencia de volumen es otra operación.
- La revisión europea coordinada de 2024 afecta a cuentas nacionales y balanza de pagos. DMGE pertenece a estadísticas de comercio exterior de bienes: no se atribuye su diferencia a aquella revisión sin una nota específica de la serie.
- La razón de escala UUTG/URTG respecto al Excel es un diagnóstico. Se acepta el dato actual publicado, conservando su unidad literal; no se afirma la causa exacta del factor en la referencia.

Fuentes metodológicas: https://economy-finance.ec.europa.eu/economic-research-and-databases/economic-databases/ameco-database_en y https://ec.europa.eu/eurostat/web/esa-2010/data-revision.

## ¿Está toda España?

No todavía. Los 74/76 eran códigos AMECO, no todas las filas de las diez hojas base. El lector anterior omitía encabezados con un año de edición aislado seguido de años de la serie, como en Produzón-CI-VA. Se ha corregido y ampliado `filas_sin_codigo_inventario.csv`.

| Bloque | Estado comprobado | Trabajo restante |
|---|---|---|
| AMECO | 74 series recuperadas y aceptadas | AMGE y AXGE no recuperadas; mantener ausencia explícita |
| Producción, consumos intermedios e impuestos netos sobre productos | Ya descargados en observations.parquet desde INE, 1995–2024 | Integrarlos en espana.parquet; revisar edición más reciente y derivar VAB según valoración correcta |
| Remuneración: sueldos/salarios y cotizaciones | D11 y D12 presentes en descarga Eurostat, sin selección final para esta tabla | Filtrar precios corrientes/unidad y conservar correspondencia; revisar otros impuestos netos sobre producción por separado |
| Empleo y horas PWT; cambio de moneda | Datos ya descargados en otras fuentes del proyecto | Elegir correspondencias e integrar; no duplicar empleo sin indicar universo ni confundir horas totales y medias |
| Demografía adicional | Excel contiene nacimientos, defunciones y matrimonios | Recuperar o seleccionar series oficiales; verificar necesidad de cada una para el informe |
| Trabajo adicional | Paro EPA actual integrado 2006–2025 | Histórico anterior, paro registrado y salario mínimo: pendientes de selección/descarga |
| Quiebras y suspensiones de pagos | Series históricas presentes en el Excel | Revisar definiciones, continuidad y fuentes actuales |
| M1, M2, M3 y base monetaria | Series históricas presentes en el Excel | Revisar fuentes y cambio de marco monetario con la entrada en el euro |
| Filas calculadas o duplicadas | Inventariadas junto a las no codificadas | Clasificar para no contarlas como datos base ausentes: CHECK, multiplicadores monetarios, variantes antiguas, etc. |

La igualdad entre dos ediciones deja de ser una condición de aceptación. El siguiente trabajo es seleccionar e integrar las series que faltan en la tabla unificada y resolver los huecos documentales, no continuar investigando todas las discrepancias históricas de AMECO.
