#import "@local/master-uvigo-templates:0.1.0": base-styles, font_sizes, homework_econ

#import "@preview/lilaq:0.6.0" as lq

#show: base-styles
#show: homework_econ.with(
  author: ("Adrián Berges Enfedaque", "Juan Tadeo Fariñas Pereira", "Miguel Sampayo Muñoz"),
  course: [Análisis de Decisiones Económicas y Mercados],
  title: "Teoría del consumidor · Ejercicio 5C",
  heading-numbering: "I.1.1",
)

#set text(size: font_sizes.normalsize)
#set table(stroke: (x: none, y: 0.6pt), align: center)
#set table.hline(stroke: 1.25pt)
#show table.header.where(level: 1): strong

#let enunciado(content) = {
  set text(style: "italic")
  block(fill: luma(200), inset: 8pt, radius: 4pt, stroke: 1pt)[#content]
}

// Los comentarios conservan las claves y los resultados de control de la revisión.
// Los enunciados se transcriben con ajustes tipográficos menores.
// Usar font_sizes.normalsize, font_sizes.footnotesize, etc. para los tamaños.
// No se copia el aviso de IA de la plantilla: revisarlo según el uso final.

// Fuente: Ejercicio-Consumidor-5C.pdf, apartados 1-6.
// Contraste: 5C_JuanTadeo.pdf del ZIP. El archivo denominado
// Ej.Consumidor_5C_MiguelSampayo.pdf contiene realmente dos páginas del 5B;
// por tanto no aporta una segunda comprobación independiente del 5C.
// Modelo estándar: cantidades divisibles, p1,p2>0 y M>=0.
// La referencia a bolsas/latas no cambia automáticamente el dominio a enteros.
#align(center, block(width: 80%, align(center)[
  #set text(size: font_sizes.footnotesize)
  *Aviso de autoría*: en el transcurso del trabajo se ha usado GPT-6.1 Sol Light.
  Su rol ha sido de ayuda para las dudas, edición y mejora de las explicaciones y
  elaboración de gráficas.
]))

= Describiendo los gustos individuales
#enunciado[
  Invita a unos amigos a ver un partido en casa. Sus gustos consisten en
  tomar una bolsa de patatas fritas (bien 1, abscisas) por cada dos latas de
  cerveza (bien 2, ordenadas).
]

== Relación binaria
#enunciado[
Indique formalmente las preferencias de sus colegas a través de una relación binaria.
]

// Definir X=R_+^2. Para x,y en X: x ≽ y si y solo si
// min(2*x1,x2)>=min(2*y1,y2). Son complementarios perfectos.
// Interpretar min(x1,x2/2) como número de combinaciones completas;
// min(2*x1,x2) mide lo mismo en unidades de cerveza aprovechable.
// Un excedente aislado del bien abundante no mejora el bienestar.
// La relación es completa y transitiva porque compara números reales.
// Es débilmente monótona y localmente no saciable, pero no estrictamente
// monótona en cada bien: no confundir estas propiedades.


El espacio de cestas válidas es $X = RR_(>=0)^2$. Aunque compramos bolsas y
latas enteras, usaremos el modelo continuo para estudiar las curvas de
indiferencia, la RMS y las funciones de demanda. En los tres casos numéricos
la cesta óptima tendrá cantidades enteras.
Para $x, y in X$, $
  x succ.eq y <==> min(2x_1, x_2) >= min(2y_1, y_2).
$

Esto indica que los amigos prefieren 1 bolsa de patatas por cada 2 cervezas.
Un excedente aislado del bien abundante no mejora el bienestar, por lo que son
bienes complementarios perfectos. La relación es completa y transitiva,
ya que estamos comparando números reales.

== Conjuntos de indiferencia
#enunciado[
(2.1) Describa formalmente las preferencias mediante conjuntos de indiferencia.
(2.2) Compruebe que $(1,2)$, $(5,2)$ y $(1,5)$ son indiferentes.
(2.3) Indique los conjuntos de indiferencia de $(1,2)$, $(2,4)$ y $(3,6)$.
(2.4) Dibuje esos conjuntos en un mismo gráfico.
(2.5) Defina la relación marginal de sustitución (RMS).
(2.6) Indique la RMS en $(1,2)$, $(5,2)$ y $(1,5)$.
(2.7) Generalice a cualquier cesta y explique su intuición económica.
]

