# Recuperación de precios históricos de supermercado

**Actualización del 7 de noviembre de 2026:** se han cargado 222 precios de 74 referencias en la copia revisada del Excel. Catorce valores se apoyan en las fuentes recuperadas (incluida una referencia equivalente de zanahoria), uno arrastra una fuente anterior y 207 conservan el precio base como estimación sin cambios. La hoja `Fuentes precios` distingue el origen de cada semana y enlaza las fuentes. La investigación del 2 de noviembre que figura a continuación se conserva como registro de búsqueda.

Consulta: 2 de noviembre de 2026. Semanas del ejercicio: 12–18/10, 19–25/10 y 26/10–01/11/2026.

## Resultado de la investigación

Existen fuentes que permiten recuperar parte de los precios. No se ha completado la hoja de cálculo: cada dato requiere comprobar la coincidencia de producto, marca, formato, unidad y ámbito geográfico. Un precio de tienda online obtenido de un tercero debe identificarse como tal, no como una visita propia al supermercado.

### Mercadona: MercaIndex

- Página de datos: https://www.mercaindex.es/datos
- Catálogo: https://www.mercaindex.es/productos
- La web anuncia seguimiento semanal de precios y 19 meses de datos. Se ha verificado en el navegador que la ficha individual de pimiento rojo presenta un gráfico interactivo con observaciones fechadas, también de octubre de 2026.
- Ejemplo comprobado: https://www.mercaindex.es/productos/69310

| Producto de la fuente | Fecha del punto del gráfico | Precio de referencia | Correspondencia candidata |
| --- | --- | --- | --- |
| Pimiento rojo, producto 69310, EAN 2105470693108 | 14/10/2026 | 2,900 €/kg | Fila 35 de Mis Gastos |
| Pimiento rojo, producto 69310, EAN 2105470693108 | 21/10/2026 | 2,900 €/kg | Fila 35 de Mis Gastos |

También se consultó el punto del 07/10/2026, fuera del seguimiento solicitado, que muestra 2,900 €/kg. No se ha verificado un punto de la tercera semana. Los valores se leyeron en las ayudas emergentes del gráfico de precio por kilo. El precio por pieza cambia además con el peso de referencia: no debe confundirse con €/kg.

El acceso por descarga directa y por el extractor web falló en la ficha individual, pero la consulta ordinaria en el navegador funcionó sin iniciar sesión. No se ha confirmado una descarga masiva pública ni se ha extraído el histórico completo del catálogo. La cobertura geográfica del histórico requiere una comprobación adicional antes de equipararlo con la tienda física concreta del ejercicio.

### Mercadona: CestaHoy

- Sitio: https://cestahoy.com/
- Ejemplo comprobado: https://cestahoy.com/producto/chocolate-negro-72-cacao-hacendado-con-almendras-enteras-tableta-29062/
- La ficha identifica chocolate negro 72 % de cacao Hacendado con almendras enteras, tableta de 200 g, EAN 8480000290625. Es una correspondencia candidata con la fila 30, cuya descripción abreviada es NEGRO 72% ALMENDRAS Mercadona.
- La página indica precio de 2,65 € el 26/10/2026, una variación desde el inicio de seguimiento y estas entradas en el historial: 22/09/2026, 2,75 €; 28/09/2026, 2,65 €.
- La observación del 26/10 cae en la tercera semana. Extender 2,65 € a fechas intermedias de octubre sería una reconstrucción basada en el registro de cambios publicado, no tres observaciones independientes recogidas en tienda. Debe explicarse así.
- La fuente declara que usa el catálogo online de Mercadona para península y Baleares y que es independiente del supermercado. No se ha contrastado cada precio del historial con un ticket u otra fuente.

### Mercadona: otras fuentes localizadas

**Compráctica** — https://compractica.es/

Anuncia precios e historial diario por producto. La portada se pudo consultar, pero no se consiguió verificar una ficha histórica concreta de los productos de esta cesta. Es una fuente candidata, no una cobertura histórica ya acreditada para el trabajo.

**PreciosDelSuper** — https://www.preciosdelsuper.es/producto/bocaditos-de-queso-y-chile-hot-cheese-hacendado-ultracongelados

El resultado del buscador muestra una ficha de Hot Cheese con seguimiento desde junio y un apartado de evolución. La ficha no se pudo abrir de forma verificable. El precio de junio no acredita el de octubre. No se propone introducirlo en el Excel.

**tuTándem** — https://tutandem.es/datos

