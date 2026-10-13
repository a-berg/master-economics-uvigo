"""Resuelve los cuatro apartados del supuesto 1.3; ejecutar con uv run solve.py."""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy.optimize import minimize_scalar, brentq
from scipy.stats import chi2


DATA_DIR = Path(__file__).resolve().parents[2] / "datos"
SOURCE = DATA_DIR / "Supuesto 1.3 Modelos salarios. Hill.csv"


def scalar(value):
    return float(np.asarray(value).item())


def box_cox_analysis(data, full_x, reduced_x):
    """Gaussian regression profile likelihood, including the response Jacobian."""
    log_y = np.log(data.WAGE.to_numpy())
    n = len(log_y)

    def loglike(lam, x=full_x):
        transformed = log_y if abs(lam) < 1e-10 else np.expm1(lam * log_y) / lam
        fit = sm.OLS(transformed, x).fit()
        return float(fit.llf + (lam - 1) * log_y.sum())

    optimum = minimize_scalar(lambda lam: -loglike(lam), bounds=(-2, 2), method="bounded")
    if not optimum.success or abs(optimum.x) > 1.99:
        raise RuntimeError("Revisar la búsqueda del máximo Box-Cox.")
    lam = float(optimum.x)
    ll = loglike(lam)
    cutoff = chi2.ppf(0.95, 1)
    boundary = lambda value: 2 * (ll - loglike(value)) - cutoff
    ci = (brentq(boundary, -2, lam), brentq(boundary, lam, 2))
    tests = []
    for label, value, x, df in (
        ("Logarítmico con interacción: λ = 0", 0, full_x, 1),
        ("Niveles con interacción: λ = 1", 1, full_x, 1),
        ("Niveles del enunciado: λ = 1 y β₄ = 0", 1, reduced_x, 2),
    ):
        lr = 2 * (ll - loglike(value, x))
        tests.append((label, lr, df, float(chi2.sf(lr, df))))
    return lam, ci, tests


