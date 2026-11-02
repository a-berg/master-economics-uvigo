#import "@preview/lilaq:0.6.0" as lq
#import "@local/master-uvigo-templates:0.1.0": uvigo-blue, uvigo-gray

#let data = json("../output/apendice_lilaq/graficas.json")
#set document(title: "China y España · Apéndice de gráficas", author: "Adrián Berges Enfedaque")
#set text(font: "Liberation Sans", size: 10pt, lang: "es")
#set par(first-line-indent: 0pt, leading: .5em)
#set page(
  paper: "a4",
  margin: (x: 20mm, top: 22mm, bottom: 19mm),
  header: text(size: 8pt, fill: uvigo-gray)[APÉNDICE DE GRÁFICAS #h(1fr) CHINA Y ESPAÑA],
  footer: context text(size: 8pt, fill: uvigo-gray)[Primera compilación para revisión #h(1fr) #counter(page).display("1") / #data.count],
)

#let series-legend(entries) = {
  let columns = if entries.len() > 4 { 3 } else if entries.len() > 1 { 2 } else { 1 }
  grid(columns: (1fr,) * columns, column-gutter: 10pt, row-gutter: 5pt,
    ..entries.map(e => grid(columns: (14pt, 1fr), column-gutter: 4pt, align: horizon,
      line(length: 12pt, stroke: 1.5pt + rgb(e.color)), text(size: 8.5pt, e.label)))
  )
}

#let chart(panel, compact: false) = {
  set text(size: if compact { 8pt } else { 9pt })
  let plots = ()
  for series in panel.series {
    for run in series.runs {
      plots.push(lq.plot(
        run.x, run.y,
        color: rgb(series.color),
        stroke: if panel.kind == "scatter" { none } else { 1.25pt },
        mark: if panel.kind == "scatter" or run.x.len() == 1 { "o" } else { none },
        mark-size: if panel.kind == "scatter" { 3.2pt } else { 4.5pt },
      ))
    }
  }
  if panel.show_zero {
    plots.push(lq.hlines(0, stroke: (paint: luma(65%), thickness: .5pt, dash: "dashed")))
  }
  lq.diagram(
    width: 100%, height: 0% + if compact { 65mm } else { 78mm },
    title: text(weight: "bold", size: 10pt, panel.title),
    xlabel: text(size: if compact { 8pt } else { 9pt }, panel.xlabel),
    ylabel: text(size: if compact { 8pt } else { 9pt }, panel.ylabel),
    legend: none,
    xlim: array(panel.xlim), ylim: array(panel.ylim),
    xaxis: (ticks: panel.xticks.map(t => (t.at(0), t.at(1))), subticks: none, exponent: 0, offset: 0, mirror: none),
    yaxis: (ticks: panel.yticks.map(t => (t.at(0), t.at(1))), subticks: none, exponent: 0, offset: 0, mirror: none),
    grid: (stroke: .35pt + luma(90%)),
    ..plots,
  )
}

#for (i, fig) in data.figures.enumerate() {
  if i > 0 { pagebreak() }
  text(size: 10pt, fill: uvigo-blue, weight: "bold")[GRÁFICO #fig.id]
  v(3pt)
  block(width: 100%, text(size: 16pt, weight: "bold", fig.title))
  v(9pt)
  series-legend(fig.legend)
  v(12pt)
  if fig.panels.len() == 4 {
    grid(columns: (1fr, 1fr), column-gutter: 12pt, row-gutter: 12pt,
      ..fig.panels.map(p => chart(p, compact: true)))
  } else {
    chart(fig.panels.at(0))
    v(10pt)
    chart(fig.panels.at(1))
  }
  v(12pt)
  block(width: 100%, stroke: (top: .5pt + luma(80%)), inset: (top: 7pt), {
    set text(size: 8.5pt, fill: uvigo-gray)
    strong[Fuente: ]
    fig.source
    linebreak()
    strong[Cobertura: ]
    fig.coverage
    v(3pt)
    strong[Nota: ]
    fig.note
    if fig.status == "PARCIAL" {
      v(3pt)
      text(weight: "bold")[Resultado parcial: consultar la limitación indicada antes de interpretar la comparación.]
    }
  })
}