Publica enlaces a CSV diarios desde octubre de 2026 para varias cadenas, incluida Mercadona. La propia documentación especifica que son medianas de precios por kilo, litro o unidad de 26 categorías básicas, no el precio de cada marca y referencia. Por ello, no sustituyen directamente los precios de los artículos concretos del IPC personal. La descarga directa del CSV devolvió 403 y no se inspeccionaron sus filas. No se ha confirmado cobertura de todas las fechas requeridas. Puede servir como contraste agregado.

### Froiz: folleto oficial fechado

- Página de folletos: https://froiz.es/folleto/
- PDF oficial: https://froiz.es/wp-content/uploads/2026/10/2026.10.15-SUPER-Galicia-LINKS.pdf
- Se descargó el PDF y se verificó su portada: **del 15 de octubre al 2 de noviembre de 2026**. Tiene 20 páginas; el archivo se identifica como Súper Galicia. La copia consultada contiene precios y condiciones de promociones.
- El intervalo se solapa con las tres semanas del ejercicio: 15–18/10 en la primera, toda la segunda y toda la tercera. No acredita los días 12–14 de octubre. Un precio anunciado puede documentar una fecha comprendida en su vigencia si el establecimiento y el producto coinciden y se cumplen las condiciones de la oferta.
- Se debe distinguir Súper, Hiper y Cash, y evitar las promociones de Froiz Portugal para un estudio de precios españoles. También hay que comprobar las ofertas limitadas a centros con una sección determinada y las promociones por compra múltiple.
- El folleto no contiene todo el catálogo y no demuestra que otros artículos mantuviesen su precio.

También se localizaron estas ediciones semanales en archivos de terceros:

| Semana | Fuente localizada | Comprobación realizada |
| --- | --- | --- |
| 12–18/10/2026 | https://www.kimbino.es/ciudad/sarria/froiz/ y https://g.precio24.es/froiz | Listado de edición con fechas; sin transcribir precios de las imágenes |
| 19–25/10/2026 | https://www.ofertero.es/froiz/froiz-oferta-semanal-desde-lunes-19-10-2026-98097/ | Página con intervalo de vigencia y páginas del folleto; imágenes no verificadas |
| 26/10–01/11/2026 | https://www.ofertero.es/froiz/froiz-oferta-semanal-desde-lunes-26-10-2026-98352/ | Página con intervalo de vigencia; sin transcribir precios de imágenes |

No se ha localizado y verificado una base pública completa de precios semanales de Froiz. Estos archivos son vías para recuperar precios de productos promocionados, no una serie completa de todos sus artículos.

## Cómo utilizar los datos sin perder la trazabilidad

1. Mantener la cesta y las cantidades base. Un producto Mercadona no se sustituye por uno Froiz solo por ser de la misma categoría. Si es necesario sustituirlo, registrar la decisión y revisar la comparabilidad.
2. Para cada producto y semana, registrar precio, unidad, fecha efectiva del dato, tienda/zona, marca y formato, URL o identificador de ticket, y modo de obtención.
3. Separar **ticket propio**, **ticket u observación documentada de un compañero**, **precio anunciado en folleto**, **histórico online de tercero** e **imputación**. La fecha de consulta no sustituye a la fecha del precio.
4. No llamar promedio semanal a un precio de un solo día. Escoger una regla de observación semanal y documentarla. Las series con fechas diferentes deben conservar esa diferencia.
5. Conservar una copia fechada de las evidencias, pues las páginas y los folletos actuales se reemplazan.

## Si quedan huecos

Pedir tickets o fotografías fechadas a compañeros es una vía válida para recuperar observaciones. Hay que comprobar que coincidan artículo, formato, fecha, zona y condiciones de compra. El recuerdo de un precio sin justificante debe identificarse como recuerdo, con menor capacidad de verificación.

Si un precio no se recupera, se puede proponer al profesor una imputación explícita, por ejemplo mantener el último precio observado. Esa regla supone estabilidad: no demuestra que la hubiera y puede reducir artificialmente la variación del índice. Otra opción es trabajar con una cesta reducida de cobertura suficiente, manteniéndola idéntica en todas las semanas y recalculando la base y las ponderaciones. Debe informarse de qué proporción del gasto queda cubierta.

Crear variaciones arbitrarias y presentarlas como precios recogidos impediría verificar los resultados. Una reconstrucción documentada, con las imputaciones identificadas, permite conservar el valor del ejercicio y explicar su limitación.

## Siguiente paso recomendado

Empezar por las referencias Mercadona de mayor peso y sus fichas históricas. Para Froiz, contrastar la lista concreta con el folleto oficial y con tickets de las semanas correspondientes. Antes de rellenar huecos por hipótesis, acordar el criterio de tratamiento de ausencias con el profesor. El Excel permanece sin nuevos precios tras esta investigación.
