# Guion de redacción a partir de los datos preparados

El objetivo es comparar cómo han evolucionado el crecimiento, la inversión, la productividad y el mercado laboral de China y España. La comparación principal cubre 1990–2023; el crecimiento de largo plazo se estudia desde 1960. La [guía de resultados](../output/preparacion_informe/GUIA_PARA_REDACTAR.md) contiene las primeras cifras y enlaces a todos los ejercicios.

## Materiales y métodos: texto de partida

Se utiliza PWT 11 para disponer de una base común de producto, capital, empleo y horas, y su complemento de cuentas nacionales para estudiar la demanda. Las series nacionales de precios y rentas proceden de AMECO, WDI y OCDE. Las fuentes españolas conservan la integración previa de INE y SEPE; los datos estructurales chinos proceden del NBS. Las fechas de consulta y los archivos originales se registran para poder reproducir los cálculos.

La falta de determinadas series chinas obligó a adaptar algunos ejercicios. La evolución de la demanda se presenta mediante índices y tasas; el consumo de capital fijo real se aproxima con información de cuatro grupos de activos PWT. Las rentas chinas incluyen un excedente agregado con renta mixta y una magnitud tributaria interpretada como neta. Las subvenciones disponibles representan una categoría fiscal parcial. Cada adaptación se indica junto al resultado y limita las conclusiones que pueden extraerse.

Las estadísticas cíclicas se calculan sobre tasas anuales de observaciones consecutivas. Para cada par de variables se utilizan los mismos años en ambos países y se muestra el tamaño de muestra. Se comparan las ventanas 1996–2019 y 1996–2023 para observar la sensibilidad a los años posteriores a 2019. En las existencias, que son un flujo y pueden ser negativas, se emplean cambios del flujo escalado. No se interpolan datos ni se empalman fuentes para prolongar coberturas.

La contabilidad del crecimiento supone una función Cobb–Douglas con participación del capital igual a un tercio. Se descompone el crecimiento logarítmico anualizado en aportaciones del capital, el empleo y un residuo. Las tasas compuestas se presentan por separado. El residuo recoge factores omitidos y errores de medición, además de posibles cambios tecnológicos.

## Qué explicar en cada tema

| Tema | Evidencia preparada | Pregunta para orientar el comentario |
|---|---|---|
| 2A. Oferta | Producción, CI, VAB y PIB nominal/real | ¿Qué distingue producción bruta, valor añadido y PIB? ¿Qué permite comparar un dato estructural chino con una serie española? |
| 2B. Demanda | Participaciones, promedios, tasas y 2008=100 | ¿Qué componentes tienen mayor peso y volatilidad? ¿Cómo cambia la demanda tras 2008? |
| 2C. Inputs | Inversión, CCF aproximado, capital, empleo, horas y productividad | ¿Cuánto aporta acumular capital por trabajador y cómo cambia la productividad por hora respecto a la productividad por ocupado? |
| 2D. Rentas | Remuneración y excedente sobre coste de factores, IO china | ¿Cómo se distribuyen las rentas productivas? ¿Qué cambia al incluir renta mixta o usar tributos netos? |
| 3. Precios | IPC, deflactor y remuneración por ocupado | ¿Por qué divergen IPC y deflactor? ¿Cómo cambia la lectura de la remuneración al descontar precios? |
| 4. Trabajo | Modelos comparables, demografía, registro y encuesta aparte | ¿Cómo influye la estructura demográfica? ¿Por qué registro, encuesta y modelización dan cifras distintas? |
| 5. Ciclos | Tablas y gráficos reutilizados | ¿Qué variables son más volátiles o procíclicas? ¿Cambian las asociaciones al incluir 2020–2023? |
| 6. Crecimiento | CAGR por subperiodos, PIB por habitante PPA y Gini | ¿Cambian las diferencias entre países al considerar población? ¿Qué muestran los pares observados de desigualdad, sin atribuir causalidad? |
| 7. Fuentes | Contabilidad 1960–2023 y mismos subperiodos | ¿Qué peso tienen capital, empleo y residuo? ¿Cómo afectan la medición del trabajo y la omisión de capital humano a la interpretación? |

## Cómo explicar las dificultades sin convertirlas en el centro del informe

En métodos basta resumir que las fuentes no ofrecen todos los conceptos con igual cobertura y que se han utilizado alternativas identificadas. En cada resultado se incorpora solo la diferencia que afecta a su interpretación: por ejemplo, «excedente incluida renta mixta», «CCF aproximado» o «paro modelizado». El registro técnico completo puede quedar como apéndice de fuentes.

Los obstáculos más relevantes fueron la ausencia de CCF real y D3 comparables, el carácter estructural de la IO china, las diferencias de universo laboral y el acceso bloqueado al Excel reciente del FMI. La respuesta fue seleccionar aproximaciones útiles, comprobar su coherencia y conservar los huecos. Esto permite demostrar que se entiende qué mide cada agregado y por qué dos series de nombre parecido pueden responder a preguntas distintas.

## Antes de cerrar

La comparación IO bilateral requiere todavía incorporar la tabla española. Las referencias históricas de otros países que aparecían en las tablas docentes tampoco se han reconstruido. El borrador Typst de octubre debe actualizarse para utilizar esta nueva base; sus comentarios de «pendiente» y sus cifras no representan automáticamente el estado actual.

Las fuentes de datos adicionales están preparadas en [fuentes_datos_informe.bib](fuentes_datos_informe.bib). Queda añadir bibliografía económica que ayude a interpretar los resultados, sin presentar asociaciones descriptivas como pruebas de mecanismos causales.
