#import "@local/master-uvigo-templates:0.1.0": base-styles, font_sizes, homework_econ
#import "@preview/lilaq:0.6.0" as lq

// #show math.equation: set text(font: "Libertinus Math")
#show: base-styles
#show: homework_econ.with(
  author: ("Iván Sobreira Solar", "Sergio Gustavo Bravo Matta", "Adrian Berges Enfedaque"),
  course: [Análisis de Decisiones Económicas y Mercados],
  title: "Ejercicio 7 · Equilibrio walrasiano",
  date: datetime(year: 2026, month: 11, day: 1),
  heading-numbering: "1.a.1",
)
#set text(lang: "es", size: font_sizes.normalsize)
#set table(stroke: (x: none, y: 0.6pt), align: center, inset: 5pt)
#show table.header: strong
#let enunciado(body) = {
  set text(style: "italic")
  block(breakable: false, fill: luma(200), inset: 8pt, radius: 4pt, stroke: 1pt)[#body]
}
#let punto(x, y, color: red) = lq.plot((x,), (y,), mark: "o", stroke: none, color: color)
#let caja(..objetos) = lq.diagram(
  width: 85%, height: 6cm, xlim: (0,4), ylim: (0,6),
  xlabel: [Vino de la colega ($a$)], ylabel: [Cola de la colega ($b$)],
  lq.plot((0,4,4,0,0), (0,0,6,6,0), mark: none, color: black),
  ..objetos.pos(),
)
// Fuentes: Ejercicio-Equilibrio-Xeral.pdf y transp-M-PIII-6-English.pdf.
// Apuntes: demanda neta, pp. 14-17; ley de Walras, pp. 22-23;
// equilibrio, pp. 32-33; eficiencia de Pareto, p. 49; curva de contrato, p. 58.
// Las páginas se cuentan desde la primera diapositiva del archivo.

= Intercambio, eficiencia y equilibrio
#enunciado[
Queda con una colega para ir de botellón, y acuerdan en llevar vino tinto y latas de Cola (de 500 ml.). Su colega es muy exquisita y le gusta beber kalimotxos en proporciones exactas: 1 litro de vino por 2 latas de Cola (1 litro de Cola). A Usted, sin embargo, no le hace efecto el alcohol, y sólo bebe para hidratarse: así, si para quitar la sed bebe 1 litro de líquido, le resulta indiferente, por ejemplo, beber «1 litro de vino», o bien «1 litro (2 latas) de Cola», o bien «0,5 litro de vino y 0,5 litros de Cola (1 lata)».
]

== Preferencias
#enunciado[
Presente analíticamente las preferencias que describan los gustos de su colega y las suyas.

_Pista 1._ Las preferencias son distintas. _Pista 2._ Recuerde las preferencias del Ejercicio 1. Teoría del Consumidor. _Pista 3._ Aunque hablamos de litros de vino y Cola, considere mejor las mercancías botellas de vino y latas de Cola.
]
Llamamos $A$ a la colega y $B$ a uno mismo. Si $x_1$ son botellas de vino y $x_2$
son latas de Cola, podemos representar las preferencias como:
$
 u_A (x_1,x_2)=min(2x_1,x_2), quad u_B (x_1,x_2)=x_1+x_2/2.
$
Para $A$ son *complementarios perfectos*: el excedente de un bien no aumenta
su bienestar. Para $B$ son *sustitutivos perfectos*: una botella y dos latas
aportan el mismo líquido. Formalmente, $x succ.eq_i y$ si y sólo si
$u_i (x)>=u_i (y)$. Usaremos cantidades no negativas y divisibles, como en el
apartado que propone una cesta de 1.5 botellas.

== Mapas de indiferencia
#enunciado[
Situando la mercancía botellas de vino (litros de vino) en el eje de abscisas, y la mercancía latas de Cola (litros de Cola) en el eje de ordenadas, dibuje las preferencias de su colega en su conjunto de consumo, y las suyas en su respectivo conjunto de consumo.
]
Los conjuntos de $A$ tienen forma de L, con vértices en $x_2=2x_1$.
Los de $B$ son rectas $x_2=2u_B-2x_1$, con pendiente $-2$.

