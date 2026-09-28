#import "@local/master-uvigo-templates:0.1.0": homework_econ
#import "@preview/lilaq:0.6.0" as lq
#import "@preview/tiptoe:0.4.0"

#show: homework_econ.with(
  course: [Análisis de Decisiones Económicas y Mercados],
  title: [Calculando el equilibrio de mercado],
  heading-numbering: "1.a.1",
)
#show quote.where(block: true): it => emph(it)
#set text(lang: "es")
#set math.equation(numbering: "(1)")

// #show ref: it => {
//   let eq = math.equation
//   let el = it.element
//   // Skip all other references.
//   if el == none or el.func() != eq { return it }
//   // Override equation references.
//   link(el.location(), counter(eq).display(at: el.location()))
// }

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

#let enunciado(content) = {
  set text(style: "italic")
  block(fill: luma(200), inset: 8pt, radius: 4pt, stroke: 1pt)[#content]
}

#let x = lq.linspace(0, 21)

= Construcción del agregado a partir de las decisiones individuales, y cálculo del equilibrio de mercado.
#set enum(numbering: "i)")

#let consumer-i = p => calc.max(0, 10 - p)
#let consumer-h = p => calc.max(0, 20 - 4 * p)
#let producer-j = p => calc.max(0, p - 2)
#let producer-k = p => calc.max(0, 2 * p)

== Construcción de la curvas de demanda de mercado.
#enunciado[
  Considere dos consumidores i y h, donde sus respectivas curvas de demanda
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

Para combinar las curvas individuales de demanda y obtener la curva de demanda
de mercado agregada tenemos que obtener los ceros de las demandas individuales,
que marcan los puntos de transición:

$
  q^i > 0 & <=> p < 10, \
  q^h > 0 & <=> 4p < 20 <=> p < 5
$

Es decir, para $p in [0, 5)$ tendremos $q^i > 0 #sym.and q^h > 0$, mientras que con
$p in [5, 10)$ será $q^i > 0 #sym.and q^h < 0$. Por tanto:

$
  D(p) = cases(
    q^i + q^h & "si" 0 <= p < 5,
    q^i & "si" 5 <= p < 10,
    0 & "si" p >= 10,
  ) = cases(
    30 - 5p & "si" 0 <= p < 5,
    10 - p & "si" 5 <= p < 10,
    0 & "si" p >= 10,
  ).
$ <eq:Dp>

La representación gráfica de cada una de las curvas se puede ver en
// @fig:curvas-agregada-ejercicio-1.

#{
  show: lq.layout

  figure(
    grid(
      columns: 3,
      lq.diagram(legend: (position: top + left), plot_dscurve(x, consumer-i, $q^i (p)$)),
      lq.diagram(legend: (position: top + left), plot_dscurve(x, consumer-h, $q^h (p)$)),
      lq.diagram(legend: (position: top + left), plot_dscurve(x, p => consumer-i(p) + consumer-h(p), $D(p)$)),
    ),
    caption: "Curvas de demanda individuales y agregada.",
  )
} <fig:curvas-agregada-ejercicio-1>

// #lq.diagram(
//   title: [Curvas de demanda],
//   // xlim: (auto, 35),
//   plot_dscurve(x, producer-j, $q^j (p)$),
//   plot_dscurve(x, producer-k, $q^k (p)$),
//   plot_dscurve(x, p => producer-j(p) + producer-k(p), $S (p)$),
// )

== Construcción de la curvas de oferta de mercado.

#enunciado[
  Considere dos empresas j y k, donde sus respectivas curvas de oferta
  individuales de una mercancía son:
  $
    q^j & = o^j (p) = p -2 \
    q^k & = o^k (p) = 2p.
  $

  + Obtenga la curva de oferta de mercado de un bien $Q = O(p)$ analíticamente
    e gráficamente como suma horizontal de las ofertas individuales ($Q = O(p)
    ≡ o^j (p) + o^k (p)$).
  + Dibuje las curvas de oferta individuales, y la curva de oferta de mercado
    una al lado de la otra horizontalmente. En los tres gráficos indique las
    cantidades individuales y las de mercado que se consumen a un precio $p
    = 4$.
]

