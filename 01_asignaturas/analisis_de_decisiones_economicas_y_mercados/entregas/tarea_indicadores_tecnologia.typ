#import "@local/master-uvigo-templates:0.1.0": homework_econ
#import "@preview/lilaq:0.6.0" as lq

// #let author = "Adrian_Berges_"
// #let title = "Indicadores de la Tecnología"
// #let course = "AnDec"
// #let output_title = (author, course, title).join("_").replace(" ", "_")

#show: homework_econ.with(
  course: [Análisis de Decisiones Económicas y Mercados],
  title: "Indicadores de la Tecnología",
  heading-numbering: "a.1)",
)
#show: lq.set-diagram(
  xaxis: (tick-args: (tick-distance: 1)),
  yaxis: (tick-args: (tick-distance: 1)),
  legend: (position: (100% + .5em, 0%)),
)


#set text(lang: "es")

= Tecnología de la cafetería

Se da la producción por hora, $Q(L, K)$, donde $L$ es el número de camareros/as
y $K$ el número de salidas de la cafetera.

#table(
  columns: (1.7fr, 1fr, 1fr, 1fr),
  inset: 8pt,
  align: center,
  table.header([*Camareros/as ($L$)*], [*1 salida*], [*2 salidas*], [*3 salidas*]),
  [*1*], [10 cafés], [30 cafés], [50 cafés],
  [*2*], [30 cafés], [50 cafés], [60 cafés],
  [*3*], [50 cafés], [60 cafés], [100 cafés],
)

Los mapas de isocuantas por tanto serán:

#lq.diagram(
  width: 11cm,
  height: 9cm,
  xlabel: [Camareros/as ($L$)],
  ylabel: [Salidas de la cafetera ($K$)],
  lq.plot((1,), (1,), color: rgb("#777777"), mark: "o", label: [$Q=10$]),
  lq.plot((1, 2), (2, 1), color: rgb("#386cb0"), mark: "s", label: [$Q=30$]),
  lq.plot((1, 2, 3), (3, 2, 1), color: rgb("#e07a1f"), mark: "o", label: [$Q=50$]),
  lq.plot((2, 3), (3, 2), color: rgb("#2b8a5c"), mark: "^", label: [$Q=60$]),
  lq.plot((3,), (3,), color: rgb("#a23b72"), mark: "d", label: [$Q=100$]),
)
// Sólo se representan las combinaciones observadas en el enunciado. No se
// interpolan curvas continuas entre ellas, pues la tabla no indica la producción
// para cantidades intermedias de inputs.
= Producción de las máquinas

== Gráficos de producción a corto plazo

La cafetera elegida tiene dos salidas: $K=2$. El número de camareros/as $L$ es
el _input_ variable.

#lq.diagram(
  width: 10cm,
  height: 6cm,
  xlabel: [Camareros/as ($L$)],
  ylabel: [Salidas de la cafetera ($K$)],
  lq.plot((1, 2), (2, 1), color: rgb("#386cb0"), mark: "s", label: [$Q=30$]),
  lq.plot((1, 2, 3), (3, 2, 1), color: rgb("#e07a1f"), mark: "o", label: [$Q=50$]),
  lq.plot((2, 3), (3, 2), color: rgb("#2b8a5c"), mark: "^", label: [$Q=60$]),
  lq.plot((1, 2, 3), (2, 2, 2), color: black, label: [$K=2$], stroke: (2pt)),
)

La función de producción a corto plazo es $Q(L, 2)$: para $L=1,2,3$ toma los
valores $30,50,60$ cafés por hora, respectivamente.

#lq.diagram(
  width: 10cm,
  height: 6cm,
  xlabel: [Camareros/as ($L$)],
  ylabel: [Cafés por hora ($Q$)],
  yaxis: (tick-args: (tick-distance: auto)),
  lq.plot((1, 2, 3), (30, 50, 60), color: rgb("#e07a1f"), mark: "o", label: [$Q(L,2)$]),
)

== Valores de producción media y producción marginal

La productividad media es $"PMe"_L(L)=Q(L,2)/L$. La productividad marginal al
contratar una unidad adicional es $"PMg"_L(L)=(Q(L,2)-Q(L-1,2))/(L-(L-1))$. Por
tanto, tenemos:

#table(
  columns: (0.7fr, 1.1fr, 1.4fr, 1.6fr),
  inset: 7pt,
  align: center,
  table.header([*$L$*], [*$Q(L,2)$*], [*Productividad media*], [*Productividad marginal*]),
  [1], [30], [$30/1=30$], [--],
  [2], [50], [$50/2=25$], [$(50-30)/(2-1)=20$],
  [3], [60], [$60/3=20$], [$(60-50)/(3-2)=10$],
)

No podemos asignar un valor numérico a la productividad marginal del primer
camarero/a, ya que no está definido.

== Curvas de producción media y producción marginal

#lq.diagram(
  width: 10cm,
  height: 6cm,
  xlim: (0.7, 3.3),
  ylim: (0, 35),
  xlabel: [Camareros/as ($L$)],
  ylabel: [Cafés por camarero/a y hora],
  yaxis: (tick-args: (tick-distance: auto)),
  lq.plot((1, 2, 3), (30, 25, 20), color: rgb("#386cb0"), mark: "o", label: [Productividad media]),
  lq.plot((2, 3), (20, 10), color: rgb("#e07a1f"), mark: "s", label: [Productividad marginal]),
)



