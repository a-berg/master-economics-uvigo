"""Plan de carga: fuentes verificadas y conservación explícita del precio base."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'entregas/ipc'
data=json.loads((DATA/'datos_ipc.json').read_text())
items=[i for i in data['items'] if any(t in i['name'].lower() for t in ('mercadona','froiz'))]
assert len(items)==74
root='https://cestahoy.com/producto/'
choc=root+'chocolate-negro-72-cacao-hacendado-con-almendras-enteras-tableta-29062/'
cottage=root+'queso-fresco-crema-estilo-cottage-hacendado-tarrina-17461/'
greek=root+'yogur-griego-ligero-natural-hacendado-2-mg-bote-21358/'
mandarina=root+'mandarina-pieza-3238/'
pera=root+'pera-conferencia-pieza-3119/'
kiwi=root+'kiwi-verde-pieza-3820/'
pimiento='https://www.mercaindex.es/productos/69310'
froiz='https://froiz.es/wp-content/uploads/2026/10/2026.10.15-SUPER-Galicia-LINKS.pdf'

def obs(price,kind,date,url,note=''):
    return dict(price=price,kind=kind,date=date,url=url,note=note)

overrides={
  30:[obs(2.65,'Histórico reconstruido',date,choc,'Precio vigente desde 28/09 según historial de cambios; tableta 200 g.') for date in ('2026-10-14','2026-10-21','2026-10-26')],
  35:[obs(2.9,'Histórico',date,pimiento,'Precio de referencia €/kg leído en el gráfico.') for date in ('2026-10-14','2026-10-21')]+[obs(2.9,'Catálogo fechado','2026-10-26','https://cestahoy.com/bajadas-de-precio/','Precio €/kg; no se utiliza el importe de una pieza de peso variable.')],
  34:[None,None,obs(2.55,'Catálogo fechado','2026-10-26',mandarina,'€/kg publicado; no se deduce de la serie de importes por pieza.')],
  68:[None,None,obs(2.5,'Catálogo fechado','2026-10-26',pera,'€/kg de la pera por pieza; no se usa la bolsa de 1,06 kg a 2,30 €/kg.')],
  70:[None,None,obs(4.65,'Catálogo fechado','2026-10-26',kiwi,'€/kg publicado; no se convierten a kilos los importes históricos de piezas de peso desconocido.')],
  18:[None,None,obs(1.5,'Catálogo fechado','2026-10-26',cottage,'Tarrina de 200 g, correspondencia con queso cottage del registro.')],
  19:[None,obs(2.1,'Catálogo fechado','2026-10-20',greek,'Bote de 1 kg; correspondencia apoyada por el precio base de 2,10 €.'),obs(2.1,'Arrastre de fuente','2026-10-20',greek,'Se conserva la observación del 20/10 para la última semana.')],
  44:[obs(1.3,'Equivalente de folleto',date,froiz,'Pág. 2: zanahoria bolsa 500 g a 0,65 € = 1,30 €/kg. Referencia equivalente al producto a granel del registro, con distinto formato.') for date in ('2026-10-15','2026-10-22','2026-10-29')],
}
plan=[]
for item in items:
    values=[]
    for week in range(3):
        explicit=overrides.get(item['row'],[None]*3)[week]
        values.append(explicit or obs(item['base_price'],'Estimación sin cambios','', '', 'Se conserva el precio medio de la base. No hay observación histórica recuperada para esta semana y referencia.'))
    plan.append(dict(**item,observations=values))
counts={}
for item in plan:
    for o in item['observations']:
        counts[o['kind']]=counts.get(o['kind'],0)+1
payload=dict(updated='2026-11-07',items=plan,counts=counts,manual=[i for i in data['items'] if i not in items])
(DATA/'plan_precios.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print('Productos:',len(plan),'Observaciones:',len(plan)*3,'Tipos:',counts,'Pendientes manuales:',len(payload['manual']))
