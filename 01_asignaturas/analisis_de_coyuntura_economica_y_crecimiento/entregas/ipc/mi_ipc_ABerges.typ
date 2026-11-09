#import "@local/master-uvigo-templates:0.1.0": essay, base-styles, font_sizes, uvigo-blue, uvigo-gray
#import "@preview/lilaq:0.6.0" as lq
#let d = json("datos_ipc.json")
#let seguimiento = json("seguimiento_ipc.json")
#let completo = seguimiento.complete
#let vivienda = d.groups.at(3)
#let alimentos = d.groups.at(0)
#let restauracion = d.groups.at(10)
#let num(x, digits: 2) = {
  let parts = str(calc.round(x, digits: digits)).split(".")
  let decimals = if parts.len() > 1 { parts.last() } else { "" }
  parts.first() + if digits > 0 { "," + decimals + "0" * calc.max(0, digits - decimals.len()) } else { "" }
}
#let portada(titulo, autor) = {
  set align(center + horizon)
  set page(header: none, footer: none)
  { set text(hyphenate: false); title(titulo) }
  v(1em)
  text(size: font_sizes.Large)[Septiembre–octubre de 2026]
  v(1em)
  text(size: font_sizes.large)[#autor]
  v(1em)
  [Universidade de Vigo \
  Máster Universitario en Economía \
  Análisis de Coyuntura Económica y Crecimiento]
  v(1em)
  [7 de noviembre de 2026]
}
#show: base-styles
#show: essay.with(
  essay-title: [Índice de Precios al Consumo personal],
  author: "Adrián Berges Enfedaque",
  title-page: portada,
  abstract: [
    Se construye un Índice de Precios al Consumo personal a partir de los
    gastos registrados entre el 8 de septiembre y el 6 de octubre de 2026. Los
    tickets de compra sirven para anotar importes, cantidades y productos en
    una hoja de Excel. La hoja calcula los precios unitarios de referencia, las
    ponderaciones por grupo y el coste de mantener la misma cesta durante tres
    semanas, del 12 de octubre al 1 de noviembre. El índice toma el valor 100 en
    la base.
    #if completo [
      Los índices obtenidos son #num(seguimiento.weeks.at(0).index,
      digits: 3), #num(seguimiento.weeks.at(1).index, digits: 3) y
      #num(seguimiento.weeks.at(2).index, digits: 3). La variación acumulada
      es del #num(seguimiento.weeks.last().index - 100, digits: 3)~%.
    ] else [
      El resultado agregado queda pendiente de completar los precios restantes.
    ]
    La estabilidad depende del predominio de precios constantes y del peso de
    la hipoteca, que representa el 73,98~% de la cesta. Las ponderaciones se
    comparan con las de España y Galicia de 2025 publicadas por el INE.
  ],
)
#set page(header: context {
  set text(size: font_sizes.footnotesize, fill: uvigo-gray)
  h(1fr); emph[Análisis de Coyuntura Económica y Crecimiento]
})
#set table(stroke: (x: none, y: 0.4pt + luma(180)), inset: 5pt)
#show table.header: strong
#show figure.where(kind: table): set text(size: font_sizes.footnotesize)
#show lq.selector(lq.diagram): set text(size: font_sizes.footnotesize)
#show lq.selector(lq.diagram): it => align(center, it)
#set figure(gap: 9pt)
#show figure.caption: set text(size: font_sizes.footnotesize)

= Introducción
El IPC personal permite estudiar cómo influye la composición del gasto en
la exposición a los cambios de precios. Un índice agregado resume una cesta
representativa de la población. Una cesta individual puede asignar un peso muy
distinto a los mismos grupos de consumo. El INE explica esta diferencia entre la
experiencia de precios de un hogar y la medida general de inflación @ine-faq.

En este trabajo se plantea cuánto variaría el coste de adquirir una cesta
fija definida por los registros de gasto de Adrián Berges Enfedaque. Se emplea
como referencia el período del 8 de septiembre al 6 de octubre de 2026. El
seguimiento comprende las semanas del 12 al 18 de octubre, del 19 al 25 de
octubre y del 26 de octubre al 1 de noviembre.

Los registros permiten establecer la cesta y sus ponderaciones. El gasto total
asciende a 1.751,93 euros y presenta una elevada concentración en vivienda. El
seguimiento combina precios recuperados de fuentes online y estimaciones sin
cambios.
#if completo [
  El índice de la última semana alcanza #num(seguimiento.weeks.last().index),
  frente a 100 en la base.
] else [
  Faltan por completar #seguimiento.missing_count partidas de la cesta para
  obtener el índice agregado.
]

