import urllib.request,ssl,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
r=Path('trabajo_china');url='https://www.mites.gob.es/estadisticas/bel/SMI/smi1.xls'
# Petición pública sin credenciales. Se registra esta limitación de transporte, no se oculta.
try:
 with urllib.request.urlopen(url,context=ssl._create_unverified_context(),timeout=25) as response:raw=response.read();headers=dict(response.headers)
 if not (raw.startswith(bytes.fromhex('d0cf11e0a1b11ae1')) or raw.startswith(b'PK')):raise ValueError('Respuesta no reconocida como Excel')
 dest=r/'datos/bronze/mites_smi_public_20261020';dest.mkdir(parents=True,exist_ok=True)
 sha=hashlib.sha256(raw).hexdigest();stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S');p=dest/(stamp+'_'+sha[:12]+'.xls');p.write_bytes(raw)
 m=dict(id='mites_smi_public_20261020',url=url,artifact=p.relative_to(r).as_posix(),sha256=sha,bytes=len(raw),accessed_at_utc=datetime.now(timezone.utc).isoformat(),content_type=headers.get('Content-Type'),publication_date=None,transport_certificate_verified=False,transport_note='Archivo público sin credenciales; certificado no verificable en este entorno. Firma Excel comprobada; contrastar valores con publicaciones oficiales independientes.')
 text=json.dumps(m,ensure_ascii=False,indent=2)+'\n';(dest/'latest.json').write_text(text);(dest/(p.name+'.json')).write_text(text);print('SMI original archivado',len(raw))
except Exception as e:print(type(e).__name__,str(e))
