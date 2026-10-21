"""Aplicación revisable: primero comprobar; añadir --apply para copiar. Nunca borra archivos."""
import argparse,hashlib,json,shutil
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files():
    return [p for p in ROOT.rglob('*') if p.is_file() and not any(x in {'.venv','.mplconfig','__pycache__'} for x in p.relative_to(ROOT).parts)]
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('destination',type=Path)
    p.add_argument('--apply',action='store_true');a=p.parse_args();target=a.destination.resolve()
    if target==ROOT:raise SystemExit('Origen y destino deben ser distintos.')
    baselines=json.loads((ROOT/'baseline_original.json').read_text());changes=[];conflicts=[]
    for src in files():
        rel=src.relative_to(ROOT).as_posix();dst=target/rel
        if dst.is_symlink():conflicts.append(rel+' (enlace simbólico)');continue
        if dst.exists():
            if not dst.is_file():conflicts.append(rel+' (no es archivo)');continue
            if sha(src)==sha(dst):continue
            if rel not in baselines or sha(dst)!=baselines[rel]:conflicts.append(rel+' (ha cambiado o ya existe)');continue
        changes.append((src,dst))
    if conflicts:raise SystemExit('No se aplica ningún cambio. Resolver conflictos:\n'+'\n'.join(conflicts))
    print(f'{len(changes)} archivos nuevos o actualizados; ninguna eliminación.')
    if not a.apply:
        print('Comprobación terminada. Para aplicar: repetir con --apply.');return
    backup=target/'backups_coyuntura'/datetime.now().strftime('%Y%m%dT%H%M%S')
    for src,dst in changes:
        if dst.exists():
            saved=backup/dst.relative_to(target);saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dst,saved)
        dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
    print('Cambios aplicados. Los archivos sustituidos se han respaldado en',backup)
if __name__=='__main__':main()
