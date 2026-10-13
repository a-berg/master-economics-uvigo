#import "@local/master-uvigo-templates:0.1.0": font_sizes, homework_econ
#import "@preview/lilaq:0.6.0" as lq

#show: homework_econ.with(
  course: [Análisis de Decisiones Económicas y Mercados],
  title: [Ejercicios del Tema 5],
)

#set text(lang: "es")

#align(center, block(width: 80%, align(center)[
  #set text(size: font_sizes.footnotesize)
  *Aviso de autoría*: en el transcurso del trabajo se ha usado GPT-6 Sol Light.
  Su aportación ha sido resolución de dudas y creación de gráficas.
]))

= Función de costes e indicadores de costes

Tenemos los siguientes gastos para producir:

$
  & 100 #sym.euro/"caseta" #sym.times overline(k) "casetas", \
  & 10 #sym.euro/"hora" #sym.times l "horas", \
  & 1 #sym.euro/"materiales" #sym.times q "materiales".
$

Por tanto:

$
  C(l, overline(k), q) = 100 overline(k) + 10 l + q.
$

Ahora, para calcular la función de costes $C(q)$, necesitamos sustituir
$overline(k)$ por su valor dado y despejar en la función de tecnología la
variable $l$ para obtener $l(q)$, y así sustituir en $C(l, overline(k), q)$.
Dado que (fijado $overline(k)$) $q = 100l$, podemos calcular que $C(q)$ es:
$
  C(q)=100+10(q)/(100)+q =100+ 1.1q.
$

Además,
$
  overline(C F) = 100, quad quad C V(q) = 1.1q.
$

Los costes medios se calculan dividiendo éstos términos calculados por la
cantidad producida, $q$. Entonces:

$
  C F M e (q) & = overline(C F)/q = 100/q \
  C V M e (q) & = (C V(q))/q = 1.1 \
  C T M e (q) & = C(q)/q = C F M e (q) + C V M e (q) = 100/q + 1.1.
$

El coste marginal es la derivada respecto $q$ del coste $C(q)$:

$
  C M g(q) = (d C(q))/(d q) = 1.1.
$

#let q = range(1, 1001).map(i => i / 2)
#figure(
  lq.diagram(
    width: 12cm,
    height: 10cm,
    xlabel: [Producción $q$ (cuncas)],
    ylabel: [Coste por unidad (€/cunca)],
    xlim: (0, 500),
    ylim: (0, 12),
    legend: (position: top + right),
    lq.plot(
      q,
      q.map(x => 100 / x + 1.1),
      label: $"CTMe"(q) = 100/q + 1.1$,
      stroke: 2pt,
      color: rgb("#2563eb"),
      mark: none,
    ),
    lq.plot((0, 500), (1.1, 1.1), label: $"CVMe"(q) = 1.1$, stroke: 3pt, color: rgb("#0d9488"), mark: none),
    lq.plot(
      (0, 500),
      (1.1, 1.1),
      label: $"CMg"(q) = 1.1$,
      stroke: (thickness: 1.5pt, dash: "dashed"),
      color: rgb("#e87924"),
      mark: none,
    ),
  ),
  caption: [
    *CVMe y CMg coinciden:* la línea discontinua está sobre la continua. \
    CTMe disminuye y se aproxima a 1,10 € desde arriba. \
    #text(
      size: 9pt,
      fill: luma(150),
    )[Vista limitada a 12 €/cunca; CTMe crece sin límite cuando q se acerca a cero.]
  ],
)

= Curva de oferta individual, precio de cierre, precio de beneficio cero, decisiones del empresario que se enfrenta a diferentes precios

#let CF = 100
#let data = (
  // q: (10,15,20,25),
  // CVq: (200, 300, 420, 550),
  (10, 200),
  (15, 300),
  (20, 420),
  (25, 550),
)
#let CT(cvq) = CF + cvq
#let CVMe(cvq, q) = cvq / q
#let CTMe(cvq, q) = CT(cvq) / q
// #let CMg()

El coste fijo mensual de la empresa es de $"CF" = #CF €$. El coste variable
mensual viene dado en la primera columna de la @tab:tabla-costes. Para calcular
el resto de columnas, necesitaremos las siguientes definiciones:

$
    "CT"(q) & ="CF"+"CV"(q) \
  "CVMe"(q) & =("CV"(q))/q \
  "CTMe"(q) & =("CT"(q))/q\
  "CMg"&=(Delta"CT")/(Delta q)=(Delta"CV")/(Delta q).
