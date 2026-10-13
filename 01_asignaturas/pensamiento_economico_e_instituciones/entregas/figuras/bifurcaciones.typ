// Árbol de síntesis: las conexiones expresan problemas y respuestas,
// no una genealogía exclusiva ni una sustitución completa entre enfoques.
#let arbol-bifurcaciones(cetz) = {
  set text(size: 8.5pt, hyphenate: false)
  set par(first-line-indent: 0pt, justify: false, leading: 0.2em, spacing: 0pt)
  cetz.canvas(length: 1cm, {
    import cetz.draw: content, line
    let azul = rgb("#254B64")
    let claro = rgb("#EEF4F7")
    let gris = rgb("#777777")
    let nodo(pos, titulo, cuerpo, ancho: 3.5cm, alto: 2.1cm, relegado: false) = {
      content(pos, block(
        width: ancho, height: alto, inset: 5pt, radius: 3pt,
        fill: if relegado { rgb("#F4F4F4") } else { claro },
        stroke: if relegado { (paint: gris, thickness: 0.7pt, dash: "dashed") } else { azul + 0.7pt },
        align(center + horizon)[
          #text(weight: "bold", fill: if relegado { gris } else { azul }, titulo)
          #linebreak()
          #cuerpo
        ],
      ))
    }
    let enlace(a, b, ..puntos) = line(a, ..puntos.pos(), b, stroke: azul + 0.7pt, mark: (end: ">"))

    nodo((0, 0), [Haavelmo · 1944], [Probabilidad, estructura y autonomía], ancho: 6cm, alto: 1.25cm)
    enlace((0, -0.65), (0, -1.5))
    nodo((0, -2.2), [Cowles · años 1940–1950], [Identificación y estimación de sistemas\ Programa influyente en econometría], ancho: 7.8cm, alto: 1.4cm)
    enlace((0, -2.95), (0, -3.7))
    nodo((0, -4.5), [Bifurcación · años 1970–1980], [Lucas: invariancia · Sims: restricciones\ Leamer: sensibilidad · LaLonde: comparación], ancho: 9cm, alto: 1.6cm)

    // Una rama cuestionada y tres respuestas que continúan coexistiendo.
    for x in (-5.7, -1.9, 1.9, 5.7) {
      enlace((0, -5.35), (x, -6.5), (0, -5.85), (x, -5.85))
    }
    nodo((-5.7, -7.55), [Modelos tradicionales], [Grandes sistemas:\ exclusiones discutidas], relegado: true)
    nodo((-1.9, -7.55), [Renovación estructural], [Decisiones, expectativas y mecanismos])
    nodo((1.9, -7.55), [VAR y sensibilidad], [Otras restricciones;\ distintas especificaciones])
    nodo((5.7, -7.55), [Experimentos y diseños], [Asignación y variación para identificar efectos])

    for x in (-5.7, -1.9, 1.9, 5.7) {
      enlace((x, -8.65), (x, -9.4))
    }
    nodo((-5.7, -10.55), [Práctica relegada], [Pierde autoridad causal; persiste la modelización], alto: 2.3cm, relegado: true)
    nodo((-1.9, -10.55), [Tradición activa], [Macroeconomía y organización industrial: escenarios y políticas], alto: 2.3cm)
    nodo((1.9, -10.55), [Vías persistentes], [VAR en macroeconomía; sensibilidad como exigencia transversal], alto: 2.3cm)
    nodo((5.7, -10.55), [Expansión desde 1990], [Trabajo, educación, salud y desarrollo], alto: 2.3cm)
    enlace((5.7, -11.75), (5.7, -12.5))
    nodo((5.7, -13.45), [Revisión · 2021–2024], [DiD: heterogeneidad y adopción escalonada], alto: 1.8cm)

    // Estos lenguajes y herramientas cruzan ramas; no se dibujan como
    // descendientes exclusivos de la revolución de la credibilidad.
    content((-2, -13.45), block(width: 10.5cm, inset: 9pt, stroke: rgb("#BBBBBB") + 0.5pt)[
      *Debates y herramientas transversales*
      #v(4pt)
      Resultados potenciales y grafos causales: lenguajes de supuestos.
      Datos y aprendizaje automático: nuevas posibilidades de estimación.
      Las ramas activas pueden combinar evidencia y modelos.
    ])
  })
}
