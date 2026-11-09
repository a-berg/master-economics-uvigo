# Scripts del IPC personal

Ejecutar desde la raíz de la asignatura. Los scripts están en `source/ipc/`,
los documentos y sus datos en `entregas/ipc/`, y los resultados en `output/ipc/`.

## Actualización del informe

```bash
uv run python source/ipc/actualizar_informe.py
```

Lee el Excel revisado, actualiza `entregas/ipc/seguimiento_ipc.json` y compila
el Typst existente. No modifica el Excel ni el texto del informe. Las opciones
`--workbook /ruta/al/archivo.xlsx` y `--no-compile` permiten elegir otra copia
o actualizar únicamente los datos y la guía.

Para compilar solo el documento:

```bash
typst compile --root . entregas/ipc/mi_ipc_ABerges.typ output/ipc/mi_ipc_ABerges.pdf
```

## Preparación y revisión

- `analizar_ipc.py`: genera los datos base a partir del Excel original y aplica
  las ponderaciones oficiales guardadas en `entregas/ipc/ponderaciones_2025.json`.
- `preparar_seguimiento.py`: prepara el plan de fuentes y estimaciones.
- `actualizar_ponderaciones.mjs`, `revisar_cuotas.mjs` y `ajustar_graficos.py`:
  documentan las correcciones posteriores de ponderaciones, cuotas y gráficos.
- `preparar_importacion.py`, `completar_excel.mjs` y `cargar_seguimiento.mjs`:
  preparación y carga iniciales. **No volver a ejecutarlos sobre el Excel ya
  completado**, porque pueden reconstruirlo o reemplazar copias temporales.
- `revisar_excel.mjs` y los scripts `verificar_*`: revisión y comprobaciones.
  Algunas comprobaciones corresponden a etapas intermedias y esperan precios
  vacíos o copias temporales de aquella etapa.

Los scripts JavaScript requieren `@oai/artifact-tool` del runtime de Codex.
El enlace local `node_modules` y las cachés de Python se excluyen de Git.
No se incluyen las dependencias instaladas dentro del código fuente.
