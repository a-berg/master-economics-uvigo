#import "@local/homework_template:0.1.0": *
#import "@preview/lilaq:0.6.0" as lq

#show: homework_econ.with(
  course: [Análisis de Decisiones Económicas y Mercados],
  title: [Construyendo curvas agregadas],
  pdf_title: "AnDec_entrega_2a",
)

#show: lq.set-diagram(
  xlabel: $p$,
  ylabel: $Q$,
)

#let demandA = p => calc.max(0, 12 - 2 * p)
#let demandB = p => calc.max(0, 21 - p)
#let supplyJ = p => calc.max(0, 5 * p - 1)
#let supplyK = p => calc.max(0, p - 2)
#let x = lq.linspace(0, 10)


= Demanda del mercado de una mercancía

Tenemos que las demandas individuales de los individuos A y B son:

$
  q^A & = d^A (p) = max{0, 21 - p} \
  q^B & = d^B (p) = max{0, 12 - 2p}
$

Cuyos gráficos individuales son:

#align(center)[
  #lq.diagram(
    lq.plot(x, demandA, mark: none),
    lq.plot(x, demandB, mark: none),
  )
]

La definición de la demanda agregada de una mercancía es:

$
  Q = D(p) = sum_(i #sym.in I) d^i (p).
$

Dado que la demanda de un bien no puede ser negativa, la suma debe tener en
cuenta los tramos en los que cada demanda individual es 0 debido a que el precio
es demasiado alto para el consumidor $i$. Esto da la siguiente función:

$
  D(p) = cases(
    0 "si" p > 21,
    21 - p "si" 6 < p <= 21,
    33 - 3p "si" 0 <= p <=6,
  )
$

El diagrama será:

#align(center)[#lq.diagram(
    lq.plot(x, p => demandA(p) + demandB(p), mark: none),
  )
]
= Oferta del mercado de una mercancía

En este caso, las ofertas individuales de las firmas J y K son:

$
  q^J & = s^J (p) = max{0, 5p - 1} \
  q^K & = s^K (p) = max{0, p - 2}
$

Cuyos gráficos individuales son:

#align(center)[
  #lq.diagram(
    lq.plot(x, supplyJ, mark: none),
    lq.plot(x, supplyK, mark: none),
  )
]
Ahora, la definición de la oferta agregada de una mercancía es:

$
  Q = S(p) = sum_(i #sym.in I) d^i (p).
$

Nuevamente, dado que la oferta de cada agente no puede ser negativa, se trata
de una función a trozos, definida como:

$
  S(p) = cases(
    0 "si" p < frac(1, 5),
    p - 2 "si" frac(1, 5) <= p < 2,
    6p - 3 "si" p >= 2,
  )
$

El diagrama de la curva agregada será:

#align(center)[#lq.diagram(
    lq.plot(x, p => supplyJ(p) + supplyK(p), mark: none),
  )
]
