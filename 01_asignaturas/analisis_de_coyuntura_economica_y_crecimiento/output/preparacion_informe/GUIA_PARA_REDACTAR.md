# Base preparada para redactar el informe China–España

Esta entrega transforma los datos auditados en resultados que pueden utilizarse directamente al escribir. Incluye 38 figuras, 21 tablas y una ficha para cada uno de los 27 bloques de requisitos. Las figuras que usan aproximaciones o adaptan el ejercicio lo indican en su pie. No es todavía el informe redactado.

## Empezar por estos archivos

- [Índice visual de resultados](index.html): gráficos, tablas y notas de uso.
- [Estado por requisito](estado_requisitos.csv): qué está preparado, adaptado o parcial.
- [Catálogo de figuras y tablas](catalogo_resultados.csv): identificadores y rutas para citar.
- [Limitaciones](limitaciones.csv): problema encontrado, decisión e implicación para el informe.
- [Indicadores](../../datos/gold/informe/indicadores.parquet) y [diccionario](../../datos/gold/informe/diccionario.csv): país, año, variable, unidad, fuente y fórmula.
- [Notebook de revisión](../../notebooks/06_datos_informe.ipynb): cobertura, tablas y selección de gráficos.

## Decisiones de análisis

La comparación principal usa 1990–2023. Las tablas 6.3–6.4 y 7.1 comparten los subperiodos 1960–1989, 1989–2000, 2000–2008, 2008–2019 y 2019–2023. Los promedios de participaciones usan ventanas sin solapamiento salvo la fila de conjunto. Las correlaciones usan 1996–2019 y 1996–2023, con los mismos años para ambos países dentro de cada par de variables. Se conservan n y la lista exacta de años; el tamaño de muestra puede diferir entre variables.

PWT 11 es la base común de PIB, capital, empleo, horas y crecimiento. La demanda usa PWT NA. Precios y rentas nacionales se conservan en su propia base. Para los salarios docentes se divide D1 nacional por empleo PWT y se deflacta con el PIB nacional. No se denomina salario de asalariados a este promedio por ocupado. El bloque laboral comparable usa datos modelizados OIT/WDI para ambos países, con ocupados y parados derivados; encuestas y registros nacionales se muestran aparte.

Los niveles en monedas nacionales se presentan en paneles separados. Solo el PIB por habitante a PPA se usa para comparar niveles internacionales de renta. En productividad se prefieren índices para mostrar evolución. Cada gráfico exporta sus datos a `datos/gold/informe/figuras_datos/`.

## Resultados descriptivos de partida

- Entre 1960 y 2023 el PIB real PWT registra un crecimiento anual compuesto del 7.63% en China y del 3.24% en España.
- Por habitante, las tasas compuestas son 6.31% y 2.50%, respectivamente.
- En la descomposición logarítmica, China presenta 2.83 puntos de capital, 0.99 de empleo y 3.53 de residuo; España, 1.29, 0.56 y 1.33. Estas contribuciones suman crecimiento logarítmico, no CAGR.
- El comentario económico debe contrastar estos resultados con demanda, productividad y subperiodos. Las cifras no identifican por sí solas causas ni efectos de políticas.

## A qué nos hemos enfrentado

**Producción e intermedios.** China solo tiene un año IO 2023 y una escala monetaria inferida por cotejo de D1. Precios de productor, no mercado. Figura estructural y cocientes; sin reconstruir una historia anual.

**Demanda real.** Las escalas y bases monetarias de componentes PWT no se han acreditado para comparar niveles nacionales. Índices dentro de cada serie, tasas y participaciones nominales internas. No sumar volúmenes.

**Consumo de capital fijo.** Falta CCF real oficial chino comparable con AMECO. PWT aporta CCF corriente y precios por activos. CCF real aproximado ΣDc/Np; sensibilidad previa disponible. Depreciación por CCF/stock a coste corriente.

**Existencias.** FMI/IFS real termina en 2019 y no acredita P53; España incluye P52+P53. El flujo puede ser cero o negativo. Escala con |valor 2008|; cambios anuales del índice. Sin tasas porcentuales ni relleno de 2020–2023.

**Rentas.** China: D2 distribuido coincide en 2023 con neto NBS; excedente incluye renta mixta y termina en 2021. Coste de factores aproximado; discrepancia explícita, sin atribuir residuo a D3.

**Subvenciones.** D3 anual exacta no recuperada; solo categoría fiscal histórica parcial y referencia FMI 2023. Excel reciente FMI bloqueado por HTTP 403. Serie de subvenciones a precios con categoría parcial. No usarla para cerrar la identidad de rentas.

**Salario medio docente.** D1 corresponde a asalariados y el denominador solicitado incluye a todos los ocupados; se combina fuente nacional con PWT. Denominar remuneración por ocupado. Deflactor del PIB, no cesta IPC. Tasas e índices comparados.

**Mercado laboral.** Encuestas, modelos OIT y registros tienen distintos universos; registro chino urbano y momento no precisado. Bloque común modelizado WDI para ambos países; derivaciones explícitas. Encuesta y registro aparte, sin empalme.