#figure(grid(columns: (1fr,1fr), gutter: 14pt,
  lq.diagram(width: 100%, height: 4.4cm, xlim: (0,4), ylim: (0,6),
    xlabel: [Vino de $A$], ylabel: [Cola de $A$],
    ..(1,2,3).map(t => lq.plot((t,t,4), (6,2*t,2*t), mark: none, color: blue)),
  ),
  lq.diagram(width: 100%, height: 4.4cm, xlim: (0,4), ylim: (0,6),
    xlabel: [Vino de $B$], ylabel: [Cola de $B$],
    ..(1,2,3).map(t => lq.plot((0,t), (2*t,0), mark: none, color: red)),
  ),
), caption: [Preferencias de $A$ (azul) y de $B$ (rojo).])

== Caja de Edgeworth
#enunciado[
Cuando se encuentra con su colega, resulta que entre los dos tienen en total 4 botellas de vino (4 litros de vino) y 6 latas de 500 ml. de Cola (3 litros de Cola), es decir, la dotación agregada es $omega=(4,6)$.

Dibuje la caja de Edgeworth, suponiendo que en el vértice inferior izquierdo estamos ubicando la cesta «cero vino, cero Cola» (asignación $(0,0)$) de su colega, y en el vértice superior derecho de la caja está su cesta «cero vino, cero Cola» (su asignación $(0,0)$).
]
La caja tiene anchura $4$ y altura $6$. Cada punto $(a,b)$ representa el reparto:
$
 x_A=(a,b), quad x_B=(4-a,6-b), quad 0<=a<=4, quad 0<=b<=6.
$
El origen $O_A$ está en $(0,0)$ y $O_B$ en $(4,6)$. Desde $O_B$ las cantidades
propias se leen hacia la izquierda y hacia abajo. Por ejemplo, el punto
$(1,2)$ representa una cesta $(1,2)$ para $A$ y $(3,4)$ para $B$.

== Preferencias dentro de la caja
#enunciado[
Dibuje en la misma caja de Edgeworth las preferencias de su colega y las suyas (las representadas en el apartado b)): es decir, conjuntamente el mapa de indiferencias de mi colega y mi mapa de indiferencias en la caja de Edgeworth.
]
En coordenadas de $B$, la utilidad propia es:
$
 u_B (4-a,6-b)=7-a-b/2.
$
Por tanto, sus rectas de indiferencia son $b=14-2u_B-2a$. Las de $B$
siguen siendo las mismas L. El bienestar de $A$ aumenta hacia el nordeste,
y el de $B$, hacia el sudoeste.

#figure(caja(
  ..(1,2,3).map(t => lq.plot((t,t,4), (6,2*t,2*t), mark: none, color: blue)),
  ..(4,6,8,10).map(c => lq.plot((0,4), (c,c - 8), mark: none, color: red, stroke: (dash: "dashed"))),
  lq.place(0.1,0.15, align: bottom + left, [$O_A$]),
  lq.place(3.9,5.85, align: top + right, [$O_B$]),
), caption: [Caja de Edgeworth y mapas de indiferencia. Los ejes indican las cantidades de $B$; las suyas ($A$) son las restantes.])

== Conjunto de Pareto o curva de contrato
#enunciado[
«Una asignación (un reparto de recursos de la economía) es Pareto eficiente (o eficiente en el sentido de Pareto) cuando no existe ninguna otra asignación factible (otro reparto factible de los mismos recursos) donde algún agente puede mejorar sin que empeore ningún otro».

En el gráfico obtenido en el apartado d), indique el conjunto de Pareto (o curva de contrato), es decir, el conjunto de las asignaciones Pareto eficientes en la caja de Edgeworth.
]
Si a $B$ le sobra vino, puede ceder parte a $A$ sin perder bienestar,
y $A$ mejora. Lo mismo ocurre si le sobra Cola. Por tanto, una asignación
con excedentes de alguno de los dos bienes para $B$ no es eficiente.

El conjunto de Pareto es el segmento donde consume en la proporción exacta:
$
 "CP"={(a,b):b=2a, 0<=a<=3}.
$
El límite es $a=3$, porque sólo hay 6 latas. Para comprobar la eficiencia,
en $(t,2t)$ $B$ obtiene $2t$. Mantener ese bienestar exige darle al
menos $t$ botellas y $2t$ latas. Si mejora, necesita más de ambos y $A$
pierde líquido; si $A$ mejora quitándole algo, $B$ empeora.
Esto también incluye los extremos $(0,0)$ y $(3,6)$.

