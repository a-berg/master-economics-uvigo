// Ejecutar desde la raíz del repositorio. El original nunca se sobrescribe.
import fs from 'node:fs/promises';
import {FileBlob, SpreadsheetFile} from '@oai/artifact-tool';
await fs.mkdir('tmp/ipc',{recursive:true});
const out='output/ipc';
await fs.mkdir(out,{recursive:true});
const data=JSON.parse(await fs.readFile('entregas/ipc/datos_ipc.json','utf8'));
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load('tmp/ipc/importable.xlsx'));
const s=wb.worksheets.getItem('Mis Gastos');
const t=wb.worksheets.getItem('Tablas e Gráficos');
const groups=[[6,7,70],[71,72,72],[73,74,74],[75,76,77],[78,79,89],[90,91,91],[92,93,93],[94,95,95],[96,97,99],[100,101,101],[102,103,125],[126,127,127]];
const headers=groups.map(g=>g[0]);
s.getRange('CK96').formulas=[['=SUM(CK97:CK99)']];
// La fila 99 es una reserva de producto: conserva una fórmula coherente.
for(const [column,offset] of [['CK',0],['CL',1]]){
  const cells=[];
  for(let c=2+offset;c<89;c+=3){
    let n=c, label=''; while(n){n--;label=String.fromCharCode(65+n%26)+label;n=Math.floor(n/26);}
    cells.push(`${label}99`);
  }
  s.getRange(`${column}99`).formulas=[['='+cells.join('+')]];
}
s.getRange('CM99').formulas=[['=IF(A99="","",A99)']];
s.getRange('CK1').values=[['BASE 08/09–06/10/2026']];
for(const [cost,price] of [['CO','CP'],['CQ','CR'],['CS','CT']]){
  for(const [head,start,end] of groups){
    for(let row=start;row<=end;row++){
      s.getRange(`${cost}${row}`).formulas=[[`=IF(CL${row}=0,0,IF(${price}${row}="","",${price}${row}*CL${row}))`]];
    }
    s.getRange(`${cost}${head}`).formulas=[[`=IF(COUNT(${cost}${start}:${cost}${end})<ROWS(${cost}${start}:${cost}${end}),"",SUM(${cost}${start}:${cost}${end}))`]];
  }
  const refs=headers.map(row=>`${cost}${row}`).join(',');
  s.getRange(`${cost}3`).formulas=[[`=IF(COUNT(${refs})<12,"",SUM(${refs}))`]];
  // Resalta solamente los precios de bienes con gasto en la base.
  for(const item of data.items){
    s.getRange(`${price}${item.row}`).format.fill='#FFF2CC';
    s.getRange(`${price}${item.row}`).setNumberFormat('0.00');
  }
}
t.getRange('D1:G1').values=[['Período','Coste cesta fija (€)','IPC (base = 100)','Variación (%)']];
t.getRange('D2').values=[['08/09–06/10/2026 (base)']];
t.getRange('D3:D5').values=[['12–18/10/2026'],['19–25/10/2026'],['26/10–01/11/2026']];
for(let r=3;r<=5;r++){
  const col=['CO','CQ','CS'][r-3];
  t.getRange(`E${r}`).formulas=[[`=IF('Mis Gastos'!${col}3="","",'Mis Gastos'!${col}3)`]];
  t.getRange(`F${r}`).formulas=[[`=IF(E${r}="","",E${r}/$E$2*100)`]];
  t.getRange(`G${r}`).formulas=[[`=IF(OR(F${r}="",F${r-1}=""),"",(F${r}/F${r-1}-1)*100)`]];
}
t.getRange('E2:G5').setNumberFormat('0.00');
t.getRange('F7').clear({applyTo:'contents'});
t.getRange('D7:G8').merge();
t.getRange('D7').values=[['Precios pendientes: completar CP, CR y CT de Mis Gastos. La primera variación compara la semana 12–18/10 con toda la base; no es una tasa semanal.']];
t.getRange('D7:G8').format={wrapText:true,verticalAlignment:'center',font:{size:10},fill:'#FFF2CC'};
t.getRange('D7:G8').format.rowHeight=28;
t.getRange('D1:G1').format.wrapText=true;
t.getRange('D1:G1').format.rowHeight=34;
t.getRange('E1:G1').format.columnWidth=19;
t.getRange('A16').values=[['Base: 08/09–06/10/2026']];
t.getRange('C16').values=[['Referencia oficial: 2024']];
t.getRange('B30:D30').formulas=[['=SUM(B18:B29)','=SUM(C18:C29)','=SUM(D18:D29)']];
t.getRange('A18:A29').format.wrapText=true;
t.getRange('A18:D29').format.autofitRows();
// Excel dibuja como cero los resultados de fórmula "". Los auxiliares NA()
// hacen que los gráficos omitan explícitamente los precios aún ausentes.
t.getRange('J16:L16').values=[['Período (gráficos)','IPC','Variación (%)']];
for(let row=17;row<=20;row++){
  const src=row-15;
  t.getRange(`J${row}:L${row}`).formulas=[[`=D${src}`,`=IF(F${src}="",NA(),F${src})`,`=IF(G${src}="",NA(),G${src})`]];
}
t.getRange('J16:L20').format.font={size:10};
t.getRange('J16:J20').format.columnWidth=28;
t.getRange('K16:L20').format.columnWidth=16;
t.getRange('K17:L20').setNumberFormat('0.00');
t.getRange('J22:L24').merge();
t.getRange('J22').values=[['Datos auxiliares de los gráficos. #N/A indica una observación pendiente y evita dibujarla como cero.']];
t.getRange('J22:L24').format={wrapText:true,verticalAlignment:'center',font:{size:10}};
// Mantiene los dos gráficos nativos y sus posiciones.
const charts=t.charts.items;
for(let i=0;i<charts.length;i++){
  console.log('Gráfico original',i,charts[i].title?.text,charts[i].series.items.map(x=>({values:x.formula,categories:x.categoryFormula})));
}
// Los gráficos originales tienen los datos del índice y de la tasa.
for(const chart of charts){
  const rate=chart.series.items.some(x=>String(x.formula).includes('$G$'));
  chart.title=rate?'Variación del IPC personal (%)':'IPC personal (base 08/09–06/10/2026 = 100)';
  chart.setData([t.getRange('J16:J20'),t.getRange(rate?'L16:L20':'K16:K20')]);
}
wb.recalculate();
console.log((await wb.inspect({kind:'table',range:"'Tablas e Gráficos'!D1:G5",include:'values,formulas',tableMaxRows:5,tableMaxCols:4,maxChars:3000})).ndjson);
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:20},maxChars:2000})).ndjson);
for(const [sheetName,range,name] of [['Tablas e Gráficos','D1:G8','resumen_despues'],['Mis Gastos','CK94:CT100','ocio_despues']]){
  const blob=await wb.render({sheetName,range,scale:1.5,format:'png'});
  await fs.writeFile(`tmp/ipc/${name}.png`,new Uint8Array(await blob.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(`${out}/IPC-ADRIAN BERGES-revisado.xlsx`);
console.log('Exportado');
