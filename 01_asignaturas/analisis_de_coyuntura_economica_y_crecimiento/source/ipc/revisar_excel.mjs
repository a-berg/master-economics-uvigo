import fs from 'node:fs/promises';
import {FileBlob, SpreadsheetFile} from '@oai/artifact-tool';
await fs.mkdir('tmp/ipc',{recursive:true});
const final=process.argv.includes('--final');
const source=final?'output/ipc/IPC-ADRIAN BERGES-revisado.xlsx':'tmp/ipc/importable.xlsx';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(source));
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:1500})).ndjson);
const views=final?[['Tablas e Gráficos','J1:W14','graficos_despues'],['Tablas e Gráficos','A15:D32','pesos_despues']]:[['Tablas e Gráficos','D1:G7','resumen_antes'],['Mis Gastos','CK94:CT100','ocio_antes']];
for(const [name,range,file] of views){
  const blob=await wb.render({sheetName:name,range,scale:1.5,format:'png'});
  await fs.writeFile(`tmp/ipc/${file}.png`,new Uint8Array(await blob.arrayBuffer()));
}
