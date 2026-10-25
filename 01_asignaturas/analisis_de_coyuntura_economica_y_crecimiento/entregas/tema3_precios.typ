#import "@local/master-uvigo-templates:0.1.0": font_sizes, homework_econ
#import "@preview/lilaq:0.6.0" as lq

#show: homework_econ.with(
  course: [Análisis de Coyuntura Económica y Crecimiento],
  title: [Ejercicio 3 · Tema 3. Agregados de precios],
  date: datetime(year: 2026, month: 10, day: 25),
  heading-numbering: (..nums) => {
    let n = nums.pos()
    if n.len() == 1 { numbering("1.", n.first()) }
    else { numbering("1.a)", ..n) }
  },
)
#set text(lang: "es", size: font_sizes.normalsize)
#show heading.where(level: 1): set text(size: font_sizes.large)
#show heading.where(level: 2): set text(size: font_sizes.large)
#set table(stroke: (x: none, y: .5pt), align: center, inset: 4pt)
#show table.header: strong
#show lq.selector(lq.diagram): set text(size: font_sizes.footnotesize)
#show lq.selector(lq.diagram): it => align(center, it)

// Fuente: lista-M-tema3-Prezos.pdf. Numeración automática de ejercicios y apartados.
#let enunciado(body) = {
  set text(style: "italic")
  block(fill: luma(200), inset: 8pt, radius: 4pt, stroke: 1pt)[#body]
}
#let ro2(x) = calc.round(x, digits: 2)
// #let enunciado(body) = block[
//   *Enunciado* #h(1em) #emph(body)
// ]

= PIB nominal, PIB real y deflactor
#enunciado[
  Con la siguiente información sobre los precios y cantidades, responda a las
  siguientes preguntas indicando claramente los cálculos y justificando los pasos
  que da para presentar su solución.

  #align(center, block(breakable: false, table(
    columns: 5,
    table.header([Año], [Precio leche], [Cantidad leche], [Precio miel], [Cantidad miel]),
    [2021], [1 €], [200 litros], [2 €], [100 litros],
    [2022], [1 €], [400 litros], [2 €], [200 litros],
    [2023], [2 €], [400 litros], [4 €], [200 litros],
  )))
]

== PIB nominal, PIB real y deflactor con base 2021
#enunciado[Calcule el PIB nominal, el PIB real y el deflactor del PIB de cada año empleando el año 2021 como año base.]

El PIB nominal valora las cantidades de cada año a sus precios corrientes,
mientras que el real mantiene los precios de 2021. Por tanto:
$
  Y_t^N = sum_i p_(i,t) q_(i,t), quad
  Y_t^R = sum_i p_(i,2021) q_(i,t), quad
  D_t = Y_t^N/Y_t^R dot 100.
$
Sustituyendo los precios y cantidades de leche y miel:
$
  Y_2021^N &= 1 dot 200 + 2 dot 100 = 400, \
  Y_2022^N &= 1 dot 400 + 2 dot 200 = 800, \
  Y_2023^N &= 2 dot 400 + 4 dot 200 = 1600.
$
En términos reales, el cálculo es el mismo para 2021 y 2022. En 2023,
$Y_2023^R = 1 dot 400 + 2 dot 200 = 800$. Así, tenemos:

#align(center, block(breakable: false, table(
  columns: 4,
  table.header([Año], [PIB nominal (€)], [PIB real (€ de 2021)], [Deflactor]),
  [2021], [400], [400], [$400/400 dot 100 = 100$],
  [2022], [800], [800], [$800/800 dot 100 = 100$],
  [2023], [1600], [800], [$1600/800 dot 100 = 200$],
)))

== Variaciones porcentuales
#enunciado[Calcule la variación porcentual del PIB nominal, del PIB real y del deflactor del PIB en 2022 y 2023 respecto al año anterior.]

Para cada serie usamos $g_(X,t) = (X_t/X_(t-1)-1) dot 100$:

#align(center, block(breakable: false, table(
  columns: 4,
  table.header([Año], [Variación PIB nominal], [Variación PIB real], [Variación deflactor]),
  [2022], [$ (800/400-1)100 = 100% $], [$ (800/400-1)100 = 100% $], [$0%$],
  [2023], [$ (1600/800-1)100 = 100% $], [$0%$], [$ (200/100-1)100 = 100% $],
)))

== Gráficos temporales
#enunciado[Dibuje los gráficos temporales para el período 2021-2023 de las series obtenidas en los dos apartados anteriores. Indique un gráfico para cada serie.]

No calculamos tasas para 2021 porque no tenemos datos de 2020.

