#import "@local/master-uvigo-templates:0.1.0": essay, font_sizes, uvigo-gray, base-styles

// TITLE PAGE
#let title-page(essay-title, author) = {
  set par(first-line-indent: 0em)
  set align(center + horizon)
  set page(footer: none, header: none)
  title(essay-title)
  text(size: font_sizes.Huge, [*Informe Final*])
  linebreak()
  v(1.5em)
  text(size: font_sizes.LARGE, author)
  linebreak()
  v(1em)
  [
    #text(size: font_sizes.Large)[Universidade de Vigo] \
    #text(size: font_sizes.large, emph[Facultade de Ciencias Económicas e Empresariais])
  ]
  linebreak()
  v(1.1em)
  text(size: font_sizes.Large, datetime.today().display("[year]"))
}

#show: base-styles
#show: essay.with(
  author: "Adrián Berges Enfedaque",
  essay-title: [Comparativa económica entre la República Popular China y España],
  title-page: title-page,
  abstract: lorem(200),
)

#set page(
  header: context {
    h(1fr)
    set text(size: font_sizes.footnotesize, fill: uvigo-gray)
    emph[Análisis de Coyunyura Económica y Crecimiento]
  },
  footer: context {
    set align(center)
    set text(size: font_sizes.footnotesize)
    counter(page).display("1/1", both: true)
  },
)

#let country = "China"

= Introducción
#lorem(10)
= Datos y metodología
// Esta es la sección de “materiales y métodos” de los químicos y médicos. Hay
// que indicar (muy brevemente, nada de enrollarse):
//     a) La base de datos empleada, y el rango temporal elegido; e,
//     b) Las herramientas que empleó en el análisis.
// Nota. Cuando se describen las herramientas NO se indican los resultados. Los
// resultados se presentan en la siguiente sección 3 de resultados.
== Bases de datos
#lorem(10)
== Metodología
===
= Resultados
== Agregados en cantidades
=== PIB: el lado de la oferta
=== PIB: el lado de la demanda
=== Los inputs capital y trabajo
=== PIB: La remuneración de los factores de producción
=== Agregados en cantidades: comparativa #country y España
== Mercado de trabajo
=== Mercado de trabajo: comparativa #country y España
== Ciclos económicos: el corto plazo
=== Ciclos económicos y agregados en cantidades
=== Ciclos económicos y factores productivos
Explicar la ciclicidad y/o contraciclidad das variables de los gráficos correspondientes Gráficos 2C.1-2C.10 y Tablas 2C.1-2C.2
=== Ciclos económicos y mercado laboral
Explicar la ciclicidad y/o contraciclidad das variables de los gráficos correspondientes Gráficos 2.1-2.2, y Tablas 2.1
=== Ciclos económicos y agregados de precios
Explicar la ciclicidad y/o contraciclidad das variables de los gráficos correspondientes Gráficos 4.1-4.5 y las Tablas 4.1-4.2
=== Ciclos económicos: comparativa #country y España
== Crecimiento económico: el largo plazo
=== Crecimiento económico: conceptos básicos
=== Fuentes del crecimiento económico

= Conclusiones y extensiones

#pagebreak()
#bibliography("fuentes.bib", style: "harvard-cite-them-right")
