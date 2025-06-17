# ===============================================================================
# COMPLETAR PAPER 1 CON RESULTADOS EMPÍRICOS
# ===============================================================================
# Instrucciones para Manuel: Una vez que tengas los resultados del framework
# ===============================================================================

"""
🎯 OBJETIVO: Completar el Paper 1 con los valores específicos de tus resultados

Una vez que ejecutes INSTRUCCIONES_INMEDIATAS.py y tengas el framework al 100%,
necesitas extraer estos valores específicos y completar el paper.
"""

# ===============================================================================
# VALORES QUE NECESITAS EXTRAER DE TU NOTEBOOK
# ===============================================================================

VALORES_PARA_PAPER = {
    
    # SECCIÓN: Model Performance Table
    "model_performance": {
        "description": "Tabla principal con métricas de performance de los 5 modelos",
        "variables_notebook": [
            "results_df (VAR)",
            "rf_results (Random Forest)", 
            "arima_results (ARIMA)",
            "lstm_results (LSTM)",
            "dfm_results_improved (DFM)",
            "resilience_5models_df"
        ],
        "valores_necesarios": {
            "VAR": {"mae": "CALCULAR", "rmse": "CALCULAR", "resilience": "EXTRAER"},
            "Random_Forest": {"mae": 2.34, "rmse": 6.54, "resilience": 1.096},  # YA TIENES ESTOS
            "ARIMA": {"mae": 4.26, "rmse": 11.27, "resilience": 0.303},
            "LSTM": {"mae": 2.34, "rmse": 5.47, "resilience": 0.469},
            "DFM": {"mae": 4.01, "rmse": 9.55, "resilience": 0.293}
        }
    },
    
    # SECCIÓN: Model Dispersion Analysis
    "model_dispersion": {
        "description": "Estadísticas de dispersión entre modelos por período",
        "variables_notebook": ["dispersion_5models_df"],
        "valores_necesarios": {
            "average_dispersion_stable": "[CALCULAR: promedio 2019Q1-2019Q4]",
            "average_dispersion_crisis": "[CALCULAR: promedio 2020Q1-2020Q4]",
            "max_dispersion_2020Q2": "[EXTRAER: dispersion_5models_df loc['2020Q2']]",
            "max_dispersion_2021Q1": "[EXTRAER: dispersion_5models_df loc['2021Q1']]",
            "max_dispersion_2021Q2": "[EXTRAER: dispersion_5models_df loc['2021Q2']]"
        }
    },
    
    # SECCIÓN: Within-Model Variability
    "within_model_uncertainty": {
        "description": "Uncertainty promedio por modelo",
        "variables_notebook": ["results_with_uncertainty"],
        "valores_necesarios": {
            "Random_Forest_avg": "[CALCULAR: promedio uncertainty Random Forest]",
            "LSTM_avg": "[CALCULAR: promedio uncertainty LSTM]", 
            "VAR_avg": "[CALCULAR: promedio uncertainty VAR]",
            "ARIMA_avg": "[CALCULAR: promedio uncertainty ARIMA]",
            "DFM_avg": "[CALCULAR: promedio uncertainty DFM]"
        }
    },
    
    # SECCIÓN: Composite Index Statistics
    "composite_index": {
        "description": "Estadísticas del índice compuesto final",
        "variables_notebook": ["composite_index_final_new"],
        "valores_necesarios": {
            "mean": "[CALCULAR: composite_index_final_new['composite_index'].mean()]",
            "std": "[CALCULAR: composite_index_final_new['composite_index'].std()]",
            "min": "[CALCULAR: composite_index_final_new['composite_index'].min()]",
            "max": "[CALCULAR: composite_index_final_new['composite_index'].max()]",
            "periods_total": "[CALCULAR: len(composite_index_final_new)]"
        }
    },
    
    # SECCIÓN: Regime Distribution Table
    "regime_distribution": {
        "description": "Distribución de períodos por régimen de incertidumbre",
        "variables_notebook": ["composite_index_final_new"],
        "valores_necesarios": {
            "low_periods": "[CALCULAR: períodos con composite_index 0-25]",
            "moderate_periods": "[CALCULAR: períodos con composite_index 25-50]",
            "high_periods": "[CALCULAR: períodos con composite_index 50-75]",
            "extreme_periods": "[CALCULAR: períodos con composite_index 75-100]",
            "low_percentage": "[CALCULAR: % de períodos low]",
            "moderate_percentage": "[CALCULAR: % de períodos moderate]",
            "high_percentage": "[CALCULAR: % de períodos high]",
            "extreme_percentage": "[CALCULAR: % de períodos extreme]"
        }
    },
    
    # SECCIÓN: Crisis Detection Performance
    "crisis_detection": {
        "description": "Performance del índice en detectar crisis",
        "variables_notebook": ["composite_index_final_new"],
        "valores_necesarios": {
            "quarters_advance_covid": "[ANALIZAR: cuántos quarters antes detectó COVID]",
            "recovery_accuracy": "[CALCULAR: % acierto en detectar recovery]",
            "correlation_epu": "[CALCULAR SI TIENES DATOS EPU]"
        }
    }
}

