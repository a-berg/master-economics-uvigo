#import "@local/master-uvigo-templates:0.1.0": base-styles, font_sizes, homework_econ
#import "@preview/lilaq:0.6.0" as lq

#show: base-styles
#show: homework_econ.with(
  author: ("Adrián Berges Enfedaque", "Juan Tadeo Fariñas Pereira", "Miguel Sampayo Muñoz"),
  course: [Análisis de Decisiones Económicas y Mercados],
  title: "Producción",
  heading-numbering: "1.1.a",
)

#set table(stroke: (x: none, y: 0.6pt), align: center)
#set table.hline(stroke: 1.25pt)
#show table.header.where(level: 1): strong

#let enunciado(content) = {
  set text(style: "italic")
  block(fill: luma(200), inset: 8pt, radius: 4pt, stroke: 1pt)[#content]
}
#let argmax = math.op("arg max", limits: true)

#align(center, block(width: 80%, align(center)[
  #set text(size: font_sizes.footnotesize)
  *Aviso de autoría*: en el transcurso del trabajo se ha usado GPT-6 Astra Light.
  Su rol ha sido de ayuda para las dudas, en la redacción de algunos apartados y
  elaboración de gráficas.
]))

= Asignación de un recurso entre dos actividades
#enunciado[
  Suponga que en la ría de Vigo existen dos áreas de pesca de cabotaje: una
  hacia Rande (que denotaremos E por Este), y otra hacia las Islas Cíes (que
  denotaremos O por Oeste). Dada la información de biodiversidad en la ría de
  Vigo proporcionada por los biólogos del CSIC, los ingenieros de nuestra
  empresa, teniendo en cuenta la capacidad de nuestros barcos, nos proporcionan
  la siguiente relación entre barcos y capturas (en Toneladas).
  #{
    set align(center)
    block(width: 60%, table(
      columns: (1fr, 1.5fr, 1.5fr),
      table.header[qO (Tm)][Flota][qE (Tm)],
      table.hline(),
      [$0$], [$0$], [$0$],
      [$100$], [$1$], [$130$],
      [$200$], [$2$], [$240$],
      [$300$], [$3$], [$330$],
      [$380$], [$4$], [$400$],
    ))
  }
  Nuestra empresa tiene $4$ barcos, y el armador cree que es mejor mandar los $4$
  barcos hacia Rande porque en promedio los $4$ barcos traen más pesca que si se
  mandan todos hacia las Cíes. Usted le indica al armador que lo que tiene que
  hacer es mandar $2$ barcos a las Cíes, obteniendo una captura total de $200 "Tm"$,
  y $2$ barcos hacia Rande, obteniendo una captura total de $240 "Tm"$. El armador
  se burla de Usted: “No puede ser esa la mejor decisión: si en promedio cada
  barco en las Cíes captura $100 "Tm"$, y en Rande captura $120 "Tm"$, sería mejor
  mandar un barco más a Rande y uno menos a las Cíes.” Se pide:
  #set enum(numbering: "a)")

  + Utilizando la teoría económica, explíquele a su armador cuál es la
    distribución óptima entre ambos bancos de pesca; (_Pista $1$.-_ Utilice
    en su razonamiento la regla de decisión racional en el análisis marginal.
    _Pista $2$.-_ Suponga que los costes de enviar un barco a cualquiera de los
    dos bancos de pesca son iguales.)
  + Hágale ver cuál es su error al tomar la productividad media tanto al
    principio cuando quería mandar todos los barcos hacia Rande, como después, cuando quería mandar un barco más a Rande.
]


== Distribución óptima de la flota

Para distribuir los barcos tenemos que comparar la captura que añade un barco
al banco de destino con la que se pierde al retirarlo del banco de origen.
Como enviar un barco a cualquiera de los dos bancos cuesta lo mismo, y
suponiendo que el pescado se vende al mismo precio, interesa maximizar la
captura total. Calculemos el producto marginal de cada barco:

#align(center, table(
  columns: 3,
  inset: (x: 5pt, y: 3pt),
  table.header([Barco añadido], [$"PMg"_O$ (Tm)], [$"PMg"_E$ (Tm)]),
  table.hline(),
  [$1$], [$100$], [$130$],
  [$2$], [$100$], [$110$],
  [$3$], [$100$], [$90$],
  [$4$], [$80$], [$70$],
))

