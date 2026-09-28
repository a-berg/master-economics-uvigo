# Supuesto 1.3: modelos de salarios

Fuente: `Supuesto 1.3 Modelos salarios. Hill.csv`. Muestra: 1000 observaciones, sin exclusiones.
Estimación por MCO con constante. Inferencia convencional bajo homocedasticidad,
al nivel del 5 %. Los resultados describen asociaciones condicionales; por sí solos
no identifican efectos causales.

## 1. Modelo del logaritmo del salario

ln(WAGE) = β₀ + β₁ EDUC + β₂ EXPER + β₃ EXPER² + β₄ EDUC·EXPER + ε.

| Término | Coeficiente | Error estándar | p-valor |
| --- | ---: | ---: | ---: |
| Intercept | -0.264598 | 0.180767 | 0.143577 |
| EDUC | 0.150557 | 0.012719 | 2.44777e-30 |
| EXPER | 0.067060 | 0.009533 | 3.71938e-12 |
| I(EXPER ** 2) | -0.000696 | 0.000108 | 1.82047e-10 |
| EDUC:EXPER | -0.002019 | 0.000555 | 0.000285565 |

R² = 0.309480; R² ajustado = 0.306704.
El modelo explica el 30.95 % de la variación muestral
del logaritmo del salario. F global = 111.485525,
p = 1.51555e-78.

El efecto de EDUC sobre ln(WAGE) es 0.150557 -0.002019·EXPER:
el coeficiente de EDUC por separado corresponde a EXPER = 0.
A 15 años de experiencia, un año de educación se asocia aproximadamente con
un 12.0272 % de cambio salarial.
El efecto de EXPER es β₂ + 2β₃ EXPER + β₄ EDUC; β₂ corresponde a EDUC = EXPER = 0.
El término cuadrático implica una pendiente de experiencia
decreciente, manteniendo EDUC constante.
La interacción indica cómo cambia el rendimiento de una variable al variar la otra;
su p-valor individual es 0.000285565.
La constante corresponde a EDUC = EXPER = 0 y puede carecer de interpretación
económica práctica si ese perfil queda fuera del soporte de los datos.

## 2. Efecto marginal de experiencia: EXPER = 15, EDUC = 16

∂ln(WAGE)/∂EXPER = β₂ + 30β₃ + 16β₄ = 0.01387016.
Esto equivale a una semielasticidad de aproximadamente 1.3870 % por año.
Error estándar = 0.00222234; IC del 95 % en unidades logarítmicas:
[0.00950914, 0.01823118]; t = 6.241230;
p = 6.41584e-10.

La derivada es local. Para el incremento discreto de 15 a 16 años,
Δln(WAGE) = β₂ + 31β₃ + 16β₄ = 0.01317393, y el cambio porcentual exacto
de exp(predicción logarítmica) es 100·(exp(Δln(WAGE))−1) = 1.3261 %.
Su interpretación como cambio de la media salarial requiere un factor de
retransformación constante entre ambos perfiles.

## 3. Significación conjunta de la educación

H₀: β₁ = β₄ = 0; H₁: al menos uno de los dos coeficientes es distinto de cero.
Hay que incluir la interacción: contrastar solo β₁ no evalúa el efecto total de EDUC.
F(2, 995) = 171.267714;
p = 1.20254e-64. Se rechaza H₀ al 5 %.

## 4. Comparación con el modelo en niveles

WAGE = β₀ + β₁ EDUC + β₂ EXPER + β₃ EXPER² + ε.
R² = 0.270934; R² ajustado = 0.268738.
Los R² (incluidos los ajustados) de ambos modelos no son directamente comparables:
uno mide variación de ln(WAGE) y el otro de WAGE. Tampoco se comparan directamente
sus AIC/BIC sin ajustar la verosimilitud por la transformación de la respuesta.

Para comparar en la misma escala y muestra, se retransfoma el modelo logarítmico:
WAGE estimado = exp(ln(WAGE) estimado) × media(exp(residuo)), con factor de Duan
1.11094565. El factor global aproxima la media condicional si el momento
E[exp(ε)|X] es constante; puede no ser adecuado bajo heterocedasticidad.

| Modelo | RMSE en WAGE | MAE en WAGE | 1 − SSE/TSS en WAGE |
| --- | ---: | ---: | ---: |
| Logarítmico (retransformación de Duan) | 5.285704 | 3.714974 | 0.283284 |
| Lineal en niveles | 5.331049 | 3.806712 | 0.270934 |

El menor RMSE dentro de la muestra corresponde a: **Logarítmico (retransformación de Duan)**.
El último indicador se calcula sobre WAGE para ambos modelos; en el modelo
retransformado no es su R² MCO original. Son medidas de ajuste dentro de la muestra,
no evidencia de superioridad predictiva fuera de ella. Las especificaciones también
difieren por la interacción, además de la transformación de la respuesta.

Los resúmenes completos de ambas estimaciones se guardan en `supuesto_1_3_resumenes.txt`.
