#let headline = json("../datos/gold/headline.json")
#import "@local/master-uvigo-templates:0.1.0": essay, font_sizes, uvigo-gray, base-styles
#import "@preview/lilaq:0.6.0" as lq 

// TITLE PAGE
#let title-page(essay-title, author) = {
  set par(first-line-indent: 0em)
  set align(center + horizon)
  set page(footer: none, header: none)
  title(essay-title)
  text(size: font_sizes.Huge, [*Informe Final*])
  linebreak()
  v(1.5em)
  text(size: font_sizes.large, [Borrador con resultados parciales])
  linebreak()
  v(1em)
  text(size: font_sizes.LARGE, author)
  linebreak()
  v(1em)
  [
    #text(size: font_sizes.Large)[Universidade de Vigo] \
    #text(size: font_sizes.large, emph[Facultade de Ciencias Económicas e Empresariais])
  ]
  linebreak()
  v(1.1em)
  text(size: font_sizes.Large, [16 de octubre de 2026])
}

#show: base-styles
#show: essay.with(
  author: "Adrián Berges Enfedaque",
  essay-title: [Comparativa económica entre la República Popular China y España],
  title-page: title-page,
  abstract: [
En este informe comparamos la evolución de China y España y preguntamos qué diferencias presentan sus patrones de crecimiento, inversión y productividad entre 1990 y 2023. Se ha preparado una base reproducible con archivos originales, metadatos de procedencia y transformaciones programadas. El análisis combina una base común Penn World Table 11.0, series oficiales de España obtenidas de Eurostat y datos de precios, demografía, empleo y desigualdad publicados por el Banco Mundial. Se calculan tasas de crecimiento, participaciones de demanda, correlaciones y una descomposición del crecimiento con participación del capital de un tercio. Los resultados iniciales muestran un crecimiento anual compuesto del PIB real del #headline.china.gdp % en China y del #headline.espana.gdp % en España. Las contribuciones factoriales y el residuo se presentan separadamente. Este borrador no cierra todavía el análisis de oferta, rentas, salarios ni tablas input-output. Las comparaciones internacionales exigen distinguir precios nacionales constantes, paridades de poder adquisitivo y diferentes conceptos de empleo.
],
)

#set page(
  header: context {
    h(1fr)
    set text(size: font_sizes.footnotesize, fill: uvigo-gray)
    emph[Análisis de Coyuntura Económica y Crecimiento]
  },
  footer: context {
    set align(center)
    set text(size: font_sizes.footnotesize)
    counter(page).display("1/1", both: true)
  },
)

#let country = "China"

= Introducción
La comparación entre China y España permite estudiar dos trayectorias de crecimiento y composición de la demanda en un marco de medición explícito. El interés del informe reside en identificar qué diferencias aparecen en los datos y qué parte de ellas depende de las definiciones empleadas.

La pregunta de trabajo es cómo difieren el crecimiento del producto, la acumulación de capital y la productividad en China y España durante 1990–2023. Se complementa con el análisis de la demanda, los precios y el mercado laboral.

El estudio combina análisis gráfico y estadística descriptiva. Se utiliza PWT 11.0 como base común para los dos países, junto con descargas oficiales de Eurostat para España y WDI para precios, demografía y desigualdad. Las fuentes y sus revisiones se mantienen separadas.

La primera ejecución produce diferencias de crecimiento sustanciales entre ambos países, detalladas en @tabla-crecimiento. La descomposición de @tabla-contabilidad distingue contribuciones del capital y empleo y un residuo; este último no se identifica exclusivamente con progreso tecnológico. Estos resultados son provisionales mientras se completa la validación conceptual.

El informe presenta las fuentes y métodos, analiza cantidades, precios, trabajo, ciclos y crecimiento, y finaliza con conclusiones y un apéndice de resultados. Los apartados sin evidencia suficiente permanecen señalados como pendientes.
= Datos y metodología
// Esta es la sección de “materiales y métodos” de los químicos y médicos. Hay
// que indicar (muy brevemente, nada de enrollarse):
//     a) La base de datos empleada, y el rango temporal elegido; e,
//     b) Las herramientas que empleó en el análisis.
// Nota. Cuando se describen las herramientas NO se indican los resultados. Los
// resultados se presentan en la siguiente sección 3 de resultados.
== Bases de datos
La edición 11.0 de PWT, publicada el 7 de octubre de 2025, constituye la base común @pwt11. Se conservan su archivo principal, el complemento de cuentas nacionales y el detalle de capital. Los componentes de demanda de ese complemento están expresados a precios nacionales corrientes y constantes de 2021.

Las series oficiales españolas se descargan de Eurostat @eurostat. Las cuentas integradas del INE se conservan en la edición 1995–2024 identificada por el profesor @ine-cuentas. Los indicadores WDI se descargan para ambos países en una consulta común @wdi. Las fechas de acceso, actualización, URLs y hashes se registran por descarga; una fecha de consulta no se confunde con fecha de publicación.

El intervalo principal de comparación es 1990–2023. Cada figura conserva su cobertura efectiva. No se imputa el Gini de los años ausentes ni se concatenan automáticamente proveedores o ediciones.
== Metodología
Se conservan los originales en bronze, se normalizan observaciones y metadatos en silver y se construyen tablas y figuras en gold. Las transformaciones se ejecutan con Python y Polars mediante un entorno bloqueado con uv. Esta organización permite rastrear cada resultado hasta los archivos de entrada.

Las tasas anuales requieren observaciones consecutivas. Las correlaciones y desviaciones muestrales se calculan sobre parejas válidas del mismo período. El análisis cíclico se basa aquí en tasas de crecimiento, no en un filtro de tendencia ni en correlaciones de niveles crecientes. Se incluyen ventanas con y sin los años de la pandemia.