La sección 2 presenta la construcción del indicador en Excel. La sección 3
analiza las ponderaciones y los resultados semanales. La sección 4 recoge las
conclusiones y posibles extensiones. Las tablas y los gráficos se sitúan en
el apéndice.

= Metodología: construcción del IPC personal
== Registro de compras y seguimiento en Excel
El registro inicial se elabora a partir de los tickets de compra. En la hoja
*Mis Gastos* se anotan la fecha, el importe, la cantidad y la descripción de
cada producto o servicio. Las compras se clasifican en los doce grupos de la
plantilla. Se agregan los registros del 8 de septiembre al 6 de octubre de 2026,
ambos inclusive. Este es el período base efectivo y no coincide exactamente con
el mes natural de septiembre.

Excel suma el gasto y las cantidades de cada partida y obtiene su precio
unitario de referencia. Cuando hay varias compras del mismo producto, divide
el importe total entre la cantidad total. Para el seguimiento se introducen
los precios unitarios en las columnas CP, CR y CT, manteniendo las unidades del
registro: kilogramos, envases, unidades o servicios.

// Las semanas sin registro contemporáneo se completan con precios históricos de
// MercaIndex y CestaHoy, un folleto fechado de Froiz y estimaciones que conservan
// el precio base. La procedencia y las fechas figuran en la hoja *Fuentes
// precios*. También se conserva el precio base de la bombilla, el spray y las
// ceras como estimación sin cambios. Estas referencias completan el seguimiento,
// pero no equivalen a tickets recogidos en cada semana.

Netflix, Spotify e hipoteca mantienen sus tarifas mensuales. La hoja aplica
esas tarifas a las cantidades de la cesta base en todas las observaciones. No
es necesario comprar de nuevo cada partida. Las columnas de gasto de seguimiento
representan el coste de repetir la cesta, no nuevos desembolsos semanales.

== Cálculo del índice y las variaciones
Para hacer el cálculo del índice se mantienen fijas las cantidades iniciales y
se estudia cuánto cuesta adquirirlas a los precios de cada semana.
Este enfoque permite aislar el cambio de precios de los cambios en las compras
@ine-faq. Excel calcula el peso de cada grupo como su proporción del gasto base,
revaloriza la cesta y obtiene el índice:
$
 I_t=100 times ("Coste de la cesta a precios de la semana " t)/("Coste de la cesta a precios de la base"). 
$
Todos los cálculos y gráficos de la hoja se actualizan a partir de los precios
introducidos. La tasa se obtiene como la variación porcentual del índice
respecto al anterior. La primera observación compara con toda la base; las otras
dos comparan semanas consecutivas.

== Alcance de la comparación
La comparación utiliza las ponderaciones oficiales de España y Galicia
empleadas durante 2025, descargadas de la tabla 50952 del INE
@ine-ponderaciones. Se expresan en porcentaje y mantienen los mismos doce
grupos de la plantilla. Esto permite actualizar la referencia de 2024 sin
cambiar la estructura de la hoja.

Estas ponderaciones de 2025 se distinguen del sistema denominado *IPC base
2025*, que entró en vigor en enero de 2026 con trece grupos @ine-base2025.
El cambio de clasificación no impide la comparación si se armonizan las
categorías. En este trabajo se utiliza la clasificación común de doce grupos,
por lo que no es necesario realizar esa adaptación.
#footnote[
  De éste hecho se dio cuenta GPT al pedir la búsqueda de datos actuales.
]

Se mantienen las dos cuotas hipotecarias y la clasificación de gastos de la
hoja original. Esta elección da mucho peso a la vivienda. Al incluir pagos de
financiación, el indicador describe la cesta registrada y su comparación con el
IPC oficial tiene ese límite.

= Resultados
== Ponderación de los grupos en el gasto total
La @tab-ponderaciones muestra que la vivienda representa el 73,98~% del total,
frente al #num(vivienda.spain)~% de España y al #num(vivienda.galicia)~%
de Galicia en las ponderaciones de 2025. Las diferencias son de
#num(vivienda.weight - vivienda.spain) y #num(vivienda.weight -
vivienda.galicia) puntos porcentuales, respectivamente. La concentración
responde a dos pagos de 648 euros.

Los alimentos y bebidas no alcohólicas suponen el 11,00~%, por debajo
del #num(alimentos.spain)~% de España y del #num(alimentos.galicia)~%
de Galicia. Restaurantes y hoteles representan el 9,09~%, frente al
#num(restauracion.spain)~% y el #num(restauracion.galicia)~%.
// Estas diferencias dependen del denominador: al incluir la hipoteca, disminuye la
// participación relativa de los restantes grupos aunque sus importes no cambien.