== Asignación autárquica
#enunciado[
Suponga que de las 4 botellas de vino y 6 latas de 500 ml. de Cola, su colega trajo 3 botellas de vino y 1 lata de Cola, es decir, la dotación inicial de su colega es $omega_"colega"=(3,2)$, mientras que Usted trajo el resto, es decir, su dotación inicial es $omega_"Usted"=(1,4)$.

Indique en la caja de Edgeworth la asignación que representa las dotaciones iniciales de su colega y la suya.

_Pista._ Recuerde que estamos representando las asignaciones de su colega en el vértice inferior izquierdo, y las suyas en el vértice superior derecho.
]
Tomamos $omega_A=(3,2)$ y $omega_B=(1,4)$, por lo que la autarquía se representa
en el punto $W=(3,2)$. Las utilidades iniciales son:
$
 u_A (3,2)=2, quad u_B (1,4)=3.
$
#text(size: font_sizes.footnotesize)[
  El enunciado dice «1 lata», pero escribe $omega_A=(3,2)$ y $omega_B=(1,4)$.
  Usamos estas dotaciones explícitas, que suman el total $(4,6)$.
]

#figure(caja(
  lq.plot((0,3), (0,6), mark: none, color: green, stroke: 2pt),
  punto(3,2), lq.place(3.1,2.1, align: bottom + left, [$W=(3,2)$]),
  punto(3,6, color: green),
), caption: [Curva de contrato en verde y dotación inicial en rojo.])

== Lente de intercambio
#enunciado[
Indique en el gráfico presentado en el apartado f) la región de asignaciones de la caja de Edgeworth donde tanto mi colega como yo mejoraríamos llegando a acuerdos.
]
Para que ninguno empeore respecto a la autarquía se necesita:
$
 min(2a,b)>=2 quad "y" quad 7-a-b/2>=3.
$
Por tanto, la región de intercambios débilmente beneficiosos es:
$
 L={(a,b):a>=1, b>=2, a+b/2<=4}.
$
Es el triángulo de vértices $(1,2)$, $(3,2)$ y $(1,6)$.
Para que *ambos mejoren estrictamente*, las tres desigualdades deben ser
estrictas: $a>1$, $b>2$ y $a+b/2<4$. En las fronteras al menos uno queda
igual que al principio.

== Núcleo de la economía
#enunciado[
«El núcleo de una economía es el conjunto de asignaciones del conjunto de Pareto donde ambos consumidores están como mínimo igual que en sus dotaciones iniciales».

Indique en el gráfico presentado en el apartado g) el núcleo de la economía.
]
El núcleo es la parte de la curva de contrato que está en la lente.
Sustituyendo $b=2a$ en sus restricciones:
$
 2a>=2, quad 7-2a>=3 quad => quad 1<=a<=2.
$
Por tanto:
$
 "N"={(a,2a):1<=a<=2}.
$
En $(1,2)$ $B$ queda igual y $A$ mejora; en $(2,4)$ $A$ queda igual
y $B$ mejora. Entre ambos extremos mejoran los dos.

#figure(caja(
  ..range(1,40).map(i => {
    let b = 2+i/10
    lq.plot((1,4-b/2), (b,b), mark: none, color: rgb("d5e6f4"))
  }),
  lq.plot((1,3,1,1), (2,2,6,2), mark: none, color: blue),
  lq.plot((0,3), (0,6), mark: none, color: gray, stroke: (dash: "dashed")),
  lq.plot((1,2), (2,4), mark: none, color: green, stroke: 3pt),
  punto(3,2), punto(1,2, color: green), punto(2,4, color: green),
  lq.place(3.1,2.1, align: bottom + left, [$W$]),
  lq.place(2.1,4.1, align: bottom + left, [$(2,4)$]),
  lq.place(1.1,1.7, align: top + left, [$(1,2)$]),
), caption: [Lente de intercambio rayada y núcleo en verde. La recta gris prolonga la curva de contrato.])

== Primera propuesta de equilibrio
#enunciado[
Finalmente llega a un acuerdo con su colega de intercambiar vino y Cola.

Suponga que el acuerdo alcanzado consiste en que su colega consume «2 botellas de vino y 4 latas de Cola» (asignación $x_"colega"=(2,4)$) y Usted «2 botellas de vino y 2 latas de Cola» (asignación $x_"Usted"=(2,2)$). ¿Puede ser esta una asignación de equilibrio?

