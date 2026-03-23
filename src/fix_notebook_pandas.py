import nbformat
import re

notebook_path = r'C:/Users/Usuario/Documents/Github/Entropía/src/risk index.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    changes_made = 0
    for cell in nb.cells:
        if cell.cell_type == 'code':
            original_source = cell.source
            # Corregir resample('Q') a resample('QE')
            new_source = original_source.replace("resample('Q')", "resample('QE')")
            new_source = new_source.replace('resample("Q")', 'resample("QE")')
            
            if new_source != original_source:
                cell.source = new_source
                changes_made += 1
                
    if changes_made > 0:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"✅ Se corrigieron {changes_made} celdas cambiando resample('Q') por resample('QE').")
    else:
        print("ℹ️ No se encontraron instancias de resample('Q') para corregir.")
        
except Exception as e:
    print(f"❌ Error al intentar corregir el notebook: {e}")