Como ejercicio comparativo, al retirar únicamente las dos cuotas
hipotecarias el total se reduce a 455,93 euros. Los alimentos pasan a
representar el 42,25~%, la restauración el 34,93~% y el ocio el 10,96~%. Este
cálculo ilustra el efecto de delimitar la cesta.
// No constituye por sí solo una estimación completa del consumo comparable, ya que
// podrían faltar otros gastos del hogar o requerirse nuevas reclasificaciones.

Los grupos sin gasto registrado tienen ponderación cero, aunque podrían ser
importantes en el presupuesto anual. La base abarca solo 29 días y recoge dos
pagos de algunos servicios mensuales, por lo que las ponderaciones dependen del
calendario de cobro.

== IPC semanal
La @tab-semanal y el @fig-ipc presentan el coste de la cesta y su índice. La
base cuesta 1.751,93 euros y su índice es 100 por definición.
#if completo [
  Los índices de las tres semanas son #num(seguimiento.weeks.at(0).index,
  digits: 3), #num(seguimiento.weeks.at(1).index, digits: 3) y
  #num(seguimiento.weeks.at(2).index, digits: 3). La última cesta cuesta
  #num(seguimiento.weeks.last().cost) euros. La diferencia respecto a la base es
  de #num(seguimiento.weeks.last().cost - seguimiento.base) euros.
] else [
  Los precios de supermercado están completos mediante fuentes
  recuperadas y estimaciones. El cálculo agregado queda pendiente de
  #seguimiento.missing_count partidas fuera de supermercados. Los valores
  pendientes no se interpretan como ceros.
]

La estabilidad responde en parte a que la gran mayoría precios de supermercado
conservan el precio base. Además, la hipoteca mantiene su importe y concentra
casi tres cuartas partes de la ponderación.
 
== Tasa de inflación semanal
La @tab-semanal y el @fig-inflacion presentan las variaciones del índice.
#if completo [
  La primera semana registra una variación del
  #num(seguimiento.weeks.at(0).rate, digits: 3)~% respecto a la base. Las tasas
  entre semanas consecutivas son del #num(seguimiento.weeks.at(1).rate, digits:
  3)~% y del #num(seguimiento.weeks.at(2).rate, digits: 3)~%.
] else [
  Las tasas permanecen pendientes hasta completar los precios restantes. Su
  cálculo requiere índices válidos para los dos períodos que se comparan.
]

La tasa inicial compara el 12–18 de octubre con toda la base. Las tasas
posteriores comparan semanas consecutivas.
// No se confrontan estas variaciones con una tasa mensual o interanual del IPC
// oficial, ya que no medirían el mismo intervalo temporal.

= Conclusiones y extensiones
El trabajo ha permitido construir un IPC personal a partir de una cesta de
1.751,93 euros y estudiar su evolución manteniendo constantes las cantidades
adquiridas. El registro y los cálculos en Excel permiten relacionar el resultado
con los precios de cada partida y con su importancia en el presupuesto.
#if completo [
  Durante las tres semanas analizadas, el coste de la cesta apenas cambia:
  el índice final se sitúa en #num(seguimiento.weeks.last().index, digits: 3),
  con una variación del #num(seguimiento.weeks.last().index - 100, digits: 3)~%
  respecto a la base. Bajo los precios utilizados, recomprar la cesta al final
  del período cuesta prácticamente lo mismo que al inicio.
] else [
  El índice agregado queda pendiente de completar los precios restantes.
]

La comparación con España y Galicia muestra que la composición del gasto
personal difiere de las ponderaciones oficiales de 2025. La vivienda concentra
el 73,98~% por la inclusión de dos cuotas hipotecarias, cuyo importe permanece
constante y reduce el efecto relativo de las variaciones de otras partidas.
Así, la estabilidad del índice se entiende tanto por los precios introducidos
como por el peso de cada grupo en esta cesta concreta.

Como extensión, sería útil ampliar el registro a varios meses para recoger
compras menos frecuentes y reducir la influencia del calendario de pagos.
Mantener también el seguimiento de precios permitiría comprobar si la
estabilidad observada persiste o si aparecen diferencias entre grupos. De este
modo, se podría valorar hasta qué punto los resultados dependen del período
elegido y obtener una imagen más representativa del gasto habitual.

#pagebreak(weak: true)
#bibliography("referencias.bib", title: "Bibliografía", style: "apa")

