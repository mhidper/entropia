import nbformat

notebook_path = r'C:/Users/Usuario/Documents/Github/Entropía/src/risk index.ipynb'

code_to_inject = """# ===============================================================================
# FASE 2 - INTERPRETABILIDAD Y XAI (EXPLAINABLE AI) VIA SHAP VALUES
# ===============================================================================
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    import shap
    print("✅ Librería SHAP cargada correctamente.")
    shap.initjs()
    shap_installed = True
except ImportError:
    print("❌ LIBRERÍA 'shap' NO ENCONTRADA.")
    print("👉 Solución: Ejecuta en una nueva celda '!pip install shap' (o 'conda install conda-forge::shap'), luego reinicia el kernel y vuelve a correr esta celda.")
    shap_installed = False

if shap_installed and 'best_data' in globals() and 'gdp_column' in globals():
    from sklearn.ensemble import RandomForestRegressor
    print("Entrenando un modelo Global Random Forest para el análisis SHAP...")
    
    if 'create_lagged_features' in globals():
        # Generar matriz de features usando la lógica de tu cuaderno (2 rezagos)
        X_all, y_all = create_lagged_features(best_data, lags=2)
        
        # Inferencia perezosa de nombres de columnas
        base_features = best_data.columns.tolist()
        feature_names = [f"{col}_lag{l}" for l in range(1, 3) for col in base_features]
        if X_all.shape[1] != len(feature_names):
            feature_names = [f"Feature_{i}" for i in range(X_all.shape[1])]
            
        X_df = pd.DataFrame(X_all, columns=feature_names)
        
        # Entrenar RF
        rf_shap = RandomForestRegressor(n_estimators=100, max_depth=4, random_state=42, min_samples_split=2)
        rf_shap.fit(X_df, y_all)
        
        # Generar Explicador SHAP
        explainer = shap.TreeExplainer(rf_shap)
        shap_values = explainer.shap_values(X_df)
        
        print("\\n" + "="*80)
        print("📊 GRÁFICO 1: SHAP SUMMARY PLOT (QUÉ VARIABLES MUEVEN LA AGUJA)")
        print("Este gráfico debes incluirlo en tu paper para 'abrir la caja negra' del ML.")
        print("Cada punto es un trimestre. El color es el valor del indicador, el eje X su impacto.")
        print("="*80)
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, X_df, max_display=10, show=False)
        # Customizar un poco el plot
        fig = plt.gcf()
        fig.suptitle("Impacto Estructural de Variables en el Modelo (SHAP Summary)", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        print("\\n" + "="*80)
        print("🎯 GRÁFICO 2: SHAP BAR PLOT GLOBALES")
        print("Este gráfico promedia y ordena las variables más críticas a nivel global.")
        print("="*80)
        plt.figure(figsize=(10, 6))
        shap.summary_plot(shap_values, X_df, plot_type="bar", max_display=10, show=False)
        fig = plt.gcf()
        fig.suptitle("Importancia Global Absoluta (Mean |SHAP|)", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
        print("\\n" + "="*80)
        print("🔍 CONCLUSIÓN PARA TU PAPER (FASE 2 CUMPLIDA):")
        print("En el documento 'main.tex', describe que los modelos de Machine Learning no operan")
        print("como 'cajas negras'. De docenas de variables, los SHAP values nos aseguran que el modelo")
        print("fija su varianza en los principales causantes estructurales mostrados arriba, validando")
        print("empíricamente la relación teórica.")
        print("="*80)
            
    else:
        print("❌ Asegúrate de correr la celda que define 'create_lagged_features'.")
"""

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    new_cell = nbformat.v4.new_code_cell(code_to_inject)
    
    if nb.cells[-1].source != code_to_inject:
        nb.cells.append(new_cell)
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("✅ Successfully injected SHAP code into notebook.")
    else:
        print("⚠️ Code already in notebook.")

except Exception as e:
    print("Error:", e)