El razonamiento es exactamente igual que en el caso anterior. Los precios que
marcan el cambio de régimen son:

$
  q^j > 0 & <=> p > 2, \
  q^k > 0 & <=> p > 0
$

y por tanto la curva de oferta agregada es:

$
  O(p) = cases(
    q^j + q^k & "si" p > 2,
    q^k & "si" 0<p<=2,
    0 & "en otro caso",
  ) = cases(
    3p - 2 & "si" p > 2,
    2p & "si" 0<p<=2,
    0 & "en otro caso",
  ).
$ <eq:Op>

La representación gráfica de cada una de las curvas se puede ver en
#{
  show: lq.layout

  figure(
    grid(
      columns: 3,
      lq.diagram(legend: (position: top + left), plot_dscurve(x, producer-j, $o^j (p)$)),
      lq.diagram(legend: (position: top + left), plot_dscurve(x, producer-k, $o^k (p)$)),
      lq.diagram(legend: (position: top + left), plot_dscurve(x, p => producer-j(p) + producer-k(p), $O(p)$)),
    ),
    caption: "Curvas de oferta individuales y agregada.",
  )
} <fig:curvas-oferta-ejercicio-1>

== Equilibrio de mercado de la mercancı́a

#enunciado[

  Indique cuántas unidades consumen en el equilibrio el consumidor i y el h, y
  cuántas unidades producen en el equilibrio la empresa j y k.
]

El precio de equilibrio $p^*$ es el precio para el que se cumple $D(p^*) = O(p^*)$.
Para hacer bien el cálculo deberíamos comparar todas las combinaciones de tramos
posibles, no obstante, si comenzamos comparando el intervalo $[2, 6]$ obtenemos
una solución plausible:

$
  30 - 5p^* & = 3p^* - 2 \
         32 & = 8p^* \
          4 & = p^*.
$

Siendo además $Q^* = 10.$ Puede consultarse en la @fig:equilibrio-1.

En éste nivel de precios, los consumos y ofertas parciales son:

$
  q^i & = 10 - p^* = 6 \
  q^h & = 20 - 4p^* = 4 \
  q^j & = p^* - 2 = 2 \
  q^k & = 2p^* = 8.
$

#figure(
  lq.diagram(
    width: 10cm,
    height: 6cm,
    xlim: (0, 30),
    ylim: (0, 12),
    legend: (position: (100% + .5em, 0%)),
    plot_dscurve(x, p => consumer-i(p) + consumer-h(p), $D(p)$),
    plot_dscurve(x, p => producer-j(p) + producer-k(p), $O(p)$),
  ),
  caption: "Equilibrio.",
) <fig:equilibrio-1>

== Análisis de Bienestar

#enunciado[
  Calcule:
  + El Excedente del Consumidor, el Excedente del Productor y el Excedente
    Total a partir de las funciones de Demanda de Mercado y Oferta de Mercado.
  + El bienestar de los consumidores i y h. Compruebe que la suma del
    bienestar de los consumidores coincide con el Excedente del Consumidor.
  + El bienestar de las empresas j y k. Compruebe que la suma del bienestar de
    las empresas coincide con el Excedente del Productor.
]

El Excedente del Consumidor es el área entre la curva de demanda agregada $D(p)$ y
el eje de ordenadas, desde el par $(p^*, Q^*)$ hasta $(p_max, 0)$. Asimismo el
Excedente del Productor es el área entre la curva de oferta agregada $O(p)$ y el eje
de ordenadas desde el par $(p^*, Q^*)$ hasta $(0, 0)$.

Para calcular el Excedente del Consumidor, partamos de la @eq:Dp. El área que queremos
calcular es igual al área bajo la curva:

#set math.lr(size: 150%)

$
  "EC" & = integral_4^10 D(p) dif p = integral_4^5 D(p)dif p + integral_5^10 D(p)dif p \
       & = integral_4^5 (30 - 5p)dif p + integral_5^10 (10 - p)dif p \
       & = lr(30 p - 5/2 p^2|)_4^5 + lr(10p - p^2/2|)_5^10 \
       & = 7.5 + 12.5 = 20.
