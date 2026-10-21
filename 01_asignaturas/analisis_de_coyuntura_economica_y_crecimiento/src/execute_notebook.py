"""Ejecuta celdas con IPython en proceso, sin sockets; deja registrada esta modalidad."""
import contextlib,os
from pathlib import Path
import nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
ROOT=Path(__file__).resolve().parents[1]

def execute(path=ROOT/'notebooks/01_eda.ipynb'):
    notebook=nbformat.read(path,as_version=4)
    shell=InteractiveShell.instance();count=0
    prior=Path.cwd()
    try:
        os.chdir(path.parent)
        for cell in notebook.cells:
            if cell.cell_type!='code':continue
            count+=1
            with capture_output() as cap:
                result=shell.run_cell(cell.source,store_history=False)
            if result.error_before_exec or result.error_in_exec:
                raise RuntimeError(f'Celda {count}: {result.error_before_exec or result.error_in_exec}')
            outputs=[]
            if cap.stdout:outputs.append(nbformat.v4.new_output('stream',name='stdout',text=cap.stdout))
            if cap.stderr:outputs.append(nbformat.v4.new_output('stream',name='stderr',text=cap.stderr))
            outputs.extend(nbformat.v4.new_output('display_data',data=o.data,metadata=o.metadata) for o in cap.outputs)
            cell.outputs=outputs;cell.execution_count=count
        notebook.metadata['execution_mode']='in_process_ipython_no_jupyter_kernel'
        notebook.metadata['execution_note']='All code cells evaluated with IPython. Jupyter kernel startup was blocked by socket restrictions. Widget callbacks need re-execution in a local kernel.'
        # Guardar los modelos de widgets para que el frontend pueda mostrar el estado inicial.
        import ipywidgets
        state=ipywidgets.Widget.get_manager_state()
        notebook.metadata['widgets']={'application/vnd.jupyter.widget-state+json':state}
        nbformat.validate(notebook);nbformat.write(notebook,path)
    finally:os.chdir(prior)
    print(f'{count} celdas ejecutadas correctamente mediante IPython en proceso: {path}')
if __name__=='__main__':execute()
