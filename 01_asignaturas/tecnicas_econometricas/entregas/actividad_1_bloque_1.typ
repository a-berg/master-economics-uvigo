#import "@local/master-uvigo-templates:0.1.0": homework_econ

#show: homework_econ.with(
  title: [Actividad 1 Bloque 1],
  course: "Técnicas Econométricas",
)

#set math.equation(numbering: none)
#let WAGE = math.upright("WAGE")
#let EDUC = math.upright("EDUC")
#let EXPER = math.upright("EXPER")
#set table(inset: 5pt, stroke: (x: none, y: 0.3pt + luma(25%)))
#let tab(body) = figure(
  block(width: 80%)[
    #set text(size: 9pt)
    #set par(first-line-indent: 0pt)
    #body
  ],
)

= Estimación del modelo

Los modelos se han estimado en Python usando Statsmodels.
Estimando por MCO con las $1000$ observaciones del supuesto $1.3$, obtenemos:

$
  hat(ln(WAGE)) & = -0.2646 + 0.1506 EDUC + 0.0671 EXPER \
                & quad - 0.0007 EXPER^2 - 0.0020 EDUC dot EXPER.
$

#tab(table(
  columns: (1.5fr, 1fr, 1fr, 1fr),
  align: (left, right, right, right),
  table.header([*Variable*], [*Coeficiente*], [*Error estándar*], [*Valor p*]),
  table.hline(stroke: 1.25pt),
  [Constante], [$-0.2646$], [$0.1808$], [$0.1436$],
  [$EDUC$], [$0.1506$], [$0.0127$], [$< 0.0001$],
  [$EXPER$], [$0.0671$], [$0.0095$], [$< 0.0001$],
  [$EXPER^2$], [$-0.0007$], [$0.0001$], [$< 0.0001$],
  [$EDUC dot EXPER$], [$-0.0020$], [$0.0006$], [$0.0003$],
))

Tenemos $R^2 = 0.3095$ y $R^2$ ajustado de $0.3067$. Todos los coeficientes,
salvo la constante, son significativos al $5%$. El término cuadrático negativo
indica que el efecto de la experiencia va disminuyendo. Asimismo, la interacción
negativa indica que el efecto de la educación disminuye con la experiencia.
Los errores estándar son los habituales de MCO, bajo homocedasticidad.

= Efecto marginal de la experiencia

Para obtener el efecto marginal tenemos que derivar respecto a la experiencia
y sustituir $EXPER = 15$ y $EDUC = 16$:

$
  (partial hat(ln(WAGE))) / (partial EXPER)
  = hat(beta)_2 + 2 hat(beta)_3 EXPER + hat(beta)_4 EDUC
  = hat(beta)_2 + 30 hat(beta)_3 + 16 hat(beta)_4 approx 0.0139.
$

Es decir, un año adicional de experiencia supone aproximadamente un $1.3870%$
más de salario, manteniendo la educación constante. El cálculo se hace con los
coeficientes sin redondear.

= Significación de la educación

Como la educación aparece también en la interacción, tenemos que contrastar
ambos coeficientes conjuntamente:

$
  H_0: beta_1 = beta_4 = 0,
  quad H_1: (beta_1, beta_4) != (0, 0).
$

Obtenemos $F(2, 995) = 171.2677$, con $p < 0.0001$. Por tanto, rechazamos
$H_0$ al $5%$: la educación sí contribuye a explicar los salarios.

#pagebreak()
= Comparación del ajuste

Estimando el modelo en niveles obtenemos:

$ hat(WAGE) = -9.8177 + 1.2101 EDUC + 0.3409 EXPER - 0.0051 EXPER^2. $

Su $R^2 = 0.2709$ y su $R^2$ ajustado es $0.2687$. No podemos comparar
directamente estos valores con los anteriores porque ahora la variable
dependiente es el salario, no su logaritmo. Para comparar las formas funcionales
usamos Box-Cox:

$
  y_i(lambda) = cases(
    (WAGE_i^lambda - 1)/lambda & "si" lambda != 0,
    ln(WAGE_i) & "si" lambda = 0,
  ).
$

Manteniendo los regresores del primer modelo, estimamos $lambda$ por máxima
verosimilitud, incluyendo el jacobiano de la transformación. Obtenemos
$hat(lambda) = -0.1340$, con intervalo del $95%$ de $[-0.2318; -0.0370]$.
Los contrastes de razón de verosimilitudes dan:

