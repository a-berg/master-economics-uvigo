# Completar China con alternativas útiles — 02/11/2026

Objetivo acordado: disponer de datos utilizables en un trabajo de máster, distinguiendo una equivalencia de una aproximación sin exigir identidad perfecta. Una serie corta publicada puede ser más útil que una reconstrucción larga arbitraria. No se interpolan años ni se impone el cierre de identidades a datos de ediciones distintas. España, v0 y las anotaciones manuales de `contratos.csv` se conservan.

| Necesidad | Búsqueda y objetivo | Alternativa de cierre y uso |
|---|---|---|
| Existencias reales | Mantener búsqueda P52+P53 → P52 ya realizada; revisar FMI/IFS y OCDE. | Índice de la serie real FMI 1980–2019; nominal OCDE para peso en PIB. No restar cadenas ni prolongar con otra fuente. |
| CCF real | Buscar P51C en OCDE; WDI como contraste nominal; revisar detalle PWT por activos. | Aproximar volumen con Σ(Dc_activo/Np_activo), índice 2021=100. Np es precio del stock, no deflactor específico de CCF: comprobar sensibilidad con Ip. |
| Remuneración | Obtener D1 OCDE, contrastar con usos domésticos NBS. | Serie anual publicada; cuota del PIB del mismo conjunto. Mantener alcance de renta de autónomos chino como diferencia material. |
| Excedente bruto | Buscar B2G, después B2G+B3G. | Usar B2A3G publicado, con renta mixta incluida. Residuo PIB−D1−tributos netos, separado y sin empalmar, para explorar años recientes. |
| Impuestos D2 | OCDE primero; cotejar código con NBS. | Si el D2 distribuido corresponde a impuestos netos, emplearlo como aproximación neta y decirlo; fiscalidad WDI como contexto, nunca sustituir D2 sin aviso. |
| Subvenciones D3 | OCDE D3; WDI/FMI GFS; notas NBS; ampliar a investigación FMI con datos públicos y presupuestos históricos NBS. | Serie fiscal parcial de subvenciones a precios; estimación monetaria a empresas FMI aparte. No inferir cero de una celda vacía ni enlazar ambas. |
| PIB coste de factores | Buscar agregado directo; después PIB−(D2−D3) de una fuente compatible. | Aproximación PIB−serie tributaria OCDE interpretada como neta; no volver a sumar una subvención de otra definición. |
| Producción e intermedios | Tabla sectorial OCDE; revisar tabla IO NBS ya archivada. | Niveles con escala inferida por cotejo de D1 con flujos de fondos, señalada explícitamente. Cocientes producción/VAB y consumos intermedios/producción cancelan esa escala. Año estructural suficiente para el ejercicio IO. |
| Input-output | Aprovechar 400 celdas NBS comprobadas y sus totales. | Matriz 3×3 de coeficientes técnicos a_ij=z_ij/x_j. No confundirla con porcentajes sobre consumos intermedios. |
| C, G, inversión, FBCF, X, M reales | Confirmar disponibilidad OCDE y leyendas PWT. | Seleccionar los índices PWT existentes, válidos para crecimiento; bases 2021/2020 distintas no impiden comparar tasas. No sumar componentes encadenados. |
| Paro registrado y de encuesta | Conservar fuente nacional/ILO existente; identificar ámbito y frecuencia. | Series cortas aceptadas con cobertura urbana o encuesta identificada. OIT modelizada para histórico nacional, separada. |

Regla de cierre: después de consultar las fuentes prioritarias y una ampliación dirigida, seleccionar la alternativa que conserve mejor el significado económico y sea reproducible. Registrar solo las diferencias que cambian la interpretación: bruto/neto, inclusión de renta mixta, volumen/nominal, ámbito, años y estimación frente a observación. El registro técnico conserva URLs, fechas, hashes y consultas fallidas.

La tabla `seleccion_conceptos.csv` es el mapa de uso efectivo. `discrepancias_informe.md` resume las cautelas y resultados. Las nuevas series se incorporan a una vista ampliada de China, sin sobreescribir la entrega original ni las notas del usuario. La búsqueda y normalización se han ejecutado; el Excel anual FMI continúa bloqueado por HTTP 403 y se ha seleccionado el histórico parcial NBS.