$

Asimismo el Excedente del Productor se usaría la @eq:Op, integrando de forma similar:

$
  "EP" & = integral_0^4 O(p) dif p = integral_0^2(p)dif p + integral_2^4 O(p)dif p \
       & = integral_0^2 (2p)dif p + integral_2^4 (3p-2)dif p \
       & = lr(p²|)_0^2 + lr(3/2p² - 2p|)_2^4 \
       & = 4 + 14 = 18.
$

El Excedente Total es la suma de ambos excedentes: $"ET" = "EC" + "EP" = 38.$
Ahora, queda calcular las áreas individuales para comprobar que los excedentes
son iguales a la suma del bienestar de cada agente:

$
  "EC"_i & = integral_4^10 (10-p) dif p = 18 \
  "EC"_h & = integral_4^5 (20-4p) dif p = 2 \
  "EP"_j & = integral_2^4 (p - 2) dif p = 2 \
  "EP"_k & = integral_0^4 2p dif p = 16.
$

Podemos comprobar que $"EC"_i + "EC"_h = "EC"$ y $"EP"_j + "EP"_k = "EP".$

// #figure(
//   lq.diagram(
//     width: 10cm,
//     height: 6cm,
//     xlim: (0, 10),
//     ylim: (0, 12),
//     legend: (position: (100% + .5em, 0%)),
//     plot_dscurve(x, p => consumer-i(p) + consumer-h(p), $D(p)$),
//     plot_dscurve(x, p => producer-j(p) + producer-k(p), $O(p)$),
//   ),
//   caption: "Equilibrio."
// ) <fig:excedentes>


= Bienes sustitutivos, complementarios y neutros

#enunciado[

  En una ciudad la demanda y la oferta de un bien pueden expresarse mediante las
  siguientes funciones:
  $
    Q^D & = −2P + 1.5M + 6P S − 4P T + 300 \
    Q^S & = 2P − 8P C + 1494
  $
  siendo:
  - $Q^D$ Cantidad demandada de bacalao al mes (en toneladas)
  - $Q^S$: Cantidad ofrecida de bacalao al mes (en toneladas)
  - $P$: Precio de kilo de bacalao (en Euros)
  - $P T$: Precio del kilo de tomate frito (en Euros), cuyo valor es de 0,75 Euros
  - $P S$: Precio del kilo de sardinas (en Euros), cuyo valor es de 2,5 Euros,
  - $P C$: Precio del litro de combustible (en Euros), cuyo valor es de 0,75 Euros,
  - $M$: Renta media mensual familiar (en Euros) cuyo valor es 800 Euros.

  #set enum(numbering: "a)")

  Se pide:
  + Observando la función de demanda, señale las caracterı́sticas del bien (substitutivo o comple-
    mentario).
  + Obtenga las expresiones de las curvas de oferta y demanda agregadas y represéntelas gráficamente,
  + Calcule el equilibrio en este mercado. Indique por qué el precio de equilibrio va a ser el que
    obtuvo y no otro. (Pista. ¿Que pasarı́a si el precio fuese superior o inferior al precio de
    equilibrio?)
]

Según la función de demanda observada, la sardina es un producto sustitutivo y
el tomate, complementario. Para demostrarlo, veamos las derivadas parciales de
$Q^D$ respecto a dichos productos:

$
  (partial Q^D) / (partial P T) = -4 quad quad
  (partial Q^D) / (partial P S) = 6.
$

De aquí, observamos que: un aumento del precio de las sardinas aumenta la
demanda del bacalao (por tanto se consume en su lugar); mientras que un
aumento del precio del tomate baja la demanda del bacalao (al igual que
si sube el precio del bacalao baja su demanda), es decir se comportan
de forma paralela.

Para obtener las curvas de demanda y oferta agregadas, deberemos substituir
los valores dados en la expresión, obteniendo:

$
  Q^D & = -2P + 1200+15-3+300 = -2P + 1512 \
  Q^S & = 2P - 6 + 1494 = 2P + 1488.
$

