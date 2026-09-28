
// lib.typ - Funciones y configuración compartida (Typst 0.15)

// Colores corporativos UVigo (aproximaciones oficiales)
#let uvigo-blue = rgb("#003366")
#let uvigo-cyan = rgb("#0099CC")
#let uvigo-gray = rgb("#58595B")
#let uvigo-light-gray = rgb("#F2F2F2")

// Estilos base aplicados a todos los documentos
#let font_sizes = (
  "tiny": 6pt,
  "scriptsize": 8pt,
  "footnotesize": 9pt,
  "small": 10pt,
  "normalsize": 11pt,
  "large": 12pt,
  "Large": 14.4pt,
  "LARGE": 17.28pt,
  "huge": 20.74pt,
  "Huge": 24.88pt,
)

#let base-styles() = {
  set text(
    font: ("New Computer Modern", "Latin Modern Math"),
    size: font_sizes.normalsize,
    lang: "es",
  )
  set par(justify: true, leading: 0.65em, first-line-indent: 1.25em, justification-limits: (
    tracking: (min: -0.01em, max: 0.02em),
  ))
  set heading(numbering: "1.1.")

  // Estilo para los títulos
  show heading: set text(weight: "bold")
  show heading.where(level: 1): set text(size: font_sizes.Large) //fill: uvigo-blue
  show heading.where(level: 1): it => block(above: 1.5em, below: 1em, it)
  show heading.where(level: 2): set text(size: font_sizes.large) //fill: uvigo-cyan
  show heading.where(level: 2): it => block(above: 1.2em, below: 0.8em, it)

  show link: set text(fill: uvigo-blue)

  // Configuración de ecuaciones
  set math.equation(numbering: "(1)")
}

// Bloque para resaltar resultados de código (R/Julia)
#let data-result(label: "Salida de datos", body) = {
  block(
    width: 100%,
    fill: uvigo-light-gray,
    inset: 10pt,
    radius: 4pt,
    stroke: uvigo-cyan + 0.5pt,
    {
      set text(size: font_sizes.small)
      text(weight: "bold", fill: uvigo-blue)[#label]
      v(4pt)
      body
    },
  )
}
