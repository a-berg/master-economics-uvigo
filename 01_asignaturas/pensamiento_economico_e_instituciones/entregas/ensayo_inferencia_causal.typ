#import "@local/master-uvigo-templates:0.1.0": essay, font_sizes, uvigo-gray, base-styles
#import "@preview/cetz:0.5.2"
#import "figuras/bifurcaciones.typ": arbol-bifurcaciones

// TITLE PAGE
#let title-page(essay-title, author) = {
  set text(hyphenate: false)
  set par(first-line-indent: 0em)
  set align(center + horizon)
  set page(footer: none, header: none)
  title(essay-title)
  linebreak()
  text(size: font_sizes.LARGE)[Sus orígenes y evolución histórica hasta el presente]
  v(1.5em)
  text(size: font_sizes.LARGE, author)
  linebreak()
  v(1em)
  [
    #text(size: font_sizes.Large)[Universidade de Vigo] \
    #text(size: font_sizes.large, emph[Facultade de Ciencias Económicas e Empresariais])
  ]
  linebreak()
  v(1.1em)
  text(size: font_sizes.Large, datetime.today().display("[year]"))
}

#set text(font: "New Computer Modern")
#show: base-styles
#show: essay.with(
  author: "Adrián Berges Enfedaque",
  essay-title: [La Inferencia Causal en Economía],
  title-page: title-page,
  abstract: [
    Este ensayo examina la evolución de la inferencia causal en Economía
    desde la aportación de Haavelmo en los años cuarenta hasta los debates
    contemporáneos. El recorrido conecta los fundamentos probabilísticos
    y estructurales de la econometría con el programa de Cowles, sus críticas
    y la expansión de los diseños experimentales y cuasiexperimentales.
    Se examinan los problemas de identificación, estabilidad de las relaciones
    económicas y sensibilidad de los resultados que impulsaron distintas
    respuestas metodológicas durante los años setenta y ochenta. La revolución
    de la credibilidad se analiza como un cambio en las prioridades de la
    microeconomía aplicada, con mayor atención a los mecanismos de asignación
    y a la justificación de las comparaciones utilizadas para estimar efectos.
    Se sostiene que esta evolución combina avances técnicos con cambios
    en los criterios utilizados para justificar afirmaciones causales.
    Las controversias abrieron trayectorias que continúan coexistiendo:
    la identificación de efectos en contextos concretos, la explicación
    de mecanismos y la evaluación de escenarios alternativos. La comparación
    de estas trayectorias permite delimitar sus aportaciones y los supuestos
    necesarios para trasladar la evidencia a decisiones de política económica.
    También se examinan los resultados potenciales, los grafos causales y
    la incorporación del aprendizaje automático a la estimación.

    // Este ensayo examina la evolución de la inferencia causal en Economía
    // desde la aportación de Haavelmo en los años cuarenta hasta los debates
    // contemporáneos. El recorrido conecta los fundamentos probabilísticos
    // y estructurales de la econometría con el programa de Cowles, sus críticas
    // y la expansión de los diseños experimentales y cuasiexperimentales.
    // Se sostiene que esta evolución combina avances técnicos con cambios
    // en los criterios utilizados para justificar afirmaciones causales.
    // Las controversias abrieron trayectorias que continúan coexistiendo:
    // la identificación de efectos en contextos concretos, la explicación
    // de mecanismos y la evaluación de escenarios alternativos. La comparación
    // de estas trayectorias permite delimitar sus aportaciones y los supuestos
    // necesarios para trasladar la evidencia a decisiones de política económica.
    
  ],
)

#set page(
  header: context {
    h(1fr)
    set text(size: font_sizes.footnotesize, fill: uvigo-gray)
    emph[Pensamento Económico e Instituciones]
  },
  footer: context {
    set align(center)
    // set text(size: font_sizes.footnotesize)
    counter(page).display("1")
  },
)

#let do = math.op("do")

= Introducción

Preguntar por las consecuencias de aumentar el salario mínimo, introducir
un programa de formación o modificar una regla de política económica exige
comparar lo que sucede bajo una intervención con lo que habría sucedido
sin ella. Los datos observados no proporcionan directamente ambas situaciones.
La inferencia causal afronta este problema mediante supuestos y estrategias
que permiten interpretar determinadas comparaciones como evidencia sobre
los efectos de una intervención. Su importancia en Economía procede de
la necesidad de comprender decisiones e instituciones y de evaluar las
consecuencias de transformarlas.

Este ensayo estudia cómo se han diseñado, adoptado y justificado esas
estrategias en Economía desde los años cuarenta hasta los debates
contemporáneos. El punto de partida es la aportación de Haavelmo y su
relación con el programa econométrico de Cowles. El recorrido se concentra
en las controversias sobre identificación, estabilidad y diseño de
investigación, con especial atención al tránsito desde los sistemas
estructurales hacia la expansión de los métodos experimentales y
cuasiexperimentales en microeconomía aplicada. Se trata de una reconstrucción
selectiva, orientada a los cambios metodológicos y a sus bifurcaciones.