# ===============================================================================
# CÓDIGO PARA EXTRAER VALORES AUTOMÁTICAMENTE
# ===============================================================================

def extract_values_for_paper():
    """
    Función para extraer automáticamente todos los valores necesarios para el paper
    EJECUTAR DESPUÉS DE COMPLETAR EL FRAMEWORK
    """
    
    print("🔍 EXTRAYENDO VALORES PARA COMPLETAR PAPER 1")
    print("=" * 60)
    
    extracted_values = {}
    
    try:
        # 1. MODEL PERFORMANCE METRICS
        print("📊 1. Extrayendo métricas de performance de modelos...")
        
        # Calcular MAE y RMSE para cada modelo (si no los tienes ya)
        if 'results_df' in globals():
            var_mae = abs(results_df['forecast'] - results_df['actual']).mean() if 'actual' in results_df.columns else "NO_ACTUAL_DATA"
            var_rmse = ((results_df['forecast'] - results_df['actual'])**2).mean()**0.5 if 'actual' in results_df.columns else "NO_ACTUAL_DATA"
            extracted_values['VAR'] = {'mae': var_mae, 'rmse': var_rmse}
            print(f"   ✅ VAR: MAE={var_mae:.2f}, RMSE={var_rmse:.2f}")
        
        # 2. MODEL DISPERSION STATISTICS
        print("📊 2. Extrayendo estadísticas de Model Dispersion...")
        
        if 'dispersion_5models_df' in globals():
            # Períodos estables (pre-COVID)
            stable_mask = dispersion_5models_df.index < '2020-01-01'
            if stable_mask.any():
                avg_stable = dispersion_5models_df.loc[stable_mask, 'model_dispersion'].mean()
                extracted_values['avg_dispersion_stable'] = avg_stable
                print(f"   ✅ Dispersión promedio períodos estables: {avg_stable:.4f}")
            
            # Períodos de crisis (2020)
            crisis_mask = (dispersion_5models_df.index >= '2020-01-01') & (dispersion_5models_df.index < '2021-01-01')
            if crisis_mask.any():
                avg_crisis = dispersion_5models_df.loc[crisis_mask, 'model_dispersion'].mean()
                extracted_values['avg_dispersion_crisis'] = avg_crisis
                print(f"   ✅ Dispersión promedio períodos crisis: {avg_crisis:.4f}")
            
            # Valores específicos por período
            for period in ['2020Q2', '2021Q1', '2021Q2']:
                try:
                    value = dispersion_5models_df.loc[period, 'model_dispersion']
                    extracted_values[f'dispersion_{period}'] = value
                    print(f"   ✅ Dispersión {period}: {value:.4f}")
                except:
                    print(f"   ❌ No se encontró período {period}")
        
        # 3. WITHIN-MODEL UNCERTAINTY
        print("📊 3. Extrayendo Within-Model Uncertainty...")
        
        if 'results_with_uncertainty' in globals():
            uncertainty_cols = [col for col in results_with_uncertainty.columns if 'uncertainty' in col.lower()]
            if uncertainty_cols:
                avg_uncertainty = results_with_uncertainty[uncertainty_cols[0]].mean()
                extracted_values['avg_within_model_uncertainty'] = avg_uncertainty
                print(f"   ✅ Within-Model Uncertainty promedio: {avg_uncertainty:.4f}")
        
        # 4. COMPOSITE INDEX STATISTICS
        print("📊 4. Extrayendo estadísticas del Composite Index...")
        
        if 'composite_index_final_new' in globals():
            ci_stats = {
                'mean': composite_index_final_new['composite_index'].mean(),
                'std': composite_index_final_new['composite_index'].std(),
                'min': composite_index_final_new['composite_index'].min(),
                'max': composite_index_final_new['composite_index'].max(),
                'periods': len(composite_index_final_new)
            }
            extracted_values['composite_index_stats'] = ci_stats
            print(f"   ✅ Composite Index - Mean: {ci_stats['mean']:.2f}, Std: {ci_stats['std']:.2f}")
            print(f"   ✅ Composite Index - Range: {ci_stats['min']:.1f} - {ci_stats['max']:.1f}")
            print(f"   ✅ Total períodos: {ci_stats['periods']}")
            
            # 5. REGIME DISTRIBUTION
            print("📊 5. Calculando distribución por regímenes...")
            
            ci_values = composite_index_final_new['composite_index']
            regime_dist = {
                'low': len(ci_values[(ci_values >= 0) & (ci_values < 25)]),
                'moderate': len(ci_values[(ci_values >= 25) & (ci_values < 50)]),
                'high': len(ci_values[(ci_values >= 50) & (ci_values < 75)]),
                'extreme': len(ci_values[ci_values >= 75])
            }
            
            total_periods = len(ci_values)
            regime_pct = {k: (v/total_periods)*100 for k, v in regime_dist.items()}
            
            extracted_values['regime_distribution'] = {
                'counts': regime_dist,
                'percentages': regime_pct
            }
            
            print(f"   ✅ Regímenes de incertidumbre:")
            for regime, count in regime_dist.items():
                pct = regime_pct[regime]
                print(f"      {regime.title()}: {count} períodos ({pct:.1f}%)")
        
        # 6. TEMPORAL INSTABILITY STATS
        print("📊 6. Extrayendo Temporal Instability...")
        
        if 'aggregate_temporal_instability' in globals():
            temp_stats = {
                'mean': aggregate_temporal_instability.mean(),
                'std': aggregate_temporal_instability.std(),
                'max_period': aggregate_temporal_instability.idxmax(),
                'max_value': aggregate_temporal_instability.max()
            }
            extracted_values['temporal_instability_stats'] = temp_stats
            print(f"   ✅ Temporal Instability - Mean: {temp_stats['mean']:.4f}")
            print(f"   ✅ Período más inestable: {temp_stats['max_period']} ({temp_stats['max_value']:.4f})")
        
        print("\n🎊 ¡EXTRACCIÓN COMPLETADA!")
        print("📋 Usar estos valores para completar el Paper 1")
        
        return extracted_values
        
    except Exception as e:
        print(f"❌ Error durante extracción: {str(e)}")
        print("💡 Asegúrate de que todas las variables del framework estén definidas")
        return {}