Partiendo de los cuatro barcos en Rande, trasladar uno a las Cíes permite ganar
$100$ Tm y perder solo $70$ Tm. Trasladar un segundo permite ganar otras $100$ Tm y
perder $90$ Tm. Sin embargo, trasladar un tercero haría ganar $100$ Tm pero perder
$110$ Tm. Por tanto, nos detenemos en dos barcos en cada banco:

$
  n_O^* = n_E^* = 2, wide Q^* = q_O (2) + q_E (2) = 200 + 240 = 440 "Tm".
$

// Podemos comprobarlo comparando todas las distribuciones posibles:

// #align(center, table(
//   columns: 3, inset: (x: 5pt, y: 3pt),
//   table.header([Barcos en las Cíes], [Barcos en Rande], [Captura total (Tm)]),
//   table.hline(),
//   [0], [4], [400],
//   [1], [3], [430],
//   [2], [2], [440],
//   [3], [1], [430],
//   [4], [0], [380],
// ))

== El error de comparar productividades medias

El armador comete un error de elección de la función de optimización.
Él piensa que la función a optimizar es
$
  argmax_(L_O, L_E) &quad overline(q)_O L_O + overline(q)_E L_E = [overline(q)_O, overline(q)_E] dot vec(L_O, L_E, delim: "[") \
  "s.t." &quad L_O + L_E = 4,
$
siendo un problema de programación lineal de $2$ variables cuya solución,
efectivamente, es asignar todo el presupuesto al componente del vector de pesos
con mayor valor.

Sin embargo, como economistas sabemos que la asignación de recursos tiene
incrementos marginales de la productividad y que por tanto en términos
matemáticos el problema será un programa no lineal separable (porque es la suma
de $2$ funciones):
$
  argmax_(L_O, L_E) & quad q_O (L_O) + q_E (L_E) \
             "s.t." & quad L_O + L_E = 4.
$

Este fallo de razonamiento lleva a la conclusión equivocada de enviar todos
los barcos a un solo banco. Sin embargo, su razonamiento no permite descartar
que una distribución entre ambos bancos permita capturar más pescado. De hecho,
el cuarto barco en Rande añade solo $70$ Tm, mientras que el primero en las Cíes
aporta $100$ Tm.

Con dos barcos en cada banco, el mismo error aparece al comparar las medias
$240/2 = 120$ y $200/2 = 100$. El tercer barco en Rande no añade $120$ Tm,
sino $330 - 240 = 90$ Tm. Retirar el segundo de las Cíes supone perder
$200 - 100 = 100$ Tm. El traslado que propone el armador reduce la captura:

$
  Delta Q = "PMg"_E(3) - "PMg"_O(2) = 90 - 100 = -10 " Tm".
$

La decisión depende de las productividades marginales, no de las medias.
Como los barcos son indivisibles, el óptimo no exige igualar exactamente
ambos productos marginales: basta con que ningún traslado aumente la captura.

= La decisión de producción basada en la productividad de los inputs debe coincidir con la basada en los costes de producir
== La decisión de producción de la empresa basada en la productividad de los inputs productivos <ejer-2-1>
#enunciado[
  María tiene $5$ horas libres todos los días, que puede emplear en pescar o en
  trabajar en una tienda que es su mejor alternativa. Por trabajar en la tienda
  le pagan $12€$ la hora. Por otra parte es propietaria de una caña que le
  costó $10€$ y de un rollo de sedal que le costó $2€$. María no quiere
  que nadie utilice su caña con sedal, pero ambos, la caña y el sedal, podría
  alquilarlos por todo el día al precio de adquisición. Como pescadora, María
  observa la siguiente relación entre las horas que dedica a la pesca y la
  cantidad de pescado capturado:

  #{
    set align(center)
    block(width: 60%, table(
      columns: (1fr, 1.5fr, 1.5fr),
      table.header[Horas][Cantidad de pescado (kilos)][],
      table.hline(),
      [$0$], [$0$], [],
      [$1$], [$10$], [],
      [$2$], [$18$], [],
      [$3$], [$24$], [],
      [$4$], [$28$], [],
      [$5$], [$30$], [],
    ))
  }

  Se pide: Si puede vender el pescado a un precio de $2.5€$ el kilo, ¿cuántas
  horas trabajará en la tienda y cuántas empleará pescando? Justifique la
  respuesta. (Pista. Puede emplear la Regla de Decisión Racional para estudiar
  las decisiones marginales de María como empresaria maximizadora de beneficios.
  Nota.- Se han colocado columnas vacías en la tabla por si las quiere utilizar,
  aunque ni tienen que utilizarse todas, ni se pide que se utilicen.)
]

