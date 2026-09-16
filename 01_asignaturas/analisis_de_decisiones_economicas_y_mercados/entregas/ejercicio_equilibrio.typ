#import "@local/homework_template:0.1.0": *
#import "@preview/lilaq:0.6.0" as lq

#show: homework_econ.with(
  course: [Análisis de Decisiones Económicas y Mercados],
  title: [Calculando el equilibrio de mercado],
  pdf_title: "AnDec_entrega_2b",
)

#show: lq.set-diagram(
  xlabel: $p$,
  ylabel: $Q$,
  legend: (position: top + left),
)

#let x = lq.linspace(0, 10)

#let demandA = p => calc.max(0, 12 - 2*p)
#let demandB = p => calc.max(0, 21 - p)
#let supplyJ = p => calc.max(0, 5*p - 1)
#let supplyK = p => calc.max(0, p - 2)

#lq.diagram(
  title: [Curvas de oferta y demanda],
  width: 100%,
  lq.plot(x, demandA, mark: none, label: $q^A (p)$),
  lq.plot(x, demandB, mark: none, label: $q^B (p)$),
  lq.plot(x, p => demandA(p)+demandB(p), mark: none, label: $D (p)$),
  lq.plot(x, supplyJ, mark: none, label: $q^J (p)$),
  lq.plot(x, supplyK, mark: none, label: $q^K (p)$),
  lq.plot(x, p => supplyJ(p) + supplyK(p), mark: none, label: $S (p)$),
  lq.hlines(21, max: 4, stroke: (paint: luma(100), thickness: 0.75pt, dash: "dashed")),
  lq.vlines(4, max: 21, stroke: (paint: luma(100), thickness: 0.75pt, dash: "dashed")),
  lq.scatter((4,), (21,), size: 5pt, color: black),
)

#set enum(numbering: "a)")

+ *Precio de equilibrio:* debemos calcular $D(p^*) = S(p^*)$. Por inspección
  visual, $2 < p^* < 6$, por lo que usaremos los correspondientes tramos de
  dichas funciones:
  $
    33 - 3p^* &= 6p^* - 3\
    36 &= 9p^* \
    4 &= p^*.
  $
+ *Cantidades agregadas de equilibrio:* Basta con sustituir $p^*$ en alguna de
  las dos funciones, dando como resultado $Q^*=21$.
+ *Número de unidades que adquiere cada demandante:* Nuevamente, sustituimos $p^*$
  en cada una de las funciones de demanda individuales, obteniendo:
  $
    q^A (p^*) = 17\
    q^B (p^*) = 4.
  $
+ *Número de unidades que produce cada oferente:* Al igual que antes,
  sustituimos $p^*$ en cada una de las funciones de oferta, obteniendo:
  $
    q^J (p^*) = 19\
    q^K (p^*) = 2.
  $