# ===============================================================================
# TEMPLATE PARA COMPLETAR EL PAPER
# ===============================================================================

def generate_paper_completion_template():
    """
    Genera template con placeholders específicos para completar el paper
    """
    
    template = '''
# ===============================================================================
# COMPLETAR PAPER 1 - BUSCAR Y REEMPLAZAR ESTOS VALORES
# ===============================================================================

Una vez que tengas los valores extraídos, busca estos placeholders en main.tex 
y reemplázalos con los valores reales:

BUSCAR Y REEMPLAZAR EN main.tex:

1. PERFORMANCE TABLE:
   [INSERT VALUE] → Usar valores de extracted_values['VAR'], etc.

2. MODEL DISPERSION ANALYSIS:
   [INSERT VALUE] (stable periods) → extracted_values['avg_dispersion_stable']
   [INSERT VALUE] (crisis periods) → extracted_values['avg_dispersion_crisis']
   [INSERT VALUE] (2020Q2) → extracted_values['dispersion_2020Q2']
   [INSERT VALUE] (2021Q1) → extracted_values['dispersion_2021Q1']
   [INSERT VALUE] (2021Q2) → extracted_values['dispersion_2021Q2']

3. WITHIN-MODEL UNCERTAINTY:
   [INSERT VALUE] (Random Forest) → Calcular promedio por modelo
   [INSERT VALUE] (LSTM) → Calcular promedio por modelo
   [INSERT VALUE] (VAR) → Calcular promedio por modelo
   [INSERT VALUE] (ARIMA) → Calcular promedio por modelo
   [INSERT VALUE] (DFM) → Calcular promedio por modelo

4. COMPOSITE INDEX STATS:
   [INSERT VALUE] (mean) → extracted_values['composite_index_stats']['mean']
   [INSERT VALUE] (std) → extracted_values['composite_index_stats']['std']
   [INSERT VALUE] (min) → extracted_values['composite_index_stats']['min']
   [INSERT VALUE] (max) → extracted_values['composite_index_stats']['max']

5. REGIME DISTRIBUTION TABLE:
   [INSERT VALUE] (low periods) → extracted_values['regime_distribution']['counts']['low']
   [INSERT VALUE] (moderate periods) → extracted_values['regime_distribution']['counts']['moderate']
   [INSERT VALUE] (high periods) → extracted_values['regime_distribution']['counts']['high']
   [INSERT VALUE] (extreme periods) → extracted_values['regime_distribution']['counts']['extreme']
   [INSERT VALUE]% (low pct) → extracted_values['regime_distribution']['percentages']['low']
   [INSERT VALUE]% (moderate pct) → extracted_values['regime_distribution']['percentages']['moderate']
   [INSERT VALUE]% (high pct) → extracted_values['regime_distribution']['percentages']['high']
   [INSERT VALUE]% (extreme pct) → extracted_values['regime_distribution']['percentages']['extreme']

6. CRISIS DETECTION:
   [INSERT TIME] (quarters advance) → Analizar manualmente el composite index
   [INSERT VALUE]% (accuracy rate) → Calcular manualmente
   [INSERT VALUE] (correlation EPU) → Si tienes datos EPU

7. BENCHMARK CORRELATIONS:
   [INSERT VALUE] (VIX correlation) → Si tienes datos VIX
   [INSERT VALUE] (EPU correlation) → Si tienes datos EPU
   [INSERT VALUE] (Financial Stress correlation) → Si tienes datos

DESPUÉS DE COMPLETAR ESTOS VALORES:
✅ Compilar main.tex para generar PDF
✅ Revisar que todas las tablas y figuras se vean correctamente
✅ Verificar que no queden [INSERT VALUE] sin reemplazar
✅ Paper 1 listo para Semana 3!
'''
    
    print("📋 TEMPLATE PARA COMPLETAR PAPER:")
    print(template)