Para decidir cuántas horas dedicará a pescar, tenemos que comparar el ingreso
que obtiene con cada hora adicional de pesca con el salario al que renuncia
por no trabajar esa hora en la tienda (coste de oportunidad).

Sea $L$ el número de horas de pesca y $q(L)$ la cantidad capturada. El producto
marginal del trabajo es el aumento de la captura al añadir una hora de pesca:

$
  "PMg"_L = (Delta q)/(Delta L), wide
  "VPMg"_L = p dot "PMg"_L = 2.5 dot "PMg"_L.
$

La Regla de Decisión Racional indica que conviene añadir una hora de pesca
si el valor de su producto marginal es mayor que su coste de oportunidad,
es decir, si $"VPMg"_L > 12$. Calculando los incrementos de la tabla:

#figure(
  align(center, table(
    columns: (auto, auto, auto, auto, auto),
    table.header([*Horas*], [*Captura*], [$"PMg"_L$], [$"VPMg"_L$], [$"VPMg"_L - 12$]),
    table.header(level: 2,)[$L$][kg][kg/h][€/h][€/h],
    table.hline(),
    [$0$], [$0$], [—], [—], [—],
    [$1$], [$10$], [$10$], [$25$], [$13$],
    [$2$], [$18$], [$8$], [$20$], [$8$],
    [$3$], [$24$], [$6$], [$15$], [$3$],
    [$4$], [$28$], [$4$], [$10$], [$−2$],
    [$5$], [$30$], [$2$], [$5$], [$−7$],
  )),
  caption: [Productividad y ganancia de cada hora adicional de pesca.],
)

Las tres primeras horas de pesca generan más ingresos que el trabajo en la
tienda. Sin embargo, la cuarta solo aporta $10€$, frente a los $12€$
que podría ganar trabajando. Como el producto marginal es decreciente,
tampoco interesa añadir la quinta. Por tanto, la mejor alternativa es:

$
  L^* = 3, wide q^* = 24, wide L_"tienda"^* = 5 - 3 = 2.
$

Queda comprobar si compensa pescar frente a no hacerlo.
La caña y el sedal ya están comprados, por lo que su precio de adquisición no es
un nuevo desembolso diario.
No obstante, al utilizarlos María renuncia al alquiler que podría cobrar: $10€ +
2€ = 12€$ al día.
Aunque no quiera prestarlos, esa posibilidad representa un coste de oportunidad
monetario.
Es un coste fijo de pescar ese día, no un coste de $12€$ por cada hora.

El beneficio económico de pescar tres horas, descontando el salario y el
alquiler a los que renuncia, es:

$
  p q(3) - 12 dot 3 - (10 + 2) = 2.5 dot 24 - 36 - 12 = 12 > 0.
$

Es decir, pescando tres horas y trabajando dos obtiene $60€ + 24€ = 84€$, mientras
que trabajando las cinco horas y alquilando el equipo obtendría $60€ + 12€ = 72€$.
Por tanto, María dedicará $3$ horas a pescar y $2$ horas a trabajar en la tienda,
capturando $24$ kilos de pescado.
Si descarta por completo alquilar el equipo, su alternativa sería ganar $60€$
en la tienda, y la distribución óptima del tiempo seguiría siendo la misma.

// Podemos comprobar que el razonamiento en términos de costes conduce al mismo
// resultado. Para cada nivel positivo de producción de la tabla, el coste
// económico es $C(q(L)) = 12L + 12$. El coste marginal de cada tramo de
// producción, una vez asumido el coste fijo diario, es:

// $
//   "CMg" = (Delta C)/(Delta q)
//   = (12 Delta L)/(Delta q)
//   = 12 / "PMg"_L.
// $

