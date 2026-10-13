#import "@local/master-uvigo-templates:0.1.0": font_sizes, homework_econ

#show: homework_econ.with(
  course: [Análisis de Decisiones Económicas y Mercados],
  title: [Ejercicios del Tema 7],
  heading-numbering: none,
)
#show heading.where(level: 1): set text(size: font_sizes.large)

#block()[
  *Enunciado* #h(1em)
  #set text(style: "italic")
  Invita a unos amigos a ver un partido en casa. Sus amigos quieren cervezas,
  por lo que acude al supermercado. Se encuentra que hay dos tipos de
  mercancías: 'packs de 6 latas de cerveza' (mercancía 1) y 'latas de cerveza
  sueltas' (mercancía 2).
]

#let cesta1 = $(x_1, x_2)$
#let cesta2 = $(y_1, y_2)$

= Describiendo preferencias de un consumidor a través de una relación binaria

Definamos la cesta de consumo como la tupla $#cesta1 in ZZ^2$, donde:
$
  x_1 &:= "número de packs de 6 latas de cerveza", \
  x_2 &:= "número de latas de cerveza sueltas". \
$
La relación de preferencia con otra cesta de consumo #cesta2 se escribiría
como cualquiera de las siguientes expresiones:
$
  #cesta1 succ #cesta2\
  #cesta1 succ.eq #cesta2\
  #cesta1 ~ #cesta2\
  #cesta1 prec #cesta2\
  #cesta1 prec.eq #cesta2.
$

= Describiendo preferencias de un consumidor a través de conjuntos de indiferencia

Dada la definición anterior, el conjunto de indiferencia puede expresarse en
lenguaje de conjuntos como $I(#cesta1) = {#cesta2 in ZZ^2 | #cesta2 ~ #cesta1}.$

= Describiendo preferencias de un consumidor a través de una función de utilidad

En éste caso, la _utilidad_ se representaría mediante una función $u : ZZ² ->
RR$ tal que:
$
  #cesta1 succ.eq #cesta2 <==> u#cesta1 >= u#cesta2 quad forall #cesta1, #cesta2 in ZZ².
$
Como añadido, los conjuntos de indiferencia ahora se podrían reformular en
términos de $u$:
$
  I(#cesta1) = {#cesta2 in ZZ² | u#cesta1 = u#cesta2}.
$
