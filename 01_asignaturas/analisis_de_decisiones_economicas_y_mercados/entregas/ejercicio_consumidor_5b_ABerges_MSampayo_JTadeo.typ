#import "@local/master-uvigo-templates:0.1.0": base-styles, font_sizes, homework_econ
#import "@preview/lilaq:0.6.0" as lq

#show: base-styles
#show: homework_econ.with(
  author: ("Adrián Berges Enfedaque", "Juan Tadeo Fariñas Pereira", "Miguel Sampayo Muñoz"),
  course: [Análisis de Decisiones Económicas y Mercados],
  title: "Teoría del consumidor · Ejercicio 5B",
  heading-numbering: "1.a.1",
)

#set text(size: font_sizes.normalsize)
#set table(stroke: (x: none, y: 0.6pt), align: center)
#set table.hline(stroke: 1.25pt)
#show table.header.where(level: 1): strong

#let enunciado(content) = {
  set text(style: "italic")
  block(fill: luma(200), inset: 8pt, radius: 4pt, stroke: 1pt)[#content]
}
#let argmax = math.op("arg max", limits: true)

// Los comentarios conservan las claves y los resultados de control de la revisión.
// Los enunciados se transcriben con ajustes tipográficos menores.
// Usar font_sizes.normalsize, font_sizes.footnotesize, etc. para los tamaños.
// No se copia el aviso de IA de la plantilla: revisarlo según el uso final.

// Fuente: Ejercicio-Consumidor-5B.pdf, ejercicio 1, apartados a-d.
// Contraste: 5B_JuanTadeo.pdf y Ej.Consumidor_5B_MiguelSampayo.pdf del ZIP.
// Ambos coinciden en demandas, cestas y utilidad indirecta.
// ATENCIÓN: el anexo del profesor ejemplifica u=x1*x2, pero el ejercicio
// pide u=x1*x2^2. No trasladar las participaciones 1/2 del anexo.
#align(center, block(width: 80%, align(center)[
  #set text(size: font_sizes.footnotesize)
  *Aviso de autoría*: en el transcurso del trabajo se ha usado GPT-6.1 Sol Light.
  Su rol ha sido de ayuda para las dudas, edición y mejora de las explicaciones y
  elaboración de gráficas.
]))

= Cálculo analítico con utilidad diferenciable
#enunciado[
  Un consumidor con renta fija $M$ desea comprar dos mercancías a precios
  $(p_1,p_2)$. Sus preferencias están representadas por
  $u(x_1,x_2)=x_1^alpha x_2^beta$, con $alpha=1$ y $beta=2$.
  Como referencia, $M=12$ y $(p_1,p_2)=(3,1)$.
]

== Funciones de demanda marshallianas
#enunciado[
  Suponga precios $(p_1,p_2)$ y renta $M$. Calcule analíticamente las funciones de demanda $d_1(p_1,p_2,M)$ y $d_2(p_1,p_2,M)$.
]

// 1. Suponer p1,p2>0 y M>0; cantidades reales no negativas.
// Plantear max x1*x2^2 sujeto a p1*x1+p2*x2<=M.
// Hay cestas interiores con utilidad positiva; las de los ejes dan cero.
// En el interior ambos bienes aumentan la utilidad, así que se agota M.
Suponiendo $p_1,p_2>0$ y $M>0$, el problema de maximización que definen estos supuestos se puede formular como:
$
  max_(x_1, x_2 in RR^+ union {0}) x_1  x_2^2 \
  "s.t." p_1x_1+p_2x_2<=M .
$ <eq:optimizacion_a>

// 2. Sustituir x2=(M-p1*x1)/p2, con x1 en [0,M/p1].
// phi(x1)=x1*(M-p1*x1)^2/p2^2.
// phi'(x1)=(M-p1*x1)*(M-3*p1*x1)/p2^2.
// Candidato interior x1=M/(3*p1), x2=2*M/(3*p2).
// La otra raíz, x1=M/p1, es un extremo con x2=0: no es máximo.
Para despejar la primera función de demanda, sustituimos $x_2 = (M-p_1x_1)/p_2$
en la @eq:optimizacion_a y obtenemos la utilidad sobre la recta presupuestaria:
$
  phi(x_1)=x_1(M-p_1x_1)^2/p_2^2.