Se puede ver su gráfica en la @fig:apartado-2. Finalmente, para calcular el precio
de equilibrio, debemos encontrar $Q^D(P^*) = Q^S(P^*)$. Operando, obtenemos:

$
  2P^* + 1488 & = -2P^* + 1512 \
         4P^* & = 24 \
          P^* & = 6.
$

Si $P>6$, $Q^S>Q^D$ hay exceso de oferta y parte del bacalao queda sin vender,
lo que incentiva una bajada del precio. Si $P<6$, $Q^D>Q^S$: hay exceso de
demanda y compradores dispuestos a adquirir bacalao no encuentran suficiente,
lo que genera presión para que el precio suba. Por ello, $P=6$ es el precio que
vacía el mercado.

#let QD(p) = 1512 - 2 * p
#let QS(p) = 1488 + 2 * p

#figure(
  lq.diagram(
    width: 10cm,
    height: 6cm,
    xlim: (1480, 1520),
    ylim: (0, 12),
    legend: (position: (100% + .5em, 0%)),
    plot_dscurve(x, QD, $Q^D(p)$),
    plot_dscurve(x, QS, $Q^S(p)$),
  ),
  caption: "Curvas de oferta y demanda.",
) <fig:apartado-2>

= Elasticidad de la demanda de mercado

#enunciado[
  Suponga que las personas que viajan por motivos de negocios y las que viajan
  de vacaciones tienen las siguientes demandas de billetes de avión entre dos
  ciudades:
  #align(center, block(width: 60%, table(
    columns: (1fr, 1.5fr, 1.5fr),
    stroke: (x: none, y: 0.6pt),
    align: center,
    [*Precio (dólares)*],
    [*Viajes de negocios*],
    [*Viajes de vacaciones*],
    table.hline(stroke: 1.25pt),
    [150], [2100], [1000],
    [200], [2000], [800],
    [250], [1900], [600],
    [300], [1800], [400],
  )))
]

== Cálculo de la elasticidad

#enunciado[
  #set enum(numbering: "(i)")
  Cuando el precio de los billetes sube de 200\$ a 250\$, ¿cuál es la
  elasticidad-precio de la demanda correspondiente a:
  + las personas que viajan por motivos de negocios; y,
  + a las que viajan de vacaciones?
]

La elasticidad se define como:

$
  epsilon = (% Delta Q) / (% Delta P).
$

Primero calcularemos $% Delta P$:
$
  Delta P = 250 - 200 = 50 -> % Delta P = 50/200 = +25%.
$
Ahora,
$
  Delta Q_"vacaciones" = -200 -> %Delta Q_"vacaciones" = -200/800 = -25%
$
y
$
  Delta Q_"negocios" = -100 -> %Delta Q_"negocios" = -100/2000 = -5%.
$

Entonces, las elasticidades serán:

$
  epsilon_"negocios" = -0.05 / 0.25 = -0.2 \
  epsilon_"vacaciones" = -0.25 / 0.25 = -1.
$

== Comparativa de elasticidad

#enunciado[
  ¿Por qué tienen las personas que viajan de vacaciones una elasticidad
  diferente a la de las personas que viajan por motivos de negocios? (Nota.
  No explique las matemáticas, sino argumente la intución económica.)
]

Las personas que viajan de vacaciones tienen la posibilidad de cambiar las
fechas de su viaje, el medio de transporte o incluso el destino. Por el
contrario, una persona que viaja por negocios podría cambiar de transporte, pero
tiene mucho menos margen para cambiar las fechas, y el destino es prácticamente
inmutable. Por otro lado, si la empresa es la que paga el billete, el viajero no
es tan sensible al precio del mismo.

= Estática comparativa

#enunciado[
  En una pequeña ciudad universitaria, los profesores pueden vivir en
  casas de su propiedad o de alquiler viviendo en alguno de los apartamentos de la residencia de la
  Universidad para las familias de los profesores. Centrémonos en el mercado de alquiler de apartamentos
  de residencias universitarias para profesores. En un curso académico existe una situación inicial de
  equilibrio. Se pide (Notas. a) argumente utilizando el gráfico del equilibrio de mercado, b) explique
  los resultados; c) se indique genéricamente a demanda o oferta: sea estricto e indique si se refiere a
  cantidades demandadas o a la curva de demanda, o bien a las cantidades ofertadas o a la curva de
  oferta):
]

