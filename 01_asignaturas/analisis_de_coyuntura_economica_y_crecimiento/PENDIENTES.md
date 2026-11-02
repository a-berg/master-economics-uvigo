# Estado actual del informe

La preparación vigente está en [GUIA_PARA_REDACTAR.md](output/preparacion_informe/GUIA_PARA_REDACTAR.md). Hay **38 gráficos, 21 tablas y 27 fichas de requisitos**: 8 bloques preparados, 17 adaptados y 2 parciales. Los estados antiguos del pipeline inicial no describen esta nueva entrega.

## Datos y cálculos preparados

- PIB y demanda: índices nacionales, participaciones nominales, crecimientos, promedios, correlaciones y respuesta desde 2008.
- Capital y trabajo: capital/producto, depreciación, inversión y CCF aproximado, empleo, horas totales, productividad por ocupado/hora e intensidad de capital.
- Precios y remuneración: IPC, deflactor, inflación, remuneración nominal y real por ocupado y correlaciones con productividad, empleo y desempleo.
- Demografía y trabajo: edades, activos, ocupados, parados y tasas de una base común modelizada; registros y encuestas nacionales aparte.
- Crecimiento: tablas China–España desde 1960 y contabilidad con α=1/3; mismos subperiodos en 6.3–6.4 y 7.1.
- Desigualdad: pares observados de PIB por habitante PPA y Gini, sin interpolación.
- Tema 5: referencias a los gráficos y tablas anteriores; no se duplican los resultados.

## Pendientes de datos que afectan a la reproducción literal

1. **Input-output española.** La tabla china de tres sectores está preparada. Los totales de producción y consumos intermedios españoles no permiten reconstruir los nueve flujos; falta incorporar una matriz española.
2. **D2 y D3 chinos separados.** Se utiliza una magnitud tributaria interpretada como neta y subvenciones fiscales parciales. El excedente OCDE incluye renta mixta. Estos límites impiden presentar una identidad de rentas exacta; sí permiten una comparación descriptiva advertida.
3. **Referencias históricas de clase.** Las tablas 6.1–6.4 calculadas comparan China y España con PWT. No reproducen las filas históricas de otros países/Maddison; decidir si deben añadirse literalmente.

## Límites aceptados que deben acompañar a los resultados

- China: producción e intermedios del año IO 2023, precios de productor y escala monetaria inferida; sus cocientes no dependen de esa escala.
- CCF real estimado con cuatro activos PWT; sensibilidad a deflactores documentada. No se presenta como CCF oficial.
- Existencias reales FMI/IFS: 1980–2019 y alcance de objetos valiosos pendiente. Las estadísticas usan cambios del flujo escalado, no tasas porcentuales con valores negativos.
- Remuneración por ocupado: D1 nacional y empleo PWT; no salario por asalariado. El indicador real utiliza el deflactor del PIB.
- Bloque laboral principal modelizado OIT/WDI. Registro urbano chino y encuestas nacionales conservan sus universos y coberturas.
- Muestras estadísticas comunes entre países por variable y ventana; se conserva n. Una correlación no identifica causalidad.

## Trabajo de redacción y entrega

1. Redactar interpretación por temas y comparativa con España, utilizando el [guion](entregas/NOTAS_PARA_REDACTAR.md) y el [catálogo de resultados](output/preparacion_informe/catalogo_resultados.csv).
2. Seleccionar los gráficos y tablas del apéndice y citarlos por identificador. Las duplicidades y erratas docentes están documentadas en el catálogo.
3. Actualizar el borrador Typst: todavía usa el gold antiguo, no la base vigente.
4. Incorporar bibliografía temática, revisar conclusiones y preparar exposición oral.
5. Compilar y revisar el informe final. La validación de datos no sustituye la revisión editorial.

Los detalles de acceso, cobertura y comparabilidad están en [limitaciones.csv](output/preparacion_informe/limitaciones.csv), con la decisión tomada y los resultados afectados.
