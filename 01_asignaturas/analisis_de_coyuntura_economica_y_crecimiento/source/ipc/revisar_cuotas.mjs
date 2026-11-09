// Completa únicamente tarifas mensuales confirmadas como constantes.
import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
await fs.mkdir('tmp/ipc',{recursive:true});
const input='output/ipc/IPC-ADRIAN BERGES-revisado.xlsx';
const inputHash=createHash('sha256').update(await fs.readFile(input)).digest('hex');
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(input));
const s=wb.worksheets.getItem('Mis Gastos');
for(const [range,name] of [['CK94:CT99','suscripciones'],['CK75:CT77','hipoteca']]) {
  const blob=await wb.render({sheetName:'Mis Gastos',range,scale:1.5,format:'png'});
  await fs.writeFile(`tmp/ipc/${name}_antes_revision.png`,new Uint8Array(await blob.arrayBuffer()));
}
if(!process.argv.includes('--edit')) process.exit(0);
await fs.copyFile(input,`tmp/ipc/antes_cuotas_${inputHash.slice(0,12)}.xlsx`);
for(const [row,tariff] of [[76,648],[97,8],[98,16.99]]) {
  for(const col of ['CP','CR','CT']) {
    const cell=s.getRange(`${col}${row}`);
    const old=cell.values[0][0];
    if(old===null||old===''||old===undefined) cell.formulas=[[`=$CK${row}/$CL${row}`]];
    else assert.ok(Math.abs(old-tariff)<1e-8,`${col}${row}: tarifa guardada diferente; revisar.`);
  }
}
if(s.getRange('CP116').values[0][0]==='s') s.getRange('CP116').values=[[35]];
// Se habían sustituido por ceros los costes de pijama e hipoteca y borrado CO93.
// Son costes de la cesta fija, aunque no se vuelva a comprar la partida.
for(const row of [74,76,93]) for(const [cost,price] of [['CO','CP'],['CQ','CR'],['CS','CT']]) {
  s.getRange(`${cost}${row}`).formulas=[[`=IF(CL${row}=0,0,IF(${price}${row}="","",${price}${row}*CL${row}))`]];
}
if(process.argv.includes('--remaining-unchanged')) for(const row of [86,93,127]) for(const col of ['CP','CR','CT']) {
  const cell=s.getRange(`${col}${row}`);
  if([null,'',undefined].includes(cell.values[0][0])) {
    cell.formulas=[[`=$CK${row}/$CL${row}`]];
    cell.format.fill='#FFF2CC';
  }
}
// Una variación real de cero debe dibujarse, no tratarse como dato ausente.
const summary=wb.worksheets.getItem('Tablas e Gráficos');
summary.getRange('D7').values=[['Precios completos. Tarifas mensuales constantes. El gasto revaloriza la cesta base.']];
summary.getRange('K17:L20').formulas=Array.from({length:4},(_,i)=>[
  `=IF(ISNUMBER(F${i+2}),F${i+2},NA())`,
  `=IF(ISNUMBER(G${i+2}),G${i+2},NA())`,
]);
wb.recalculate();
for(const [row,tariff] of [[76,648],[97,8],[98,16.99]]) for(const [cost,price] of [['CO','CP'],['CQ','CR'],['CS','CT']]) {
  assert.ok(Math.abs(s.getRange(`${price}${row}`).values[0][0]-tariff)<1e-8);
  assert.ok(Math.abs(s.getRange(`${cost}${row}`).values[0][0]-s.getRange(`CK${row}`).values[0][0])<1e-8,JSON.stringify({row,cost,actual:s.getRange(`${cost}${row}`).values,base:s.getRange(`CK${row}`).values,formula:s.getRange(`${cost}${row}`).formulas}));
}
// Recalcular una subida en memoria comprueba que no se confunde tarifa con gasto.
const initial=s.getRange('CO97').values[0][0];
s.getRange('CP97').values=[[9]];
assert.ok(Math.abs(s.getRange('CO97').values[0][0]-initial-2)<1e-8);
s.getRange('CP97').formulas=[['=$CK97/$CL97']];
wb.recalculate();
console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},maxChars:1500})).ndjson);
for(const [range,name] of [['CK94:CT99','suscripciones'],['CK75:CT77','hipoteca']]) {
  const blob=await wb.render({sheetName:'Mis Gastos',range,scale:1.5,format:'png'});
  await fs.writeFile(`tmp/ipc/${name}_despues_revision.png`,new Uint8Array(await blob.arrayBuffer()));
}
await(await SpreadsheetFile.exportXlsx(wb)).save('tmp/ipc/cuotas_revisadas.xlsx');
await fs.writeFile('tmp/ipc/cuotas_entrada.sha256',inputHash+'\n');
console.log('Tarifas mensuales completadas; pagos originales y cantidades de la cesta conservados.');
