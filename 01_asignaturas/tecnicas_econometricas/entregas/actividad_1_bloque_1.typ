#import "@local/master-uvigo-templates:0.1.0": homework_econ

#show: homework_econ.with(
  title: "Actividad 1 Bloque 1",
  course: "Técnicas Econométricas",
  date: datetime(year: 2026, month: 9, day: 26),
)

#set math.equation(numbering: none)
#let WAGE = math.upright("WAGE")
#let EDUC = math.upright("EDUC")
#let EXPER = math.upright("EXPER")
#set table(inset: 5pt, stroke: 0.3pt + luma(75%))
#let tab(body) = block(width: 100%)[
  #set text(size: 9pt)
  #set par(first-line-indent: 0pt, leading: 0.4em)
  #body
]

= Estimación del modelo salarial

Se utilizan las 1.000 observaciones del archivo «Supuesto 1.3 Modelos salarios. Hill.csv», sin excluir registros. La variable dependiente es el logaritmo natural del salario; las variables explicativas son los años de educación y experiencia laboral, el cuadrado de la experiencia y la interacción entre educación y experiencia. Se estima por mínimos cuadrados ordinarios (MCO) el siguiente modelo:

$ ln(WAGE_i) = beta_0 + beta_1 EDUC_i + beta_2 EXPER_i + beta_3 EXPER_i^2 + beta_4 EDUC_i EXPER_i + epsilon_i. $

#tab(table(
  columns: (1.4fr, 1fr, 1fr, 1fr),
  align: (left, right, right, right),
  table.header([*Variable*], [*Coeficiente*], [*Error estándar*], [*Valor p*]),
  [Constante], [−0.264598], [0.180767], [0.143577],
  [Educación], [0.150557], [0.012719], [$2.44777 times 10^(-30)$],
  [Experiencia], [0.067060], [0.009533], [$3.71938 times 10^(-12)$],
  [Experiencia²], [−0.000696], [0.000108], [$1.82047 times 10^(-10)$],
  [Educación × experiencia], [−0.002019], [0.000555], [0.000285565],
))

El coeficiente de determinación es $R^2 = 0.309480$ y su valor ajustado es
$0.306704$. Por tanto, el modelo explica el $30.95%$ de la variación muestral
del logaritmo del salario. El contraste de significación global proporciona
$F(4.995) = 111.486$, con un valor $p$ de $1.52 times 10^(-78)$, por lo que
se rechaza que todos los coeficientes de pendiente sean simultáneamente nulos.

Los cuatro términos explicativos son individualmente significativos al $5%$,
mientras que la constante no lo es. La interpretación de los coeficientes debe
considerar la interacción: el coeficiente de educación representa su efecto
sobre el logaritmo del salario cuando la experiencia es cero. Para cualquier
otro nivel de experiencia, la semielasticidad estimada es:

$ (partial hat(ln(WAGE))) / (partial EDUC) = hat(beta)_1 + hat(beta)_4 EXPER. $

A los 15 años de experiencia, un año adicional de educación se asocia con un
incremento salarial aproximado del $12.03%$. El signo negativo de la interacción
indica que esta asociación disminuye conforme aumenta la experiencia. Asimismo,
el coeficiente negativo del término cuadrático implica rendimientos marginales
decrecientes de la experiencia, manteniendo constante la educación.

Los errores estándar y los contrastes se calculan con la matriz de covarianzas
convencional, bajo homocedasticidad. Los coeficientes describen asociaciones
condicionales y no permiten, por sí solos, establecer relaciones causales.

= Efecto marginal de un año de experiencia

Para una persona con 15 años de experiencia y 16 años de educación, el efecto
marginal se obtiene derivando la función estimada respecto a la experiencia:

$ (partial hat(ln(WAGE))) / (partial EXPER) = hat(beta)_2 + 2 hat(beta)_3 EXPER
+ hat(beta)_4 EDUC. $

Al sustituir el perfil indicado, utilizando los coeficientes sin redondear,
resulta:

$ hat(m) = hat(beta)_2 + 30 hat(beta)_3 + 16 hat(beta)_4 = 0.01387. $