#let grafico(titulo, years, valores, unidad, limites) = block(breakable: false)[
  #align(center, text(size: font_sizes.footnotesize, weight: "bold", titulo))
  #lq.diagram(
    width: 80%, height: 2.7cm,
    xlabel: none, ylabel: unidad,
    xlim: (2021, 2023), xaxis: (ticks: (2021, 2022, 2023), subticks: none),
    ylim: limites,
    lq.plot(years, valores, mark: "o", color: rgb("#2563eb"), stroke: 1.5pt),
  )
]

#grid(
  columns: (1fr, 1fr), column-gutter: 12pt, row-gutter: 8pt,
  grafico([PIB nominal], (2021, 2022, 2023), (400, 800, 1600), [€], (0, 1800)),
  grafico([Variación del PIB nominal], (2022, 2023), (100, 100), [%], (0, 110)),
  grafico([PIB real], (2021, 2022, 2023), (400, 800, 800), [€ de 2021], (0, 900)),
  grafico([Variación del PIB real], (2022, 2023), (100, 0), [%], (0, 110)),
  grafico([Deflactor del PIB], (2021, 2022, 2023), (100, 100, 200), [2021 = 100], (0, 220)),
  grafico([Variación del deflactor], (2022, 2023), (0, 100), [%], (0, 110)),
)

== Relación entre las tasas de crecimiento
#enunciado[Explique la relación que existe entre las tres tasas de crecimiento obtenidas en el apartado de variaciones porcentuales.]

Dado que $Y_t^N = Y_t^R D_t/100$, las tasas, expresadas en tanto por uno,
cumplen:
$
  1+g_N = (1+g_R)(1+pi)
  quad => quad g_N = g_R + pi + g_R pi.
$
En 2022, el aumento del PIB nominal se debe al aumento de las cantidades;
en 2023, al de los precios. En ambos años crece un $100%$. En general,
$g_N approx g_R + pi$ sólo es una aproximación; aquí la suma es exacta porque
uno de los dos términos es cero en cada año.



= Crecimiento e inflación
#enunciado[
  Nuestro ayudante de investigación ha recogido los siguientes datos del PIB
  nominal y del PIB real (con año base 2015) de un país, junto con algún dato
  de la tasa de inflación. Si lo precisa, rellene la tabla.

  #align(center, block(breakable: false, table(
    columns: 5,
    table.header([], [2016], [2017], [2018], [2019]),
    [PIB nominal], [2200], [2010], [2163], [2210,25],
    [PIB real (2015)], [2000], [2010], [2100], [2105],
    [DPIB], [], [], [], [],
    [Inflación (%)], [], [], [3,0], [1,9],
    [Crecimiento real (%)], [], [], [], [],
  )))
]

Calculamos el deflactor como antes y la inflación como su variación porcentual.
El crecimiento de la economía se obtiene del PIB real:

#align(center, block(breakable: false, table(
  columns: 5,
  table.header([], [2016], [2017], [2018], [2019]),
  [PIB nominal], [2200], [2010], [2163], [2210,25],
  [PIB real (2015)], [2000], [2010], [2100], [2105],
  [Deflactor], [110], [100], [103], [105],
  [Inflación (%)], [10], [−9,09], [3], [1,94],
  [Crecimiento real (%)], [—], [0,50], [4,48], [0,24],
)))
La inflación de 2019 es $(105/103-1)100 approx #ro2((105/103-1)*100)%$, que
coincide con el $1.9%$ del enunciado al redondear a un decimal.

== Crecimiento de la economía
#enunciado[
  Indique la respuesta correcta:
  #enum(numbering: "a)",
    [La economía creció entre 2017 y 2019.],
    [En 2017 la economía sufrió una contracción económica en el país.],
    [En 2019 disminuyeron los precios porque la tasa de inflación disminuyó.],
    [No existen datos para calcular ni la tasa de inflación ni la tasa de crecimiento de la economía para el año 2016.],
  )
]

La respuesta correcta es la *a)*: el PIB real pasa de 2010 a 2105
entre 2017 y 2019. En 2017 crece un $0.5%$, y en 2019 los precios siguen
subiendo aunque la inflación sea menor. Además, sí podemos calcular la
inflación de 2016: como $D_2015=100$, es $(110/100-1)100=10%$.
Lo que no conocemos es el crecimiento real de 2016.

== Evolución de los precios
#enunciado[
  Indique la respuesta correcta:
  #enum(numbering: "a)",
    [La tasa de inflación en el año 2016 fue del 10 %.],
    [En esta economía los precios cayeron algún año.],
    [El índice de precios en el año 2017 fue el mismo que en el año base.],
    [Todas las respuestas son correctas.],
  )
]