# ===============================================================================
# FUNCIÓN PRINCIPAL
# ===============================================================================

def main_paper_completion():
    """
    Función principal para completar el Paper 1
    """
    print("📄 COMPLETANDO PAPER 1 CON RESULTADOS EMPÍRICOS")
    print("=" * 80)
    
    # Extraer valores
    extracted_values = extract_values_for_paper()
    
    # Generar template
    generate_paper_completion_template()
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. ✅ Ejecutar INSTRUCCIONES_INMEDIATAS.py (completa framework)")
    print("2. ✅ Ejecutar extract_values_for_paper() (extrae valores)")
    print("3. ✅ Buscar y reemplazar [INSERT VALUE] en main.tex")
    print("4. ✅ Compilar LaTeX para generar PDF final")
    print("5. ✅ Paper 1 submission-ready!")
    
    return extracted_values

# ===============================================================================
# CÓDIGO ADICIONAL PARA FIGURAS Y VISUALIZACIONES
# ===============================================================================

def create_paper_figures():
    """
    Crear las figuras específicas que necesita el Paper 1
    """
    print("📊 CREANDO FIGURAS PARA EL PAPER 1")
    print("=" * 50)
    
    # Figure 1: Composite Index Evolution
    if 'composite_index_final_new' in globals():
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 2, 1)
        plt.plot(composite_index_final_new.index.to_timestamp(), 
                 composite_index_final_new['composite_index'], 
                 'purple', linewidth=3, marker='o', markersize=4)
        plt.title('Composite Uncertainty Index Evolution', fontweight='bold')
        plt.ylabel('Uncertainty Index (0-100)')
        plt.grid(True, alpha=0.3)
        
        # Add regime lines
        plt.axhline(y=25, color='green', linestyle='--', alpha=0.7, label='Low/Moderate')
        plt.axhline(y=50, color='orange', linestyle='--', alpha=0.7, label='Moderate/High')
        plt.axhline(y=75, color='red', linestyle='--', alpha=0.7, label='High/Extreme')
        plt.legend()
        
        # Figure 2: Individual Dimensions
        plt.subplot(2, 2, 2)
        for dim in ['dispersion_norm', 'uncertainty_norm', 'temporal_instability_norm']:
            if dim in composite_index_final_new.columns:
                plt.plot(composite_index_final_new.index.to_timestamp(),
                        composite_index_final_new[dim],
                        linewidth=2, label=dim.replace('_', ' ').title())
        plt.title('Individual Uncertainty Dimensions', fontweight='bold')
        plt.ylabel('Normalized Score (0-100)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Figure 3: Distribution
        plt.subplot(2, 2, 3)
        plt.hist(composite_index_final_new['composite_index'], bins=15, 
                 alpha=0.7, color='purple', edgecolor='black')
        plt.axvline(composite_index_final_new['composite_index'].mean(), 
                   color='red', linestyle='--', linewidth=2, label='Mean')
        plt.title('Distribution of Composite Index', fontweight='bold')
        plt.xlabel('Composite Index')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Figure 4: Model Performance
        plt.subplot(2, 2, 4)
        models = ['Random Forest', 'LSTM', 'DFM', 'ARIMA', 'VAR']
        mae_values = [2.34, 2.34, 4.01, 4.26, 6.22]  # From your data
        resilience_values = [1.096, 0.469, 0.293, 0.303, 0.064]  # From your data
        
        scatter = plt.scatter(mae_values, resilience_values, s=100, alpha=0.7)
        for i, model in enumerate(models):
            plt.annotate(model, (mae_values[i], resilience_values[i]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        plt.xlabel('Mean Absolute Error')
        plt.ylabel('Resilience Score')
        plt.title('Model Performance vs Resilience', fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('paper_figures_composite.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Figuras creadas y guardadas como 'paper_figures_composite.png'")
        print("📁 Usar estas figuras en el Paper 1")

if __name__ == "__main__":
    # Ejecutar proceso completo de completion del paper
    main_paper_completion()
