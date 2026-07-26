
// lib.typ - Funciones y configuración compartida (Typst 0.15)

// Colores corporativos UVigo (aproximaciones oficiales)
#let uvigo-blue = rgb("#003366")
#let uvigo-cyan = rgb("#0099CC")
#let uvigo-gray = rgb("#58595B")
#let uvigo-light-gray = rgb("#F2F2F2")

// Estilos base aplicados a todos los documentos
#let base-styles() = {
  set text(
    font: ("New Computer Modern", "Latin Modern Math"), 
    size: 11pt,
    lang: "es"
  )
  set par(justify: true, leading: 0.65em, first-line-indent: 1.25em)
  set heading(numbering: "1.1.")
  
  // Estilo para los títulos
  set heading(where level: 1)[
    #set text(size: 14pt, weight: "bold", fill: uvigo-blue)
    #block(above: 1.5em, below: 1em)
  ]
  set heading(where level: 2)[
    #set text(size: 12pt, weight: "bold", fill: uvigo-cyan)
    #block(above: 1.2em, below: 0.8em)
  ]
  
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
      set text(size: 10pt)
      text(weight: "bold", fill: uvigo-blue)[#label]
      v(4pt)
      body
    }
  )
}
