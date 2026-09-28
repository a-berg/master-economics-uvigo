#import "base-definitions.typ": *

#let tfm(
  title: "Título del TFM",
  author: "Tu Nombre",
  advisor: "Nombre del Director",
  year: "2024/2025",
  doc,
) = {
  base-styles()

  // Márgenes tipo libro (izquierdo más amplio para encuadernación)
  set page(
    paper: "a4",
    margin: (top: 3cm, bottom: 2.5cm, inner: 3.5cm, outer: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: font_sizes.footnotesize, fill: uvigo-gray)
        #h(1fr) #text(italics)[Máster en Economía — Universidade de Vigo] #h(1fr)
      ]
    },
    footer: context {
      if counter(page).get().first() > 1 [
        #set text(size: font_sizes.footnotesize, fill: uvigo-gray)
        #h(1fr) #counter(page).display("1") #h(1fr)
      ]
    },
  )

  // Ajustar numeración de headings para TFM (1.1.1)
  set heading(numbering: "1.1.1")

  // --- PORTADA ---
  {
    set par(first-line-indent: 0em)
    v(2cm)
    align(center, text(size: font_sizes.Large, fill: uvigo-cyan)[Universidade de Vigo])
    align(center, text(size: font_sizes.large, fill: uvigo-gray)[Facultade de Ciencias Económicas e Empresariais])
    v(2cm)
    align(center, text(size: font_sizes.large, weight: "bold")[MÁSTER UNIVERSITARIO EN ECONOMÍA])
    v(1.5cm)
    line(length: 60%, stroke: uvigo-blue + 1pt)
    v(1cm)
    align(center, text(size: font_sizes.Huge, weight: "bold", fill: uvigo-blue)[#title])
    v(1cm)
    line(length: 60%, stroke: uvigo-blue + 1pt)
    v(2cm)
    align(center, text(size: font_sizes.large)[Presentado por: *#author*])
    v(0.5cm)
    align(center, text(size: font_sizes.large)[Director/a: *#advisor*])
    v(2cm)
    align(center, text(size: font_sizes.large, fill: uvigo-gray)[#year])
  }

  pagebreak()

  // --- ÍNDICE ---
  {
    set par(first-line-indent: 0em)
    heading(level: 1)[Índice]
    outline(title: none, indent: 1.5em, depth: 3)
  }

  pagebreak()

  doc
}


// Plantilla común para ejercicios y trabajos del Máster en Economía.
// Uso recomendado:
// #import "@local...": homework_econ
// #show: homework_econ.with(
//   pdf_title: "AnDec_entrega 1"
//   course: [Análisis de Decisiones Económicas y Mercados],
//   title: [Regla de decisión racional y productividad],
// )
#let homework_econ(
  title: "Título del trabajo",
  author: "Adrián Berges Enfedaque",
  course: "Nombre de la Asignatura",
  date: datetime.today(),
  heading-numbering: "1.1",
  doc,
) = {
  base-styles()

  set heading(numbering: heading-numbering)

  // let pdf-title = (title, author, course).map(it => it.replace(" ", "_")).join("_")

  set document(
    // (title, author).join(" ")+".pdf",
    title: title,
    author: author,
  )

  set page(
    paper: "a4",
    margin: 2.5cm, //(top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: font_sizes.footnotesize, fill: uvigo-gray)
        #h(1fr) #course #h(1fr)
        #line(length: 100%, stroke: uvigo-cyan + 0.5pt)
      ]
    },
    footer: context {
      if counter(page).get().first() > 1 [
        #set text(size: font_sizes.footnotesize, fill: uvigo-gray)
        #line(length: 100%, stroke: uvigo-cyan + 0.5pt)
        #h(1fr) #counter(page).display("1 / 1") #h(1fr)
      ]
    },
  )

  // Portada sencilla
  // {
  //   set par(first-line-indent: 0em)
  //   v(3cm)
  //   set text(size: font_sizes.huge, weight: "bold", fill: uvigo-blue)
  //   align(center, title)
  //   v(1cm)
  //   set text(size: font_sizes.large, fill: uvigo-gray)
  //   align(center, [Autor: #author])
  //   align(center, [#course — #subject])
  //   v(2cm)
  //   line(length: 100%, stroke: uvigo-blue + 1.5pt)
  // }
  align(center)[
    #block(width: 85%, text(size: font_sizes.LARGE, weight: "bold", hyphenate: false)[#course])
    #if title != none {
      v(0.35em)
      emph(title)
    }
  ]

  v(0.8em)

  grid(
    columns: (1fr, 1fr),
    gutter: 1em,
    [*Nombre:* #author],
    align(right)[
      *Fecha:* #if type(date) == datetime { date.display("[day]/[month]/[year]") } else { date }
    ],
  )
  line(length: 100%, stroke: 0.6pt)

  doc
}