// 2.1: I(y)={x in X:min(2*x1,x2)=min(2*y1,y2)}.
// La indiferencia exige x≽y e y≽x; no es el conjunto de cestas mejores.
// 2.2: min(2,2)=min(10,2)=min(2,5)=2.
// 2.3: para k>=0, I_k={(x1,k):x1>=k/2} unión
// {(k/2,x2):x2>=k}. Usar k=2,4,6, respectivamente.
// Los vértices son (1,2),(2,4),(3,6); cada conjunto tiene forma de L.
// 2.4: dibujar tres L, con brazos hacia la derecha y arriba, ejes x1,x2;
// añadir el rayo x2=2*x1 discontinuo como guía de vértices (no es una
// curva de indiferencia). Mayor bienestar hacia el nordeste.
// Con lilaq pueden trazarse polilíneas (k/2,10),(k/2,k),(6,k),
// para k=2,4,6. Marcar además (5,2),(1,5) en la primera L.
// 2.5: RMS_12=-dx2/dx1 manteniendo u constante, cuando hay tangente.
// Es la cantidad marginal de bien 2 que se cede por una unidad de bien 1.
// Con diferenciabilidad y UMg2>0, RMS=UMg1/UMg2; no aplicar en el codo.
// 2.6: en (5,2) brazo horizontal: RMS=0; en (1,5) brazo vertical:
// pendiente vertical, RMS=+infinito en sentido extendido (sin cociente real).
// En (1,2) NO está definida: pendientes laterales distintas. No vale 2;
// la proporción fija 2 no es una tasa marginal de sustitución.
// 2.7: x2<2*x1: sobra patata, u=x2, RMS=0.
// x2>2*x1: sobra cerveza, u=2*x1, RMS vertical (+infinito).
// x2=2*x1: vértice sin RMS única. En los ejes hablar de pendientes
// unilaterales factibles; el origen tampoco tiene tangente única.
// Matiz al contrastar Juan Tadeo: su resultado por tramos es correcto,
// pero no identificar la RMS del vértice con infinito; es indefinida.


=== Conjuntos de indiferencia
La indiferencia exige que $x succ.eq y$ e $y succ.eq x$. Podemos formalizarlo como:
$
  I(y)={x in X:min(2x_1,x_2)=min(2y_1,y_2)}.
$
=== Comprobación de indiferencia
Simplemente sustituimos:
$
  min(2,2) = min(10,2) = min(2, 5) = 2.
$
=== Conjuntos de indiferencia de cestas
Para las cestas dadas, tendríamos:

$
 I(1,2) &= {(x_1,2):x_1>=1} union {(1,x_2):x_2>=2}, \
 I(2,4) &= {(x_1,4):x_1>=2} union {(2,x_2):x_2>=4}, \
 I(3,6) &= {(x_1,6):x_1>=3} union {(3,x_2):x_2>=6}.
$

=== Gráficos de conjuntos de indiferencia
Los tres conjuntos tienen forma de L. Los vértices están sobre $x_2=2x_1$;
esta recta nos sirve de guía, pero no es un conjunto de indiferencia.

#figure(
  lq.diagram(width: 85%, height: 8cm, xlim: (0,6), ylim: (0,10),
    xlabel: [Bolsas de patatas ($x_1$)], ylabel: [Latas de cerveza ($x_2$)],
    legend: (position: top + right),
    lq.plot((1,1,6), (10,2,2), mark: none, color: blue, label: [$I(1,2)$]),
    lq.plot((2,2,6), (10,4,4), mark: none, color: red, label: [$I(2,4)$]),
    lq.plot((3,3,6), (10,6,6), mark: none, color: green, label: [$I(3,6)$]),
    lq.plot((0,5), (0,10), mark: none, color: gray, stroke: (dash: "dashed")),
    lq.plot((1,5,1), (2,2,5), stroke: none, mark: "o", color: blue),
  ),
  caption: [Conjuntos de indiferencia y cestas con el mismo bienestar.],
)

=== Relación marginal de sustitución
Se define como:
$
  "RMS"_(1,2) = - lr((upright(d) x_2)/(upright(d) x_1) |)_(u " constante").
