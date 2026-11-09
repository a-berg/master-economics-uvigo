import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const plan=JSON.parse(await fs.readFile('entregas/ipc/plan_precios.json','utf8'));
const data=JSON.parse(await fs.readFile('entregas/ipc/datos_ipc.json','utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load('tmp/ipc/seguimiento_cargado.xlsx'));
const s=wb.worksheets.getItem('Mis Gastos'),t=wb.worksheets.getItem('Tablas e Gráficos');
wb.recalculate();
const get=(sheet,cell)=>sheet.getRange(cell).values[0][0];
for(const item of plan.items) for(let k=0;k<3;k++) assert.ok(Math.abs(get(s,`${['CP','CR','CT'][k]}${item.row}`)-item.observations[k].price)<1e-8);
for(const item of plan.manual) for(const col of ['CP','CR','CT']){
 assert.ok([null,'',undefined].includes(get(s,`${col}${item.row}`)));
 // Supuesto temporal para verificar el cálculo completo. No se guarda.
 s.getRange(`${col}${item.row}`).values=[[item.base_price]];
}
wb.recalculate();
const expected=Array.from({length:3},(_,week)=>plan.items.reduce((sum,i)=>sum+i.quantity*i.observations[week].price,0)+plan.manual.reduce((sum,i)=>sum+i.amount,0));
for(let k=0;k<3;k++){
 assert.ok(Math.abs(get(t,`E${k+3}`)-expected[k])<1e-8);
 const index=expected[k]/data.total*100;
 const previous=k===0?100:expected[k-1]/data.total*100;
 assert.ok(Math.abs(get(t,`F${k+3}`)-index)<1e-8);
 assert.ok(Math.abs(get(t,`G${k+3}`)-(index/previous-1)*100)<1e-8);
}
assert.equal(t.charts.items.length,2);
assert.equal(wb.worksheets.getItem('Fuentes precios').getRange('B6').values[0][0],'HOT CHEESE Mercadona');
console.log('Verificado: 222 precios, 90 pendientes conservados y cálculo completo de costes, índices y tasas en una simulación sin guardar.');
