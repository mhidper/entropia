import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import os

# Mimic the notebook data loading
def load_and_calc():
    try:
        # Load the results from the csv if possible
        # In the notebook: sigma_rev_results = calculate_historical_sigma_rev()
        # It reads cntr.csv. Let's find it.
        # However, I can also extract the arrays from the notebook metadata outputs if I want to be 100% sure what the notebook 'thinks'
        import nbformat
        with open(r'c:\Users\Usuario\Documents\Github\Entropía\src\risk index.ipynb', 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        # Searching for the output of (5) Spearman Rho
        target_full = None
        target_ex = None
        for cell in nb.cells:
            if cell.cell_type == 'code':
                for out in cell.get('outputs', []):
                    if 'text' in out:
                        if '(5) Spearman Rho:' in out['text']:
                            try:
                                target_full = float(out['text'].split('Spearman Rho:')[1].split('\n')[0].strip())
                            except: pass
                        if '1. TAREA 1: Ex-COVID Correlation' in out['text']:
                            try:
                                target_ex = float(out['text'].split('Spearman Rho:')[1].split('\n')[0].strip())
                            except: pass
        
        print(f"Notebook Real Results: Full={target_full}, Ex-COVID={target_ex}")
    except Exception as e:
        print(f"Error reading notebook: {e}")

if __name__ == "__main__":
    load_and_calc()
