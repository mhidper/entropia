import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import OLSInfluence
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import os

# Set seed for reproducible results
np.random.seed(42)

def run_full_influence_audit_fixed():
    csv_path = 'real_diagnostic_data.csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
        
    # Fixed index_col
    df = pd.read_csv(csv_path, index_col=0)
    df.index = pd.PeriodIndex(df.index, freq='Q')
    df = df.rename(columns={'y': 'sigmarev', 'x': 'ceui'})
    
    # Model OLS
    X = sm.add_constant(df['ceui'])
    model = sm.OLS(df['sigmarev'], X).fit(cov_type='HC3')
    influence = model.get_influence()
    
    # Cook's D and DFBETAS
    cooks_d = influence.cooks_distance[0]
    dfbetas = influence.dfbetas[:, 1]
    leverage = influence.hat_matrix_diag
    stud_resid = influence.resid_studentized_internal
    
    df['Cook_D'] = cooks_d
    df['DFBETA_ceui'] = dfbetas
    df['Leverage'] = leverage
    df['Student_Resid'] = stud_resid
    df['Flagged'] = np.where(df['Cook_D'] > 4/25, 'Yes', 'No')
    
    # --- OUTPUT 1: TABLE A1 (Appendix) ---
    df_sorted = df.sort_values('Cook_D', ascending=False)
    df_sorted_out = df_sorted.copy()
    df_sorted_out.index = [p.strftime('%YQ%q') for p in df_sorted_out.index]
    latex_a1 = df_sorted_out[['ceui', 'sigmarev', 'Cook_D', 'DFBETA_ceui', 'Leverage', 'Student_Resid', 'Flagged']].to_latex(
        float_format="%.4f", 
        caption="Diagnostic Statistics for Influence Analysis (Full Sample: 2019Q1--2025Q1)",
        label="tab:influence_appendix"
    )
    with open('table_a1_influence.tex', 'w') as f: f.write(latex_a1)
    
    # --- OUTPUT 2: COMPARATIVE REGRESSIONS (Sec 5.8) ---
    results_comp = []
    
    def run_sub_ols(name, mask):
        sub_df = df[mask]
        # use HC3 for t-stats
        res = sm.OLS(sub_df['sigmarev'], sm.add_constant(sub_df['ceui'])).fit(cov_type='HC3')
        rho, p_rho = spearmanr(sub_df['ceui'], sub_df['sigmarev'])
        return [name, res.params[1], res.tvalues[1], res.pvalues[1], res.rsquared, rho, len(sub_df)]

    # 1. Full
    results_comp.append(run_sub_ols('Full Sample', np.array([True]*25)))
    
    # 2. Ex-COVID (2020Q2-Q4)
    mask_nocovid = ~df.index.isin(pd.PeriodIndex(['2020Q2', '2020Q3', '2020Q4'], freq='Q'))
    results_comp.append(run_sub_ols('Ex-COVID (2020Q2-Q4)', mask_nocovid))
    
    # 3. Ex-Crisis (2020Q1-2021Q1)
    mask_21 = ~df.index.isin(pd.PeriodIndex(['2020Q1', '2020Q2', '2020Q3', '2020Q4', '2021Q1'], freq='Q'))
    results_comp.append(run_sub_ols('Ex-Crisis (2020Q1-2021Q1)', mask_21))
    
    # 4. Cook D < 4/N
    results_comp.append(run_sub_ols('Sub-threshold (Cook D < 4/N)', df['Cook_D'] <= 4/25))
    
    # 5. Ex-Most Influential
    idx_max = df['Cook_D'].idxmax()
    results_comp.append(run_sub_ols('Ex-Most Influential', df.index != idx_max))

    df_comp = pd.DataFrame(results_comp, columns=['Subsample', 'Beta', 't-stat', 'p-val', 'R2', 'Spearman', 'N'])
    with open('table_comparative_regs.tex', 'w') as f: f.write(df_comp.to_latex(index=False, float_format="%.4f"))

    # --- OUTPUT 3: FIGURE A ---
    plt.figure(figsize=(8,6))
    plt.scatter(df['ceui'], df['sigmarev'], c='blue', alpha=0.5, label='Regular Quarters')
    covid_periods = pd.PeriodIndex(['2020Q1', '2020Q2', '2020Q3', '2020Q4', '2021Q1'], freq='Q')
    mask_cov = df.index.isin(covid_periods)
    plt.scatter(df.loc[mask_cov, 'ceui'], df.loc[mask_cov, 'sigmarev'], c='red', s=100, label='COVID-19 Shock')
    
    x_range = np.linspace(df['ceui'].min(), df['ceui'].max(), 100)
    plt.plot(x_range, model.params[0] + model.params[1]*x_range, color='blue', label='OLS Full Sample')
    
    m_noc = sm.OLS(df.loc[mask_nocovid, 'sigmarev'], sm.add_constant(df.loc[mask_nocovid, 'ceui'])).fit(cov_type='HC3')
    plt.plot(x_range, m_noc.params[0] + m_noc.params[1]*x_range, color='gray', linestyle='--', label='OLS Ex-COVID')
    
    # Highlight specific labels 
    for idx in covid_periods:
        if idx in df.index:
            plt.annotate(idx.strftime('%yQ%q'), (df.loc[idx, 'ceui'], df.loc[idx, 'sigmarev']), fontsize=8, xytext=(5,5), textcoords='offset points')
            
    plt.xlabel('Composite Economic Uncertainty Index (CEUI)', fontsize=10)
    plt.ylabel('GDP Revision Volatility ($\sigma_{rev}$)', fontsize=10)
    plt.title('Influence of Economic Turbulence on Predictive Errors', fontsize=12)
    plt.legend()
    plt.savefig('fig_influence_scatter.pdf', dpi=300)
    plt.close()

    # --- OUTPUT 4: FIGURE B ---
    plt.figure(figsize=(8,6))
    plt.scatter(leverage, stud_resid, s=cooks_d*2000, alpha=0.6, edgecolors='black')
    plt.axhline(y=2, color='red', linestyle='--')
    plt.axhline(y=-2, color='red', linestyle='--')
    plt.axvline(x=2*2/25, color='gray', linestyle='--')
    
    # Use index list properly
    top5_idx = df_sorted.head(5).index
    for idx in top5_idx:
        plt.annotate(idx.strftime('%yQ%q'), (df.loc[idx, 'Leverage'], df.loc[idx, 'Student_Resid']), fontsize=9)
        
    plt.xlabel('Leverage ($h_{ii}$)')
    plt.ylabel('Studentized Residuals')
    plt.title('Influence Diagnostics: Leverage vs. Studentized Residuals', fontsize=12)
    plt.savefig('fig_influence_bubble.pdf', dpi=300)
    plt.close()
    
    print("DONE: Analysis files generated with REAL data (FIXED).")

run_full_influence_audit_fixed()