En caso afirmativo, indique ¿cuál sería el precio relativo del vino con respecto a las latas de Cola? (o, alternativamente, suponga que el precio de las latas es de 1 euro, ¿cuál sería el precio del vino en el intercambio de equilibrio?). En caso negativo, explique por qué no puede ser una asignación de equilibrio.
]
*Sí.* Como usted consume ambos bienes y una botella equivale a dos latas,
el precio relativo debe ser $p_1/p_2=2$. Normalizando $p_2=1$, tenemos
$p=(2,1)$. Las rentas son el valor de las dotaciones:
$
 M_A=2 dot 3+2=8, quad M_B=2 dot 1+4=6.
$
$B$ elige el codo $b=2a$ sobre $2a+b=8$, es decir, $(2,4)$.
$A$ obtiene $u_B=x_1+x_2/2=(2x_1+x_2)/2$, de modo que cualquier cesta
que agote sus $6€$ es óptima. En particular, $(2,2)$ lo es.

Las cantidades suman $(4,6)$: ambos eligen cestas óptimas y los mercados
se vacían. $B$ vende una botella a cambio de dos latas.

== Segunda propuesta de equilibrio
#enunciado[
Suponga que el acuerdo al que llegaron resulta en que su colega consume «1,5 litros (botellas) de vino y 3 latas de Cola» (asignación $x_"colega"=(1.5,3)$) y Usted «2,5 litros (botellas) de vino y 3 latas de Cola» (asignación $x_"Usted"=(2.5,3)$). ¿Puede ser esta una asignación de equilibrio?

En caso afirmativo, indique ¿cuál sería el precio relativo del vino con respecto a las latas de Cola? (o, alternativamente, suponga que el precio de las latas es de 1 euro, ¿cuál sería el precio del vino en el intercambio de equilibrio?). En caso negativo, explique por qué no puede ser una asignación de equilibrio.
]
*No.* El reparto es factible y pertenece al núcleo, pero eso no basta para
que sea un equilibrio con estas dotaciones. Como usted consume ambos bienes,
su optimalidad exigiría de nuevo $p_1/p_2=2$.

A esos precios, la cesta de $B$ cuesta $2 dot 1.5+3=6€$, pero dispone
de $8€$. Puede elegir $(2,4)$ y pasar de utilidad 3 a 4, así que $(1.5,3)$
no es óptima. Además, su cesta $(2.5,3)$ cuesta $8€$ y $A$ sólo dispone de $6€$.

Si intentamos que el intercambio respete los presupuestos, $B$ cede
$1.5$ botellas y recibe una lata, de donde $1.5p_1=p_2$ y $p_1/p_2=2/3$.
Pero con esa relación $A$ prefiere gastar todo en vino, que hidrata más por
euro. Por tanto, tampoco son precios que sostengan el reparto propuesto.

#figure(caja(
  lq.plot((0,3), (0,6), mark: none, color: gray, stroke: (dash: "dashed")),
  lq.plot((1,4), (6,0), mark: none, color: blue),
  punto(3,2), punto(2,4, color: green), punto(1.5,3, color: orange),
  lq.place(3.1,2.1, align: bottom + left, [$W$]),
  lq.place(2.1,4.1, align: bottom + left, [Equilibrio]),
  lq.place(1.6,2.9, align: top + left, [Segunda propuesta]),
), caption: [La recta presupuestaria $2a+b=8$ pasa por la dotación y el equilibrio, pero no por la segunda propuesta.])

#pagebreak()
= Demanda de mercado y equilibrio walrasiano
#enunciado[
Sea una economía compuesta por dos agentes $i=A,B$ y dos mercancías $L=1,2$, es decir, la economía $epsilon={(X_A,succ.eq_A,omega_A),(X_B,succ.eq_B,omega_B)}$, donde:

(1) (Conjunto de consumo) $X_i equiv RR_+^2$; (2) (dotaciones) $omega_A=(5,1)$ y $omega_B=(1,5)$; y (3) las funciones de demanda (walrasianas) de los consumidores son:
$ d_A (p_1,p_2)=(d_(A 1) (p_1,p_2),d_(A 2) (p_1,p_2))=((5p_1+p_2)/(2p_1),(5p_1+p_2)/(2p_2)); $
$ d_B (p_1,p_2)=(d_(B 1) (p_1,p_2),d_(B 2) (p_1,p_2))=((p_1+5p_2)/(2p_1),(p_1+5p_2)/(2p_2)). $
]

