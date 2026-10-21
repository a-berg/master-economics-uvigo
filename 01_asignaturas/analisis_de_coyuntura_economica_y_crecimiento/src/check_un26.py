"""Comprueba presencia de China/España en UNdata tabla 2.6 (grupo 206, ISIC Rev.4)."""
import re,json,urllib.parse
from acquire_core import fetch
from snapshot import ROOT

def main():
 out=ROOT/'output/revision_equivalencias';out.mkdir(parents=True,exist_ok=True);results=[]
 for country,num in [('CHN',156),('ESP',724)]:
  url='https://data.un.org/Data.aspx?'+urllib.parse.urlencode({'d':'SNA','f':f'group_code:206;country_code:{num}'})
  m=fetch(dict(id='un26_'+country.lower()+'_presence',url=url,extension='html',publication_date=None,landing_url='https://unstats.un.org/unsd/econstats/national-accounts/data/madt'))
  text=(ROOT/m['artifact']).read_text(encoding='utf8')
  count=re.search(r'id="spanRecordCountB">([\d,]+)</span>',text)
  if not count:raise ValueError('No se identifica el contador de registros de UNdata; no se concluye ausencia.')
  n=int(count.group(1).replace(',',''));no_data='No data was found matching your query' in text
  if n==0 and not no_data:raise ValueError('Respuesta ambigua: contador cero sin aviso de ausencia')
  result=dict(country=country,country_code=num,table='2.6',group_code=206,classification='ISIC Rev.4',records=n,
      status='SIN_REGISTROS_EN_CONSULTA_OFICIAL' if n==0 else 'REGISTROS_PRESENTES_NO_DESCARGA_COMPLETA',
      last_update=re.search(r'Last update in UNdata:\s*([^<]+)',text).group(1),
      country_checkbox_present=f'name="{ "China" if country=="CHN" else "Spain" }"' in text,
      evidence=m,limit='Resultado de esta tabla, variante y consulta en esta fecha. No demuestra ausencia en otras tablas o fuentes; Hong Kong no equivale a China continental.')
  results.append(result)
 (out/'un26_presencia.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 print([(r['country'],r['records'],r['status']) for r in results])
if __name__=='__main__':main()