$

Como una cesta con ambos bienes tiene utilidad positiva, el óptimo no estará
en los ejes. Además, en el interior podemos aumentar la utilidad si queda renta
sin gastar, por lo que en el óptimo se agota $M$.
Observamos que $phi(0) = 0$ y $phi(M/p_1) = 0$, mientras que $phi(x_1)>0$
para $0<x_1<M/p_1$. Por lo tanto, el máximo es interior y cumple
$phi'(x_1) = 0$:
$
  phi'(x_1)=(M-p_1x_1)(M - 3 p_1x_1)/p_2^2 = 0 <=> cases(x_1 = M/(3 p_1), x_1 = M/p_1).
$
De estas dos raíces, sólo $x^*_1 = M/(3 p_1)$ puede ser el máximo, puesto que para
$x_1 = M/p_1$, el valor de $x_2$ sería 0. En este máximo, el valor de $x^*_2$ es:

$
  x^*_2 = (M-p_1x^*_1)/p_2 = (M - M/3)/p_2 = (2M)/(3p_2)
$

// 3. Comparar los extremos (0,M/p2),(M/p1,0), de utilidad cero,
// con el interior, de utilidad 4*M^3/(27*p1*p2^2)>0.
// Además phi' es positiva antes de M/(3*p1) y negativa después,
// salvo su anulación en el extremo: queda demostrado el máximo único.

// 4. Resultado: d1=M/(3*p1), d2=2*M/(3*p2).
// Se gasta 1/3 de la renta en el bien 1 y 2/3 en el bien 2.
// Comprobación alternativa interior: UMg1=x2^2, UMg2=2*x1*x2;
// RMS=UMg1/UMg2=x2/(2*x1)=p1/p2. No basta citar tangencia
// sin justificar interioridad y optimalidad. Con M=0 la cesta es (0,0).

Por tanto podemos concluir que:

$
  d_1(p_1, p_2, M) &= M/(3 p_1)\
  d_2(p_1, p_2, M) &= (2M)/(3 p_2)
$ <eq:solucion_1>

== Elección óptima <sec:eleccion_optima>
#enunciado[
  Calcule la cesta óptima para $M=12$ y: b1) $(p_1,p_2)=(3,1)$; b2) $(12,1)$; b3) $(6,1)$.
]

// Sustituir en las demandas y conservar fracciones exactas:
// b1: (x1,x2)=(4/3,8), gasto 3*(4/3)+8=12, utilidad 256/3.
// b2: (x1,x2)=(1/3,8), gasto 12*(1/3)+8=12, utilidad 64/3.
// b3: (x1,x2)=(2/3,8), gasto 6*(2/3)+8=12, utilidad 128/3.
// Proponer una tabla con caso, p1, p2, x1, x2 y gasto.
// Aunque aumenta p1, x2 permanece en 8: su demanda no depende de p1.
// Los resultados coinciden con ambos compañeros; evitar redondear antes
//  de comprobar el presupuesto.


Los tres casos se resuelven por sustitución directa en la @eq:solucion_1:

// #set enum(numbering: "1")
+ $(d_1(3, 1, 12),d_2(3, 1, 12))=(4/3,8)$, gasto $3(4/3)+8=12$, utilidad $ 256/3 approx 85.33$.
+ $(d_1(12, 1, 12),d_2(12, 1, 12))=(1/3,8)$, gasto $12(1/3)+8=12$, utilidad $ 64/3 approx 21.33$.
+ $(d_1(6, 1, 12),d_2(6, 1, 12))=(2/3,8)$, gasto $6(2/3)+8=12$, utilidad $ 128/3 approx 42.67$.

== Curvas de demanda
#enunciado[
  c.1) Represente gráficamente las curvas de demanda de ambos bienes respecto de sus respectivos precios. c.2) Sitúe las cestas óptimas de b1), b2) y b3). Recuerde la definición de curva de demanda y los posibles desplazamientos.
]