La respuesta es la *d)*. La inflación de 2016 fue del $10%$,
los precios cayeron en 2017 y el deflactor de ese año es 100, igual que en 2015.


= IPC e inflación
<ej:ipc>
#enunciado[
  Suponga que los habitantes de un país vegetariano gastan toda su renta en
  coliflor, brócoli y zanahorias.

  #align(center, block(breakable: false, table(
    columns: 7,
    table.header([Año], [Precio coliflor], [Cantidad coliflor], [Precio brócoli], [Cantidad brócoli], [Precio zanahorias], [Cantidad zanahorias]),
    [2019], [200], [100], [75], [50], [50], [500],
    [2020], [225], [75], [125], [80], [100], [500],
  )))
]

== IPC con base 2019
#enunciado[Si escogemos como año base 2019, ¿cuál es el IPC de los dos años? ¿Y la tasa de inflación?]

Con base 2019, mantenemos fija la cesta de ese año:
$
  C_2019 &= 200 dot 100 + 75 dot 50 + 50 dot 500 = 48750, \
  C_2020 &= 225 dot 100 + 125 dot 50 + 100 dot 500 = 78750.
$
Por tanto:
$
  "IPC"_2019 = 100, quad "IPC"_2020 = 78750/48750 dot 100 approx #ro2(78750/48750*100), \
  pi_2020 = (78750/48750-1)100 approx #ro2((78750/48750-1)*100)%.
$

== IPC con base 2020
#enunciado[Si escogemos como año base 2020, ¿cuál es el IPC de los dos años? ¿Y la tasa de inflación?]

Ahora usamos las cantidades de 2020 para valorar la cesta en los dos años:
$
  C_2019 &= 200 dot 75 + 75 dot 80 + 50 dot 500 = 46000, \
  C_2020 &= 225 dot 75 + 125 dot 80 + 100 dot 500 = 76875.
$
Luego:
$
  "IPC"_2019 = 46000/76875 dot 100 approx #ro2(46000/76875*100), quad "IPC"_2020 = 100, \
  pi_2020 = (76875/46000-1)100 approx #ro2((76875/46000-1)*100)%.
$
En ambos apartados calculamos la inflación de 2020 respecto a 2019;
para la de 2019 necesitaríamos datos de 2018.

== Comparación de resultados
#enunciado[Compare las respuestas de los dos apartados anteriores.]

La inflación es mayor con la cesta de 2020: $67.12%-61.54%=#ro2(67.12-61.54)$
puntos porcentuales. Cambian las cantidades usadas como ponderación, por lo
que no estamos simplemente reescalando el mismo índice. Con una cesta fija,
cambiar únicamente la referencia a 100 no alteraría la inflación.


= Indiciación en Valdeorras
#enunciado[
  Estamos realizando un estudio sobre las condiciones de vida en la comarca de
  Valdeorras a principios del siglo XX, comparándolas con las de principios del
  siglo XXI. En nuestra investigación hemos encontrado la siguiente información:

  - Un artículo académico de la Universidade de Vigo especifica que la familia
    representativa de Valdeorras consumía principalmente carne, leche y vino Mencía.
  - A partir de anuncios en periódicos lucenses de la época se han encontrado
    los precios de estos tres productos en 1910.
  - Con un proyecto de investigación hemos realizado un estudio del consumo
    de estos productos y sus precios en Valdeorras en 2019.
  - En 1910, un operario minero de la comarca recibía un salario de 3 euros al mes.

  Los precios y cantidades consumidas por una familia representativa son:
  #align(center, block(breakable: false, table(
    columns: 5,
    table.header([Producto], [Precio 1910 (€)], [Cantidad 1910], [Precio 2019 (€)], [Cantidad 2019]),
    [Carne], [0,04], [20], [20], [30],
    [Leche], [0,01], [15], [2], [15],
    [Vino], [0,01], [5], [14], [5],
  )))
]

== Construcción del IPC
#enunciado[
  Si elegimos como año base 1910, indique: (i) el gasto de la familia
  representativa en 1910; (ii) lo que gastaría en 2019 si hubiese adquirido la
  cesta de 1910; (iii) el IPC de 2019 con base 1910.
  #enum(numbering: "a)",
    [(i) 1; (ii) 700; (iii) 70.000 %.],
    [(i) 40; (ii) 50; (iii) 125 %.],
    [(i) 0,06; (ii) 36; (iii) 60.000 %.],
    [(i) 1; (ii) 500; (iii) 50.000 %.],
  )
]

El gasto de la familia representativa en 1910 es:
$
  C_1910 = 0.04 dot 20 + 0.01 dot 15 + 0.01 dot 5 = 1€.
