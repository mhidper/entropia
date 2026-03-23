import nbformat

notebook_path = r'C:/Users/Usuario/Documents/Github/Entropía/src/risk index.ipynb'

code_to_inject = """# ===============================================================================
# SEMANA 2 - BENCHMARK CONTRA ÍNDICES ESTABLECIDOS: EPU SPAIN (CORREGIDO)
# ===============================================================================
import pandas as pd
import matplotlib.pyplot as plt

print("Descargando el índice de Economic Policy Uncertainty (EPU) para España...")
url_epu = "https://www.policyuncertainty.com/media/Spain_Policy_Uncertainty_Data.xlsx"

try:
    epu_df = pd.read_excel(url_epu)
    if 'Year' not in epu_df.columns:
        epu_df = pd.read_excel(url_epu, header=1)
        
    if 'Year' in epu_df.columns and 'Month' in epu_df.columns:
        epu_col = [c for c in epu_df.columns if 'Uncertainty' in str(c) or 'EPU' in str(c) or 'Index' in str(c) or 'Unnamed' not in str(c)][-1]
        epu_df['Date'] = pd.to_datetime(epu_df[['Year', 'Month']].assign(DAY=1))
        epu_df.set_index('Date', inplace=True)
        epu_quarterly = epu_df[epu_col].resample('QE').mean()
        epu_quarterly = epu_quarterly.loc['2019-01-01':]
        
        # Buscar el nombre real de la variable del Composite Index en esta sesión
        ci_df = None
        ci_col = None
        
        if 'uncertainty_framework_complete' in globals():
            ci_df = globals()['uncertainty_framework_complete'].copy()
            ci_col = 'composite_uncertainty_index'
        elif 'composite_index_complete' in globals():
            ci_df = globals()['composite_index_complete'].copy()
            ci_col = 'composite_index'
        elif 'composite_index_final' in globals():
            ci_df = globals()['composite_index_final'].copy()
            ci_col = 'composite_index'
            
        if ci_df is not None:
            plt.figure(figsize=(12, 6))
            epu_norm = (epu_quarterly - epu_quarterly.min()) / (epu_quarterly.max() - epu_quarterly.min()) * 100
            
            # Plot EPU
            plt.plot(epu_norm.index, epu_norm.values, color='gray', linestyle='--', linewidth=2, label='EPU Spain (Normalizado 0-100)')
            
            # Plot Composite Index
            if hasattr(ci_df.index, 'to_timestamp'):
                x_idx = ci_df.index.to_timestamp()
            elif isinstance(ci_df.index, pd.DatetimeIndex):
                x_idx = ci_df.index
            else:
                x_idx = pd.to_datetime(ci_df['date'] if 'date' in ci_df.columns else ci_df.index)
                
            plt.plot(x_idx, ci_df[ci_col], color='red', linewidth=3, label='Multidimensional Composite Index')
            plt.title('Benchmark: Composite Uncertainty Index vs Economic Policy Uncertainty (EPU)', fontsize=14, fontweight='bold')
            plt.ylabel('Nivel de Incertidumbre Normalizado (0-100)', fontsize=12)
            plt.legend(fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
            print("🚀 El gráfico generado proporciona un benchmark empírico fuerte para incorporar al paper.")
        else:
            print("⚠️ Gráfico de EPU generado (No encontré las variables del framework para superponer. Asegúrate de correr todas las celdas previas)")
            plt.figure(figsize=(10, 5))
            plt.plot(epu_quarterly.index, epu_quarterly.values, color='gray', linewidth=2)
            plt.title('Economic Policy Uncertainty (EPU) - España', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.show()
    else:
        print("❌ Formato de EPU no reconocido.")
except Exception as e:
    print("❌ Error en el proceso EPU:", e)
"""

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    # Replace the source of the LAST cell with the new injected code
    nb.cells[-1].source = code_to_inject
    
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
        
    print("✅ Successfully updated the EPU Benchmark cell in the notebook.")
except Exception as e:
    print("Error:", e)
