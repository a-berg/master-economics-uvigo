"""Fija y verifica versiones de datos. Nunca sobrescribe una versión ya creada."""
from __future__ import annotations
import argparse,hashlib,json,re,shutil
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(version,root=ROOT):
    folder=root/'datos/snapshots'/version
    expected=(folder/'manifest.sha256').read_text().split()[0]
    if sha(folder/'manifest.json')!=expected:raise ValueError('Manifiesto alterado')
    m=json.loads((folder/'manifest.json').read_text())
    for item in m['frozen_files']:
        path=folder/item['path']
        if not path.is_file() or sha(path)!=item['sha256']:raise ValueError(f'Snapshot alterado: {path}')
    for item in m['bronze_files']:
        path=root/item['path']
        if not path.is_file() or sha(path)!=item['sha256']:raise ValueError(f'Bronze alterado o ausente: {path}')
    return m

def create(version,root=ROOT):
    if not re.fullmatch(r'[A-Za-z0-9_-]+',version):raise ValueError('Identificador de versión inválido')
    folder=root/'datos/snapshots'/version
    if folder.exists():raise FileExistsError(f'{version} ya existe; no se sobrescribe. Usar otro ID.')
    # Verificar bronze antes de crear el directorio de versión.
    bronze=[];seen=set()
    for path in sorted((root/'datos/bronze').rglob('*.json')):
        m=json.loads(path.read_text())
        if 'artifact' not in m:continue
        artifact=root/m['artifact']
        if sha(artifact)!=m['sha256']:raise ValueError(f'Bronze corrupto: {artifact}')
        if m['artifact'] not in seen:
            seen.add(m['artifact']);bronze.append(dict(path=m['artifact'],sha256=m['sha256'],metadata=m))
    selected=list((root/'datos/silver').glob('*'))+list((root/'datos/gold').glob('*'))+list((root/'datos/catalogo').glob('*'))+list((root/'src').glob('*.py'))+[root/'pyproject.toml',root/'uv.lock']
    folder.mkdir(parents=True)
    frozen=[]
    try:
        for src in sorted(selected):
            if not src.is_file():continue
            rel=src.relative_to(root);dest=folder/'frozen'/rel
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
            frozen.append(dict(path=dest.relative_to(folder).as_posix(),sha256=sha(dest),bytes=dest.stat().st_size))
        m=dict(version=version,created_at_utc=datetime.now(timezone.utc).isoformat(),
            status='frozen_initial_inputs_not_certified_final_data',
            policy='No refresh; never overwrite this version. EDA reads frozen data, not latest pointers.',
            bronze_files=bronze,frozen_files=frozen)
        (folder/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
        # El recibo externo detecta cambios accidentales al manifiesto.
        (folder/'manifest.sha256').write_text(sha(folder/'manifest.json')+'  manifest.json\n')
    except Exception:
        shutil.rmtree(folder);raise
    return verify(version,root)

def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['create','verify']);p.add_argument('version');a=p.parse_args()
    if a.command=='verify':
        folder=ROOT/'datos/snapshots'/a.version
        expected=(folder/'manifest.sha256').read_text().split()[0]
        if sha(folder/'manifest.json')!=expected:raise ValueError('Manifiesto alterado')
    m=create(a.version) if a.command=='create' else verify(a.version)
    print(m['version'],':',len(m['bronze_files']),'originales bronze y',len(m['frozen_files']),'archivos congelados; hashes correctos.')
if __name__=='__main__':main()