#pagebreak()
#heading(numbering: none)[Apéndice: tablas y gráficos]
#let labels = ("Alimentos y bebidas no alcohólicas", "Bebidas alcohólicas y tabaco", "Vestido y calzado", "Vivienda y suministros", "Muebles y mantenimiento del hogar", "Sanidad", "Transporte", "Comunicaciones", "Ocio y cultura", "Enseñanza", "Restaurantes y hoteles", "Otros bienes y servicios")
#figure(
  table(
    columns: (2.5fr, 1fr, 0.85fr, 0.85fr, 0.85fr),
    align: (left, right, right, right, right),
    table.header([Grupo], [Gasto (€)], [Personal (%)], [España (%)], [Galicia (%)]),
    ..d.groups.enumerate().map(((i, g)) => (
      labels.at(i), num(g.amount), num(g.weight), num(g.spain), num(g.galicia),
    )).flatten(),
    strong[Total], strong(num(d.total)), strong[100,00], strong[100,00], strong[100,00],
  ),
  caption: [
    Ponderaciones personales de la base 08/09–06/10/2026 y ponderaciones
    oficiales de España y Galicia utilizadas en 2025 (IPC base 2021, doce
    grupos). Fuente: registros propios e INE, tabla 50952, período 2025. Los
    valores oficiales, publicados en tanto por mil, se dividen entre diez para
    expresarlos en porcentaje. Suman 100,0001~% en España y 100~% en Galicia
    por redondeo.
  ],
) <tab-ponderaciones>

#v(1em)
#figure(
  table(
    columns: (2.1fr, 1fr, 0.75fr, 1.15fr),
    align: (left, right, right, right),
    table.header([Período], [Coste cesta (€)], [IPC], [Variación (%)]),
    [08/09–06/10/2026 (base)], [1.751,93], [100,00], [—],
    ..seguimiento.weeks.map(w => (
      w.label,
      if w.cost == none { [Pendiente] } else { num(w.cost) },
      if w.index == none { [—] } else { num(w.index, digits: 3) },
      if w.rate == none { [—] } else { num(w.rate, digits: 3) },
    )).flatten(),
  ),
  caption: [
    Coste de la cesta fija, IPC y variaciones calculados en Excel. La primera
    variación compara con la base; las dos siguientes son semanales. Se muestran
    tres decimales para distinguir las variaciones pequeñas de un valor cero.
    Fuente: elaboración propia.
  ],
) <tab-semanal>

#pagebreak()
#let puntos = ((x: 0, valor: 100),) + seguimiento.weeks.enumerate().filter(((i, w)) => w.index != none).map(((i, w)) => (x: i+1, valor: w.index))
#let tasas = seguimiento.weeks.enumerate().filter(((i, w)) => w.rate != none).map(((i, w)) => (x: i+1, valor: w.rate))
#figure(
  [
    #lq.diagram(
      width: 100%, height: 5cm,
      xlim: (-0.2, 3.2), ylim: (calc.min(..puntos.map(p => p.valor))-0.1, calc.max(..puntos.map(p => p.valor))+0.1),
      xaxis: (ticks: (0, 1, 2, 3), subticks: none),
      xlabel: [0: base · 1, 2 y 3: semanas de seguimiento],
      ylabel: [Base = 100],
      lq.plot(puntos.map(p => p.x), puntos.map(p => p.valor), mark: "o", color: uvigo-blue),
    )
    #if not completo { align(center, text(size: font_sizes.footnotesize)[Pendiente de completar precios fuera de supermercados.]) }
  ],
  kind: image, supplement: [Gráfico],
  caption: [
    IPC personal. Base 08/09–06/10/2026 = 100. Se representan únicamente los
    índices calculables. Fuente: elaboración propia.
  ],
) <fig-ipc>

#v(1em)
#figure(
  [
    #lq.diagram(
      width: 100%, height: 5cm,
      xlim: (0.8, 3.2), ylim: if tasas.len() > 0 { (calc.min(0, ..tasas.map(p => p.valor))-0.005, calc.max(0, ..tasas.map(p => p.valor))+0.005) } else { (-1, 1) },
      xaxis: (ticks: (1, 2, 3), subticks: none),
      xlabel: [Semana de seguimiento], ylabel: [Variación (%)],
      ..if tasas.len() > 0 { (lq.plot(tasas.map(p => p.x), tasas.map(p => p.valor), mark: "o", color: uvigo-blue),) } else { () },
    )
    #if tasas.len() == 0 { align(center, text(size: font_sizes.footnotesize)[Sin tasas calculables hasta completar la cesta.]) }
  ],
  kind: image, supplement: [Gráfico],
  caption: [
    Variación del IPC personal. La primera tasa compara con la base y las dos
    siguientes con la semana anterior. Fuente: elaboración propia.
  ],
) <fig-inflacion>