Así, un año adicional de experiencia se asocia localmente con un aumento
salarial aproximado del *1.3870%*, manteniendo constante la educación. El
error estándar de esta combinación lineal, calculado con la matriz completa de
covarianzas, es 0.00222234. Su intervalo de confianza del 95% es $[0.0095;
0.0182]$, equivalente aproximadamente a un intervalo entre el $0.951%$ y el
$1.823%$. El contraste de efecto marginal nulo proporciona $t = 6.2412$ y un
valor p de $6.41584 times 10^(-10)$.

Conviene distinguir la derivada local del cambio discreto de 15 a 16 años.
Debido al término cuadrático, este último es:

$ Delta hat(ln(WAGE)) = hat(beta)_2 + (16^2 - 15^2) hat(beta)_3 + 16 hat(beta)_4 = 0.01317. $

La variación porcentual exacta de la predicción exponenciada es, por tanto, $100
(exp(0. 01317) - 1) = 1.3261%$. Interpretarla como una variación de la media
condicional del salario requiere que el factor de retransformación permanezca
constante entre ambos perfiles.

= Significación estadística de la educación

Dado que la educación aparece tanto de forma individual como en la interacción,
su relevancia debe evaluarse mediante un contraste conjunto:

$ H_0: beta_1 = beta_4 = 0. quad H_1: (beta_1. beta_4) != (0.0). $

Bajo la hipótesis nula, la educación no contribuye a explicar el salario para
ningún nivel de experiencia. El estadístico del contraste es:

$ F(2.995) = 171.2677 quad p = 1.2025 times 10^(-64). $

Se rechaza la hipótesis nula al nivel de significación del 5%. Existe, por
tanto, evidencia estadística de una contribución conjunta de la educación y
su interacción con la experiencia a la explicación del salario. Contrastar
únicamente el coeficiente de educación no respondería a esta pregunta, pues
dicho coeficiente recoge su efecto cuando la experiencia es cero.

= Comparación de la bondad del ajuste

El modelo alternativo se estima sobre la misma muestra y expresa el salario en
niveles, sin incluir la interacción:

$ WAGE_i = beta_0 + beta_1 EDUC_i + beta_2 EXPER_i + beta_3 EXPER_i^2 + epsilon_i. $

La ecuación estimada, con coeficientes redondeados, es:

$ hat(WAGE)_i = -9.8177 + 1.2101 EDUC_i + 0.3409 EXPER_i - 0.0051 EXPER_i^2. $

Su coeficiente de determinación es $R^2 = 0.2709$ y su valor ajustado es
$0.2687$. Estos valores no se pueden comparar directamente con los del primer
modelo: la variación explicada se refiere al salario en un caso y a su logaritmo
en el otro. Por la misma razón, los valores de AIC y BIC de las salidas
originales tampoco son directamente comparables sin ajustar la verosimilitud por
la transformación de la variable dependiente.

Para evaluar el ajuste en una escala común, se transforma la predicción del
primer modelo a unidades de salario. La exponenciación simple no recupera,
en general, la media condicional. Se aplica el factor de corrección de Duan,
calculado como la media de los residuos exponenciados:

$ hat(s) 
  = 1/n sum_(i=1)^n exp(hat(epsilon)_i) 
  = 1.1110. quad hat(WAGE)_i 
  = hat(s) exp(hat(ln(WAGE))_i). $

Este factor global aproxima la media condicional si $E[exp(epsilon_i) | X_i]$
es constante. Su uso puede resultar inadecuado si dicho momento varía entre
observaciones. Las medidas de ajuste obtenidas sobre el salario y la misma
muestra son:

#tab(table(
  columns: (2fr, 1fr, 1fr, 1.2fr),
  align: (left, right, right, right),
  table.header([*Modelo*], [*RMSE*], [*MAE*], [*$1 - "SSE"/"TSS"$*]),
  [Logarítmico con corrección de Duan], [5.285704], [3.714974], [0.283284],
  [Lineal en niveles], [5.331049], [3.806712], [0.270934],
))

RMSE es la raíz del error cuadrático medio y MAE es el error absoluto medio. SSE
representa la suma de los errores de predicción al cuadrado y TSS la suma de las
desviaciones cuadráticas del salario respecto a su media. Todas estas medidas se
calculan dentro de la muestra de estimación.

