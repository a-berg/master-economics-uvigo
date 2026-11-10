# Primera compilación: apéndice de gráficas en Lilaq

PDF: [apéndice para revisión](../pdf/apendice_graficas_revision.pdf).

Contiene 38 gráficas en 38 páginas, con paneles de China y España, identificadores docentes, fuentes, coberturas y notas. No incluye tablas ni el texto principal del informe. Las referencias repetidas de los temas 4 y 5 reutilizan las gráficas originales del catálogo.

Las gráficas se dibujan con **Lilaq 0.6.0** dentro de Typst; no se insertan las imágenes Matplotlib de la exploración. Se conservan los 6.479 puntos de los CSV verificados, con cambios explícitos de escala para que los ejes sean legibles. No se unen observaciones separadas por años ausentes.

- Fuente editable: `entregas/apendice_graficas_lilaq.typ`.
- Datos de dibujo: `output/apendice_lilaq/graficas.json`.
- Exportador: `src/build_lilaq_appendix.py`.
- Validación de puntos, fuentes y PDF: `src/verify_lilaq_appendix.py`.
- Los hashes de entrada están en `manifest.json`; la comprobación está en `verification.json`.

```sh
uv run --offline python src/build_lilaq_appendix.py
mkdir -p output/pdf
typst compile --root . entregas/apendice_graficas_lilaq.typ output/pdf/apendice_graficas_revision.pdf
uv run --offline python src/verify_lilaq_appendix.py
```

La primera revisión comprobó las 38 páginas renderizadas, las leyendas, las notas y la ausencia de texto fuera de página. El PDF no contiene imágenes ráster incrustadas. Las series y las capas silver/gold se conservan.