// Así, los costes marginales de los sucesivos tramos son $1.2$, $1.5$, $2$,
// $3$ y $6$ euros por kilo. El tercer tramo, de 18 a 24 kilos, cuesta 2 euros
// por kilo y se vende a 2,5; el cuarto cuesta 3 euros por kilo y ya no compensa.
// La condición $p dot "PMg"_L > 12$ equivale a $p > "CMg"$: ambas formas
// de plantear la decisión llevan a producir 24 kilos. El coste fijo se tiene
// en cuenta al comparar pescar con no pescar, como hemos comprobado antes.

== La decisión de producción de la empresa basada en los costes de producir
#enunciado[
  Considere ahora a María como una empresaria que dirige una explotación
  productiva dedicada a capturas de pescado utilizando dos inputs: horas (de
  trabajo) y capital (la caña con sedal de pescar) y cuya tecnología es la
  descrita en el @ejer-2-1[Ejercicio].

  #{
    set align(center)
    block(width: 100%, table(
      columns: (auto, auto, auto, auto, auto, auto, auto, auto),
      table.header([$L$], [$q$], [CF], [CV], [CT], [CVMe], [CTMe], [CMg]),
      table.hline(),
      [$0$], [$0$], [], [], [], [], [], [],
      [$1$], [$10$], [], [], [], [], [], [],
      [$2$], [$18$], [], [], [], [], [], [],
      [$3$], [$24$], [], [], [], [], [], [],
      [$4$], [$28$], [], [], [], [], [], [],
      [$5$], [$30$], [], [], [], [], [], [],
    ))
  }
]


=== Costes de la explotación
#enunciado[
  Complete la tabla de costes de la explotación pesquera para cada nivel de
  producción. (_Pista $1$._ Piense cuáles son los costes variables (CV) y los
  costes fijos (CF) de la empresa. _Pista $2$._ Para la remuneración del input
  trabajo, piense cuál es el coste de oportunidad de cada hora empleada en
  la actividad de pesca. _Pista $3$._ Para la remuneración del input capital
  -caña con sedal-, piense cuál será el coste de oportunidad de la unidad
  de capital.)
]

Tomando como coste variable el salario al que María renuncia y como coste fijo
la remuneración diaria del capital, definimos:

$
  "CF" = 10 + 2 = 12, wide "CV" = 12 L, wide "CT" = 12 + 12 L.
$

Para $q > 0$, los costes medios y el coste marginal se calculan como:

$
  "CVMe" = (12 L)/q, quad "CTMe" = (12 + 12 L)/q, quad
  "CMg" = (Delta "CT")/(Delta q) = 12/(Delta q).
$

Realizando todas las operaciones, la tabla de costes de explotación completa es:

#figure(
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto, auto),
    table.header([$L$], [$q$], [CF], [CV], [CT], [CVMe], [CTMe], [CMg]),
    table.hline(),
    [$0$], [$0$], [$12$], [$0$], [$12$], [—], [—], [—],
    [$1$], [$10$], [$12$], [$12$], [$24$], [$1.20$], [$2.40$], [$1.20$],
    [$2$], [$18$], [$12$], [$24$], [$36$], [$1.33$], [$2.00$], [$1.50$],
    [$3$], [$24$], [$12$], [$36$], [$48$], [$1.50$], [$2.00$], [$2.00$],
    [$4$], [$28$], [$12$], [$48$], [$60$], [$1.71$], [$2.14$], [$3.00$],
    [$5$], [$30$], [$12$], [$60$], [$72$], [$2.00$], [$2.40$], [$6.00$],
  ),
  caption: [Tabla de costes de explotación, completa.],
)

// Por ejemplo, pasar de 18 a 24 kilos requiere una hora adicional y cuesta
// 12 euros, por lo que $"CMg" = 12/(24 - 18) = 2$ euros por kilo. En la tabla,
// $L$ se expresa en horas; $q$, en kilos; los costes totales, en euros al día;
// y los medios y marginales, en euros por kilo. Las cifras están redondeadas
// a dos decimales. Con producción nula los costes medios no están definidos,
// y tampoco hay un tramo anterior para calcular el coste marginal.

=== Precio de beneficio cero y precio de cierre
#enunciado[
  En el corto plazo ¿cuál es el precio de beneficio cero?, ¿cuál es el
  precio de cierre de la empresa?
]
El precio de beneficio cero es el mínimo del coste total medio. Comparando
los niveles de producción disponibles, obtenemos:

