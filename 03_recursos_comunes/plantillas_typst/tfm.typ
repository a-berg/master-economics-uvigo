
// Plantilla para el TFM
#import "lib.typ": *

#let tfm(
  title: "Título del TFM",
  author: "Tu Nombre",
  advisor: "Nombre del Director",
  year: "2024/2025",
  doc
) = {
  base-styles()
  
  // Márgenes tipo libro (izquierdo más amplio para encuadernación)
  set page(
    paper: "a4",
    margin: (top: 3cm, bottom: 2.5cm, inner: 3.5cm, outer: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: uvigo-gray)
        #h(1fr) #text(italics)[Máster en Economía — Universidade de Vigo] #h(1fr)
      ]
    },
    footer: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: uvigo-gray)
        #h(1fr) #counter(page).display("1") #h(1fr)
      ]
    }
  )
  
  // Ajustar numeración de headings para TFM (1.1.1)
  set heading(numbering: "1.1.1")

  // --- PORTADA ---
  {
    set par(first-line-indent: 0em)
    v(2cm)
    align(center, text(size: 14pt, fill: uvigo-cyan)[Universidade de Vigo])
    align(center, text(size: 12pt, fill: uvigo-gray)[Facultade de Ciencias Económicas e Empresariais])
    v(2cm)
    align(center, text(size: 12pt, weight: "bold")[MÁSTER UNIVERSITARIO EN ECONOMÍA])
    v(1.5cm)
    line(length: 60%, stroke: uvigo-blue + 1pt)
    v(1cm)
    align(center, text(size: 24pt, weight: "bold", fill: uvigo-blue)[#title])
    v(1cm)
    line(length: 60%, stroke: uvigo-blue + 1pt)
    v(2cm)
    align(center, text(size: 12pt)[Presentado por: *#author*])
    v(0.5cm)
    align(center, text(size: 12pt)[Director/a: *#advisor*])
    v(2cm)
    align(center, text(size: 12pt, fill: uvigo-gray)[#year])
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