La tesis que organiza el trabajo es que la evolución de la inferencia causal
combina desarrollos técnicos con cambios en lo que los economistas consideran
una justificación convincente de sus afirmaciones. En el programa estructural,
esa justificación se articula mediante un modelo del funcionamiento económico
y restricciones que permiten identificar sus relaciones. Con el ascenso
de los diseños de investigación, adquiere mayor protagonismo la defensa
de la variación y de las comparaciones utilizadas para estimar efectos.
La identificación es central en ambas tradiciones; cambian la organización
de sus argumentos y el alcance de las preguntas que priorizan.

Las lecturas de Pearl, Panhans y Singleton, y Angrist y Pischke ofrecen
perspectivas distintas sobre este recorrido: una interpretación de Haavelmo
desde el cálculo causal, una reconstrucción histórica de la transformación
de la práctica empírica y una defensa de la revolución de la credibilidad
@pearl2015 @panhans_singleton2015 @angrist_pischke2010. El ensayo las contrasta
con contribuciones originales y críticas posteriores para desarrollar
su propia interpretación. Primero se presentan los fundamentos y la
consolidación del programa estructural; después, las críticas y respuestas
de los años setenta y ochenta y la expansión de los diseños causales.
Finalmente, se examina la convivencia de enfoques y la tensión entre
identificar efectos, explicar mecanismos y generalizar resultados.

La @fig-bifurcaciones sintetiza respuestas a problemas compartidos, sin
atribuir a cada método un origen exclusivo. El seguimiento de las ramas se
valora por campos: una práctica puede perder autoridad en uno y seguir activa
en otro. Las cajas discontinuas señalan prácticas cuestionadas o relegadas.

#figure(
  arbol-bifurcaciones(cetz),
  placement: auto,
  caption: [Bifurcaciones de la inferencia causal en Economía. Síntesis propia
    basada en @panhans_singleton2015 y @angrist_pischke2010, y en las
    aportaciones contemporáneas examinadas en el texto.],
) <fig-bifurcaciones>

= Haavelmo y los fundamentos de la inferencia causal econométrica

== Antecedentes y contexto intelectual

La publicación de _The Probability Approach in Econometrics_ en 1944 constituye
un punto de partida para estudiar la evolución de la inferencia causal en
Economía desde mediados del siglo XX. Su aportación se inscribe en un proyecto
anterior: conectar la teoría económica, la medición de los fenómenos económicos
y la inferencia estadística. Durante los años treinta, los trabajos de Ragnar
Frisch sobre los ciclos económicos y los modelos macroeconométricos de Jan
Tinbergen habían avanzado en la representación cuantitativa del funcionamiento
de la economía. La estimación de relaciones económicas debía permitir tanto
comprender sus mecanismos como evaluar los efectos de distintas políticas.
La reconstrucción histórica de Panhans y Singleton sitúa en este contexto las
aspiraciones del programa econométrico de la Cowles Commission, fundada en 1932
@panhans_singleton2015[pp. 9–11].

La relación entre Haavelmo y Cowles debe entenderse como parte de la formación
de ese programa. En el prefacio de su monografía, Haavelmo explica que la idea
del trabajo surgió durante su etapa como ayudante de Frisch en Oslo y que una
primera versión circuló en Harvard en 1941. También reconoce la influencia de
Abraham Wald en su tratamiento de la teoría estadística y las conversaciones
mantenidas con Jacob Marschak, director de investigación de Cowles. Por tanto,
aunque el texto se publicó durante la Segunda Guerra Mundial, sus antecedentes
remiten a la econometría de entreguerras y su influencia se proyectó sobre el
desarrollo de la disciplina en la posguerra @haavelmo1944[pp. v–vi].

== El fundamento probabilístico de la econometría

El problema que Haavelmo identifica al comienzo de su obra es la falta de un
fundamento coherente para contrastar las teorías económicas con los datos.
La práctica que cuestiona consistía en formular relaciones teóricas exactas
y juzgar después si se ajustaban suficientemente a las observaciones. Se
utilizaban herramientas estadísticas, como errores estándar y coeficientes de
correlación, sin aceptar siempre los modelos probabilísticos que daban sentido
a la inferencia. Para Haavelmo, esa separación era insostenible: una teoría
destinada a contrastarse estadísticamente debía formular hipótesis sobre la
distribución de las variables observables @haavelmo1944[pp. iii–iv].

Una dificultad procedía de la naturaleza de los datos económicos. Las
observaciones de una serie temporal no suelen ser independientes y las
condiciones en las que se producen pueden cambiar. Haavelmo sostiene que esto
no excluye por sí mismo el tratamiento probabilístico: es posible considerar
el conjunto de observaciones como una realización de variables sujetas a una
distribución conjunta. La propuesta permite incorporar la dependencia al modelo,
aunque su aplicación sigue requiriendo supuestos sobre esa distribución. De este
modo, la probabilidad proporciona un marco explícito para relacionar teoría y
evidencia, en lugar de limitarse a calificar informalmente las discrepancias
entre ambas @haavelmo1944[pp. iii–iv].

== Estructura, experimentos hipotéticos y autonomía

