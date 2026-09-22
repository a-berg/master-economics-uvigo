#import "@local/homework_template:0.1.0": *
#import "@preview/lilaq:0.6.0" as lq

#show: homework_econ.with(
  course: [Análisis de Decisiones Económicas y Mercados],
  title: [Calculando el equilibrio de mercado],
  pdf_title: "AnDec_ejercicio_4",
  heading-numbering: "1.a.",
)

// Make all diagrams centered by default
#show lq.selector(lq.diagram): it => { align(center)[#it] }
#show lq.selector(lq.diagram): set text(0.8em)

// Some global diagram settings such as xlabel etc
#show: lq.set-diagram(
  xlabel: $Q$,
  ylabel: $p$,
  width: 75%,
  legend: (position: top + left),
)

#let plot_dscurve(x, ds, label) = {
  lq.plot.with(mark: none, label: label)(
    ..x.map(ds).zip(x).filter(((x, _)) => x > 0).fold(((), ()), ((acc1, acc2), (x, y)) => (acc1 + (x,), acc2 + (y,))),
  )
}

#let x = lq.linspace(0, 21)

= Construcción del agregado a partir de las decisiones individuales, y cálculo del equilibrio de mercado.
#set enum(numbering: "i)")

#let consumer-i = p => calc.max(0, 10 - p)
#let consumer-h = p => calc.max(0, 20 - 4 * p)
#let producer-j = p => calc.max(0, p - 2)
#let producer-k = p => calc.max(0, 2 * p)

== Construcción de la curvas de demanda de mercado.
#quote(block: true)[Considere dos consumidores i y h, donde sus respectivas curvas de demanda
  individuales de una mercancía son:
  $
    q^i & = d^i (p) = 10 - p \
    q^h & = d^h (p) = 20 - 4p.
  $

  + Obtenga la curva de demanda de mercado de un bien $Q = D(p)$ analíticamente
    e gráficamente como suma horizontal de las demandas individuales ($Q = D(p)
    ≡ d_i (p) + d_h (p)$).
  + Dibuje las curvas de demanda individuales, y la curva de demanda de mercado
    una al lado de la otra horizontalmente. En los tres gráficos indique las
    cantidades individuales y las de mercado que se consumen a un precio $p
    = 4$.
]

#{
  show: lq.layout

  grid(
    columns: 3,
    lq.diagram(legend: none, plot_dscurve(x, consumer-i, $q^i (p)$)),
    lq.diagram(legend: none, plot_dscurve(x, consumer-h, $q^h (p)$)),
    lq.diagram(legend: none, plot_dscurve(x, p => consumer-i(p) + consumer-h(p), $D(p)$)),
  )
}

#lq.diagram(
  title: [Curvas de demanda],
  // xlim: (auto, 35),
  plot_dscurve(x, producer-j, $q^j (p)$),
  plot_dscurve(x, producer-k, $q^k (p)$),
  plot_dscurve(x, p => producer-j(p) + producer-k(p), $S (p)$),
)