$
La misma cesta, valorada a precios de 2019, cuesta:
$
  C_2019 = 20 dot 20 + 2 dot 15 + 14 dot 5 = 500€.
$
Por tanto, $"IPC"_2019 = 500/1 dot 100 = 50000$. La respuesta es la *d)*.
El enunciado lo escribe como $50000%$, aunque el índice se expresa en puntos
con base 100; el aumento de precios es del $49900%$.

== Salario real
#enunciado[
  ¿Cuál sería el sueldo mensual de un operario minero en 2019 para que poseyera
  el mismo poder adquisitivo que en 1910? Justifique la respuesta.
  a) 2100 euros; b) 3,75 euros; c) 1800 euros; d) 1500 euros.
]

Para mantener el poder adquisitivo, actualizamos el salario con el IPC:
$
  w_2019 = w_1910 "IPC"_2019/"IPC"_1910
  = 3 dot 50000/100 = 1500€.
$
La respuesta es la *d)*. Con ese sueldo se pueden comprar las mismas tres
cestas que con los 3 € de 1910.


= Cambio de base y enlace de series
#enunciado[
  Estamos estudiando la evolución de un índice de precios (IP) a lo largo del
  tiempo. Hemos encontrado dos series truncadas: una tiene año base 2019 y
  otra tiene año base 2022.

  #align(center, block(breakable: false, table(
    columns: 3,
    table.header([Año], [IP (base 2019)], [IP (base 2022)]),
    [2018], [95], [],
    [2019], [100], [],
    [2020], [102,5], [],
    [2021], [105], [90],
    [2022], [], [100],
    [2023], [], [115],
  )))
  Queremos tener una única serie de precios desde 2018 a 2023 aprovechando toda
  la información disponible.
]

== Serie con base 2019
#enunciado[Construya una serie de IP con año base 2019.]

El año común es 2021. En ese año, el índice con base 2019 vale 105 y
el de base 2022 vale 90. Para prolongar la primera serie multiplicamos los
datos de la segunda por $105/90$:
$
  "IP"_2022^((2019)) = 100 dot 105/90 approx #ro2(100*105/90), quad
  "IP"_2023^((2019)) = 115 dot 105/90 approx #ro2(115*105/90).
$

== Serie con base 2022
#enunciado[Construya una serie de IP con año base 2022.]

Para expresar toda la serie con base 2022 hacemos la operación inversa:
multiplicamos los datos de base 2019 por $90/105$. Por ejemplo,
$"IP"_2018^((2022)) = 95 dot 90/105 approx #ro2(95*90/105)$.

== Tasas de inflación
#enunciado[
  Calcule la tasa de inflación utilizando:
  #enum(numbering: "a)",
    [La serie de 2018 a 2023 del IP con año base 2019.],
    [La serie de 2018 a 2023 del IP con año base 2022.],
  )
]

Usando $pi_t = ("IP"_t/"IP"_(t-1)-1)100$, obtenemos:

#align(center, block(breakable: false, table(
  columns: 5,
  table.header([Año], [IP (2019 = 100)], [IP (2022 = 100)], [Inflación (%)\ Base 2019], [Inflación (%)\ Base 2022]),
  [2018], [95,00], [81,43], [—], [—],
  [2019], [100,00], [85,71], [5,26], [5,26],
  [2020], [102,50], [87,86], [2,50], [2,50],
  [2021], [105,00], [90,00], [2,44], [2,44],
  [2022], [116,67], [100,00], [11,11], [11,11],
  [2023], [134,17], [115,00], [15,00], [15,00],
)))

#block(breakable: false)[
Las tasas se han calculado con los índices sin redondear. Por ejemplo:
$
  pi_2019 &= (100/95-1)100 approx #ro2((100/95-1)*100)%, \
  pi_2022 &= (100/90-1)100 approx #ro2((100/90-1)*100)%, \
  pi_2023 &= (115/100-1)100 = 15%.
$
]
No podemos calcular la inflación de 2018 porque falta el índice de 2017.

== Comparación de la inflación
#enunciado[Indique la diferencia existente entre la inflación obtenida con las dos bases en el apartado anterior.]

No hay diferencia entre las tasas de inflación. Las dos series sólo
difieren en un factor constante, que se cancela al dividir:
$
  ((k "IP"_t)/(k "IP"_(t-1))-1)100
  = ("IP"_t/"IP"_(t-1)-1)100.
$
A diferencia del ejercicio #ref(<ej:ipc>, form: "normal", supplement: none), aquí cambiamos la escala del índice conservando
la evolución de precios de las series originales.