Ese fundamento estadístico no basta, sin embargo, para atribuir un significado
causal a cualquier relación estimada. Haavelmo vincula la interpretación
económica de los modelos con los experimentos reales o imaginables que
permitirían dar contenido a sus variables y relaciones. Al formular una ecuación
económica, el investigador debe precisar qué magnitudes representa y bajo qué
condiciones tendría sentido observar la relación propuesta @haavelmo1944[p. 6].

El problema puede ilustrarse con un mercado en el que la oferta y la demanda
determinan conjuntamente el precio y la cantidad intercambiada.
Los pares de precios y cantidades observados representan resultados del
funcionamiento conjunto de la oferta y la demanda.
Su relación estadística no permite, por sí sola, recuperar los parámetros de
ambas funciones estructurales.
Para identificar la respuesta de la demanda ante variaciones del precio es
necesario introducir restricciones sobre el sistema y disponer de variación que
permita distinguir los desplazamientos de la oferta de los de la demanda.
La interpretación depende del sistema que genera las observaciones y de las
restricciones que permiten distinguir sus relaciones.
Este ejemplo muestra por qué la simultaneidad ocupa un lugar central en el
programa econométrico asociado a Haavelmo y Cowles @panhans_singleton2015[pp.
10–11].

La noción de _autonomía_ permite profundizar en esta distinción. Una relación
puede describir con precisión los datos disponibles y dejar de hacerlo cuando
cambia otra parte del sistema. Haavelmo lo ilustra mediante un automóvil:
la relación entre la posición del acelerador y la velocidad puede resultar
útil en determinadas condiciones, pero depende de numerosos componentes del
vehículo y no revela por sí sola su funcionamiento. Las relaciones que describen
esos componentes pueden conservar su validez ante un conjunto más amplio de
modificaciones. La autonomía expresa, por tanto, una invariancia respecto de
ciertos cambios, sin suponer que toda relación estructural sea universalmente
inmutable @haavelmo1944[pp. 26–28]. El grado de autonomía de una relación debe
entenderse, por tanto, en referencia a las modificaciones del sistema frente a
las que se pretende conservar su validez.

Para el análisis económico de las intervenciones, esta idea plantea una
exigencia decisiva: establecer qué relaciones se modifican y cuáles pueden
mantenerse al alterar alguna condición del sistema. Pearl interpreta estas
aportaciones como antecedentes del cálculo causal contemporáneo @pearl2015.
Conviene distinguir esa reconstrucción retrospectiva de la formulación original:
el lenguaje de los experimentos hipotéticos y de la autonomía permite reconocer
una preocupación causal en Haavelmo sin atribuirle el formalismo posterior de
los grafos o del operador de intervención.

Sin embargo, la formulación probabilística y estructural no resolvía por sí
misma todos los problemas de la inferencia económica. La posibilidad de estimar
parámetros estructurales dependía de restricciones adicionales sobre el sistema,
cuya justificación no siempre podía obtenerse directamente de los datos. La
identificación se convertiría así en uno de los problemas centrales de la
econometría de posguerra, y la credibilidad de tales restricciones sería objeto
de controversias metodológicas posteriores.

= El paradigma estructural de posguerra

== La consolidación del programa de Cowles

Durante los años cuarenta y cincuenta, los fundamentos expuestos por Haavelmo
se integraron en un programa colectivo de investigación. La Cowles Commission,
establecida en Chicago entre 1939 y 1955, reunió a economistas y estadísticos
entre los que figuraban Jacob Marschak y Tjalling Koopmans. Su contribución
consistió en desarrollar métodos para identificar y estimar relaciones
económicas dentro de sistemas de ecuaciones simultáneas. La reconstrucción
histórica de Christ sitúa en esta etapa una transformación de los métodos y
de la práctica econométrica @christ1994.

El modelo estructural representaba la economía mediante relaciones de
comportamiento, restricciones técnicas e identidades contables. La distinción
entre variables endógenas, determinadas dentro del sistema, y variables
exógenas formaba parte de su especificación. Las ecuaciones debían describir
los mecanismos cuya interacción generaba las observaciones. De este modo,
la teoría intervenía en la interpretación de los parámetros y en la selección
de las restricciones necesarias para recuperarlos a partir de los datos
@panhans_singleton2015[pp. 9–11].

La construcción de modelos macroeconométricos para analizar políticas fue
una aplicación importante de esta perspectiva. Sin embargo, el programa
estructural no se define por el tamaño del modelo ni queda limitado a la
macroeconomía. Panhans y Singleton muestran también su continuidad en el
análisis microeconómico de decisiones individuales, mediante el estudio de
los rendimientos de la educación. Lo característico del enfoque es la
conexión explícita entre el mecanismo económico propuesto y la estrategia
de estimación @panhans_singleton2015.

== Identificación, estimación y evaluación de políticas

La distinción entre identificación y estimación resulta esencial para entender
este programa. La identificación plantea si la distribución de las variables
observables, junto con las restricciones del modelo, permite determinar de
manera única el parámetro de interés. La estimación utiliza una muestra para
atribuirle un valor. Si estructuras diferentes son compatibles con la misma
distribución observable y asignan valores distintos a ese parámetro, aumentar
el número de observaciones no resuelve por sí solo la indeterminación.
La cuestión debe abordarse mediante información o restricciones adicionales
sobre el sistema.

