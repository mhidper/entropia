import nbformat

notebook_path = r'C:/Users/Usuario/Documents/Github/Entropía/src/risk index.ipynb'

code_to_inject = """# ===============================================================================
# SEMANA 2 - BENCHMARK CONTRA ÍNDICES ESTABLECIDOS: EPU SPAIN
# ===============================================================================
import pandas as pd
import matplotlib.pyplot as plt

print("Descargando el índice de Economic Policy Uncertainty (EPU) para España...")
url_epu = "https://www.policyuncertainty.com/media/Spain_Policy_Uncertainty_Data.xlsx"

try:
    # El archivo Excel del EPU suele tener texto informativo en la fila 0, la cabecera real es la 1
    epu_df = pd.read_excel(url_epu)
    if 'Year' not in epu_df.columns:
        epu_df = pd.read_excel(url_epu, header=1)
        
    if 'Year' in epu_df.columns and 'Month' in epu_df.columns:
        # Encontrar la columna que contiene los valores de incertidumbre
        epu_col = [c for c in epu_df.columns if 'Uncertainty' in str(c) or 'EPU' in str(c) or 'Index' in str(c) or 'Unnamed' not in str(c)][-1]
        
        epu_df['Date'] = pd.to_datetime(epu_df[['Year', 'Month']].assign(DAY=1))
        epu_df.set_index('Date', inplace=True)
        
        # Resample a frecuencia trimestral (promedio del trimestre)
        epu_quarterly = epu_df[epu_col].resample('Q').mean()
        
        # Filtrar a partir de 2019Q1 (tu periodo de análisis principal)
        epu_quarterly = epu_quarterly.loc['2019-01-01':]
        
        print("✅ Datos EPU descargados y alineados trimestralmente.")
        
        # Plotear junto al Composite Index si está en entorno local/global
        if 'composite_index_final' in locals() or 'composite_index_final' in globals():
            plt.figure(figsize=(12, 6))
            
            # Normalizar EPU a una escala similar de 0 a 100 para comparar dinámicas
            epu_norm = (epu_quarterly - epu_quarterly.min()) / (epu_quarterly.max() - epu_quarterly.min()) * 100
            
            # Plot EPU
            plt.plot(epu_norm.index, epu_norm.values, color='gray', linestyle='--', linewidth=2, label='EPU Spain (Normalizado 0-100)')
            
            # Plot Composite Index
            ci_df = composite_index_final.copy()
            
            # Manejo básico del index del composite index
            if hasattr(ci_df.index, 'to_timestamp'):
                x_idx = ci_df.index.to_timestamp()
            elif isinstance(ci_df.index, pd.DatetimeIndex):
                x_idx = ci_df.index
            else:
                x_idx = pd.to_datetime(ci_df['date'] if 'date' in ci_df.columns else ci_df.index)
                
            plt.plot(x_idx, ci_df['composite_index'], color='red', linewidth=3, label='Multidimensional Composite Index')
                
            plt.title('Benchmark: Composite Uncertainty Index vs Economic Policy Uncertainty (EPU)', fontsize=14, fontweight='bold')
            plt.ylabel('Nivel de Incertidumbre Normalizado (0-100)', fontsize=12)
            plt.legend(fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
            
            print("🚀 El gráfico generado proporciona un benchmark empírico fuerte para la Tabla 2 del paper.")
        else:
            print("⚠️ Gráfico de EPU generado (El Composite Index aún no está cargado en esta sesión para superponerlo)")
            plt.figure(figsize=(10, 5))
            plt.plot(epu_quarterly.index, epu_quarterly.values, color='gray', linewidth=2)
            plt.title('Economic Policy Uncertainty (EPU) - España', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.show()
    else:
        print("❌ Formato de EPU no reconocido. Columnas:", epu_df.columns.tolist())
except Exception as e:
    print("❌ Error en el proceso EPU:", e)
"""

print("Reading notebook...")
try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    # Create new code cell
    new_cell = nbformat.v4.new_code_cell(code_to_inject)
    
    # Check if the last cell is exactly this code to avoid duplicates
    if nb.cells[-1].source != code_to_inject:
        nb.cells.append(new_cell)
        
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("✅ Successfully injected EPU Benchmark code into the notebook.")
    else:
        print("⚠️ Code was already injected into the last cell of the notebook.")

except Exception as e:
    print("Error:", e)
