"""Resuelve los cuatro apartados del supuesto 1.3; ejecutar con uv run solve.py."""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


DATA_DIR = Path(__file__).resolve().parents[2] / "datos"
SOURCE = DATA_DIR / "Supuesto 1.3 Modelos salarios. Hill.csv"


def scalar(value):
    return float(np.asarray(value).item())


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
    smearing = float(np.exp(log_model.resid).mean())
    predictions = {
        "Logarítmico (retransformación de Duan)": np.exp(log_model.fittedvalues) * smearing,
        "Lineal en niveles": level_model.fittedvalues,
    }
    tss = float(((data.WAGE - data.WAGE.mean()) ** 2).sum())
    metrics = {}
    for name, prediction in predictions.items():
        residual = data.WAGE - prediction
        metrics[name] = (
            float(np.sqrt(np.mean(residual**2))),
            float(np.mean(np.abs(residual))),
            1 - float(np.sum(residual**2)) / tss,
        )
    winner = min(metrics, key=lambda name: metrics[name][0])
    table = "\n".join(
        f"| {name} | {rmse:.6f} | {mae:.6f} | {r2:.6f} |"
        for name, (rmse, mae, r2) in metrics.items()
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

Para comparar en la misma escala y muestra, se retransfoma el modelo logarítmico:
WAGE estimado = exp(ln(WAGE) estimado) × media(exp(residuo)), con factor de Duan
{smearing:.8f}. El factor global aproxima la media condicional si el momento
E[exp(ε)|X] es constante; puede no ser adecuado bajo heterocedasticidad.

| Modelo | RMSE en WAGE | MAE en WAGE | 1 − SSE/TSS en WAGE |
| --- | ---: | ---: | ---: |
{table}

El menor RMSE dentro de la muestra corresponde a: **{winner}**.
El último indicador se calcula sobre WAGE para ambos modelos; en el modelo
retransformado no es su R² MCO original. Son medidas de ajuste dentro de la muestra,
no evidencia de superioridad predictiva fuera de ella. Las especificaciones también
difieren por la interacción, además de la transformación de la respuesta.

Los resúmenes completos de ambas estimaciones se guardan en `supuesto_1_3_resumenes.txt`.
"""
    summaries = (
        "MODELO 1: LOGARITMO DEL SALARIO\n\n" + log_model.summary().as_text()
        + "\n\nMODELO 2: SALARIO EN NIVELES\n\n" + level_model.summary().as_text() + "\n"
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