Podemos concretar esta distinción retomando el ejemplo de oferta y demanda.
Supongamos que una variable de costes desplaza la oferta y modifica el precio
de equilibrio. Para utilizar esa variación con el fin de identificar la
respuesta de la demanda, necesitamos justificar que la variable no afecta
directamente a esta última y que no está relacionada con sus perturbaciones
no observadas. También debe generar variación efectiva en el precio. Bajo
estos supuestos, y dentro de una especificación adecuada del mercado, los
desplazamientos de la oferta permiten distinguir la relación de demanda de
la simple asociación entre precios y cantidades de equilibrio. La exclusión
de la variable de costes de la ecuación de demanda expresa así una hipótesis
económica sustantiva, cuya validez no se deriva de que el modelo pueda estimarse.

// El ejemplo anterior es una ilustración expositiva del ensayo, no un caso
// empírico tomado de Christ o de Panhans y Singleton.

La simultaneidad condicionaba, además, la elección del procedimiento de
estimación. Cuando una variable explicativa se determina conjuntamente con
la variable dependiente, puede estar correlacionada con la perturbación de
la ecuación. En esas condiciones, aplicar mínimos cuadrados ordinarios a
cada relación por separado puede producir estimaciones inconsistentes.
El programa de Cowles desarrolló procedimientos que tenían en cuenta la
estructura probabilística del sistema, con un papel destacado de los métodos
de máxima verosimilitud @panhans_singleton2015[pp. 10–11]. La aportación
metodológica consistía en adecuar la estimación al mecanismo postulado;
su sofisticación estadística no sustituía la necesidad de identificarlo.

La evaluación de políticas añadía una exigencia distinta. Una vez estimado
el modelo, era posible modificar una condición o una regla y calcular sus
consecuencias sobre las variables endógenas. Pero la interpretación del
ejercicio dependía de que las relaciones mantenidas en la simulación
conservaran su validez bajo la intervención considerada. La autonomía
discutida por Haavelmo adquiría aquí un significado operativo: había que
explicitar qué partes del sistema podían cambiar y cuáles se suponían
estables @haavelmo1944[pp. 26–28].

== Alcance y tensiones del enfoque estructural

La principal ambición de este enfoque era vincular la evidencia con una
explicación del funcionamiento económico que permitiera analizar escenarios
alternativos. Su alcance excedía la predicción bajo las condiciones ya
observadas: aspiraba a estudiar las consecuencias de modificar esas
condiciones. Sin embargo, la capacidad de realizar tales ejercicios dependía
de la interpretación económica de las ecuaciones, de las restricciones de
identificación y de los supuestos de invariancia.

Desde la perspectiva de este ensayo, esa dependencia permite localizar una
tensión central del paradigma. Un buen ajuste a los datos no demuestra por
sí solo que la estructura postulada sea la adecuada para una intervención.
Algunas restricciones pueden tener implicaciones contrastables, pero la
evidencia no siempre permite discriminar entre todas las explicaciones
estructurales compatibles con las observaciones. La credibilidad del resultado
requiere, por ello, defender los supuestos que hacen posible su interpretación.

Esta tensión abre las controversias posteriores sobre cómo justificar las
restricciones y la estabilidad del modelo. Frente al programa estructural
se formularán críticas y alternativas que convivirán con su desarrollo.

= Crisis de la econometría tradicional

== Estabilidad e identificación en los modelos macroeconométricos

Durante los años setenta y ochenta, distintas críticas cuestionaron las
justificaciones utilizadas en la práctica econométrica. La expresión
_crisis de la econometría tradicional_ designa aquí esa convergencia de
objeciones, cuyos diagnósticos y propuestas no fueron uniformes. El problema
común era la distancia entre disponer de una estimación y poder defender
su interpretación económica. En particular, la estabilidad de las relaciones,
las restricciones de identificación y la sensibilidad a la especificación
pasaron a ocupar el centro de controversias con consecuencias diferentes
en macroeconomía y microeconomía aplicada @panhans_singleton2015.

La crítica de Lucas se dirigió a la evaluación de políticas mediante modelos
cuyos parámetros se suponían constantes al cambiar las reglas de actuación
de las autoridades. Si los agentes adaptan sus expectativas y decisiones a
esas reglas, las relaciones estimadas bajo un régimen pueden modificarse
cuando este cambia. La capacidad de describir o predecir dentro de un régimen
no garantiza, por tanto, la validez de una simulación de otro distinto.
El problema recupera la cuestión de la autonomía, pero hace explícito el
papel de las expectativas y de las decisiones ante la política económica
@lucas1976. Esta crítica favorecía la búsqueda de modelos que explicaran
esas respuestas; no constituía una defensa de abandonar la modelización
estructural en favor de los experimentos.