El modelo logarítmico retransformado presenta un ajuste ligeramente mejor:
registra menores RMSE y MAE, así como un mayor valor de $1 - "SSE"/"TSS"$.
Este último indicador no coincide con el $R^2$ original del modelo logarítmico.
La comparación no demuestra superioridad predictiva fuera de la muestra y
refleja tanto la transformación de la variable dependiente como la distinta
especificación, ya que solo el primer modelo incorpora la interacción.

#pagebreak()
#heading(numbering: none)[Anexo. Resúmenes de las estimaciones MCO]

Los siguientes cuadros recogen los estadísticos de las salidas de statsmodels. Se conservan las precisiones del resumen original; los valores p mostrados allí como 0.000 se expresan como menores que 0.001. Ambos modelos incluyen constante, utilizan 1.000 observaciones y emplean una matriz de covarianzas no robusta.

#heading(level: 2, numbering: none)[Modelo 1: logaritmo del salario]
#tab(table(
  columns: (1.2fr, 1fr, 1fr, 0.8fr, 0.8fr, 1.5fr),
  align: (left, right, right, right, right, right),
  table.header([*Variable*], [*Coef.*], [*EE*], [*t*], [*p*], [*IC 95 %*]),
  [Constante], [−0.2646], [0.181], [−1.464], [0.144], [−0.619; 0.090],
  [Educación], [0.1506], [0.013], [11.837], [< 0.001], [0.126; 0.176],
  [Experiencia], [0.0671], [0.010], [7.034], [< 0.001], [0.048; 0.086],
  [Experiencia²], [−0.0007], [0.000], [−6.443], [< 0.001], [−0.001; −0.000],
  [Educ. × exp.], [−0.0020], [0.001], [−3.641], [< 0.001], [−0.003; −0.001],
))

#heading(level: 2, numbering: none)[Modelo 2: salario en niveles]
#tab(table(
  columns: (1.2fr, 1fr, 1fr, 0.8fr, 0.8fr, 1.5fr),
  align: (left, right, right, right, right, right),
  table.header([*Variable*], [*Coef.*], [*EE*], [*t*], [*p*], [*IC 95 %*]),
  [Constante], [−9.8177], [1.055], [−9.306], [< 0.001], [−11.888; −7.747],
  [Educación], [1.2101], [0.070], [17.228], [< 0.001], [1.072; 1.348],
  [Experiencia], [0.3409], [0.051], [6.629], [< 0.001], [0.240; 0.442],
  [Experiencia²], [−0.0051], [0.001], [−4.252], [< 0.001], [−0.007; −0.003],
))

#tab(table(
  columns: (2fr, 1fr, 1fr),
  align: (left, right, right),
  table.header([*Estadístico*], [*Modelo 1*], [*Modelo 2*]),
  [Grados de libertad del modelo / residuos], [4 / 995], [3 / 996],
  [$R^2$ / $R^2$ ajustado], [0.309 / 0.307], [0.271 / 0.269],
  [F global], [111.5], [123.4],
  [Valor p del contraste F], [$1.52 times 10^(-78)$], [$5.98 times 10^(-68)$],
  [Log-verosimilitud], [−640.54], [−3092.5],
  [AIC / BIC], [1291 / 1316], [6193 / 6213],
  [Ómnibus / valor p], [0.797 / 0.671], [431.290 / < 0.001],
  [Jarque–Bera / valor p], [0.667 / 0.717], [3211.659 / < 0.001],
  [Asimetría / curtosis], [−0.024 / 3.117], [1.808 / 11.001],
  [Durbin–Watson], [0.574], [0.491],
  [Número de condición], [$9.16 times 10^3$], [$4.29 times 10^3$],
))

#text(size: 9pt)[
  *Notas.* EE: error estándar; IC: intervalo de confianza. Los ceros en errores estándar y límites de intervalos reflejan el redondeo de la salida. Los números de condición elevados pueden reflejar problemas de escala o multicolinealidad, particularmente con términos polinómicos e interacciones. El estadístico Durbin–Watson depende del orden de las observaciones y no debe interpretarse automáticamente como evidencia de autocorrelación temporal en esta muestra.
]
