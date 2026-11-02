#import "@local/master-uvigo-templates:0.1.0": font_sizes, homework_econ

#show: homework_econ.with(
  course: [Análisis de Decisiones Económicas y Mercados],
  title: [Ejercicio 8 · Interacción estratégica],
  date: datetime(year: 2026, month: 10, day: 25),
  heading-numbering: (..nums) => {
    let n = nums.pos()
    if n.len() == 1 { numbering("1.", n.first()) }
    else { numbering("1.a.", ..n) }
  },
)
#set text(lang: "es", size: font_sizes.normalsize)
#show heading.where(level: 1): set text(size: font_sizes.large)
#show heading.where(level: 2): set text(size: font_sizes.large)
#set table(stroke: (x: none, y: .5pt), align: center, inset: 5pt)
#show table.header: strong

#let enunciado(body) = {
  set text(style: "italic")
  block(fill: luma(200), inset: 8pt, radius: 4pt, stroke: 1pt)[#body]
}
// Fuente: Ejercicio-Interacción Estratéxica.pdf.
// Se corrigen erratas tipográficas y las letras repetidas del enunciado.

= Trabajo de curso
#enunciado[
  Suponga que a usted y a un compañero de clase se les asigna un trabajo de curso por el que
  recibirán una calificación conjunta. (Nota. Es obligatorio realizar el trabajo conjuntamente.)
  Cada uno de ustedes quiere recibir una buena calificación, pero también quieren trabajar poco.
  En concreto, he aquí la situación:

  - Si los dos trabajan mucho, reciben un sobresaliente, lo que reporta a cada uno 40 unidades de felicidad.
  - Si sólo trabaja mucho uno de ustedes, ambos reciben un notable, que les da a cada uno 30 unidades de felicidad.
  - Si no trabaja mucho ninguno de los dos, ambos reciben un aprobado, que les da a cada uno 10 unidades de felicidad.
  - Trabajar mucho cuesta 25 unidades de felicidad.
]

== Tabla de decisiones
#enunciado[Indica los resultados en la siguiente tabla de decisiones: las filas recogen la decisión de tu compañero de clase (trabajar o vaguear) y las columnas, tu decisión (trabajar o vaguear).]

Restamos el coste de trabajar únicamente a quien trabaja. Si ambos trabajan,
cada uno obtiene $40-25=15$; si sólo trabaja uno, éste obtiene $30-25=5$
y el otro, 30. Si ambos vaguean, cada uno obtiene 10.

En cada casilla escribimos *(tu pago, pago de tu compañero)*:
#align(center, block(breakable: false, table(
  columns: 3,
  table.header([Compañero / Tú], [Trabajar], [Vaguear]),
  [Trabajar], [$(15, 15)$], [$(30, 5)$],
  [Vaguear], [$(5, 30)$], [$(10, 10)$],
)))

== Resultado probable
#enunciado[¿Cuál es el resultado probable? Explique su respuesta.]

Si tu compañero trabaja, prefieres vaguear: obtienes 30 en lugar de 15.
Si vaguea, también prefieres vaguear: obtienes 10 en lugar de 5.
Como sus preferencias son iguales a las tuyas, él razona del mismo modo.

Por tanto, *vaguear es una estrategia estrictamente dominante para ambos*.
El único equilibrio de Nash es *(vaguear, vaguear)*, con pagos $(10,10)$:
ninguno mejora cambiando por su cuenta de decisión.

== Eficiencia de Pareto
#enunciado[El resultado probable, ¿es eficiente en sentido de Pareto? En caso negativo, indique un par de estrategias donde ambos jugadores mejoren.]

*No es eficiente en sentido de Pareto.* Si ambos trabajan, pasan de 10 a 15
unidades de felicidad cada uno. Los dos mejoran, aunque individualmente tengan
incentivos a vaguear. Es un dilema del prisionero.

== Trabajos durante todo el año
#enunciado[Si usted tiene que hacer una serie de trabajos de clase con este compañero durante todo el año en lugar de uno solo, ¿cómo cambiaría eso el resultado que ha predicho en la parte (b)? Explique su respuesta.]

La repetición puede favorecer que ambos trabajen: vaguear hoy puede provocar
que el compañero deje de colaborar en los siguientes trabajos. Así, la ganancia
inmediata de vaguear se compara con la pérdida futura de cooperación.

Pero *si hay un número finito de trabajos, conocido por ambos*, y no hay otros
premios ni castigos, la predicción sigue siendo que ambos vaguean en todos.
En el último trabajo ya no hay cooperación futura que perder, por lo que ambos
vaguean. Lo mismo ocurre en el penúltimo y, razonando hacia atrás, en los demás.

Si la relación puede continuar sin un último trabajo conocido, sí puede
sostenerse la cooperación cuando ambos valoran suficientemente el futuro.
Por ejemplo, si acuerdan trabajar mientras nadie haya vagueado y vaguear para
siempre tras una desviación, con factor de descuento $0 <= delta < 1$ se necesita:
$
  15/(1-delta) >= 30 + (10 delta)/(1-delta)
  quad <=> quad delta >= 0.75.
$
El lado izquierdo es el pago de seguir cooperando; el derecho, el de vaguear
una vez y recibir 10 en los trabajos siguientes. Por tanto, la repetición abre
la posibilidad de cooperar, pero no lo garantiza.

== Un compañero que valora más las notas
#enunciado[
  A otro compañero de clase le importa más obtener buenas calificaciones: recibe 50 unidades
  de felicidad por un notable y 80 por un sobresaliente. Si hicieras los trabajos de clase con
  este compañero (pero tus preferencias no variaran):
  #enum(numbering: "1.",
    [¿Cómo cambiarían las respuestas a las partes (a) y (b)?],
    [¿Cuál de los dos compañeros preferirías para hacer los trabajos de clase?],
    [¿También querría él hacerlos contigo?],
  )
]