Sims cuestionó, por su parte, la credibilidad de las restricciones empleadas
para identificar los grandes modelos macroeconométricos. Que ciertas
variables quedaran excluidas de determinadas ecuaciones podía permitir su
estimación sin que existiera una justificación económica convincente para
tales exclusiones. Su propuesta de trabajar con sistemas de vectores
autorregresivos buscaba reducir esas restricciones previas al describir las
interdependencias dinámicas de las variables @sims1980. Sin embargo, describir
esas interdependencias tampoco identifica automáticamente perturbaciones
causales: atribuir significado económico a las innovaciones del sistema
requiere restricciones adicionales. La controversia desplazaba la discusión
hacia cuáles podían defenderse y para qué preguntas.

== Especificación, sensibilidad y transparencia

La objeción de Leamer incidía en las decisiones que median entre los datos
y los resultados publicados. La selección de variables, las formas
funcionales y otros supuestos pueden modificar las conclusiones, aunque
la presentación final de una regresión oculte el conjunto de alternativas
consideradas. La precisión estadística calculada dentro de una especificación
no recoge necesariamente la incertidumbre sobre la elección de esa
especificación @leamer1983.

Su respuesta consistía en examinar sistemáticamente la sensibilidad de los
resultados a cambios razonables en los supuestos. El investigador debía
mostrar qué conclusiones se mantenían y cuáles dependían de decisiones
discutibles. La propuesta apuntaba a hacer visible la fragilidad de la
inferencia, sin suponer que existiera una especificación única que los datos
pudieran seleccionar de manera automática @leamer1983. Para nuestro recorrido,
esta crítica resulta importante porque sitúa la credibilidad en la defensa
explícita de las decisiones de investigación, además de en las propiedades
formales de los estimadores.

== La evaluación de programas y la apertura de alternativas

En microeconomía aplicada, LaLonde introdujo una comparación especialmente
influyente. Partió de un programa de formación laboral evaluado mediante
asignación aleatoria y examinó si distintos procedimientos no experimentales,
utilizando grupos de comparación externos, recuperaban sus resultados.
Las discrepancias encontradas pusieron en cuestión la capacidad de esos
procedimientos para corregir la selección de los participantes en el contexto
estudiado @lalonde1986. El experimento proporcionaba una referencia empírica
con la que evaluar métodos cuya fiabilidad se había defendido, en gran medida,
mediante sus supuestos estadísticos.

El alcance del ejercicio debe delimitarse: no demuestra que toda investigación
observacional sea inválida ni que cualquier experimento esté libre de
problemas. Muestra que la elección del grupo de comparación y las condiciones
de participación pueden ser decisivas para interpretar una estimación.
Esta preocupación contribuiría a reforzar el interés por los mecanismos
de asignación y por las comparaciones capaces de aproximar un experimento
@angrist_pischke2010.

Las críticas abrieron, así, varias ramas metodológicas: modelos que incorporaban
las respuestas de los agentes a las reglas de política, sistemas dinámicos
con otras restricciones, análisis de sensibilidad y diseños experimentales
o cuasiexperimentales. Para este ensayo, la bifurcación relevante es la
pluralidad de respuestas ante el problema de justificar la inferencia.
La expansión posterior de los diseños cuasiexperimentales fue una de esas
trayectorias, especialmente influyente en determinadas áreas de la
microeconomía, y convivió con la continuidad del análisis estructural
@panhans_singleton2015.

= La revolución de la credibilidad

== El diseño de investigación como criterio de credibilidad

Angrist y Pischke utilizan la expresión _revolución de la credibilidad_ para
interpretar la transformación de la investigación empírica, especialmente
en microeconomía aplicada. Aunque reconocen la contribución de mejores datos
y avances econométricos, atribuyen un papel principal a la calidad de los
diseños de investigación. Su lectura del cambio destaca la búsqueda de
variación que permita sostener comparaciones causales convincentes
@angrist_pischke2010. Esta interpretación debe distinguirse de una descripción
neutral de toda la disciplina: constituye también una defensa de una manera
de hacer investigación.

La identificación ya ocupaba un lugar central en Cowles. El cambio radica en
la forma de organizar y justificar la investigación: adquieren protagonismo
las circunstancias concretas que generan la variación utilizada para estimar
un efecto. La pregunta por el mecanismo de asignación del tratamiento permite
examinar por qué unas unidades reciben una intervención y otras no, y bajo
qué condiciones estas últimas proporcionan un contrafactual adecuado.
La identificación sigue dependiendo de supuestos, pero su discusión se
vincula de forma explícita al contexto institucional y al diseño de la
comparación @panhans_singleton2015.

El lenguaje de los resultados potenciales ayuda a precisar el objeto de
interés: el efecto de un tratamiento compara el resultado de una unidad bajo
tratamiento con el que tendría sin él. Como ambos no se observan
simultáneamente, la estimación exige construir una comparación entre unidades
o situaciones. La aleatorización permite justificar esa comparación mediante
el mecanismo de asignación, mientras que los estudios observacionales
requieren argumentos adicionales @rubin1974. Su adopción en Economía forma
parte de una transformación que combina desarrollos estadísticos con nuevas
prácticas de investigación empírica.

== Experimentos y estrategias cuasiexperimentales

Las estrategias agrupadas en este movimiento no fueron inventadas todas
durante su expansión. Panhans y Singleton destacan su historia previa y su
difusión entre campos de investigación. La novedad histórica que interesa
aquí es el lugar que adquieren en la práctica de los economistas y en la
definición de una evidencia convincente @panhans_singleton2015.