$
Es la cantidad marginal de bien 2 que se cede por una unidad más de bien 1,
manteniendo el mismo bienestar. Donde la curva de indiferencia tiene una
pendiente definida, la RMS es esa pendiente cambiada de signo.
En el codo no hay una única tangente, así que no podemos aplicar esa fórmula.
En el brazo vertical se habla de RMS infinita, en sentido extendido.

=== Aplicar definición de RMS
Vayamos caso por caso:
+ $(1,2)$: no está definida, pendientes laterales distintas.
+ $(5,2)$: brazo horizontal, $"RMS"=0$.
+ $(1,5)$: brazo vertical, $"RMS"=+oo$
=== RMS en cesta arbitraria

$
  "RMS"(x_1, x_2) = cases(
    0 &"si" quad x_2 < 2x_1,
    "no definido" &"si" quad x_2 = 2x_1,
    +oo &"si" quad x_2 > 2x_1
  )
$

Cuando $x_2<2x_1$ sobran patatas: añadir más patatas no aumenta el bienestar,
y no estamos dispuestos a ceder cerveza a cambio, por lo que la RMS es cero.
Cuando $x_2>2x_1$ sobra cerveza: lo que limita el bienestar son las patatas,
y el brazo de indiferencia es vertical. En la proporción exacta no sobra
ninguno de los dos bienes y la RMS no está definida.

== Función de utilidad
#enunciado[
(3.1) Construya una función de utilidad que represente estas preferencias.
(3.2) Compruebe la indiferencia de $(1,2)$, $(5,2)$ y $(1,5)$.
(3.3) ¿Es única? Si no, indique otra.
]

=== Función que representa las preferencias
Podemos usar la función:
$
 u(x_1,x_2)=min(2x_1,x_2).
$
El bienestar queda limitado por el bien que falta para mantener la proporción
una bolsa por cada dos cervezas. Tener más del otro bien no lo mejora.

=== Comprobación de indiferencia
Simplemente sustituimos:
$
 u(1,2)&=min(2,2)=2, \
 u(5,2)&=min(10,2)=2, \
 u(1,5)&=min(2,5)=2.
$
Por tanto, las tres cestas proporcionan el mismo bienestar.

=== Otra función de utilidad
No es única. Por ejemplo, podemos usar:
$
 w(x_1,x_2)=min(x_1,x_2/2)=u(x_1,x_2)/2.
$
Sólo cambia la escala de los valores, pero se mantiene la misma ordenación
de las cestas. Cualquier transformación estrictamente creciente de $u$
representa también estas preferencias.

= Elección óptima

== Decisión y regla de decisión racional
#enunciado[
La renta es $M=12$.
(4.1) Con precios $(p_1,p_2)=(1,1)$, ¿qué cesta elegiría? Razone intuitivamente.
(4.2) Suponga que primero encuentra el anaquel de cervezas: ¿cuántas latas elegiría? Explique mediante análisis marginal si debe sustituir sucesivamente latas por patatas.
(4.3) Repita con precios $(2,1)$.
(4.4) Repita con precios $(4,1)$. ¿Puede la teoría económica explicar su elección?
]

// 4.1: una combinación (1,2) cuesta 3; se compran cuatro: (4,8).
// 4.2: comenzar en (0,12), u=0. No se compra todavía: se ajusta el carro.
// Sobre el presupuesto x2=12-x1, u=min(2*x1,12-x1).
// Hasta x1=4 limita 2*x1 y u aumenta; después limita x2 y u cae.
// Secuencia entera ilustrativa: (0,12),(1,11),(2,10),(3,9),(4,8),
// con u=0,2,4,6,8; el siguiente (5,7) reduce u a 7.
// En la zona con exceso de cerveza, RMS extendida > p1/p2; interesa
// sustituir cerveza por patatas. Tras cruzar el codo, RMS=0<p1/p2.
// No imponer RMS=p1/p2 en el óptimo, pues allí la RMS no existe.
// 4.3: x2=12-2*x1, u=min(2*x1,12-2*x1). Igualar ramas da
// x1=3,x2=6. Secuencia (0,12),(1,10),(2,8),(3,6), utilidades 0,2,4,6;
// el paso (4,4) baja a 4. Cada bolsa cuesta renunciar a dos latas.
// 4.4: x2=12-4*x1, u=min(2*x1,12-4*x1); máximo (2,4), u=4.
// Secuencia (0,12),(1,8),(2,4),(3,0), utilidades 0,2,4,0.
// Justificación global: t combinaciones exigen al menos (t,2*t),
// coste mínimo (p1+2*p2)*t; por tanto t<=12/(p1+2*p2), cota alcanzada
// por las cestas anteriores. Esto prueba optimalidad sin derivar el mínimo.
// Si se interpretan unidades indivisibles, en estos tres casos los codos
// son enteros y siguen siendo óptimos; las fórmulas generales del 6
// presuponen divisibilidad y no deben extrapolarse sin más al modelo entero.

