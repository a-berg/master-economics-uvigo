# Estado de requisitos del informe

Este proyecto genera una primera base analítica. No equivale al informe final ni a la reproducción completa de los ejercicios.

## Pendientes sustantivos

- China: localizar y validar producción total, consumos intermedios, remuneración de asalariados y rentas factoriales en cuentas nacionales. No sustituir la participación laboral ajustada de PWT por remuneración de asalariados.
- Obtener tablas input-output de ambos países y agregarlas en tres sectores. Candidato China: NBS, anuario 2025, tablas 3-21 y 3-22 (año 2023).
- Validar CCF real y existencias. PWT publica depreciación y consumo de capital corriente por activo, pero no se convierte automáticamente con el deflactor del PIB. Eurostat no entrega observaciones para la selección de existencias encadenadas probada.
- Obtener paro registrado de España desde SEPE y decidir una medida nacional de encuesta comparable para China. Los datos OIT modelizados están claramente identificados.
- Completar los gráficos y estadísticos de oferta, rentas, salarios reales y mercado laboral exigidos.
- Añadir a las tablas de crecimiento las referencias históricas de países de la clase, si son exigidas, sin mezclar silenciosamente sus períodos con 1990–2023.
- Revisar interpretación económica, bibliografía temática, conclusiones y exposición oral.

## Cobertura por requisito

- 2A.production — Producción, consumos intermedios y valor añadido: pending_validation
- 2A.gdp — PIB nominal y real: pending_validation
- 2B.levels — Demanda real: data_available_pwt
- 2B.shares — Composición y medias de demanda: data_available_pwt
- 2B.growth — Tasas de crecimiento de demanda: data_available_pwt
- 2B.stats — Correlación y desviación relativa: data_available_pwt
- 2B.2008 — Demanda normalizada 2008=100: data_available_pwt
- 2C.investment — FBC, FBCF, existencias, CCF y reposición: pending_validation
- 2C.capital — PIB/capital y depreciación: pending_validation
- 2C.capital_cycles — Crecimiento y correlaciones de capital e inversión: pending_validation
- 2C.labor — PIB, empleo, horas y productividad: data_available_pwt
- 2C.intensity — Capital por trabajador y hora: data_available_pwt
- 2D.income — PIB y rentas factoriales: pending_validation
- 2D.io — Tabla input-output tres sectores: pending_validation
- 3.prices — IPC y deflactor, inflación y PIB: inflation_generated_other_statistics_pending
- 3.wages — Remuneración por ocupado nominal y real: pending_validation
- 3.wage_employment — Salario real, empleo y paro: pending_validation
- 4.demography — Población y estructura por edades: wdi_downloaded_definition_validation_pending
- 4.labor — Activos ocupados parados y tasas: modeled_labor_derived_not_survey
- 4.registered — Paro registrado y paro de encuesta: pending_validation
- 4.cycles — Crecimiento y correlaciones laborales: pending_validation
- 6.1 — Crecimiento medio PIB: generated_pwt_common_basis
- 6.2 — Crecimiento medio PIB por habitante: generated_pwt_common_basis
- 6.3 — PIB por subperíodos: generated_pwt_common_basis
- 6.4 — PIB por habitante por subperíodos: generated_pwt_common_basis
- 6.kuznets — PIB por habitante y desigualdad: generated_observed_pairs_interpretation_pending
- 7.1 — Contabilidad del crecimiento: generated_pwt_common_basis