$
  p_"beneficio cero" = min "CTMe" = 2 " €/kg".
$

A ese precio, tanto $18$ como $24$ kilos permiten cubrir exactamente todos los
costes: $2 dot 18 = 36$ y $2 dot 24 = 48$.

En el modelo de corto plazo, el coste fijo se soporta incluso si la empresa no
produce. Por ello, interesa producir siempre que los ingresos cubran los costes
variables. Bajo este supuesto, el precio de cierre es:
$
  p_"cierre" = min "CVMe" = 12/10 = 1.2 " €/kg".
$

A $1.20€$ por kilo, producir $10$ kilos o cerrar genera la misma pérdida de
$12€$. Entre $1.20€$ y $2€$ por kilo, la empresa produce aunque tenga
pérdidas, porque recupera parte del coste fijo.

// Hay una diferencia relevante respecto al @ejer-2-1[Ejercicio]: si María puede
// alquilar el equipo al dejar de pescar, recupera los 12 euros de remuneración
// del capital. En ese caso, este coste es fijo respecto a la cantidad producida,
// pero evitable al cerrar. La comparación relevante pasa a ser
// $p q - 12 L >= 12$, de modo que el umbral para pescar frente a trabajar y
// alquilar el equipo es *2 euros por kilo*. Así, 1,20 euros es el precio de
// cierre con coste fijo comprometido; 2 euros es el umbral cuando el alquiler
// alternativo está disponible. Esta distinción explica el tratamiento de
// $"CF" = 12$ incluso para $q = 0$ en la tabla de corto plazo.

=== Curvas de costes y oferta a corto plazo
#enunciado[
  Represente en el mismo gráfico las curvas de coste total medio (CTMe),
  coste variable medio (CVMe) y coste marginal (CMg) de la empresa de pesca.
  Adicionalmente, represente en el mismo gráfico la curva de oferta a corto
  plazo, e indique también en el gráfico el precio de cierre y el precio de
  beneficio cero.
]

La @fig:costes-pesca representa los costes de la tabla y la oferta bajo el
supuesto de coste fijo comprometido.
// Como solo conocemos seis niveles de producción, mantenemos las cantidades
// discretas.
// Las líneas que unen los costes medios sirven de guía visual; no suponen una
// tecnología continua.
Cada tramo horizontal del coste marginal corresponde al incremento de producción
entre dos filas consecutivas.

#figure(
  align(center, lq.diagram(
    width: 100%,
    height: 8cm,
    xlim: (0, 32),
    ylim: (0, 7),
    xlabel: [Cantidad de pescado (kg)],
    ylabel: [Precio y costes (€/kg)],
    legend: (position: top + left),
    lq.plot((10, 18, 24, 28, 30), (2.4, 2, 2, 60 / 28, 2.4), color: blue, mark: "o", label: [CTMe]),
    lq.plot((10, 18, 24, 28, 30), (1.2, 24 / 18, 1.5, 48 / 28, 2), color: red, mark: "o", label: [CVMe]),
    lq.plot(
      (10, 18, 24, 28, 30),
      (1.2, 1.5, 2, 3, 6),
      color: orange,
      step: start,
      mark: none,
      label: [CMg],
      stroke: 1.25pt,
    ),
    lq.plot(
      (0, 10, 18, 24, 28, 30),
      (1.2, 1.5, 2, 3, 6, 7),
      color: green,
      mark: "o",
      label: [Oferta],
      stroke: (dash: "dashed", thickness: 0.5pt),
      // smooth: true,
    ),
    // ..((0, 10, 1.2), (10, 18, 1.5), (18, 24, 2), (24, 28, 3), (28, 30, 6))
    //   .enumerate()
    //   .map(((i, t)) => lq.plot((t.at(0), t.at(1)), (t.at(2), t.at(2)), color: orange, mark: none, label: if i == 0 {
    //     [CMg]
    //   } else { none })),
    // ..((0, 0, 1.2), (10, 1.2, 1.5), (18, 1.5, 2), (24, 2, 3), (28, 3, 6), (30, 6, 7))
    //   .enumerate()
    //   .map(((i, t)) => lq.plot(
    //     (t.at(0), t.at(0)),
    //     (t.at(1), t.at(2)),
    //     color: green,
    //     stroke: 2pt,
    //     mark: none,
    //     label: if i == 0 { [Oferta CP] } else { none },
    //   )),
    lq.plot((0, 32), (1.2, 1.2), color: gray, stroke: (dash: "dashed"), mark: none),
    lq.plot((0, 32), (2, 2), color: gray, stroke: (dash: "dashed"), mark: none),
    lq.place(1, 1.28, align: bottom + left, text(size: 8pt)[Cierre: $1.20$]),
    lq.place(1, 2.08, align: bottom + left, text(size: 8pt)[Beneficio cero: $2$]),
  )),
  caption: [Costes y oferta de corto plazo con coste fijo comprometido.
    Las líneas discontinuas indican los dos precios de referencia.],
) <fig:costes-pesca>