// Mantener M=12. Usar dos paneles con cantidad horizontal y precio vertical.
// Bien 1: fijar p2=1, x1=4/p1; inversa p1=4/x1 para x1>0.
// Marcar puntos (cantidad,precio): (4/3,3),(1/3,12),(2/3,6).
// Son movimientos sobre una única curva, no desplazamientos.
// Bien 2: x2=8/p2; inversa p2=8/x2 para x2>0.
// Para p1=3,12,6 la curva es idéntica: no depende del precio del otro bien.
// Las tres observaciones se superponen en (8,1); etiquetar b1=b2=b3.
// No confundir una cesta (x1,x2) con un punto de demanda (xi,pi).
// Para dibujar con lilaq, importar @preview/lilaq:0.6.0 como en la plantilla;
// usando cantidades positivas, muestrear las inversas anteriores, sin x=0.
// Ventanas sugeridas: bien 1 x en [0,5], p en [0,14]; bien 2 x en [0,16],
// p en [0,10]. Añadir ejes, leyendas, unidades y los puntos de control.
// Los gráficos de Juan Tadeo y Miguel confirman estas curvas y superposición.

//
Con $M=12$, las demandas son $x_1=4/p_1$ y $x_2=8/p_2$.
En el bien 1, los tres puntos son movimientos sobre la misma curva. En el bien 2,
la demanda no depende de $p_1$, por lo que las tres observaciones coinciden en $(8,1)$.

#let cantidades1 = range(1, 161).map(i => i / 32)
#let cantidades2 = range(1, 161).map(i => i / 10)
#figure(
  grid(columns: (1fr, 1fr), gutter: 12pt,
    lq.diagram(width: 100%, height: 7cm, xlim: (0,5), ylim: (0,14),
      xlabel: [$x_1$], ylabel: [$p_1$ (€)],
      lq.plot(cantidades1, cantidades1.map(x => 4/x), mark: none, color: blue),
      lq.plot((4/3,1/3,2/3), (3,12,6), stroke: none, mark: "o", color: red),
      lq.place(1.5,3, align: left, [b1]),
      lq.place(0.5,12, align: left, [b2]),
      lq.place(0.85,6, align: left, [b3]),
    ),
    lq.diagram(width: 100%, height: 7cm, xlim: (0,16), ylim: (0,10),
      xlabel: [$x_2$], ylabel: [$p_2$ (€)],
      lq.plot(cantidades2, cantidades2.map(x => 8/x), mark: none, color: blue),
      lq.plot((8,), (1,), stroke: none, mark: "o", color: red),
      lq.place(8,1.5, align: bottom, [b1 = b2 = b3]),
    ),
  ),
  caption: [Demandas de ambos bienes y puntos obtenidos en el apartado b.],
)


== Función indirecta de utilidad
#enunciado[
  Calcule la función indirecta de utilidad.
]

// Definición: v(p1,p2,M)=u(d1(p1,p2,M),d2(p1,p2,M)).
// Sustituir: v=[M/(3*p1)]*[2*M/(3*p2)]^2=4*M^3/(27*p1*p2^2).
// Comprobar las tres utilidades del apartado b. Es creciente en M y
//  decreciente en ambos precios para datos positivos; homogénea de grado
// cero al escalar simultáneamente precios y renta por t>0.
// No usar M^2/(4*p1*p2): corresponde al ejemplo distinto del anexo.


Usamos la definición de la función indirecta de utilidad, y operamos
sustituyendo lo obtenido en la @eq:solucion_1:

$
  v(p_1,p_2,M) &= u(d_1(p_1,p_2,M),d_2(p_1,p_2,M)) \
  &= [M/(3p_1)][2M/(3p_2)]^2
  &= 4M^3/(27p_1p_2^2).
$

#let indirect_utility(p1, p2, M) = calc.round(4*calc.pow(M,3)/(27*p1*calc.pow(p2,2)), digits: 2)

A modo de comprobación, la usaremos para volver a calcular lo pedido en la
@sec:eleccion_optima:

+ $v(3, 1,12) = 4 dot 12^3/(27 dot 3 dot 1^2) approx #indirect_utility(3,  1, 12).$ 
+ $v(12, 1,12) = 4 dot 12^3/(27 dot 12 dot 1^2) approx #indirect_utility(12,  1, 12).$ 
+ $v(6,1,12) = 4 dot 12^3/(27 dot 6 dot 1^2) approx #indirect_utility(6, 1, 12).$ 
