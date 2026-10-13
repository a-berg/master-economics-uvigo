#import "base-definitions.typ": *

#let essay(
  essay-title: "Título del Ensayo",
  author: "Adrián Berges Enfedaque",
  abstract: [#lorem(200)],
  title-page: (essay-title, author, year) => [#title[#essay-title] \ #author \ #datetime.today().display("[year]")],
  with-index: true,
  doc,
) = {
  set document(
    title: essay-title,
    author: author,
  )

  set page(footer: context {
    set align(center)
    set text(size: font_sizes.footnotesize)
    counter(page).display("i")
  })

  // Ajustar numeración de headings para una (1.1.1)
  set heading(numbering: "1.1.1")
  // Ajustar titulo
  show title: set text(size: font_sizes.Huge, weight: "black")
  show title: set align(center)
  show title: set block(below: 1.2em)

  // --- PORTADA ---
  {
    title-page(essay-title, author)
    pagebreak()
  }

  // abstract
  if abstract != none {
    align(center)[
      *Resumen*\
      #abstract
    ]
    pagebreak()
  }

  // --- ÍNDICE ---
  if with-index {
    set par(first-line-indent: 0em)
    outline(indent: 1.5em, depth: 3)
    pagebreak()
  }

  counter(page).update(1)
  set page(
    footer: context {
      set align(center)
      set text(size: font_sizes.footnotesize)
      counter(page).display("1")
    },
  )
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
  author: ("Adrián Berges Enfedaque",),
  course: "Nombre de la Asignatura",
  date: datetime.today(),
  heading-numbering: "1.1",
  doc,
) = {
  // show: base-styles

  set heading(numbering: heading-numbering)

  // let pdf-title = (title, author, course).map(it => it.replace(" ", "_")).join("_")

  set document(
    // (title, author).join(" ")+".pdf",
    title: title,
    author: author,
  )

  set page(
    paper: "a4",
    // margin: 2.5cm, //(top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 {
        set text(size: font_sizes.footnotesize, fill: uvigo-gray)
        h(1fr)
        course
        h(1fr)
        line(length: 100%, stroke: uvigo-cyan + 0.5pt)
      }
    },
    footer: context {
      {
        set text(size: font_sizes.footnotesize, fill: uvigo-gray)
        line(length: 100%, stroke: uvigo-cyan + 0.5pt)
        h(1fr)
        counter(page).display("1")
        h(1fr)
      }
    },
  )

  align(center)[
    #block(width: 80%, text(size: font_sizes.LARGE, weight: "bold", hyphenate: false)[#course])
    #if title != none {
      v(0.35em)
      emph(title)
    }
  ]

  v(0.8em)

  grid(
    columns: (1fr, 1fr),
    gutter: 1em,
    [*Nombre:* #author.join(", ").],
    align(right)[
      *Fecha:* #if type(date) == datetime { date.display("[day]/[month]/[year]") } else { date }
    ],
  )
  line(length: 100%, stroke: 0.6pt)

  doc
}
