# Supuesto 1.3 — regresión salarial

Desde esta carpeta:

```bash
uv run --locked solve.py
```

`uv` crea el entorno `.venv` e instala las dependencias fijadas en `uv.lock`.
El script utiliza pandas y statsmodels, localiza el CSV respecto a su propia ruta,
y guarda en `../../datos/`:

- `supuesto_1_3_resultados.md`: respuestas en español a los cuatro apartados.
- `supuesto_1_3_resumenes.txt`: resúmenes completos de los dos ajustes MCO.

Se usan errores estándar convencionales y la misma muestra en ambos modelos.
Los valores ausentes, no numéricos, infinitos o salarios no positivos generan
un error explícito. El CSV original se conserva sin modificaciones.
