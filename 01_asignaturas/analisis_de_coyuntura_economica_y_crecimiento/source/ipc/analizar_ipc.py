"""Audita los datos originales y genera las entradas del informe, sin editar Excel."""
from pathlib import Path
import json
import hashlib
import openpyxl

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path('/home/xylon/Documents/Master_Economia/Analisis de Coyuntura y Crecimiento/entregable_ipc/IPC-ADRIAN BERGES.xlsx')
OUT = ROOT / 'entregas/ipc'
GROUPS = [(6,7,70),(71,72,72),(73,74,74),(75,76,77),(78,79,89),(90,91,91),(92,93,93),(94,95,95),(96,97,99),(100,101,101),(102,103,125),(126,127,127)]

def analyze(path=SOURCE):
    w = openpyxl.load_workbook(path, data_only=True)
    s, t = w.worksheets
    groups, items, transactions = [], [], []
    for number, (header, start, end) in enumerate(GROUPS, 1):
        amount = 0
        for r in range(start, end+1):
            spend = quantity = 0
            for c in range(2,89,3):
                value, q = s.cell(r,c).value, s.cell(r,c+1).value
                if isinstance(value,(int,float)):
                    spend += value
                    quantity += q or 0
                    transactions.append(dict(row=r,date=s.cell(4,c).value.isoformat()[:10],amount=value,quantity=q,description=s.cell(r,c+2).value))
            if spend:
                items.append(dict(row=r,group=number,name=s.cell(r,1).value,amount=round(spend,2),quantity=quantity,base_price=spend/quantity if quantity else None))
            amount += spend
        groups.append(dict(number=number,row=header,name=t.cell(17+number,1).value,amount=round(amount,2),spain=t.cell(17+number,3).value,galicia=t.cell(17+number,4).value))
    reference_path=OUT/'ponderaciones_2025.json'
    reference=json.loads(reference_path.read_text()) if reference_path.exists() else None
    if reference:
        for i,g in enumerate(groups):
            g.update(spain=reference['spain'][i],galicia=reference['galicia'][i])
    total=round(sum(g['amount'] for g in groups),2)
    for g in groups:
        g['weight']=100*g['amount']/total
        g['without_mortgage']=100*(g['amount'] if g['number']!=4 else 0)/(total-1296)
    result=dict(source=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),base_start='2026-09-08',base_end='2026-10-06',total=total,original_total=s['CK3'].value,groups=groups,items=items,transactions=transactions,weeks=['12–18 oct. 2026','19–25 oct. 2026','26 oct.–1 nov. 2026'])
    if reference:
        result['official_reference']={k:v for k,v in reference.items() if k not in ('spain','galicia')}
    OUT.joinpath('datos_ipc.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('items','transactions')},ensure_ascii=False,indent=2))
    print('Productos con gasto:',len(items),'Transacciones:',len(transactions))
    return result

if __name__=='__main__':
    analyze()