$

Los cálculos están en la @tab:tabla-costes. El precio de cierre es el mínimo
coste variable medio, es decir $p_C = 20€$, lo que se cumple con $q=10$ y
$q=15$, mientras que el precio de beneficio cero es el mínimo coste total medio,
es decir $p_(B=0) = 26€$, lo que se cumple con $q=20$ y $q=25$.

#figure(
  block(width: 100%, table(
    columns: (1.7fr, 1fr, 1fr, 1.2fr, 1.2fr, 1.2fr),
    align: (center, center, center, center, center, center),
    stroke: (x: none, y: .5pt),

    [*Cantidad de envases producidos al mes*],
    [*Coste variable*],
    [*Coste total*],
    [*Coste variable medio*],
    [*Coste total medio*],
    [*Coste marginal*],

    table.hline(stroke: 1.25pt),
    [10], [200], [$200+100 = 300$], [$200/10 = 20$], [$300/10 = 30$]   , [$(200-0)/(10-0) = 20$],
    [15], [300], [$300+100 = 400$], [$300/15 = 20$], [$400/15 = 26.67$], [$(300-200)/(15-10) = 20$],
    [20], [420], [$420+100 = 520$], [$420/20 = 21$], [$520/20 = 26$], [$(420-300)/(20-15) = 24$],
    [25], [550], [$550+100 = 650$], [$550/25 = 22$], [$650/25 = 26$]   , [$(550-420)/(25-20) = 26$],
  )),
  caption: [Tabla de costes.],
) <tab:tabla-costes>

Cuando el precio iguala al precio de cierre, tenemos:

$
  p = p_C = 20€.
$

Con $q=15$:

$
  I T = p q = 20 dot 15 = 300,
$

y sabemos que

$
  C V = 300, quad quad C T = 400.
$

Por tanto

$
  pi = I T - C T = 300 - 400 = -100€,
$

lo que también ocurre con $q=10$.

Cuando el precio iguala al precio de beneficio cero, tenemos:

$
  p = p_(B=0) = 26€.
$

Con $q=25$:

$
  I T = p q = 26 dot 25 = 650.
$

De la tabla:

$
  C V = 550, quad quad C T = 650,
$

Luego

$
  pi =  = 650 - 650 = 0€.
$

Esto también ocurre con $q = 20$.

Cuando $p=21$ podemos calcular directamente los beneficios de todas las
cantidades:

#figure(
  block(width: 75%, table(
    columns: (auto, auto, auto, auto),
    align: (center, center, center, center, center, center),
    stroke: (x: none, y: .5pt),
    [$q$], [$I T=p q$], [$C T$], [$pi=I T-C T$],
    table.hline(stroke: 1.25pt),
    [ 10 ], [210], [ 300 ], [-90] ,
    [ 15 ], [315], [ 400 ], [*-85*] ,
    [ 20 ], [420], [ 520 ], [-100] ,
    [ 25 ], [525], [ 650 ], [-125] ,
  )),
  caption: [Tabla de beneficios a $p=21€$.],
) <tab:tabla-beneficios-p21>

Dado que la alternativa de cerrar produce $pi = -100€$, la alternativa es
producir 15 envases, que minimiza las pérdidas.

Por el contrario, si $p=18$, entonces:

#figure(
  block(width: 75%, table(
    columns: (auto, auto, auto, auto),
    align: (center, center, center, center, center, center),
    stroke: (x: none, y: .5pt),
    [$q$], [$I T=p q$], [$C T$], [$pi=I T-C T$],
    table.hline(stroke: 1.25pt),
    [10], [180], [300], [-120],
    [15], [270], [400], [-130],
    [20], [360], [520], [-160],
    [25], [450], [650], [-200],
  )),
  caption: [Tabla de beneficios a $p=18€$.],
) <tab:tabla-beneficios-p18>

Dado que todas las posibilidades dan un beneficio inferior a las pérdidas por cierre,
lo óptimo es producir 0 envases.

En el largo plazo, no hay costes fijos inevitables porque las empresas pueden
entrar o salir libremente. Anteriormente hemos obtenido que el precio mínimo
para operar sin beneficios es $26€$. Por tanto en el largo plazo un $p=21€ < p_(B=0)$ no
constituye un precio de equilibrio competitivo, porque las empresas no operarán
con pérdidas indefinidamente. A partir de $p>=26€$, sí puede darse un equilibrio
a largo plazo.