== Demandas de mercado
#enunciado[
Agregue las funciones de demanda de la mercancía 1 y de la mercancía 2, y obtenga las curvas de demanda de mercado para cada una de las mercancías; es decir,
$Q_1=D_1 (p_1,p_2)=d_(A 1) (p_1,p_2)+d_(B 1) (p_1,p_2)$ y
$Q_2=D_2 (p_1,p_2)=d_(A 2) (p_1,p_2)+d_(B 2) (p_1,p_2)$.

_Curiosidad._ Observe que podría dibujar la curva de demanda de la mercancía 1 para cualquier precio de la mercancía 2 (por ejemplo, para $p_2=5$ podría dibujar $Q_1=D_1 (p_1,5)$); y, análogamente, indicando un precio de la mercancía 1 (por ejemplo, $p_1=0.2$), podría dibujar la curva de demanda de la mercancía 2, $Q_2=D_2 (0.2,p_2)$.
]
Simplemente sumamos las demandas individuales:
$
 D_1(p_1,p_2)=(6p_1+6p_2)/(2p_1)=3+3p_2/p_1, \
 D_2(p_1,p_2)=(6p_1+6p_2)/(2p_2)=3+3p_1/p_2.
$
La renta cambia con los precios, porque procede de vender las dotaciones.
Para dibujar cada curva de demanda propia mantenemos fijo el precio del otro bien.

== Ofertas de mercado
#enunciado[
Obtenga las curvas de oferta de mercado para cada una de las mercancías; es decir,
$Q_1=S_1 (p_1,p_2)=omega_(A 1)+omega_(B 1)$ y
$Q_2=S_2 (p_1,p_2)=omega_(A 2)+omega_(B 2)$.
]
Como es una economía de intercambio puro, la oferta total es la dotación:
$S_1=5+1=6$ y $S_2=1+5=6$. Ambas curvas son verticales en $Q=6$.

== Mercados con precios $(2,1)$
#enunciado[
c.1) Dibuje (con Excel o con R) las curvas de demanda y oferta en cada uno de los mercados de las mercancías $l=1$ y $l=2$ (es decir, 2 gráficos), si el vector de precios es $p=(2,1)$.

c.2) ¿Es $p=(2,1)$ un vector de precios de equilibrio? (sí/no). ¿Existe un exceso de oferta o de demanda en los mercados a este vector de precios? (1 línea).

c.3) ¿Podrían estar ambos mercados en exceso de demanda positiva para algún otro vector de precios? Indique en qué resultado teórico se basa para su respuesta (1 línea).
]
Para el mercado 1 fijamos $p_2=1$; para el mercado 2 fijamos $p_1=2$.
#let qs = range(1,151).map(i => 3+i/15)
#figure(grid(columns: (1fr,1fr), gutter: 14pt,
  lq.diagram(width: 100%, height: 5cm, xlim: (0,13), ylim: (0,4),
    xlabel: [$Q_1$], ylabel: [$p_1$],
    lq.plot(qs, qs.map(q => 3/(q - 3)), mark: none, color: blue),
    lq.plot((6,6), (0,4), mark: none, color: red),
    lq.plot((0,7), (2,2), mark: none, color: gray, stroke: (dash: "dashed")),
    punto(4.5,2), punto(6,2),
    lq.place(2.5,2.15, align: bottom, [D = 4,5]),
    lq.place(7.8,2.15, align: bottom, [S = 6]),
  ),
  lq.diagram(width: 100%, height: 5cm, xlim: (0,13), ylim: (0,4),
    xlabel: [$Q_2$], ylabel: [$p_2$],
    lq.plot(qs, qs.map(q => 6/(q - 3)), mark: none, color: blue),
    lq.plot((6,6), (0,4), mark: none, color: red),
    lq.plot((0,10), (1,1), mark: none, color: gray, stroke: (dash: "dashed")),
    punto(9,1), punto(6,1),
    lq.place(9.8,1.15, align: bottom, [D = 9]),
    lq.place(5.3,1.15, align: bottom, [S = 6]),
  ),
), caption: [Demanda en azul y oferta en rojo. Se señalan las cantidades a los precios propuestos.])
*No hay equilibrio*: en el bien 1 sobra $6-4.5=1.5$ y en el bien 2 faltan $9-6=3$.
Con precios positivos, ambos excesos no pueden ser positivos a la vez por
la *ley de Walras*: $p_1z_1+p_2z_2=0$.

