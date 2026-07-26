#import "../../03_recursos_comunes/plantillas_typst/asignatura.typ": *

#show: asignatura.with(
  title: "Ejercicio 1",
  author: "Tu Nombre",
  subject: "Métodos cuantitativos"
)

== Planteamiento del problema
Aquí va el enunciado o tus notas.

== Resolución
Aquí pones la matemática: $ integral_0^infinity e^(-x) dif x = 1 $.

== Resultados computacionales
Aquí importarías la imagen generada por R o Julia.

#data-result(label: "Salida del modelo OLS")[
  - Coeficiente $beta$: 0.85
  - P-valor: 0.002
]