Comparando el precio con el coste de cada incremento de producción, la oferta
para precios no negativos es:

$
  q^s (p) = cases(
    0 & "si" 0 <= p < 1.2,
    10 & "si" 1.2 < p < 1.5,
    18 & "si" 1.5 < p < 2,
    24 & "si" 2 < p < 3,
    28 & "si" 3 < p < 6,
    30 & "si" p > 6.
  )
$

En los precios frontera hay indiferencia entre las dos cantidades adyacentes,
al tratarse de datos discretos, no podemos afirmar que las cantidades intermedias
sean factibles, por lo que en la @fig:costes-pesca se representa con puntos aunque
unidos por trazos discontinuos.
// a $p = 1.2$, entre 0 y 10; a $p = 1.5$, entre 10 y 18; a $p = 2$, entre
// 18 y 24; a $p = 3$, entre 24 y 28; y a $p = 6$, entre 28 y 30. Al tratarse
// de datos discretos, no afirmamos que las cantidades intermedias sean factibles.
// Si el equipo se puede alquilar al cerrar, la oferta es cero para $p < 2$;
// a $p = 2$ son óptimas 0, 18 y 24, y para $p > 2$ coincide con la anterior.

=== Producción a un precio de $2.5€$ por kilo <apartado-2-2-d>
#enunciado[
  ¿Cuántos kilos de pescado debería pescar la empresa de María si el
  precio del kilo de pescado es de $2.5€$? (_Pista._ Puede emplear la Regla
  de Decisión Racional para estudiar las decisiones marginales de María como
  empresaria minimizadora de costes.)
]

Conviene producir los tres primeros tramos, cuyos costes marginales son
$1.20$, $1.50$ y $2$ € por kilo. El siguiente tramo cuesta $3€$ por kilo,
más que el precio de venta. Por tanto:

$
  q^* = 24 "kg", quad
  pi(q^*) = 2.5 dot 24 - 48 = 12 "€".
$

Para comprobarlo, los beneficios para $q = 0, 10, 18, 24, 28, 30$ son,
respectivamente, $-12, 1, 9, 12, 10, 3$ € bajo el supuesto de coste fijo
comprometido. El máximo se alcanza en $24$ kilos.

// Si cerrar permite alquilar
// el equipo, el beneficio económico de esa alternativa es cero y sigue siendo
// preferible producir 24 kilos. Aunque el enunciado habla de minimizar costes,
// la elección de cuánto producir requiere comparar ingresos y costes para
// maximizar el beneficio.

=== Comparación con la decisión basada en la productividad
#enunciado[
Compare la respuesta del apartado @apartado-2-2-d[] con el que obtuvo en el
@ejer-2-1[Ejercicio]. ¿La decisión de horas de trabajo de María coincide
con la decisión productiva de la empresa de María? Justifique la
respuesta.
]

La decisión coincide con la del @ejer-2-1[Ejercicio]: para capturar $24$ kilos,
María necesita tres horas de pesca y le quedan dos para trabajar en la tienda.
La equivalencia se obtiene directamente de:

$
  p dot "PMg"_L > 12
  quad <=> quad p > 12/"PMg"_L = "CMg".
$

La tercera hora añade $6$ kilos, con un valor de $2.5 dot 6 = 15€$,
superior a su coste de $12€$. La cuarta añade $4$ kilos, valorados en
$10€$, por debajo de su coste. Comparar el valor del producto marginal
con el salario o el precio con el coste marginal conduce a la misma decisión.