*1. Matriz y resultado.* Mantenemos para el nuevo compañero el coste de trabajar
(25) y la felicidad por el aprobado (10), que el enunciado no modifica.
Conservamos el orden *(tu pago, pago de tu compañero)*:
#align(center, block(breakable: false, table(
  columns: 3,
  table.header([Nuevo compañero / Tú], [Trabajar], [Vaguear]),
  [Trabajar], [$(15, 55)$], [$(30, 25)$],
  [Vaguear], [$(5, 50)$], [$(10, 10)$],
)))
Para ti, vaguear sigue siendo estrictamente dominante. Para él, trabajar es
estrictamente dominante: si tú trabajas, obtiene $80-25=55>50$; si vagueas,
obtiene $50-25=25>10$. El único equilibrio es *tú vagueas y él trabaja*,
con pagos $(30,25)$.

*2. Tu elección.* Prefieres al nuevo compañero: en el equilibrio obtienes
30 en lugar de 10 con el primero.

*3. Su elección.* Si la alternativa fuera obtener un aprobado y recibir 10,
sí preferiría trabajar contigo y obtener 25. Pero el trabajo conjunto es obligatorio
y el enunciado no concreta qué otros compañeros puede elegir. Si pudiera elegir a alguien
que trabajase, preferiría a esa persona: obtendría 55 en lugar de 25.
Por tanto, que tú lo prefieras no implica que tú seas su compañero preferido.

= Entrada en el mercado del café
#enunciado[
  Sugar es una pequeña empresa de café que está considerando la posibilidad de entrar en un
  mercado dominado por Ristretto. Los beneficios de cada una dependen de que entre la primera
  y de que la segunda fije un precio alto o bajo.

  Si Sugar entra y Ristretto mantiene el precio alto, entonces Sugar recibe 2 millones de euros
  de beneficio y Ristretto recibe 3 millones de euros de beneficio. Si Sugar no entra y Ristretto
  mantiene el precio alto, entonces Sugar recibe 0 millones de euros de beneficio y Ristretto
  recibe 7 millones de euros de beneficio. Si Sugar entra y Ristretto baja el precio, entonces
  Sugar tiene 1 millón de euros de pérdidas y Ristretto recibe 1 millón de euros de beneficio.
  Si Sugar no entra y Ristretto baja el precio, entonces Sugar no tiene beneficio y Ristretto
  recibe 2 millones de euros de beneficio.
]

== Jugadores, estrategias y matriz de pagos
#enunciado[Describa la situación como un juego: a.1) jugadores, a.2) estrategias y a.3) la matriz de pagos.]

Los *jugadores* son Sugar y Ristretto. Sugar elige entre *entrar* y *no entrar*;
Ristretto, entre *mantener el precio alto* y *bajar el precio*.

Los pagos se expresan en millones de euros, en el orden *(Sugar, Ristretto)*:
#align(center, block(breakable: false, table(
  columns: 3,
  table.header([Sugar / Ristretto], [Precio alto], [Precio bajo]),
  [Entrar], [$(2,3)$], [$(-1,1)$],
  [No entrar], [$(0,7)$], [$(0,2)$],
)))

== Estrategias dominantes
#enunciado[¿Tiene alguno de los dos jugadores una estrategia dominante?]

*Ristretto tiene una estrategia estrictamente dominante: mantener el precio alto.*
Si Sugar entra, gana $3>1$; si no entra, gana $7>2$.

Sugar no tiene una estrategia dominante. Si el precio es alto, prefiere entrar
porque $2>0$; si es bajo, prefiere no entrar porque $0>-1$.

== Decisión de Sugar
#enunciado[¿Le ayuda la respuesta que ha dado en la pregunta (a) a averiguar qué debe hacer Sugar?]

Sí. La matriz muestra que a Ristretto siempre le conviene mantener el precio alto.
Si Sugar anticipa esa decisión, *debe entrar*: gana 2 millones en lugar de 0.
La conclusión utiliza también la estrategia dominante identificada en el apartado anterior.

== Equilibrio de Nash
#enunciado[¿Cuál es el equilibrio de Nash? ¿Sólo hay uno?]

El único equilibrio de Nash es *(entrar, precio alto)*, con pagos $(2,3)$.
Con precio alto, Sugar no mejora si se queda fuera: pasa de 2 a 0.
Si Sugar entra, Ristretto no mejora bajando el precio: pasa de 3 a 1.

No hay otro equilibrio, tampoco con estrategias mixtas: Ristretto siempre
prefiere estrictamente el precio alto, y frente a él Sugar prefiere estrictamente entrar.

== Credibilidad de la amenaza
#enunciado[
  Ristretto amenaza a Sugar diciéndole: «Si entras, vamos a fijar un precio muy bajo,
  por lo que lo mejor que puedes hacer es no entrar». ¿Crees que Sugar debe creerse
  la amenaza? ¿Por qué sí o por qué no?
]

*No debe creérsela con los pagos del enunciado.* Una vez que Sugar haya entrado,
Ristretto gana 3 manteniendo el precio alto y sólo 1 bajándolo.
Cumplir la amenaza le costaría 2 millones, por lo que no tiene incentivos a hacerlo.

Si interpretamos que Sugar decide primero y Ristretto fija después el precio,
la inducción hacia atrás lleva al mismo resultado: Ristretto mantiene el precio
alto tanto si Sugar entra como si no; anticipándolo, Sugar entra.
La amenaza no es creíble porque propone una decisión que a Ristretto no le conviene
cuando llega el momento de tomarla.