En un experimento aleatorizado, la asignación busca hacer comparables los
grupos antes de la intervención; las pérdidas de seguimiento, el incumplimiento
y los efectos entre unidades pueden complicar su interpretación. Cuando la
asignación no es aleatoria, los diseños cuasiexperimentales recurren a rasgos
del entorno para justificar comparaciones específicas. Las variables
instrumentales utilizan una fuente de variación que afecta al tratamiento,
pero cuya influencia sobre el resultado debe operar por el canal postulado.
La discontinuidad en regresión aprovecha un umbral de asignación y requiere,
en su formulación habitual, continuidad de los resultados potenciales en ese
punto. Las diferencias en diferencias comparan cambios entre grupos y exigen
que, sin tratamiento, sus resultados hubieran seguido tendencias paralelas.
Cada estrategia debe defender sus propios supuestos; su nombre no constituye
por sí mismo una garantía de identificación @angrist_pischke2010.

El estudio de Card y Krueger sobre el salario mínimo ilustra la lógica de
estas comparaciones. Los autores analizaron el empleo en restaurantes de
comida rápida antes y después del aumento del salario mínimo de Nueva Jersey
en 1992, utilizando establecimientos de Pensilvania, donde no se produjo
el mismo cambio, como grupo de comparación. Su estudio no encontró la
reducción relativa del empleo que cabría esperar de una aplicación simple
del modelo competitivo @card_krueger1994.

Para la historia metodológica, lo relevante es la construcción del
contrafactual: el cambio del empleo en Pensilvania sirve como aproximación
al que se habría producido en Nueva Jersey sin la reforma. La interpretación
causal requiere defender esa comparación, considerar posibles perturbaciones
diferenciales y descartar que la intervención altere sustancialmente el grupo
de control. El resultado se refiere a una intervención, un sector y un
periodo concretos; su extrapolación exige argumentos adicionales. El ejemplo
muestra cómo el debate puede centrarse en la comparabilidad de los grupos
y en las condiciones de una política efectivamente observada.

== El efecto identificado y los límites de su alcance

La precisión sobre el efecto estimado constituye otra aportación central.
Imbens y Angrist muestran que, con un instrumento válido y bajo condiciones
como la relevancia, la exclusión, la independencia y la monotonicidad, es
posible identificar un efecto medio local del tratamiento para las unidades
cuya participación cambia al variar el instrumento. Ese efecto no coincide
necesariamente con el efecto medio para toda la población
@imbens_angrist1994. La heterogeneidad obliga, por tanto, a especificar a
quién se refiere la conclusión causal.

Esta delimitación puede interpretarse como una ganancia de claridad: el
investigador explicita qué comparación respaldan sus datos y supuestos.
También plantea una dificultad cuando la pregunta de política se refiere
a otra población, a una intervención distinta o a su aplicación a mayor
escala. Identificar un efecto en el contexto estudiado y justificar su
generalización son problemas relacionados, pero diferentes. Asimismo,
conocer el efecto de una intervención no equivale necesariamente a explicar
todos los mecanismos que lo producen @deaton2010.

La revolución de la credibilidad reordenó prioridades en una parte de la
Economía empírica. La discusión contemporánea se abre en torno a cómo combinar
la defensa de comparaciones concretas con la explicación de mecanismos y
el análisis de políticas que exceden la variación observada.

= La bifurcación contemporánea

== Ramas relegadas y continuidad por campos

Las controversias alteraron la posición de ciertas prácticas sin producir
un abandono general de la econometría estructural. En macroeconomía, las
críticas de Lucas y Sims debilitaron la pretensión de evaluar cambios de
política mediante grandes sistemas cuyas restricciones e invariancia se
daban por suficientemente justificadas. La rama relegada fue esa manera
de defender su interpretación causal; las respuestas incluyeron modelos
que explicaban expectativas y decisiones, y sistemas de series temporales
con otras estrategias de identificación @lucas1976 @sims1980.

En microeconomía aplicada, Panhans y Singleton describen el desplazamiento
relativo desde modelos estructurales hacia un repertorio de diseños
cuasiexperimentales. Su penetración fue desigual entre campos, revistas y
departamentos: ganó especial influencia en trabajo, educación, salud y
economía pública, mientras que el análisis estructural conservó una posición
central en organización industrial @panhans_singleton2015[pp. 17–18].
La búsqueda de mecanismos y escenarios contrafactuales quedó menos visible
en parte de la investigación centrada en efectos de tratamiento, pero
continuó desarrollándose en otras áreas @nevo_whinston2010.

También conviene distinguir la pérdida de protagonismo de una propuesta
de su incorporación a otras prácticas. Angrist y Pischke reconocen el
papel del análisis de sensibilidad de Leamer, aunque atribuyen el cambio
principal a los diseños de investigación @angrist_pischke2010. La sensibilidad
persistió como una exigencia que puede acompañar distintas estrategias.
Por ello, las ramas oscurecidas de este recorrido son relativas al campo
y al criterio de credibilidad considerado; calificarlas de abandonadas
exigiría evidencia adicional de su desaparición.

