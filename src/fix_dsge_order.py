import nbformat
import re

notebook_path = r'C:\Users\Usuario\Documents\Github\Entropía\src\dsge model incertidumbre.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    for cell in nb.cells:
        if cell.cell_type == 'code':
            source = cell.source
            # If the cell uses compute_loss but defines results_biased later
            if 'loss_t, total_loss = compute_loss(results_biased, results_perfect)' in source and 'results_biased, results_perfect, error_percepcion =' in source:
                
                # Vamos a mover la ejecución de compare_perception... justo ANTES de llamar a compute_loss
                run_compare_str = "results_biased, results_perfect, error_percepcion = compare_perception_vs_perfect_info(model, uncertainty_episodes, bias=-0.05)"
                
                # Remove the original call if it's placed incorrectly at the bottom
                new_source = re.sub(r"results_biased,\s*results_perfect,\s*error_percepcion\s*=\s*compare_perception_vs_perfect_info.*", "", source)
                
                # Replace the exact line calling compute loss to first calculate the results
                fix_block = f"""
# Primero ejecutamos la simulación para calcular results_biased y results_perfect
{run_compare_str}

# Calcular y graficar la función de pérdida
loss_t, total_loss = compute_loss(results_biased, results_perfect)
"""
                new_source = new_source.replace("# Calcular y graficar la función de pérdida\nloss_t, total_loss = compute_loss(results_biased, results_perfect)", fix_block)
                # Cleanup double identical calls safely
                new_source = new_source.replace("loss_t, total_loss = compute_loss(results_biased, results_perfect)\n\nplt.figure", "plt.figure")

                if new_source != source:
                    cell.source = new_source
                    print("✅ Celda del DSGE reordenada correctamente.")
                    
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
        
except Exception as e:
    print(f"❌ Error al intentar arreglar el notebook: {e}")