#tab(table(
  columns: (2.8fr, 1fr, 0.5fr, 1fr),
  align: (left, right, right, right),
  table.header([*Hipótesis*], [*LR*], [*gl*], [*Valor p*]),
  table.hline(stroke: 1.25pt),
  [Logarítmico: $lambda = 0$], [$7.3647$], [$1$], [$0.0067$],
  [Niveles con interacción: $lambda = 1$], [$574.8559$], [$1$], [$< 0.0001$],
  [Niveles del enunciado: $lambda = 1$, $beta_4 = 0$], [$577.5937$], [$2$], [$< 0.0001$],
))

La última restricción es necesaria porque el modelo en niveles del enunciado
no incluye la interacción. Al $5%$ se rechazan todas estas hipótesis frente al
modelo Box-Cox sin restringir, por lo que tampoco podemos decir que la
transformación logarítmica sea la óptima.

Para elegir entre los dos modelos pedidos, comparamos además sus AIC en la
escala original, ajustando por el jacobiano y contando la varianza residual
como parámetro:

$
  "AIC"_("log") = 5626.7440,
  quad "AIC"_("niveles") = 6194.9731.
$

Por tanto, entre los dos nos quedamos con el logarítmico, que tiene menor AIC,
aunque Box-Cox sugiere una transformación algo distinta.

#pagebreak()
#heading(numbering: none)[Anexo. Salidas de los modelos]

Se recogen los resultados de Statsmodels, con errores estándar no robustos.

#heading(level: 2, numbering: none)[Modelo logarítmico]
#tab(table(
  columns: (1.3fr, 1fr, 1fr, 1fr, 1fr),
  align: (left, right, right, right, right),
  table.header([*Variable*], [*Coef.*], [*EE*], [*t*], [*Valor p*]),
  table.hline(stroke: 1.25pt),
  [Constante], [$-0.2646$], [$0.1808$], [$-1.4638$], [$0.1436$],
  [$EDUC$], [$0.1506$], [$0.0127$], [$11.8370$], [$< 0.0001$],
  [$EXPER$], [$0.0671$], [$0.0095$], [$7.0344$], [$< 0.0001$],
  [$EXPER^2$], [$-0.0007$], [$0.0001$], [$-6.4431$], [$< 0.0001$],
  [$EDUC dot EXPER$], [$-0.0020$], [$0.0006$], [$-3.6410$], [$0.0003$],
))

#heading(level: 2, numbering: none)[Modelo en niveles]
#tab(table(
  columns: (1.3fr, 1fr, 1fr, 1fr, 1fr),
  align: (left, right, right, right, right),
  table.header([*Variable*], [*Coef.*], [*EE*], [*t*], [*Valor p*]),
  table.hline(stroke: 1.25pt),
  [Constante], [$-9.8177$], [$1.0550$], [$-9.3062$], [$< 0.0001$],
  [$EDUC$], [$1.2101$], [$0.0702$], [$17.2282$], [$< 0.0001$],
  [$EXPER$], [$0.3409$], [$0.0514$], [$6.6292$], [$< 0.0001$],
  [$EXPER^2$], [$-0.0051$], [$0.0012$], [$-4.2515$], [$< 0.0001$],
))

#tab(table(
  columns: (2fr, 1fr, 1fr),
  align: (left, right, right),
  table.header([*Estadístico*], [*Logarítmico*], [*Niveles*]),
  table.hline(stroke: 1.25pt),
  [Observaciones], [$1000$], [$1000$],
  [gl del modelo / residuos], [$4 slash 995$], [$3 slash 996$],
  [$R^2$], [$0.3095$], [$0.2709$],
  [$R^2$ ajustado], [$0.3067$], [$0.2687$],
  [F global], [$111.4855$], [$123.3772$],
  [Valor p de F], [$< 0.0001$], [$< 0.0001$],
  [Log-verosimilitud], [$-640.5354$], [$-3092.4865$],
  [AIC], [$1291.0707$], [$6192.9731$],
  [BIC], [$1315.6095$], [$6212.6041$],
  [Ómnibus], [$0.7966$], [$431.2900$],
  [Valor p de Ómnibus], [$0.6714$], [$< 0.0001$],
  [Jarque–Bera], [$0.6665$], [$3211.6587$],
  [Valor p de Jarque–Bera], [$0.7166$], [$< 0.0001$],
  [Asimetría], [$-0.0243$], [$1.8076$],
  [Curtosis], [$3.1167$], [$11.0006$],
  [Durbin–Watson], [$0.5743$], [$0.4911$],
  [Número de condición], [$9159.2823$], [$4291.1761$],
))

#text(size: 9pt)[EE: error estándar. Los AIC de esta salida corresponden a las
regresiones originales; los del apartado anterior están ajustados para compararlos.]
