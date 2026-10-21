"""Exporta tablas para Typst y un balance de resultados, sin inventar datos faltantes."""
import csv,json,hashlib
from pathlib import Path
import polars as pl

def build(root):
    gold=root/'datos/gold';d=pl.read_csv(gold/'growth_accounting.csv')
    headline={}
    for country,key in [('CHN','china'),('ESP','espana')]:
        r=d.filter((pl.col('country')==country)&(pl.col('start')==1990)&(pl.col('end')==2023)).row(0,named=True)
        headline[key]={'gdp':f"{r['gdp_cagr_pct']:.2f}".replace('.',','),'gdp_pc':f"{r['gdp_pc_cagr_pct']:.2f}".replace('.',',')}
    (gold/'headline.json').write_text(json.dumps(headline,ensure_ascii=False,indent=2)+'\n')
    table=[]
    for r in d.iter_rows(named=True):
        table.append(dict(pais='China' if r['country']=='CHN' else 'España',periodo=f"{r['start']}–{r['end']}",
             pib=f"{r['gdp_cagr_pct']:.2f}",pib_pc=f"{r['gdp_pc_cagr_pct']:.2f}",capital=f"{r['capital_contribution_pp']:.2f}",trabajo=f"{r['labor_contribution_pp']:.2f}",residuo=f"{r['solow_residual_pp']:.2f}"))
    pl.DataFrame(table).write_csv(gold/'growth_table_typst.csv')
    panel=pl.read_csv(gold/'comparison.csv')
    summary=[]
    for country in ['CHN','ESP']:
        for year in [1990,2008,2019,2023]:
            p=panel.filter((pl.col('country')==country)&(pl.col('year')==year))
            if not p.height:continue
            r=p.row(0,named=True);summary.append(dict(country=country,year=year,gdp_ppp_per_capita=r['gdp_ppp_per_capita'],household_share_pct=100*r['share_c'],investment_share_pct=100*r['share_i']))
    (gold/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    provenance=dict(config=json.loads((root/'datos/catalogo/analysis_config.json').read_text()),
       inputs=[json.loads(p.read_text()) for p in sorted((root/'datos/bronze').glob('*/latest.json'))],
       formulas=dict(growth='100*(x_t/x_tminus1-1), only consecutive positive observations',
          growth_accounting='gY=alpha*gK+(1-alpha)*gL+gA; gX=100*ln(X_end/X_start)/(end-start)',
          cagr='100*((X_end/X_start)**(1/(end-start))-1)',
          labor='PWT emp in millions; total hours=emp*avh; WDI modeled unemployed=active*u/100',
          shares='PWT NA current national-price component / current national-price GDP'),
       output_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(gold.glob('*.csv'))})
    (gold/'lineage.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
    req=json.loads((gold/'requirements_status.json').read_text())
    for r in req:
        if r['id']=='6.kuznets':r['status']='generated_observed_pairs_interpretation_pending'
        if r['id']=='4.demography':r['status']='wdi_downloaded_definition_validation_pending'
        if r['id']=='4.labor':r['status']='modeled_labor_derived_not_survey'
        if r['id']=='3.prices':r['status']='inflation_generated_other_statistics_pending'
    (gold/'requirements_status.json').write_text(json.dumps(req,ensure_ascii=False,indent=2)+'\n')
    blocked=['# Estado de requisitos del informe','',
      'Este proyecto genera una primera base analítica. No equivale al informe final ni a la reproducción completa de los ejercicios.','',
      '## Pendientes sustantivos','',
      '- China: localizar y validar producción total, consumos intermedios, remuneración de asalariados y rentas factoriales en cuentas nacionales. No sustituir la participación laboral ajustada de PWT por remuneración de asalariados.','- Obtener tablas input-output de ambos países y agregarlas en tres sectores. Para China se priorizan alternativas internacionales; NBS (anuario 2025, tablas 3-21 y 3-22, año 2023) queda como último recurso. Revisar también el origen nacional de las alternativas.','- Validar CCF real y existencias. PWT publica depreciación y consumo de capital corriente por activo, pero no se convierte automáticamente con el deflactor del PIB. Eurostat no entrega observaciones para la selección de existencias encadenadas probada.','- Obtener paro registrado de España desde SEPE y decidir una medida nacional de encuesta comparable para China. Los datos OIT modelizados están claramente identificados.','- Completar los gráficos y estadísticos de oferta, rentas, salarios reales y mercado laboral exigidos.','- Añadir a las tablas de crecimiento las referencias históricas de países de la clase, si son exigidas, sin mezclar silenciosamente sus períodos con 1990–2023.','- Revisar interpretación económica, bibliografía temática, conclusiones y exposición oral.','',
      '## Cobertura por requisito','']
    blocked.extend(f"- {r['id']} — {r['title']}: {r['status']}" for r in req)
    (root/'PENDIENTES.md').write_text('\n'.join(blocked)+'\n')
    # Apéndice generado: las cifras proceden de gold; referencias y unidades explícitas.
    lines=['= Apéndice de tablas y gráficos','',
      'Las tablas y figuras de este apéndice constituyen una selección inicial. El catálogo de requisitos identifica las restantes. Fuente: elaboración propia a partir de PWT 11.0 y WDI; consulta de las descargas en los manifiestos bronze.','',
      '#figure(table(columns: (auto, auto, 1fr, 1fr), table.header([País], [Período], [PIB], [PIB por habitante]),']
    for r in table:lines.append(f"[{r['pais']}], [{r['periodo']}], [{r['pib']}], [{r['pib_pc']}],")
    lines.extend(['), caption: [Crecimiento anual compuesto (%). Base PWT, precios nacionales constantes.]) <tabla-crecimiento>','',
       '#figure(table(columns: (auto, auto, 1fr, 1fr, 1fr), table.header([País], [Período], [Capital], [Trabajo], [Residuo]),'])
    for r in table:lines.append(f"[{r['pais']}], [{r['periodo']}], [{r['capital']}], [{r['trabajo']}], [{r['residuo']}],")
    lines.extend(['), caption: [Contabilidad del crecimiento. Contribuciones logarítmicas anualizadas en puntos porcentuales; α = 1/3. El residuo recoge todo lo no explicado por capital y empleo.]) <tabla-contabilidad>',''])
    figs=[('gdp_pc','PIB real por habitante. PWT, PIB por el lado del gasto a PPA encadenadas, dólares internacionales de 2021.'),
       ('growth','Crecimiento del PIB real. PWT, tasas anuales sobre rgdpna.'),
       ('demand_shares_CHN','China. Componentes de demanda a precios corrientes como porcentaje del PIB. C: hogares; I: inversión; G: consumo público; X: exportaciones; M: importaciones. Las importaciones se restan en la identidad del PIB.'),
       ('demand_shares_ESP','España. Componentes de demanda a precios corrientes. Base común PWT NA.'),
       ('demand_2008_CHN','China. Demanda real normalizada a 2008 = 100. PWT NA, precios nacionales constantes de 2021.'),
       ('demand_2008_ESP','España. Demanda real normalizada a 2008 = 100. PWT NA, precios nacionales constantes de 2021.'),
       ('productivity','PIB real por ocupado. PWT rgdpna/emp; valores a precios nacionales constantes, no interpretar como comparación directa de bienestar.'),
       ('capital','Capital real por ocupado. PWT rnna/emp.'),('hours','Horas anuales por ocupado. PWT avh; no confundir con horas totales.'),
       ('labor_share','Participación laboral ajustada de PWT; no equivale a remuneración de asalariados dividida por PIB.'),
       ('inflation','Inflación del IPC nacional. WDI, variación anual del índice; se conservan las bases originales.'),
       ('unemployment','Desempleo modelizado OIT publicado por WDI. No es paro registrado ni encuesta nacional directa.'),
       ('participation','Actividad de mayores de 15 años, derivada con población activa y población total menos 0–14 de WDI. Validación de universos pendiente.'),
       ('kuznets','PIB por habitante a PPA constante e índice de Gini, WDI. Solo pares observados. El gráfico no identifica una relación causal ni prueba la hipótesis de Kuznets.')]
    for i,(name,caption) in enumerate(figs):
        if i%2==0:lines.append('#pagebreak()')
        lines.extend([f'#figure(image("../output/figuras/{name}.svg", width: 92%), caption: [{caption}]) <fig-{name.replace("_","-")}>',''])
    (root/'entregas/apendice_generado.typ').write_text('\n'.join(lines)+'\n')