=== Descomposición y contabilidad del crecimiento
Se considera $Y = A K^alpha L^(1-alpha)$ con $alpha = 1/3$, siguiendo las instrucciones. Se emplean conjuntamente rgdpna, rnna y emp de PWT. Para cada subperíodo se calcula $g_X = 100 (ln X_T - ln X_0)/n$, siendo $n$ el número de años entre las observaciones inicial y final. Las contribuciones son $alpha g_K$ y $(1-alpha) g_L$, y el residuo es $g_A = g_Y - alpha g_K - (1-alpha) g_L$. Las tablas 6.3–6.4 y 7.1 comparten subperíodos.

La tasa anual compuesta se calcula por separado como $100 ((X_T/X_0)^(1/n) - 1)$, con $n$ años. No se suman tasas compuestas discretas como si constituyeran una identidad aditiva.

= Resultados
== Agregados en cantidades
=== PIB: el lado de la oferta
Pendiente de completar para China. Para España se han recuperado producción, consumos intermedios y PIB de las cuentas integradas del INE. Debe distinguirse el VAB a precios básicos del PIB a precios de mercado: producción menos consumos intermedios no incluye los impuestos netos sobre productos.
=== PIB: el lado de la demanda
Las figuras @fig-demand-shares-CHN y @fig-demand-shares-ESP presentan participaciones nominales, y @fig-demand-2008-CHN y @fig-demand-2008-ESP comparan la evolución real desde 2008. Las participaciones y los índices miden aspectos distintos. Falta completar el comentario económico y las tablas de promedios exigidas.
=== Los inputs capital y trabajo
Las figuras @fig-productivity, @fig-capital y @fig-hours separan producción por ocupado, capital por ocupado y horas anuales por ocupado. La medición de horas debe conservar la distinción entre promedio por trabajador y volumen total. Pendiente: CCF real y reproducción de todos los gráficos de este bloque.
=== PIB: La remuneración de los factores de producción
Pendiente de localizar y validar cuentas de rentas para China. La participación laboral ajustada de PWT (@fig-labor-share) no sustituye la remuneración de asalariados exigida en la plantilla. También falta agregar la tabla input-output en tres sectores.
=== Agregados en cantidades: comparativa #country y España
== Agregados en precios
La figura @fig-inflation presenta inflación del IPC nacional publicada por WDI. No se sustituye automáticamente el IPC por el IPCA. El deflactor implícito y las series oficiales españolas están disponibles en gold. Pendiente: completar estadísticos, salarios nominales y reales y sus correlaciones.
=== Agregados en precios: comparativa #country y España
El gráfico permite una descripción común de la inflación observada. La interpretación y las posibles diferencias de cobertura requieren revisión antes del cierre del informe.

== Mercado de trabajo
Las figuras @fig-unemployment y @fig-participation utilizan estimaciones modelizadas OIT publicadas por WDI. Los desempleados y ocupados derivados con esas series se identifican expresamente como tales. No se equiparan a paro registrado ni a una EPA china.
=== Mercado de trabajo: comparativa #country y España
Pendiente de contrastar universos estadísticos, fuentes nacionales de encuesta y paro registrado.

== Ciclos económicos: el corto plazo
=== Ciclos económicos y agregados en cantidades
=== Ciclos económicos y factores productivos
Las correlaciones y desviaciones relativas iniciales figuran en datos/gold/cycle_statistics.csv. Pendiente de incorporar su tabla y comentario al texto.
=== Ciclos económicos y mercado laboral
Pendiente de completar correlaciones con series laborales de definiciones coherentes.
=== Ciclos económicos y agregados de precios
Pendiente de completar los estadísticos de precios y salarios.
=== Ciclos económicos: comparativa #country y España
== Crecimiento económico: el largo plazo
=== Crecimiento económico: conceptos básicos
La @tabla-crecimiento presenta tasas compuestas del PIB y del PIB por habitante. Para 1990–2023, el PIB real crece un #headline.china.gdp % anual en China y un #headline.espana.gdp % en España. Por habitante, las tasas son #headline.china.gdp_pc % y #headline.espana.gdp_pc %, respectivamente. Son cálculos sobre una edición común de PWT, no cifras de una publicación de coyuntura de 2026. La figura @fig-gdp-pc utiliza PPA encadenadas para comparar niveles, en lugar de las monedas nacionales.

La figura @fig-kuznets combina únicamente años con Gini observado y PIB por habitante disponible en WDI. No constituye una estimación causal y exige revisar el concepto de bienestar de las encuestas.
=== Fuentes del crecimiento económico
La @tabla-contabilidad presenta las contribuciones del capital y el empleo y el residuo de Solow. La interpretación del residuo debe considerar las limitaciones de medir trabajo mediante ocupados, sin ajustar en esta especificación por horas ni capital humano. Las diferencias entre subperíodos constituyen resultados descriptivos y no identifican por sí solas mecanismos causales.

= Conclusiones y extensiones
Los resultados iniciales documentan una expansión más rápida del PIB real y del PIB por habitante en China durante el período elegido. El proyecto permite reproducir las descargas y los principales cálculos y distingue las series oficiales españolas de la base común internacional.

El informe permanece abierto: faltan los bloques de oferta y rentas de China, tablas input-output, salarios reales y parte de la estadística laboral. Su cierre exige completar estas fuentes, contrastar interpretaciones y revisar la comparación. Las figuras disponibles no sustituyen los ejercicios pendientes.

#pagebreak()
#bibliography("fuentes.bib", style: "harvard-cite-them-right")

#pagebreak()
#include "apendice_generado.typ"