== Diseños, mecanismos y alcance de las preguntas

La expansión de los diseños experimentales y cuasiexperimentales no eliminó
el análisis estructural. El debate contemporáneo puede entenderse como una
discusión sobre el alcance de las preguntas que cada estrategia permite
responder y sobre los supuestos necesarios para hacerlo. La bifurcación
designa aquí trayectorias de investigación que conviven y pueden combinarse,
aunque asignan prioridades diferentes a la identificación de efectos en
contextos observados y a la construcción de modelos para estudiar escenarios
alternativos.

El intercambio de 2010 en torno a la revolución de la credibilidad permite
situar esta controversia. Frente a la valoración de Angrist y Pischke,
Nevo y Whinston defienden que el análisis estructural también había mejorado
gracias a los avances en datos, métodos y capacidad de cálculo. Desde la
organización industrial, subrayan la utilidad de modelos basados en decisiones
económicas para responder preguntas que exceden la comparación directamente
disponible en los datos @nevo_whinston2010. La discusión afecta, por tanto,
a qué evidencia resulta suficiente para una pregunta de política y qué
modelización adicional requiere.

Como ilustración de esta diferencia, estimar el efecto de una intervención
ya realizada y anticipar las consecuencias de una reforma todavía no
observada pueden exigir información distinta. Una comparación convincente
puede identificar el efecto de la primera; estudiar la segunda puede
requerir hipótesis sobre decisiones, restricciones e interacciones entre
agentes. La extrapolación amplía el alcance del análisis, pero hace necesario
justificar los componentes del modelo que no quedan determinados por la
variación observada. A su vez, la evidencia experimental o cuasiexperimental
puede servir para contrastar mecanismos y disciplinar esos componentes.

Deaton cuestiona que la aleatorización o el uso de instrumentos otorguen
por sí mismos una superioridad general al conocimiento obtenido. Su crítica
incide en la heterogeneidad, en la pertinencia del efecto identificado para
las decisiones de política y en la necesidad de comprender mecanismos
@deaton2010. En términos de este ensayo, la tensión se encuentra entre
justificar una comparación en su contexto y explicar qué permite trasladar
sus resultados a otras poblaciones o intervenciones. Las dos exigencias
forman parte de la inferencia causal, aunque no se resuelven mediante un
único procedimiento.

== Resultados potenciales y modelos gráficos causales

Otro debate se refiere al lenguaje utilizado para formular los problemas
causales. Conviene distinguirlo de la controversia anterior: la comparación
entre resultados potenciales y modelos gráficos no equivale a la oposición
entre diseños de investigación y modelos económicos estructurales. Un modelo
de decisiones puede definir resultados potenciales, mientras que un grafo
puede representar los supuestos de una comparación experimental.

El enfoque de resultados potenciales permite precisar el efecto de interés
mediante la comparación de resultados bajo tratamientos alternativos y
formular condiciones sobre su asignación. Los modelos gráficos hacen
explícitas hipótesis sobre las relaciones causales entre variables y permiten
examinar qué ajustes o información adicional bastan para identificar una
intervención. Ambos requieren conocimiento sustantivo: ni los resultados
potenciales ni las flechas de un grafo se justifican únicamente a partir
de asociaciones observadas.

La interpretación de Pearl conecta el lenguaje de las intervenciones con
la preocupación de Haavelmo por las relaciones autónomas. En un modelo
causal estructural, intervenir puede representarse mediante la sustitución
de la ecuación de una variable, manteniendo las relaciones restantes bajo
los supuestos correspondientes @pearl2015. Este vínculo ofrece una lectura
de continuidad histórica, aunque el formalismo posterior no debe atribuirse
sin más a la econometría de los años cuarenta.

Imbens compara ambos enfoques atendiendo a su utilidad para la práctica
económica y explica por qué buena parte de esta se aproxima al lenguaje
de los resultados potenciales @imbens2020. La elección del marco debe
considerar qué pregunta se formula y qué supuestos permite expresar con
claridad. En particular, un grafo acíclico exige cuidado cuando se pretende
representar relaciones simultáneas de equilibrio, características de muchos
modelos económicos. Esta dificultad ayuda a entender que la adopción de
los lenguajes causales depende también de los problemas de cada disciplina.

== Nuevos datos y revisión de los diseños en los años 2020

La revisión de las diferencias en diferencias muestra que la exigencia
de credibilidad también transforma los métodos cuasiexperimentales ya
establecidos. Cuando las unidades reciben una política en fechas distintas
y los efectos varían entre grupos o a lo largo del tiempo, una regresión
convencional puede combinar comparaciones cuyo significado causal no
coincide con el efecto que se pretende estimar. El problema obliga a
precisar quién se compara con quién y qué efectos se agregan.

Callaway y Sant'Anna proponen identificar efectos por grupo y periodo
en contextos de adopción escalonada, con supuestos explícitos sobre tendencias
paralelas y distintas formas de agregación @callaway_santanna2021. Borusyak,
Jaravel y Spiess desarrollan una revisión de los estudios de eventos que
aborda la heterogeneidad y propone un estimador basado en imputar resultados
sin tratamiento @borusyak_et_al2024. Su aplicación a la respuesta del consumo
ante devoluciones fiscales estadounidenses conecta el refinamiento del
diseño con preguntas económicas sustantivas. Estas aportaciones prolongan
el debate sobre credibilidad hasta los años 2020: adoptar una técnica
reconocida no sustituye la justificación de las comparaciones que realiza.

