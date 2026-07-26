
// Plantilla para trabajos de asignatura
#import "lib.typ": *

#let asignatura(
  title: "Título del trabajo",
  author: "Tu Nombre",
  course: "Máster en Economía",
  subject: "Nombre de la Asignatura",
  doc
) = {
  base-styles()
  
  set page(
    paper: "a4",
    margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: uvigo-gray)
        #h(1fr) #subject #h(1fr)
        #line(length: 100%, stroke: uvigo-cyan + 0.5pt)
      ]
    },
    footer: context {
      if counter(page).get().first() > 1 [
        #set text(size: 9pt, fill: uvigo-gray)
        #line(length: 100%, stroke: uvigo-cyan + 0.5pt)
        #h(1fr) #counter(page).display("1 / 1") #h(1fr)
      ]
    }
  )

  // Portada sencilla
  {
    set par(first-line-indent: 0em)
    v(3cm)
    set text(size: 22pt, weight: "bold", fill: uvigo-blue)
    align(center, title)
    v(1cm)
    set text(size: 12pt, fill: uvigo-gray)
    align(center, [Autor: #author])
    align(center, [#course — #subject])
    v(2cm)
    line(length: 100%, stroke: uvigo-blue + 1.5pt)
  }

  doc
}