=== Precios $(1,1)$
Una bolsa con dos cervezas cuesta $1+2=3€$. Con $12€$ podemos comprar cuatro
combinaciones, por lo que elegiríamos la cesta $(4,8)$.

Si encontramos primero las cervezas, podemos meter $12$ latas en el carro.
Pero la cesta $(0,12)$ tiene utilidad cero porque faltan las patatas.
Como los precios son iguales, podemos cambiar una lata por una bolsa:

#align(center, table(columns: 3,
 table.header([Bolsas], [Latas], [Utilidad]),
 [0], [12], [0], [1], [11], [2], [2], [10], [4],
 [3], [9], [6], [4], [8], [8], [5], [7], [7],
))

Los primeros cambios aumentan el bienestar, porque sustituimos cerveza que
sobra por patatas que faltan. Al llegar a $(4,8)$ se cumple la proporción
que queremos. Un cambio más reduciría el bienestar, así que nos detenemos ahí.
Esta es la aplicación de la regla de decisión racional: hacemos el cambio
mientras su beneficio supera su coste en bienestar.

=== Precios $(2,1)$
Ahora una combinación cuesta $2+2=4€$, por lo que elegimos la cesta
$(3,6)$. Partiendo de $(0,12)$, cada bolsa cuesta renunciar a dos latas:
$
 (0,12) -> (1,10) -> (2,8) -> (3,6) -> (4,4).
$
Las utilidades son $0,2,4,6,4$, respectivamente. Hasta $(3,6)$ los cambios
mejoran el bienestar; el siguiente lo reduce. Por tanto, elegimos $(3,6)$.

=== Precios $(4,1)$
Una combinación cuesta $4+2=6€$, por lo que elegimos $(2,4)$.
Desde la cesta de sólo cervezas, la secuencia sería:
$
 (0,12) -> (1,8) -> (2,4) -> (3,0),
$
con utilidades $0,2,4,0$. De nuevo, nos detenemos donde no sobra ninguno
de los dos bienes. La teoría explica esta decisión: con menos patatas
faltaría el bien 1 y con más patatas tendríamos que renunciar a cerveza
que sí necesitamos. En el modelo continuo, sobre el presupuesto
$x_2=12-p_1x_1$ la utilidad aumenta hasta $2x_1=x_2$ y después disminuye.



= Curvas de demanda

== Demanda de cerveza y cambios del presupuesto
#enunciado[
Con los precios y las decisiones óptimas del apartado 4, dibuje la curva de demanda de latas de cerveza.
]

// Advertencia central: p2=1 no cambia; cambia p1. Los puntos (x2,p2)
// son (8,1),(6,1),(4,1) y pertenecen a TRES curvas de demanda distintas.
// No unirlos como si constituyeran una curva de demanda horizontal.
// Con M=12, D2(p2;p1)=24/(p1+2*p2). Para p1=1,2,4, respectivamente:
// 24/(1+2*p2), 24/(2+2*p2), 24/(4+2*p2).
// Eje horizontal x2, vertical p2. Inversas p2=12/x2-p1/2;
// con p2>0, dominios 0<x2<24/p1. Marcar los puntos a altura p2=1.
// Al subir el precio de las patatas la demanda de cerveza se desplaza
// hacia la izquierda: son complementarios. Derivada cruzada
// ∂d2/∂p1=-2*M/(p1+2*p2)^2<0. Coincide con Juan Tadeo.
// Puede añadirse como gráfico auxiliar x2 frente a p1, x2=24/(p1+2),
// pero etiquetarlo respuesta al precio del otro bien, no demanda propia.
// Este apartado anticipa las fórmulas que se demostrarán en 6.a.