#let demanda-0 = lq.plot(
  (0, 100),
  (50, 0),
  color: blue,
  label: [$D_0$],
)
#let oferta-0 = lq.plot(
  (20, 110),
  (0, 45),
  color: red,
  label: [$O_0$],
)

// Demanda desplazada 20 unidades a la izquierda:
// Q^D_1 = 80 - 2P.
#let demanda-1 = lq.plot(
  (0, 80),
  (40, 0),
  color: blue,
  stroke: (paint: blue, dash: "dashed"),
  label: [$D_1$],
)

// Oferta desplazada 20 unidades a la izquierda:
// Q^S_1 = 2P.
#let oferta-1 = lq.plot(
  (0, 104),
  (0, 52),
  color: red,
  stroke: (paint: red, dash: "dashed"),
  label: [$O_1$],
)

// Un punto y su rótulo. Las coordenadas siguen el orden (Q, P).
#let equilibrio(q, p, nombre) = (
  lq.scatter((q,), (p,), color: black, mark: "o"),
  lq.place(q, p, align: left, pad(0.7em)[$#nombre$]),
)

== Equilibrio inicial

#enunciado[
  Defina el equilibrio en el mercado de alquiler de apartamentos de
  residencias universitarias para profesores.
]

El mercado considerado es el de alquiler de apartamentos de las residencias
universitarias para profesores.
Su precio es la renta de alquiler $P$ y su cantidad $Q$ es el número de
apartamentos alquilados. Como muestra la @fig:alquiler-inicial, el equilibrio
inicial $E_0 = (Q_0, P_0)$ se alcanza cuando la cantidad que los profesores
desean alquilar coincide con la cantidad que la universidad ofrece: $Q^D(P_0) =
Q^S(P_0)$. A esa renta no existe exceso de demanda ni de oferta de apartamentos
en este mercado.

#figure(
  lq.diagram(
    width: 10cm,
    height: 6cm,
    xlim: (0, 110),
    ylim: (0, 52),
    xlabel: [Cantidad de apartamentos alquilados $Q$],
    ylabel: [Renta de alquiler $P$],
    demanda-0,
    oferta-0,
    ..equilibrio(60, 20, $E_0$),
  ),
  caption: [Equilibrio inicial del mercado de alquiler.],
) <fig:alquiler-inicial>

== Perturbaciones del equilibrio inicial

#enunciado[
  #set enum(numbering: "1.")
  (Estática comparativa.) Indique, intuitiva y gráficamente, ¿cómo afectará
  al equilibrio del mer- cado de alquiler para profesores después de los
  siguientes eventos que pueden acaecer en el siguiente curso académico?:
  + La universidad cierra una facultad.
  + La universidad cierra una de las residencias durante todo el curso para
    reformarla.
  + Para obtener recursos, la universidad decide vender algunos de los
    apartamentos a los profesores que las alquilaban el curso pasado.
]

=== Cierre de una facultad

El cierre de una facultad reduce previsiblemente el número de profesores que
buscan alojamiento en las residencias. A una misma renta, la cantidad demandada
de apartamentos será menor; por ello, se desplaza la curva de demanda de $D_0$
a $D_1$, hacia la izquierda, como indica la flecha de la @fig:cierre-facultad.
La curva de oferta $O_0$ no se desplaza.

En el nuevo equilibrio $E_1$, disminuyen tanto la renta como el número de
apartamentos alquilados. La menor renta provoca una reducción de la cantidad
ofrecida: este segundo cambio es un movimiento sobre $O_0$, no un desplazamiento
de la curva de oferta.

