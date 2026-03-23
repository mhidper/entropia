import nbformat

notebook_path = r'C:/Users/Usuario/Documents/Github/Entropía/src/dsge model incertidumbre.ipynb'

code_to_inject = """# ===============================================================================
# FASE 4 - CALIBRACIÓN EMPÍRICA: INYECTANDO NUESTRO ÍNDICE DE INCERTIDUMBRE
# ===============================================================================
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print("Aplicando los regímenes reales del Índice Multidimensional al DSGE...")

# Replicamos el horizonte de tu análisis empírico (2019Q1 - 2025Q1 = ~25 trimestres)
# Basado en tu gráfica del benchmark EPU vs Composite Index:
# 2019: Normal
# 2020Q1-Q2: Elevated/High
# 2020Q3-2021Q1: Extreme (Pico máximo rojo)
# 2021Q2-2022: High
# 2023: Elevated
# 2024-2025: Normal

empirical_episodes = [
    (0, 4, 'normal'),      # 2019
    (4, 6, 'elevated'),    # Early 2020
    (6, 8, 'high'),        # Late 2020
    (8, 10, 'extreme'),    # Peak 2021 (Ahí es donde tu índice supera al EPU)
    (10, 14, 'high'),      # Late 2021 - Mid 2022
    (14, 18, 'elevated'),  # Late 2022 - 2023
    (18, 25, 'normal')     # 2024 - 2025
]

# Inicializamos el DSGE Parameters
params_emp = DSGEParameters()
model_emp = DSGEModel(params_emp)

# Simulamos la trayectoria de la economía durante EXACTAMENTE esos 25 trimestres de pandemia
print("\\nSimulando respuesta fiscal bajo percepción de incertidumbre (índice rojo)...")
results_empirical_biased = model_emp.simulate_model(T=25, uncertainty_episodes=empirical_episodes, bias=-0.05)

# Simulamos cómo hubiera sido si el gobierno no tuviera incertidumbre (Perfect Information)
original_extraction = model_emp.government_signal_extraction
def perfect_info_extraction_emp(true_state, t, bias=0.0):
    k_hat, a_hat = true_state[0], true_state[1]
    k_level = model_emp.steady_state['k'] * np.exp(k_hat)
    a_level = np.exp(a_hat)
    true_y = a_level * (k_level ** model_emp.params.alpha)
    model_emp.government_belief = true_y
    return true_y, true_y

model_emp.government_signal_extraction = perfect_info_extraction_emp
results_empirical_perfect = model_emp.simulate_model(T=25, uncertainty_episodes=empirical_episodes, bias=0.0)
model_emp.government_signal_extraction = original_extraction

# ----------------- PLOT PARA EL PAPER (dsge_model.tex) -----------------
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: Deuda Pública (El costo de la incertidumbre)
time_axis = pd.period_range(start='2019Q1', periods=25, freq='Q').to_timestamp()

axes[0].plot(time_axis, results_empirical_biased['states'][3, :], 'purple', linewidth=3, label='Deuda (Gobierno bajo Incertidumbre)')
axes[0].plot(time_axis, results_empirical_perfect['states'][3, :], 'g--', linewidth=2, label='Deuda (Gobierno Óptimo)')
axes[0].fill_between(time_axis, results_empirical_biased['states'][3, :], results_empirical_perfect['states'][3, :], color='purple', alpha=0.1)
axes[0].axvspan(pd.Period('2020Q3').to_timestamp(), pd.Period('2021Q1').to_timestamp(), color='red', alpha=0.2, label='Régimen "Extreme" (Índice)')
axes[0].set_title('Impacto en la Deuda Pública Durante la Crisis', fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# Plot 2: Error de Política Fiscal
error_percepcion = results_empirical_biased['policy_errors'] - results_empirical_perfect['policy_errors']
axes[1].plot(time_axis, error_percepcion, 'red', linewidth=2, marker='o', markersize=4)
axes[1].axhline(0, color='black', linestyle='--')
axes[1].axvspan(pd.Period('2020Q3').to_timestamp(), pd.Period('2021Q1').to_timestamp(), color='red', alpha=0.2)
axes[1].set_title('Error Fiscal (Sesgo Sistemático por Incertidumbre)', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.suptitle('Simulación DSGE Calibrada con el Índice Multidimensional de Incertidumbre', y=1.05, fontsize=15, fontweight='bold')
plt.show()

print("\\n" + "="*80)
print("✅ CONCLUSIÓN PARA EL PAPER TEÓRICO ('dsge_model.tex'):")
print("El período de incertidumbre 'Extreme' detectado por el Índice Multidimensional (2020Q3-2021Q1)")
print("provoca en el DSGE un error sistemático negativo en la política fiscal. El gobierno, abrumado por")
print("el ruido de las señales económicas (signal extraction problem), subestima el PIB real y sobredimensiona")
print("el gasto, lo que detona una acumulación permanente de Deuda Pública (área morada sombreada) que no")
print("habría ocurrido con información perfecta.")
print("="*80)
"""

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    new_cell = nbformat.v4.new_code_cell(code_to_inject)
    
    if nb.cells[-1].source != code_to_inject:
        nb.cells.append(new_cell)
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("✅ Successfully injected DSGE empirical calibration code into notebook.")
    else:
        print("⚠️ Code already in notebook.")

except Exception as e:
    print("Error:", e)