En los tres casos el precio de la cerveza es el mismo, $p_2=1$, pero cambia
el precio de las patatas. Por tanto, los puntos $(8,1)$, $(6,1)$ y $(4,1)$
no pertenecen a una única curva de demanda de cerveza.

Como obtendremos en el apartado siguiente, con $M=12$ la demanda es
$x_2=24/(p_1+2p_2)$. Al aumentar $p_1$, la curva se desplaza a la izquierda:
al ser bienes complementarios, si compramos menos patatas también queremos
menos cerveza.

#let precios = range(1, 121).map(i => i / 20)
#let demanda-cerveza() = lq.diagram(
  width: 90%, height: 8cm, xlim: (0,24), ylim: (0,6),
  xlabel: [Latas de cerveza ($x_2$)], ylabel: [Precio de cerveza ($p_2$, €)],
  legend: (position: top + right),
  lq.plot(precios.map(p => 24/(1+2*p)), precios, mark: none, color: blue, label: [$p_1=1$]),
  lq.plot(precios.map(p => 24/(2+2*p)), precios, mark: none, color: red, label: [$p_1=2$]),
  lq.plot(precios.map(p => 24/(4+2*p)), precios, mark: none, color: green, label: [$p_1=4$]),
  lq.plot((0,24), (1,1), mark: none, color: gray, stroke: (dash: "dashed")),
  lq.plot((8,), (1,), stroke: none, mark: "o", color: blue),
  lq.plot((6,), (1,), stroke: none, mark: "o", color: red),
  lq.plot((4,), (1,), stroke: none, mark: "o", color: green),
)
#figure(demanda-cerveza(), caption: [Desplazamientos de la demanda de cerveza al cambiar el precio de las patatas.]) <fig:cerveza>



= Cálculo analítico de la función de demanda

== 6.a) Demandas marshallianas
#enunciado[
Para $u(x_1,x_2)=min{2x_1,x_2}$, calcule las funciones de demanda marshallianas con precios $(p_1,p_2)$ y renta $M$.
]

// Plantear max min(2*x1,x2), sujeto a p1*x1+p2*x2<=M, x>=0.
// Método sin derivadas: para utilidad z se necesita x1>=z/2, x2>=z.
// El coste mínimo de alcanzar z es (p1/2+p2)*z; así
// z<=2*M/(p1+2*p2). La cota se alcanza en el codo 2*x1=x2.
// Resolver junto con p1*x1+p2*x2=M:
// d1=M/(p1+2*p2), d2=2*M/(p1+2*p2).
// Con precios positivos no quedan sobrantes en el óptimo: para alcanzar
// la cota se agota exactamente el presupuesto en las cantidades mínimas.
// Así se demuestra unicidad, sin usar una tangencia inexistente.
// Con M=0 las fórmulas dan (0,0); precios cero requieren análisis aparte.

Suponiendo $p_1,p_2>0$ y $M>=0$, el problema se puede formular como:
$
 max_(x_1,x_2 in RR^+ union {0}) min(2x_1,x_2) \
 "s.t." quad p_1x_1+p_2x_2<=M.
$
La función no es diferenciable en los codos, por lo que no vamos a buscar
una tangencia. Para alcanzar una utilidad $z$ necesitamos al menos $z/2$
bolsas y $z$ cervezas. Su coste es $(p_1/2+p_2)z$, por lo que no podemos
alcanzar una utilidad superior a $2M/(p_1+2p_2)$.

Podemos alcanzar ese valor comprando en la proporción $x_2=2x_1$ y agotando
la renta. Por tanto, resolvemos el sistema:
$
 cases(2x_1=x_2, p_1x_1+p_2x_2=M)
 => (p_1+2p_2)x_1=M.
$
Las funciones de demanda marshallianas son:
$
 d_1(p_1,p_2,M)=M/(p_1+2p_2), quad
 d_2(p_1,p_2,M)=(2M)/(p_1+2p_2).
$ <eq:demandas5c>



== 6.b) Cestas óptimas
#enunciado[
Calcule las cestas para $M=12$ y: b1) $(1,1)$; b2) $(2,1)$; b3) $(4,1)$.
]

// Resultados: b1 (4,8), gasto 12, u=8;
// b2 (3,6), gasto 12, u=6; b3 (2,4), gasto 12, u=4.
// Comprobar en cada fila x2=2*x1 y p1*x1+p2*x2=12.
// Presentar tabla y enlazar con el razonamiento del apartado 4.