== Exceso de demanda
#enunciado[
d.1) Indique la expresión formal de la función de exceso de demanda para las mercancías $l=1$ y $l=2$, es decir,
$z_1 (p_1,p_2)=D_1 (p_1,p_2)-O_1 (p_1,p_2)$ y
$z_2 (p_1,p_2)=D_2 (p_1,p_2)-O_2 (p_1,p_2)$.

d.2) Dibuje (con Excel o con R) la función de exceso de demanda neta para la mercancía $l=1$, es decir, $z_1 (p_1/p_2,1)=D_1 (p_1/p_2)-O_1 (p_1/p_2)$, donde $p_1/p_2$ es el precio relativo de la mercancía 2 con respecto a la mercancía 1.

_Pista 1._ Dibuje el gráfico con la función de exceso de demanda $z_1 (p_1/p_2,1)$ en el eje vertical y los precios relativos en el eje horizontal.

_Pista 2._ La función de exceso de demanda neta es homogénea de grado cero, por eso $z_1 (p_1,p_2)=z_1 (p_1/p_2,1)$.

_Pista 3 (curiosidad)._ El precio relativo $p_1/p_2$ es la Relación Marginal de Intercambio, la pendiente de la recta presupuestaria.

d.3) Explique la gráfica y el significado de la raíz (el valor que hace cero a la función de exceso de demanda neta).
]
Restamos las ofertas a las demandas:
$
 z_1 (p_1,p_2)=3p_2/p_1-3, quad z_2 (p_1,p_2)=3p_1/p_2-3.
$
Se comprueba la ley de Walras:
$p_1z_1+p_2z_2=(3p_2-3p_1)+(3p_1-3p_2)=0$.
Son homogéneas de grado cero: sólo importa la relación de precios.
Llamando $r=p_1/p_2$, normalizamos $p_2=1$ y obtenemos $z_1 (r,1)=3/r - 3$.

#text(size: font_sizes.footnotesize)[
  En el enunciado hay una errata: $p_1/p_2$ es el precio del bien 1 respecto
  al 2, no al revés. La pendiente presupuestaria es $-p_1/p_2$.
]
#let rs = range(5,121).map(i => i/40)
#figure(lq.diagram(width: 80%, height: 4.8cm, xlim: (0,3), ylim: (-3,9),
  xlabel: [Precio relativo $r=p_1/p_2$], ylabel: [$z_1 (r,1)$],
  lq.plot(rs, rs.map(r => 3/r - 3), mark: none, color: blue),
  lq.plot((0,3), (0,0), mark: none, color: gray),
  punto(1,0), punto(2,-1.5, color: orange),
  lq.place(1.1,0.4, align: bottom + left, [Equilibrio]),
), caption: [Exceso de demanda del bien 1 en función de su precio relativo.])
Si $r<1$ hay exceso de demanda del bien 1; si $r>1$ hay exceso de oferta.
La raíz es $r=1$. A ese precio relativo se vacía el mercado 1 y, por la ley
de Walras, también el 2. En $r=2$ recuperamos el exceso $-1.5$ del apartado anterior.

== Equilibrio competitivo walrasiano
#enunciado[
a) Defina un equilibrio competitivo para esta economía.

b) Indique cuál es el equilibrio competitivo para los precios calculados en el apartado d).
]
Un equilibrio es un vector de precios positivos y una asignación tal que:
(1) cada consumidor elige una cesta óptima dentro del presupuesto dado por
el valor de su dotación; y (2) las demandas agregadas igualan las dotaciones.

Normalizando, $p^*=(1,1)$. Sustituimos en las demandas dadas:
$
 d_A (1,1)=(3,3), quad d_B (1,1)=(3,3).
$
Cada uno dispone de renta $6$, y las cantidades suman $(6,6)$.
Las demandas netas son $d_A-omega_A=(-2,2)$ y $d_B-omega_B=(2,-2)$:
$A$ vende dos unidades del bien 1 a cambio de dos del bien 2, y $B$ hace lo contrario.
Cualquier $p^*=(t,t)$ con $t>0$ representa el mismo equilibrio.

#text(size: font_sizes.footnotesize)[
  Referencia teórica: Eduardo L. Giménez, _Topic 8. Walrasian General Equilibrium_,
  diapositivas facilitadas en la asignatura: pp. 14-17 (demanda neta),
  22-23 (ley de Walras), 32-33 (equilibrio), 49 y 58 (eficiencia y curva de contrato).
]
