#import "@local/homework_template:0.1.0": *

#show: homework_econ.with(
  course: [Análisis de Decisiones Económicas y Mercados],
  title: [Regla de decisión racional y productividad],
  pdf_title: "AnDec_entrega_1",
  heading-numbering: "P1.i)",
)

= Contratación en verano

== Número de horas contratadas

Sea $X_h$ la acción «contratar la hora $h$». Aplicaré la regla de decisión
racional a cada hora adicional:

$
  "Contratar la hora" h quad arrow.l.r quad B(X_h) > C(X_h).
$

El beneficio marginal de contratar la hora $h$ es el ingreso que generan los
cafés servidos durante esa hora:

$
  B(X_h) = "cafés servidos en la hora" h times "precio por café".
$

El coste marginal es el salario correspondiente a esa hora:

$
  C(X_h) = "salario por hora".
$

#table(
  columns: (auto, 1fr, 1fr, 1.15fr),
  align: (center, center, center, center),
  inset: 5pt,
  stroke: 0.5pt,
  table.header([*Hora*], [*Beneficio marginal*], [*Coste marginal*], [*Decisión*]),
  [1], [100€], [45€], [Contratar],
  [2], [80€], [45€], [Contratar],
  [3], [60€], [45€], [Contratar],
  [4], [40€], [45€], [No contratar],
)

Por tanto, contrataría al camarero durante 3 horas, porque el beneficio marginal
es superior al coste marginal durante las 3 primeras horas y cae por debajo en
la cuarta hora.

== Relación entre salario y productividad

La productividad de un empleado es el beneficio marginal del empleador. Por tanto,
un $C(X_h)$ superior a dicho $B(X_h)$ hace que un agente racional (o que aplique
la regla de decisión racional) decida no contratar.

El beneficio marginal esperado (la productividad) marca el valor de reserva del
empresario.

= Contratación en invierno

== Número de horas contratadas

En invierno, el número de cafés servidos por hora es la mitad. La regla aplicada
a cada hora sigue siendo:

$
  B(X_h^"invierno") > C(X_h^"invierno").
$

La tabla de decisión sería entonces:

#table(
  columns: (auto, 1fr, 1fr, 1.15fr),
  align: (center, center, center, center),
  inset: 5pt,
  stroke: 0.5pt,
  table.header([*Hora*], [*Beneficio marginal*], [*Coste marginal*], [*Decisión*]),
  [1], [50€], [45€], [Contratar],
  [2], [40€], [45€], [No contratar],
  [3], [30€], [45€], [No contratar],
  [4], [20€], [45€], [No contratar],
)

Por tanto, en invierno contrataría al camarero durante 1 hora.

== Relación entre meses caros y productividad

En este caso, la capacidad de generar ingresos es la mitad y cae por debajo del
umbral de costes marginales antes. En verano, la tercera hora genera 60€, por
encima del salario de 45€; en invierno, esa misma hora solo genera 30€.

Es decir, en este contexto, un "mes caro" desde el punto de vista de la contratación
es un mes donde los ingresos generados por la productividad son inferiores al coste
marginal (o se llega al umbral antes, reduciendo la contratación).

= Uso de inteligencia artificial

Aunque no he usado la IA como herramienta de _one shot_, sí la incluyo en mi proceso de
aprendizaje y me parece interesante comentar mi método.

#set enum(numbering: "i)")

1. *Inteligencia artificial empleada.* GPT-5.6 Sol Light (OpenAI).
2. *Prompt empleado.* En mi caso, el prompt inicial fue:
  #quote(block: true, attribution: link("https://chatgpt.com/share/6aa70264-ecc4-83eb-8d44-f8c09c0ff76d")[ChatGPT])[
    \[Notas-Parte-II.pdf\]

    Para entender este texto, quiero aplicar una técnica de estudio de "pretest"
    en la cual me harás preguntas sobre el texto antes de que lo lea, para que mi
    cerebro esté más preparado para absorber la información cuando lo lea. En tu
    salida, no adornes demasiado la respuesta, se sucinto.
  ]

  Tras algunas preguntas que fui respondiendo conforme leía el texto, pedí una
  plantilla de #link("https://typst.app/docs/")[typst] con los apartados
  preparados para rellenar con mis respuestas.

3. *Diferencias respecto de la aplicación sistemática del tema.* Como no hice el
  trabajo de forma directa con una IA, no hay diferencias. Aunque por supuesto
  habrá influido en el formato, algunas expresiones, etc.

Desde mi punto de vista, el beneficio de la IA es claro: capacidad de trabajo
multiplicada. No obstante, también incluye un coste implícito: si dejo que
_piense_ por mi, renuncio al aprendizaje que obtendría resolviendo el ejercicio
por mí mismo. Por tanto su uso racional como herramienta de estudio debe
centrarse en funciones de tutor o herramienta de investigación, o para crear una
plantilla inicial del formato de salida (Word, LaTeX o, en mi caso, typst).
