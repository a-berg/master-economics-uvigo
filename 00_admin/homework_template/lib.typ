// Plantilla común para ejercicios y trabajos del Máster en Economía.
// Uso recomendado:
// #import "plantilla_academica.typ": trabajo
// #show: trabajo.with(
//   pdf_title: "AnDec_entrega 1"
//   course: [Análisis de Decisiones Económicas y Mercados],
//   title: [Regla de decisión racional y productividad],
// )

#let homework_econ(
  pdf_title: "",
  course: "",
  title: none,
  author: "Adrián Berges Enfedaque",
  date: datetime.today(),
  heading-numbering: "1.1",
  body,
) = {
  let font_sizes = (
    "tiny":         6pt,
    "scriptsize":   8pt,
    "footnotesize": 9pt,
    "small":        10pt,
    "normalsize":   11pt,
    "large":        12pt,
    "Large":        14.4pt,
    "LARGE":        17.28pt,
    "huge":         20.74pt,
    "Huge":         24.88pt,
  ) 
  set document(
    title: pdf_title,
    author: (author,),
  )

  set page(
    paper: "a4",
    margin: 1.75in,
    numbering: "1",
  )

  set text(
    lang: "es",
    font: "Libertinus Serif",
    size: font_sizes.normalsize,
  )

  set par(
    justify: true,
    leading: 0.55em,
    first-line-indent: 1.8em,
    justification-limits: (
      tracking: (min: -0.01em, max: 0.02em),
    ),
  )

  set heading(numbering: heading-numbering)
  show heading.where(level: 1): it => block(above: 1.4em, below: 1em)[
    #set text(size: font_sizes.Large, weight: "bold")
    #it
  ]
  show heading.where(level: 2): set text(size: font_sizes.large, weight: "bold")
  show link: set text(fill: blue)
  show quote.where(block: true): emph
  show quote.where(block: true): set block(above: 1.4em, below: 1em)

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
    [*Nombre:* #author],
    align(right)[
      *Fecha:* #if type(date) == datetime {
        date.display("[day]/[month]/[year]")
      } else {
        date
      }
    ],
  )
  line(length: 100%, stroke: 0.6pt)

  body
}