La transformación metodológica continúa con la disponibilidad de registros
administrativos y nuevas capacidades de procesamiento. Currie, Kleven y
Zwiers relacionan la evolución de la investigación económica con la
interacción entre datos y métodos, y destacan una tendencia hacia mayor
credibilidad, transparencia y combinación de evidencias
@currie_kleven_zwiers2020. Estos cambios amplían las posibilidades empíricas,
sin resolver automáticamente qué variación permite identificar un efecto.

El aprendizaje automático ofrece un ejemplo de esa complementariedad.
Chernozhukov y sus coautores desarrollan procedimientos que utilizan métodos
flexibles para estimar componentes auxiliares, como regresiones condicionales,
y limitan el impacto de sus errores sobre la estimación del parámetro de
interés. La construcción combina condiciones de ortogonalidad y separación
de muestras para abordar problemas de regularización y sobreajuste
@chernozhukov_et_al2018. Su aplicación a efectos de tratamiento o parámetros
estructurales sigue requiriendo los supuestos que identifican esos objetos.
La capacidad predictiva de un algoritmo no demuestra, por sí sola, que
una comparación tenga interpretación causal.

= Conclusiones

El recorrido permite sostener que la evolución de la inferencia causal
en Economía ha transformado tanto las herramientas disponibles como la
manera de justificar sus resultados. Haavelmo articuló un fundamento
probabilístico para la inferencia y una preocupación por el significado
y la autonomía de las relaciones económicas. El programa de Cowles
desarrolló esas aportaciones mediante la identificación y estimación
de sistemas estructurales. La posibilidad de evaluar políticas dependía
de las restricciones del modelo y de la validez de las relaciones
que se suponían estables ante la intervención considerada.

Las controversias posteriores hicieron visibles distintas dificultades
de esa práctica. Lucas cuestionó la estabilidad de las relaciones ante
cambios en las reglas de política; Sims, las restricciones de identificación
de los modelos macroeconométricos; Leamer, la fragilidad de las conclusiones
ante decisiones de especificación. En evaluación de programas, LaLonde
mostró la importancia de examinar empíricamente la capacidad de las
comparaciones no experimentales para recuperar un resultado de referencia.
Estas críticas abrieron respuestas diferentes y permiten entender la
historia como un conjunto de bifurcaciones, en lugar de una sucesión
de paradigmas que desaparecen al surgir el siguiente.

La revolución de la credibilidad reforzó la atención a los mecanismos
de asignación y a la procedencia de la variación utilizada para identificar
efectos, especialmente en microeconomía aplicada. Su aportación fue hacer
más explícita la defensa de comparaciones concretas y delimitar qué efecto
respaldaban los datos y supuestos. La cuestión causal continuó exigiendo
hipótesis sobre la economía: los experimentos y cuasiexperimentos tienen
condiciones de validez, y sus resultados pueden referirse a poblaciones,
intervenciones y contextos específicos.

El análisis estructural mantuvo su relevancia para explicar mecanismos
y estudiar escenarios que exceden la variación observada. La coexistencia
de enfoques obliga a distinguir la credibilidad de un efecto en su contexto
de la justificación necesaria para trasladarlo a otra política o población.
Asimismo, el debate entre resultados potenciales y grafos causales se refiere
a cómo expresar los supuestos y preguntas, sin reproducir exactamente
la división entre diseños y modelos económicos. Los nuevos datos y el
aprendizaje automático amplían las posibilidades de estimación dentro
de estrategias cuya identificación sigue requiriendo argumentos sustantivos.

El árbol histórico muestra además que la pérdida de protagonismo fue
selectiva. Se cuestionaron prácticas de identificación e invariancia de
los modelos tradicionales y el análisis estructural quedó en segundo plano
en parte de la microeconomía aplicada, mientras conservó fuerza en otros
campos. Las revisiones de los diseños con adopción escalonada en los años
2020 confirman que las ramas más influyentes también están sujetas a
revisión. El seguimiento mayoritario de una estrategia en un campo no
garantiza la validez de cada aplicación.

La posición que se deriva de este ensayo es que la elección metodológica
debe atender a la pregunta y al alcance de la conclusión pretendida.
Una afirmación causal convincente necesita precisar el efecto de interés,
la evidencia que lo identifica y los supuestos que permiten interpretarlo;
una recomendación de política requiere, además, justificar su pertinencia
para la intervención propuesta. La complementariedad entre diseños y
modelos resulta valiosa cuando permite contrastar mecanismos y explicitar
los pasos de la extrapolación. Desde Haavelmo hasta los debates contemporáneos,
la conexión entre teoría, evidencia e intervención permanece como el
problema central, mientras evolucionan las formas de construirla y evaluarla.

#pagebreak()
#bibliography("fuentes.bib", style: "harvard-cite-them-right")
