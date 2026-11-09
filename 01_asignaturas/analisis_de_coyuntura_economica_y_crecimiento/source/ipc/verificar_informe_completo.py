"""Prueba la rama de informe completo con un escenario temporal, sin tocar Excel."""
from pathlib import Path
import json
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DATA=ROOT/'entregas/ipc'
(ROOT/'tmp/ipc').mkdir(parents=True,exist_ok=True)
target=DATA/'seguimiento_ipc.json'
original=target.read_bytes()
try:
    d=json.loads(original)
    p=json.loads((DATA/'plan_precios.json').read_text())
    d['complete']=True
    d['missing_count']=0
    previous=100
    for k,w in enumerate(d['weeks']):
        cost=sum(i['quantity']*i['observations'][k]['price'] for i in p['items'])+sum(i['amount'] for i in p['manual'])
        index=cost/d['base']*100
        w.update(cost=cost,index=index,rate=(index/previous-1)*100,missing=[])
        previous=index
    target.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    subprocess.run(['typst','compile','--root',str(ROOT),str(DATA/'mi_ipc_ABerges.typ'),str(ROOT/'tmp/ipc/informe_completo_simulado.pdf')],check=True,cwd=ROOT)
finally:
    target.write_bytes(original)
print('Rama completa del informe compilada con datos simulados solo en tmp. JSON de trabajo restaurado.')
