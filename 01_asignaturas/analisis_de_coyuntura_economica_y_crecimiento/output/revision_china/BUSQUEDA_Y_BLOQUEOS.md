# Registro de búsqueda y bloqueos reales

Fecha de ejecución: 21/10/2026. Los instantes UTC de los originales están en cada manifiesto. Los errores de red del sandbox se resolvieron mediante la ejecución autorizada con red; no se presentan como ausencia de datos.

## Antes de NBS

Se auditó `observations.parquet`: China ya contenía PWT principal, NA y capital, WDI común y 1.226 códigos WDI del CSV local. El catálogo `existing_inventory.csv` conserva códigos, unidades originales, cobertura y hashes. El CSV WDI local tiene fecha histórica de consulta desconocida y se mantiene separado; la nueva edición API tiene manifiestos propios.

Los requisitos docentes se deduplicaron a través de `requirements.json` y se contrastaron con las instrucciones originales recuperadas del chat. Se conservó la reconciliación española y sus notas. Los contratos documentan máximos observados y el objetivo 1960–2023, sin convertirlo en una obligación de panel completo para cada variable.

La primera consulta WDI por lotes devolvió error para un lote que incluía códigos no admitidos. Se sustituyó por consultas individuales; las respuestas inválidas quedan archivadas, pero no se normalizan. La validación exige una lista de observaciones y paginación completa. Tres códigos no aportan datos válidos en source=2; seis consultas válidas no tienen valores chinos (G real, FBCF real, X real, IM real, existencias reales y tributos netos sobre productos).

Derivados evaluados antes del recurso nacional:

- Deflactor: cociente PIB nominal/real del mismo proveedor/edición; se permite, conservando base nacional no identificada por los metadatos genéricos.
- Población 15+: total menos 0–14; se permite y se contrasta además la partición 0–14/15–64/65+.
- Horas: empleo PWT por horas medias PWT; se permite como estimación derivada, no medición independiente.
- Empleo equivalente: horas/1760, conforme a la aproximación permitida por las instrucciones.
- Productividad, capital/producto y PIB por habitante PPA: base PWT internamente coherente; límites de interpretación explícitos.
- CCF real a partir de nominal, existencias reales como diferencia de cadenas y remuneración como `labsh*PIB`: no aceptados automáticamente. `labsh` no equivale a cuota salarial de asalariados.

Resultado: seguían pendientes producción/intermedios, cuentas de rentas, IO y paro registrado, además de metadatos y tramos históricos. Solo entonces se acudió al anuario NBS.

## Recurso dirigido a NBS

[Índice oficial](https://www.stats.gov.cn/sj/ndsj/2025/left_.htm), [metodología nacional](https://www.stats.gov.cn/sj/ndsj/2025/html/sme03.htm). Se preservan los originales 3-1, 3-10, 3-15, 3-21, 3-22, 4-1 y 18-1, todos con hash. No se interpreta una tabla de PIB como si fuera producción P.1.

3-21 permite matriz 20×20 de 2023 y totales estructurales; 3-22 permite comprobar orientación de usos y producción, sin imponer PIB de mercado a sus valores a precios de productor. La escala no consta explícitamente en la imagen archivada: no se etiqueta como CNY con un multiplicador supuesto. Los 40 controles de sumas admiten 1,05 unidades nativas, máximo por redondear 20 celdas y el total a una decimal; las diferencias efectivas se publican.

3-15 permite remuneración doméstica de 2023 y tributos netos; no da por sí sola D2 y D3 separados ni histórico anual. 4-1 publica registrados urbanos y tasas urbanas media/cierre; no se construye un nivel nacional con esas tasas. 18-1 es dinero a cierre, no base monetaria, y registra rupturas de perímetro. El origen monetario es PBC.

## Ampliación

- [OCDE ICIO](https://www.oecd.org/en/data/datasets/inter-country-input-output-tables.html): se localizó la edición 2025 revisada en enero 2026, con cobertura 1995–2022. La descarga HTTP desde Python de la página devolvió 403; la página pudo consultarse en la búsqueda web. Es una alternativa armonizada, no una réplica automática de la tabla nacional de 2023. No se descargaron tablas ICIO ni se declaró recuperada su cobertura.
- [ADB, indicadores IO China](https://data.adb.org/dataset/peoples-republic-china-input-output-economic-indicators): se localizó la ficha oficial con años 2000 y 2007–2022. La descarga de la ficha desde Python devolvió 403. Son indicadores derivados; no se presentan como matriz nacional ni como evidencia de cobertura anual 1960–2023.
- [FMI, metadatos SDDS de cuentas chinas](https://dsbb.imf.org/sdds/dqaf-base/country/CHN/category/NAG00): página archivada para investigación metodológica. No aporta una serie anual normalizada de CCF real en esta entrega.
- [PBC, estadísticas financieras y cambio M1](https://www.pbc.gov.cn/en/3688247/3688978/3709137/2025080817512723397/index.html): original archivado; confirma la necesidad de distinguir perímetros. No se prolonga M2 de la tabla antigua ni se añade M1 revisado a otra definición.

Los 403 son restricciones de transporte de esos recursos, no evidencia de inexistencia de datos. La falta de una serie acreditada en esta entrega tampoco demuestra que no exista en otra publicación. No se han solicitado aclaraciones sobre elecciones que podían resolverse conservadoramente; se dejan documentadas las decisiones que necesitarían fuentes/metadatos adicionales.

## Decisiones de cierre

El criterio de cierre de esta entrega es tener inventario, candidatas, transformaciones explícitas, originales y controles, más una decisión por hueco. Quedan abiertos los contratos que exigen cobertura o equivalencia no acreditada. Su resolución futura requiere acreditar escala/valoración o descargar y revisar otra tabla; no autoriza imputación, empalme ni cambio automático del universo.

En la revisión final se amplió expresamente la búsqueda de CCF real y rentas a la metodología SDDS del FMI y a la ficha OCDE de cuentas nacionales. La metodología SDDS describe deflactores específicos para CCF de administraciones y para existencias; no entrega los vectores necesarios para reconstruir el total de economía sin mezclar activos/sectores. El glosario WDI identifica `NE.GDI.STKB.KN`; se consultó y archivó expresamente su API para China, que devuelve cero valores. Esto refuerza el bloqueo de esa consulta, sin demostrar ausencia universal. No se usaron otras tablas ONU encontradas por el buscador.
