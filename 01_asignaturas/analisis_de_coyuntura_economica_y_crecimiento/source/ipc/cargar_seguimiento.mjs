// Edición incremental de la copia revisada; no recrea la base ni toca el original.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
await fs.mkdir('tmp/ipc',{recursive:true});
const input='output/ipc/IPC-ADRIAN BERGES-revisado.xlsx';
const plan=JSON.parse(await fs.readFile('entregas/ipc/plan_precios.json','utf8'));
await fs.copyFile(input,'tmp/ipc/antes_carga_20261107.xlsx');
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(input));
const s=wb.worksheets.getItem('Mis Gastos');
const t=wb.worksheets.getItem('Tablas e Gráficos');
const existing=await wb.render({sheetName:'Mis Gastos',range:'CO7:CT22',scale:1.2,format:'png'});
await fs.writeFile('tmp/ipc/precios_antes_carga.png',new Uint8Array(await existing.arrayBuffer()));
const source=wb.worksheets.add('Fuentes precios');
source.showGridLines=false;
source.getRange('A1:I1').merge();
source.getRange('A1').values=[['Precios de supermercado. Seguimiento de octubre de 2026']];
source.getRange('A1:I1').format.font={name:'Arial',size:13,bold:true};
source.getRange('A2:I3').merge();
source.getRange('A2').values=[['Verde: fuente histórica o catálogo fechado. Azul: referencia equivalente de folleto. Amarillo: estimación sin cambios o arrastre. Las fechas son las de la fuente; consulta realizada el 07/11/2026. Los precios se editan en CP, CR y CT de Mis Gastos.']];
source.getRange('A2:I3').format={wrapText:true,verticalAlignment:'center',font:{name:'Arial',size:10}};
source.getRange('A2:I3').format.rowHeight=24;
source.getRange('A5:I5').values=[['Fila','Producto','Precio base','12–18/10','19–25/10','26/10–01/11','Origen S1 / S2 / S3','Fuente','Detalle']];
const rows=plan.items.map(item=>[
 item.row,item.name,null,null,null,null,
 new Set(item.observations.map(o=>o.kind)).size===1?`${item.observations[0].kind} (S1–S3)`:item.observations.map(o=>o.kind).join(' / '),
 [...new Set(item.observations.map(o=>o.url).filter(Boolean))].join('\n')||'Registro del período base',
 item.observations.every(o=>o.kind==='Estimación sin cambios')?'Se conserva el precio base en las tres semanas.':item.observations.map((o,i)=>`S${i+1}${o.date?' ('+o.date+')':''}: ${o.note}`).join('\n'),
]);
source.getRange(`A6:I${5+rows.length}`).values=rows;
for(let i=0;i<plan.items.length;i++){
 const item=plan.items[i],dest=i+6;
 source.getRange(`C${dest}:F${dest}`).formulas=[[
  `='Mis Gastos'!CK${item.row}/'Mis Gastos'!CL${item.row}`,...['CP','CR','CT'].map(col=>`='Mis Gastos'!${col}${item.row}`)
 ]];
 for(let week=0;week<3;week++){
  const col=['CP','CR','CT'][week],o=item.observations[week];
  const cell=s.getRange(`${col}${item.row}`);
  const old=cell.values[0][0];
  if(old!==null&&old!==''&&old!==undefined) throw new Error(`Precio ya existente en ${col}${item.row}; no se sobrescribe.`);
  if(o.kind==='Estimación sin cambios') cell.formulas=[[`=$CK${item.row}/$CL${item.row}`]];
  else cell.values=[[o.price]];
  const fill=o.kind.includes('Estimación')||o.kind.includes('Arrastre')?'#FFF2CC':o.kind.includes('Equivalente')?'#DDEBF7':'#E2F0D9';
  cell.format.fill=fill;
  cell.setNumberFormat('0.00');
  source.getRange(`${['D','E','F'][week]}${dest}`).format.fill=fill;
 }
}
source.getRange('A5:I5').format={fill:'#003366',font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center'};
source.getRange('A5:I5').format.rowHeight=30;
source.getRange(`A6:I${5+rows.length}`).format.font={name:'Arial',size:10};
source.getRange(`A6:I${5+rows.length}`).format.verticalAlignment='center';
source.getRange('A1:A80').format.columnWidth=7;
source.getRange('B1:B80').format.columnWidth=40;
source.getRange('C1:F80').format.columnWidth=13;
source.getRange('G1:G80').format.columnWidth=38;
source.getRange('H1:H80').format.columnWidth=65;
source.getRange('I1:I80').format.columnWidth=82;
source.getRange(`B6:B${5+rows.length}`).format.wrapText=true;
source.getRange(`G6:I${5+rows.length}`).format.wrapText=true;
source.getRange(`A6:I${5+rows.length}`).format.autofitRows();
source.getRange(`C6:F${5+rows.length}`).setNumberFormat('0.00');
source.freezePanes.freezeRows(5);
t.getRange('D7').values=[['Supermercados completados: verde = fuente, azul = equivalente, amarillo = estimación. Falta completar gastos fuera de supermercados en CP, CR y CT.']];
wb.recalculate();
for(const item of plan.items) for(let k=0;k<3;k++) assert.ok(Math.abs(s.getRange(`${['CP','CR','CT'][k]}${item.row}`).values[0][0]-item.observations[k].price)<1e-8);
for(const item of plan.manual) for(const col of ['CP','CR','CT']) assert.ok([null,'',undefined].includes(s.getRange(`${col}${item.row}`).values[0][0]));
assert.ok(Math.abs(s.getRange('CK3').values[0][0]-1751.93)<1e-8);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:15},maxChars:1500})).ndjson);
for(const [sheetName,range,file] of [['Mis Gastos','CO7:CT37','supermercados_cargados'],['Fuentes precios','A5:G16','fuentes_cargadas'],['Tablas e Gráficos','D1:G8','resumen_carga']]){
 const preview=await wb.render({sheetName,range,scale:1.3,format:'png'});
 await fs.writeFile(`tmp/ipc/${file}.png`,new Uint8Array(await preview.arrayBuffer()));
}
await(await SpreadsheetFile.exportXlsx(wb)).save('tmp/ipc/seguimiento_cargado.xlsx');
console.log('Cargadas 222 celdas; 90 precios manuales permanecen pendientes.');