def main():
    raw = pd.read_csv(SOURCE)
    data = raw[["WAGE", "EDUC", "EXPER"]].apply(pd.to_numeric, errors="raise")
    # Fail explicitly rather than silently changing the estimation sample.
    if data.empty or not np.isfinite(data.to_numpy()).all():
        raise ValueError("La muestra debe contener datos numéricos finitos, sin ausentes.")
    if (data.WAGE <= 0).any():
        raise ValueError("WAGE debe ser positivo para calcular su logaritmo.")
    data = data.assign(LNWAGE=np.log(data.WAGE))
    log_model = smf.ols("LNWAGE ~ EDUC + EXPER + I(EXPER ** 2) + EDUC:EXPER", data).fit()
    level_model = smf.ols("WAGE ~ EDUC + EXPER + I(EXPER ** 2)", data).fit()
    for model in (log_model, level_model):
        if np.linalg.matrix_rank(model.model.exog) != model.model.exog.shape[1]:
            raise ValueError("La matriz de regresores no tiene rango completo.")

    b = log_model.params
    marginal = log_model.t_test("EXPER + 30 * I(EXPER ** 2) + 16 * EDUC:EXPER = 0")
    effect = scalar(marginal.effect)
    ci_low, ci_high = marginal.conf_int()[0]
    education = log_model.f_test("EDUC = 0, EDUC:EXPER = 0")
    # Exact discrete change from 15 to 16, holding EDUC=16.
    discrete = b["EXPER"] + 31 * b["I(EXPER ** 2)"] + 16 * b["EDUC:EXPER"]
    bc_lambda, bc_ci, bc_tests = box_cox_analysis(
        data, log_model.model.exog, level_model.model.exog
    )
    bc_table = "\n".join(
        f"| {label} | {lr:.6f} | {df} | {pvalue:.6g} |"
        for label, lr, df, pvalue in bc_tests
    )
    coefficients = "\n".join(
        f"| {name} | {b[name]:.6f} | {log_model.bse[name]:.6f} | {log_model.pvalues[name]:.6g} |"
        for name in b.index
    )
    decision = "Se rechaza" if scalar(education.pvalue) < 0.05 else "No se rechaza"
    report = f"""# Supuesto 1.3: modelos de salarios

Fuente: `{SOURCE.name}`. Muestra: {len(data)} observaciones, sin exclusiones.
Estimación por MCO con constante. Inferencia convencional bajo homocedasticidad,
al nivel del 5 %. Los resultados describen asociaciones condicionales; por sí solos
no identifican efectos causales.

## 1. Modelo del logaritmo del salario

ln(WAGE) = β₀ + β₁ EDUC + β₂ EXPER + β₃ EXPER² + β₄ EDUC·EXPER + ε.

| Término | Coeficiente | Error estándar | p-valor |
| --- | ---: | ---: | ---: |
{coefficients}

R² = {log_model.rsquared:.6f}; R² ajustado = {log_model.rsquared_adj:.6f}.
El modelo explica el {100 * log_model.rsquared:.2f} % de la variación muestral
del logaritmo del salario. F global = {log_model.fvalue:.6f},
p = {log_model.f_pvalue:.6g}.

El efecto de EDUC sobre ln(WAGE) es {b['EDUC']:.6f} {b['EDUC:EXPER']:+.6f}·EXPER:
el coeficiente de EDUC por separado corresponde a EXPER = 0.
A 15 años de experiencia, un año de educación se asocia aproximadamente con
un {100 * (b['EDUC'] + 15 * b['EDUC:EXPER']):.4f} % de cambio salarial.
El efecto de EXPER es β₂ + 2β₃ EXPER + β₄ EDUC; β₂ corresponde a EDUC = EXPER = 0.
El término cuadrático implica una pendiente de experiencia
{'decreciente' if b['I(EXPER ** 2)'] < 0 else 'creciente'}, manteniendo EDUC constante.
La interacción indica cómo cambia el rendimiento de una variable al variar la otra;
su p-valor individual es {log_model.pvalues['EDUC:EXPER']:.6g}.
La constante corresponde a EDUC = EXPER = 0 y puede carecer de interpretación
económica práctica si ese perfil queda fuera del soporte de los datos.

## 2. Efecto marginal de experiencia: EXPER = 15, EDUC = 16

∂ln(WAGE)/∂EXPER = β₂ + 30β₃ + 16β₄ = {effect:.8f}.
Esto equivale a una semielasticidad de aproximadamente {100 * effect:.4f} % por año.
Error estándar = {scalar(marginal.sd):.8f}; IC del 95 % en unidades logarítmicas:
[{ci_low:.8f}, {ci_high:.8f}]; t = {scalar(marginal.tvalue):.6f};
p = {scalar(marginal.pvalue):.6g}.

La derivada es local. Para el incremento discreto de 15 a 16 años,
Δln(WAGE) = β₂ + 31β₃ + 16β₄ = {discrete:.8f}, y el cambio porcentual exacto
de exp(predicción logarítmica) es 100·(exp(Δln(WAGE))−1) = {100 * np.expm1(discrete):.4f} %.
Su interpretación como cambio de la media salarial requiere un factor de
retransformación constante entre ambos perfiles.

## 3. Significación conjunta de la educación

H₀: β₁ = β₄ = 0; H₁: al menos uno de los dos coeficientes es distinto de cero.
Hay que incluir la interacción: contrastar solo β₁ no evalúa el efecto total de EDUC.
F({int(education.df_num)}, {int(education.df_denom)}) = {scalar(education.fvalue):.6f};
p = {scalar(education.pvalue):.6g}. {decision} H₀ al 5 %.

## 4. Comparación con el modelo en niveles

WAGE = β₀ + β₁ EDUC + β₂ EXPER + β₃ EXPER² + ε.
R² = {level_model.rsquared:.6f}; R² ajustado = {level_model.rsquared_adj:.6f}.
Los R² (incluidos los ajustados) de ambos modelos no son directamente comparables:
uno mide variación de ln(WAGE) y el otro de WAGE. Tampoco se comparan directamente
sus AIC/BIC sin ajustar la verosimilitud por la transformación de la respuesta.

Se utiliza la transformación Box-Cox: y(λ) = (WAGE^λ − 1)/λ si λ ≠ 0,
con y(0) = ln(WAGE). Se estima una familia que incluye EDUC, EXPER, EXPER² y
EDUC·EXPER, además de la constante. λ = 0 reproduce el modelo logarítmico;
λ = 1 reproduce el modelo en niveles con interacción (restar 1 solo modifica
la constante). El modelo en niveles del enunciado exige además β₄ = 0.

Se maximiza la log-verosimilitud perfilada de la regresión gaussiana,
ℓ(λ) = −n/2·[ln(2π) + 1 + ln(SSE(λ)/n)] + (λ−1)·Σln(WAGE).
El último término es el jacobiano de la transformación y permite comparar
verosimilitudes sobre la misma variable original. No se estima λ únicamente
sobre la distribución marginal del salario: se condiciona en los regresores.

λ estimado = {bc_lambda:.6f}; IC del 95 % por razón de verosimilitudes:
[{bc_ci[0]:.6f}, {bc_ci[1]:.6f}]. Para cada hipótesis se calcula
LR = 2·[ℓ(λ estimado) − ℓ(restringida)], con referencia asintótica χ² y tantos
grados de libertad como restricciones, bajo los supuestos del modelo gaussiano
homocedástico e independencia de las observaciones.

| Hipótesis nula | LR | gl | Valor p |
| --- | ---: | ---: | ---: |
{bc_table}

Al 5 %, se rechazan tanto λ = 0 como λ = 1. También se rechaza la
restricción conjunta λ = 1 y β₄ = 0, correspondiente al modelo en niveles
solicitado. El modelo logarítmico tampoco es la transformación óptima según
este contraste. Para elegir entre las dos especificaciones concretas se comparan
sus AIC sobre la escala original, incorporando el jacobiano: AIC del modelo
logarítmico = {(-2 * (log_model.llf - data.LNWAGE.sum()) + 2 * (len(log_model.params) + 1)):.6f};
AIC del modelo en niveles = {(-2 * level_model.llf + 2 * (len(level_model.params) + 1)):.6f}.
Se cuenta la varianza residual como parámetro en ambos modelos. El menor AIC
favorece al logarítmico con interacción entre las dos alternativas, aunque
Box-Cox sugiere una potencia distinta de cero. Esto no prueba superioridad predictiva fuera
de la muestra. El contraste de λ mantiene fijos los regresores; la última fila
considera además la distinta especificación del modelo alternativo.

Referencia metodológica: SAS/STAT, Box-Cox Transformations:
https://support.sas.com/documentation/cdl/en/statug/65328/HTML/default/statug_transreg_details02.htm

Los resúmenes completos de ambas estimaciones se guardan en `supuesto_1_3_resumenes.txt`.
"""
    summaries = (
        "MODELO 1: LOGARITMO DEL SALARIO\n\n" + log_model.summary().as_text()
        + "\n\nMODELO 2: SALARIO EN NIVELES\n\n" + level_model.summary().as_text() + "\n"
        + f"\nBOX-COX: lambda = {bc_lambda:.6f}; IC 95 % = {bc_ci}\n"
        + bc_table + "\n"
    )
    for filename, content in (
        ("supuesto_1_3_resultados.md", report),
        ("supuesto_1_3_resumenes.txt", summaries),
    ):
        output = DATA_DIR / filename
        output.write_text(content, encoding="utf-8")
        print(output)


if __name__ == "__main__":
    main()
