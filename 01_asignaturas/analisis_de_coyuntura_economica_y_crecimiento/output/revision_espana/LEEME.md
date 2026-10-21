# Estado vigente de España

La actualización posterior a las anotaciones del alumno está en [ACTUALIZACION_ANOTACIONES.md](ACTUALIZACION_ANOTACIONES.md).

- **97 series integradas**, 5.599 observaciones: 84 AMECO, tres EPA, dos PWT, seis cuentas INE y dos componentes salariales Eurostat.
- AMGE/AXGE están excluidas de la edición actual; no bloquean el objetivo AMECO activo.
- [filas_reconciliadas.csv](filas_reconciliadas.csv) conserva las anotaciones originales y distingue clasificación conceptual de integración efectiva.
- `datos/silver/espana.parquet/csv`: tabla larga con valores, unidades, fuente, hash, estados, previsiones y transformaciones.
- `datos/silver/espana_anual.parquet/csv`: vista ancha sin el horizonte de previsión AMECO; 1950–2025 es el rango total, no la cobertura común.
- `datos/silver/espana_catalogo.parquet` y [catalogo_espana.csv](catalogo_espana.csv): catálogo vigente, con 99 entradas incluidas las dos excluidas.
- `notebooks/02_revision_espana.ipynb`: notebook ejecutado con las 31 comparaciones históricas y la revisión de anotaciones.

Las notas de cierre anteriores se conservan como histórico de la auditoría. No reflejan los diez conceptos AMECO y las restantes series integradas en esta actualización. Permanecen descargas/selecciones pendientes para población adicional, paro registrado, SMI, empresas, dinero y tipo de cambio; el detalle está en el documento vigente.