Los tres casos se resuelven por sustitución directa en la @eq:demandas5c:

+ $(d_1(1,1,12),d_2(1,1,12))=(4,8)$, gasto $4+8=12$, utilidad $8$.
+ $(d_1(2,1,12),d_2(2,1,12))=(3,6)$, gasto $2 dot 3+6=12$, utilidad $6$.
+ $(d_1(4,1,12),d_2(4,1,12))=(2,4)$, gasto $4 dot 2+4=12$, utilidad $4$.

Coinciden con las cestas que obtuvimos mediante el análisis marginal.



== 6.c) Curvas respecto al precio propio
#enunciado[
Represente las curvas de demanda de los bienes 1 y 2 respecto de sus precios, correspondientes a las cestas de b1)-b3). Cuide los desplazamientos.
]

// Bien 1: mantener p2=1,M=12: x1=12/(p1+2).
// Inversa p1=12/x1-2, 0<x1<6 para precios positivos.
// Marcar (x1,p1)=(4,1),(3,2),(2,4): misma curva.
// Bien 2: reutilizar las tres curvas y puntos del apartado 5.
// Distinguir movimiento sobre demanda propia y desplazamiento por p1.
// Para lilaq se pueden muestrear precios p>0 y pasar coordenadas
// (cantidad(p),p), sin unir puntos de curvas diferentes. Ventanas
// sugeridas: bien 1 x=[0,6],p=[0,6]; bien 2 x=[0,14],p=[0,6].
// Identificar cada curva de cerveza por p1=1,2,4 y mantener la misma
// escala entre ellas. El gráfico de Juan Tadeo confirma esta distinción.

Para las patatas, fijamos $M=12$ y $p_2=1$. La demanda queda
$x_1=12/(p_1+2)$, y los puntos $(4,1)$, $(3,2)$ y $(2,4)$ están sobre
la misma curva: cambia el precio del propio bien.

#figure(
 lq.diagram(width: 85%, height: 7cm, xlim: (0,6), ylim: (0,6),
  xlabel: [Bolsas de patatas ($x_1$)], ylabel: [Precio de patatas ($p_1$, €)],
  lq.plot(precios.map(p => 12/(p+2)), precios, mark: none, color: blue),
  lq.plot((4,3,2), (1,2,4), stroke: none, mark: "o", color: red),
  lq.place(4.2,1, align: left, [b1]),
  lq.place(3.2,2, align: left, [b2]),
  lq.place(2.2,4, align: left, [b3]),
 ), caption: [Demanda de patatas con renta 12 y precio de la cerveza 1.],
)

Para la cerveza, las curvas son $x_2=24/(1+2p_2)$, $x_2=24/(2+2p_2)$
y $x_2=24/(4+2p_2)$. Están representadas en la @fig:cerveza.
En este caso cambia el precio del otro bien, así que son desplazamientos
de la demanda, y no movimientos sobre una misma curva.



== 6.d) Utilidad indirecta
#enunciado[
Calcule la función indirecta de utilidad.
]

// v(p1,p2,M)=min(2*d1,d2)=2*M/(p1+2*p2).
// Valores de control: 8,6,4 para los tres precios de 6.b.
// Es homogénea de grado cero en precios y renta; crece con M y
//  decrece con cada precio para M>0. Si se usa la utilidad alternativa
// w=u/2 del apartado 3.3, su indirecta será M/(p1+2*p2): mismas cestas,
// distintas etiquetas. Mantener u=min(2*x1,x2) en este apartado.

Usamos la definición de la función indirecta de utilidad y sustituimos
lo obtenido en la @eq:demandas5c:
$
 v(p_1,p_2,M) &= u(d_1(p_1,p_2,M),d_2(p_1,p_2,M)) \
 &= min((2M)/(p_1+2p_2),(2M)/(p_1+2p_2)) \
 &= (2M)/(p_1+2p_2).
$
A modo de comprobación, para los tres casos anteriores obtenemos:
$
 v(1,1,12)=24/3=8, quad
 v(2,1,12)=24/4=6, quad
 v(4,1,12)=24/6=4.
$
Coinciden con las utilidades de las cestas elegidas.