#figure(
  lq.diagram(
    width: 10cm,
    height: 6cm,
    xlim: (0, 110),
    ylim: (0, 52),
    xlabel: [Cantidad de apartamentos alquilados $Q$],
    ylabel: [Renta de alquiler $P$],
    demanda-0,
    demanda-1,
    oferta-0,

    // A P = 30, la cantidad demandada pasa de 40 a 20.
    lq.line(
      (40, 30),
      (20, 30),
      stroke: (paint: blue, thickness: 1.2pt),
      tip: tiptoe.stealth,
    ),

    ..equilibrio(60, 20, $E_0$),
    ..equilibrio(50, 15, $E_1$),
  ),
  caption: [
    Cierre de una facultad. La curva de demanda se desplaza a la
    izquierda; disminuyen la renta de equilibrio y la cantidad alquilada.
  ],
) <fig:cierre-facultad>

=== Cierre de una residencia para reformarla

Si una residencia permanece cerrada durante todo el curso, la universidad
dispone de menos apartamentos para alquilar. A una misma renta, la cantidad
ofrecida es menor; por tanto, la curva de oferta se desplaza de $O_0$ a $O_1$,
hacia la izquierda, como muestra la @fig:cierre-residencia. La curva de demanda
$D_0$ no se desplaza.

En el nuevo equilibrio $E_1$, la renta es mayor y se alquilan menos
apartamentos. La subida de la renta reduce la cantidad demandada, mediante un
movimiento sobre $D_0$.

#figure(
  lq.diagram(
    width: 10cm,
    height: 6cm,
    xlim: (0, 110),
    ylim: (0, 52),
    xlabel: [Cantidad de apartamentos alquilados $Q$],
    ylabel: [Renta de alquiler $P$],
    demanda-0,
    oferta-0,
    oferta-1,

    // A P = 30, la cantidad ofrecida pasa de 80 a 60.
    lq.line(
      (80, 30),
      (60, 30),
      stroke: (paint: red, thickness: 1.2pt),
      tip: tiptoe.stealth,
    ),

    ..equilibrio(60, 20, $E_0$),
    ..equilibrio(50, 25, $E_1$),
  ),
  caption: [
    Cierre de una residencia. La curva de oferta se desplaza a la
    izquierda; sube la renta de equilibrio y disminuye la cantidad alquilada.
  ],
) <fig:cierre-residencia>

=== Venta de apartamentos a sus antiguos inquilinos

La venta retira apartamentos del mercado de alquiler y, al mismo tiempo, sus
compradores dejan de demandarlos como inquilinos. En consecuencia, se desplazan
hacia la izquierda tanto la curva de oferta como la curva de demanda, de $O_0$ a
$O_1$ y de $D_0$ a $D_1$, respectivamente (@fig:venta-apartamentos).

Si se venden $n$ apartamentos a $n$ profesores que antes los alquilaban y cada
uno abandona este mercado, ambas curvas se reducen en la misma cantidad a cada
renta: $Q^S_1(P) = Q^S_0(P) - n$ y $Q^D_1(P) = Q^D_0(P) - n$. Al igualarlas,
$n$ se cancela. Bajo este supuesto, la renta de equilibrio permanece en $P_0$,
mientras que el número de apartamentos alquilados disminuye de $Q_0$ a $Q_0 -
n$, tal como representa el paso de $E_0$ a $E_1$ en la figura.

#figure(
  lq.diagram(
    width: 10cm,
    height: 6cm,
    xlim: (0, 110),
    ylim: (0, 52),
    xlabel: [Cantidad de apartamentos alquilados $Q$],
    ylabel: [Renta de alquiler $P$],
    demanda-0,
    demanda-1,
    oferta-0,
    oferta-1,

    // Ambos desplazamientos se miden a la misma renta P = 30.
    lq.line(
      (40, 30),
      (20, 30),
      stroke: (paint: blue, thickness: 1.2pt),
      tip: tiptoe.stealth,
    ),
    lq.line(
      (80, 30),
      (60, 30),
      stroke: (paint: red, thickness: 1.2pt),
      tip: tiptoe.stealth,
    ),

    ..equilibrio(60, 20, $E_0$),
    ..equilibrio(40, 20, $E_1$),
  ),
  caption: [
    Venta de apartamentos a sus antiguos inquilinos. Si oferta y demanda
    se reducen en igual número de apartamentos, disminuye la cantidad
    alquilada y la renta de equilibrio permanece igual.
  ],
) <fig:venta-apartamentos>