**Muestras estadísticas.** Las coberturas por fuente y variable difieren; la pandemia cambia los estadísticos. Intersección de años de ambos países por par y ventana; n, años, media y desviación muestral visibles. Ventanas 1996–2019 y 1996–2023.

**Input-output España.** No se ha incorporado una matriz española a esta entrega. Los totales INE no permiten reconstruir nueve flujos intersectoriales. Tabla china preparada. Comparativa IO bilateral identificada como parcial.

**Referencias históricas docentes.** No se han reconstruido las filas históricas de otros países empleadas en clase. Tablas comparativas China–España con PWT desde 1960; no presentarlas como reproducción literal de Maddison.

**Interpretación.** Correlaciones y relaciones de niveles no identifican causalidad; el residuo de Solow recoge todos los factores omitidos. Resultados descriptivos, sin atribuir todo el residuo a tecnología ni identificar políticas por correlación.

## Estado de cada bloque

| Bloque | Estado | Resultados |
|---|---|---|
| 2A.production · Producción, consumos intermedios y valor añadido | ADAPTADO | 2A.1;2A.3_ratios |
| 2A.gdp · PIB nominal y real | ADAPTADO | 2A.3_pib |
| 2B.levels · Demanda real | ADAPTADO | 2B.1 |
| 2B.shares · Composición y medias de demanda | ADAPTADO | 2B.3_shares;2B.T1 |
| 2B.growth · Tasas de crecimiento de demanda | PREPARADO | 2B.3_growth |
| 2B.stats · Correlación y desviación relativa | PREPARADO | 2B.T3 |
| 2B.2008 · Demanda normalizada 2008=100 | PREPARADO | 2B.4 |
| 2C.investment · FBC, FBCF, existencias, CCF y reposición | ADAPTADO | 2C.1;2C.2 |
| 2C.capital · PIB/capital y depreciación | ADAPTADO | 2C.3;2C.4;2C.T1 |
| 2C.capital_cycles · Crecimiento y correlaciones de capital e inversión | ADAPTADO | 2C.5;2C.T2 |
| 2C.labor · PIB, empleo, horas y productividad | PREPARADO | 2C.6;2C.7;2C.8;2C.9;2C.10;2C.T3 |
| 2C.intensity · Capital por trabajador y hora | PREPARADO | 2C.11;2C.12 |
| 2D.income · PIB y rentas factoriales | PARCIAL | 2D.1;2D.3;2D.T1 |
| 2D.io · Tabla input-output tres sectores | PARCIAL | 2D.T2 |
| 3.prices · IPC y deflactor, inflación y PIB | PREPARADO | 3.1;3.2;3.3;3.T1;3.T2 |
| 3.wages · Remuneración por ocupado nominal y real | ADAPTADO | 3.4;3.5;3.6;3.T3 |
| 3.wage_employment · Salario real, empleo y paro | ADAPTADO | 3.7;3.8;3.T4 |
| 4.demography · Población y estructura por edades | PREPARADO | 4.1;4.2 |
| 4.labor · Activos ocupados parados y tasas | ADAPTADO | 4.3;4.4 |
| 4.registered · Paro registrado y paro de encuesta | ADAPTADO | 4.5 |
| 4.cycles · Crecimiento y correlaciones laborales | ADAPTADO | 4.6;4.7;4.8;4.9;4.10;4.T1 |
| 6.1 · Crecimiento medio PIB | ADAPTADO | 6.T1 |
| 6.2 · Crecimiento medio PIB por habitante | ADAPTADO | 6.T2 |
| 6.3 · PIB por subperíodos | ADAPTADO | 6.T3 |
| 6.4 · PIB por habitante por subperíodos | ADAPTADO | 6.T4 |
| 6.kuznets · PIB por habitante y desigualdad | ADAPTADO | 6.1 |
| 7.1 · Contabilidad del crecimiento | PREPARADO | 7.T1 |

## Lo que falta para entregar el informe

1. Incorporar la matriz IO española si se quiere una comparación bilateral; la tabla de China sí está preparada.
2. Decidir si se añaden literalmente las referencias históricas de otros países de las tablas docentes 6.1–6.4.
3. Redactar la interpretación por temas, seleccionar los gráficos imprescindibles y trasladarlos al apéndice con sus notas.
4. Actualizar el borrador Typst, que todavía usa la base antigua de octubre. No tratarlo como reflejo de esta entrega.
5. Revisar bibliografía temática, conclusiones y exposición oral. Las limitaciones estadísticas anteriores acompañan los resultados; no impiden escribir el resto.

## Reproducción

```sh
uv run --offline python src/prepare_report.py
uv run --offline --group analysis python src/create_report_notebook.py
uv run --offline --group analysis python src/verify_report_data.py
```

La ejecución lee silver y los originales archivados. Escribe únicamente la nueva capa `datos/gold/informe/` y sus resultados. España, China y v0 se conservan.
