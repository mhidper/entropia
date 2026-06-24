import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ── Setup scratch paths ──────────────────────────────────────────────────────
PATH_FIGURES = r'C:\Users\Usuario\Documents\Github\Entropía\scratch\figures'
PATH_TABLES  = r'C:\Users\Usuario\Documents\Github\Entropía\scratch\tables'
os.makedirs(PATH_FIGURES, exist_ok=True)
os.makedirs(PATH_TABLES,  exist_ok=True)

# ── CRISIS REGIMES ───────────────────────────────────────────────────────────
CRISIS_REGIMES = {
    'Financial Crisis': (pd.Period('2008Q3', freq='Q'), pd.Period('2009Q2', freq='Q')),
    'Sovereign Debt'  : (pd.Period('2010Q2', freq='Q'), pd.Period('2013Q3', freq='Q')),
    'COVID-19'        : (pd.Period('2020Q1', freq='Q'), pd.Period('2022Q2', freq='Q')),
}

def is_crisis(p):
    return any(start <= p <= end for start, end in CRISIS_REGIMES.values())

CRISIS_COLORS = {
    'Financial Crisis': '#ffcccc',
    'Sovereign Debt'  : '#fff176',
    'COVID-19'        : '#c8e6c9',
}

# ── Load CNTR and calculate QoQ GDP rate (t/t-1) ──────────────────────────────
PATH_CNTR = r'C:\Users\Usuario\Documents\Github\Entropía\replica_pavia_2018\datos\cntr2.xlsx'
df_raw = pd.read_excel(PATH_CNTR, sheet_name='cntr', header=None, skiprows=1)

header = [str(v) for v in df_raw.iloc[0]]
header[0] = 'year'
header[1] = 'trim'
df_raw.columns = header
df_raw = df_raw.iloc[1:].reset_index(drop=True)

df_raw['year'] = pd.to_numeric(df_raw['year'], errors='coerce').ffill()
df_raw['trim'] = pd.to_numeric(df_raw['trim'], errors='coerce')
df_raw = df_raw.dropna(subset=['year', 'trim'])
df_raw = df_raw[df_raw['year'] >= 1995]
df_raw = df_raw[df_raw['trim'].isin([1.0, 2.0, 3.0, 4.0])].reset_index(drop=True)
df_raw['year'] = df_raw['year'].astype(int)
df_raw['trim'] = df_raw['trim'].astype(int)

vintage_cols = [c for c in df_raw.columns if '/' in str(c)]

df_long = df_raw.melt(
    id_vars=['year', 'trim'],
    value_vars=vintage_cols,
    var_name='vintage_str',
    value_name='pib'
)
df_long['vintage_date'] = pd.to_datetime(df_long['vintage_str'], dayfirst=True)
df_long = df_long.dropna(subset=['pib', 'year', 'trim'])
df_long['year'] = df_long['year'].astype(int)
df_long['trim'] = df_long['trim'].astype(int)
df_long['period'] = pd.PeriodIndex([f"{y}Q{q}" for y, q in zip(df_long['year'], df_long['trim'])], freq='Q')
df_long = df_long.sort_values(['period', 'vintage_date']).reset_index(drop=True)

df_pivot = df_long.pivot_table(index='period', columns='vintage_date', values='pib', aggfunc='last').sort_index()

# TASA INTERTRIMESTRAL (QoQ): pct_change(1)
df_growth = df_pivot.pct_change(1, fill_method=None) * 100

# ── Compute sigma_rev (QoQ) with 2-year window ──────────────────────────────
START_PERIOD = pd.Period('2004Q1', freq='Q')
WINDOW_YEARS = 2
records = []
n_vintages_per_period = df_growth.notna().sum(axis=1)

for period in df_pivot.index:
    if period < START_PERIOD:
        continue
    row = df_growth.loc[period].dropna()
    if len(row) < 3:
        continue
    first_vintage_date = row.index[0]
    cutoff = first_vintage_date + pd.DateOffset(years=WINDOW_YEARS)
    row_window = row[row.index <= cutoff]
    if len(row_window) < 3:
        continue
    records.append({
        'period': period,
        'sigma_rev': row_window.std(),
        'mae_rev': (row_window - row_window.iloc[-1]).abs().mean(),
        'n_vintages': len(row_window),
    })

sigma_df = pd.DataFrame(records).set_index('period')
sigma_rev = sigma_df['sigma_rev']
mae_rev = sigma_df['mae_rev']

print("=== SIGMA_REV CALCULADO EN TASA INTERTRIMESTRAL ===")
print(sigma_df.describe().round(4))

# Plot Figure 1: Revision Volatility
fig, ax = plt.subplots(figsize=(10, 5))
x = sigma_rev.index.to_timestamp()
ax.plot(x, sigma_rev.values, color='navy', linewidth=1.8, label=r'$\sigma^{rev}_t$ (QoQ)')
ax.fill_between(x, 0, sigma_rev.values, alpha=0.15, color='navy')
for start, end in CRISIS_REGIMES.values():
    ax.axvspan(start.to_timestamp(), end.to_timestamp(), alpha=0.25, color='gold')
ax.set_ylabel('Std of revisions (pp)')
ax.set_title('QoQ GDP Revision Volatility')
ax.grid(True, alpha=0.3)
fig.savefig(os.path.join(PATH_FIGURES, 'fig1_revision_volatility.pdf'), bbox_inches='tight', dpi=300)
plt.close()

# ── Load and transform Monthly Indicators to QoQ when I(1) ────────────────────
PATH_CT = r'C:\Users\Usuario\Documents\Github\crisistrackerv2'
dir_m   = os.path.join(PATH_CT, 'data', 'Vintage', 'monthly', 'IIT2025')
latest  = sorted([f for f in os.listdir(dir_m) if f.endswith('_m_rev.xlsx')])[-1]

df_m = pd.read_excel(os.path.join(dir_m, latest))
df_m = df_m.rename(columns={'Unnamed: 0': 'Fecha'})
df_m.index = pd.PeriodIndex(df_m['Fecha'].tolist(), freq='M')
df_m.drop('Fecha', axis=1, inplace=True)

# Trimestrializar (media del trimestre)
df_q_pred = df_m.to_timestamp().resample('Q').mean().to_period('Q')

PREDICTORS = [
    'AFILIACIONES A LA SS. CVEC',
    'INDICE PRODUCCION INDUSTRIAL. INDUSTRIA MANUFACTURERA. CVEC',
    'INDICE PRODUCCION INDUSTRIAL. BIENES DE EQUIPO. CVEC',
    'INDICE PRODUCCION INDUSTRIAL. BIENES INTERMEDIOS. CVEC',
    'INDICADOR SINTETICO DE INVERSION EN CONSTRUCCION. CVEC',
    'INDICADOR SINTETICO DE INVERSION EN BIENES DE EQUIPO. CVEC',
    'VGE. INTERIORES. REAL. CVEC',
    'PMI. MANUFACTURAS. ESPAÑA',
    'COMPOSITE LEADING INDICATOR. ESPAÑA ( OCDE )',
]

df_q_pred = df_q_pred[PREDICTORS].copy()

# Transform I(1) variables to QoQ growth rates
I1_VARIABLES = [
    'AFILIACIONES A LA SS. CVEC',
    'INDICE PRODUCCION INDUSTRIAL. INDUSTRIA MANUFACTURERA. CVEC',
    'INDICE PRODUCCION INDUSTRIAL. BIENES DE EQUIPO. CVEC',
    'INDICE PRODUCCION INDUSTRIAL. BIENES INTERMEDIOS. CVEC',
    'INDICADOR SINTETICO DE INVERSION EN CONSTRUCCION. CVEC',
    'INDICADOR SINTETICO DE INVERSION EN BIENES DE EQUIPO. CVEC',
    'VGE. INTERIORES. REAL. CVEC',
]

for col in I1_VARIABLES:
    # pct_change(1) since they are monthly series averaged to quarterly (index/level).
    # t/t-1 growth rate in %
    df_q_pred[col] = df_q_pred[col].pct_change(1) * 100

# Keep PMI and CLI in levels (stationary I(0))

# GDP series
gdp_series = df_growth.ffill(axis=1).iloc[:, -1].dropna()
gdp_series.name = 'PIB'

df_all = pd.concat([gdp_series, df_q_pred], axis=1)
df_all = df_all.loc['2001Q1':].dropna(how='all')
df_all = df_all.apply(pd.to_numeric, errors='coerce')

print("\n=== DATASET COMBINADO QoQ ===")
print(df_all.head(8).round(3))

# ── Out-of-sample Forecast Ensemble (2015Q1-2024Q4) ───────────────────────────
from statsmodels.tsa.api import VAR as VARModel
from statsmodels.tsa.arima.model import ARIMA as ARIMAModel
from statsmodels.tsa.statespace.dynamic_factor_mq import DynamicFactorMQ
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

import random
import tensorflow as tf
random.seed(42)
np.random.seed(42)
tf.random.set_seed(42)
try:
    tf.config.experimental.enable_op_determinism()
except Exception:
    pass
os.environ['PYTHONHASHSEED'] = '0'

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM as LSTMLayer, Dense
from tensorflow.keras.callbacks import EarlyStopping
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.filterwarnings('ignore', category=ConvergenceWarning)

EVAL_START = pd.Period('2015Q1', freq='Q')
EVAL_END   = pd.Period('2024Q4', freq='Q')
EVAL_RANGE = pd.period_range(EVAL_START, EVAL_END, freq='Q')

N_LAGS_VAR = 4
N_LAGS_RF  = 6
N_LAGS_AR  = 4
SEQ_LEN    = 8

def build_lstm():
    m = Sequential([
        LSTMLayer(16, input_shape=(SEQ_LEN, 1)),
        Dense(1)
    ])
    m.compile(optimizer='adam', loss='mse')
    return m

forecasts = {m: {} for m in ['VAR', 'ARIMA', 'RF', 'LSTM', 'DFM']}
n_total = len(EVAL_RANGE)

for i, target in enumerate(EVAL_RANGE):
    train_end  = target - 1
    train_data = df_all.loc[:train_end].dropna()
    n_train    = len(train_data)
    
    if n_train < 20:
        for m in forecasts:
            forecasts[m][target] = np.nan
        continue

    gdp_train = train_data['PIB']
    X_train   = train_data.drop(columns=['PIB'])

    # 1. VAR
    try:
        var_data   = train_data.dropna()
        model_var  = VARModel(var_data)
        lags       = max(1, model_var.select_order(maxlags=N_LAGS_VAR).aic)
        fitted_var = model_var.fit(lags)
        fc         = fitted_var.forecast(var_data.values[-lags:], steps=1)
        forecasts['VAR'][target] = fc[0, 0]
    except Exception as e:
        forecasts['VAR'][target] = np.nan

    # 2. ARIMA
    try:
        fitted_ar  = ARIMAModel(gdp_train, order=(N_LAGS_AR, 0, 1)).fit()
        fc_ar      = fitted_ar.forecast(steps=1).iloc[0]
        forecasts['ARIMA'][target] = fc_ar
    except Exception as e:
        forecasts['ARIMA'][target] = np.nan

    # 3. Random Forest
    try:
        gdp_vals = gdp_train.values
        X_rf, y_rf = [], []
        for j in range(N_LAGS_RF, len(gdp_vals)):
            row = list(gdp_vals[j-N_LAGS_RF:j])
            row += list(X_train.iloc[j-1].fillna(0).values)
            X_rf.append(row)
            y_rf.append(gdp_vals[j])

        scaler   = StandardScaler()
        X_rf_sc  = scaler.fit_transform(X_rf)
        rf       = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_rf_sc, y_rf)

        x_pred    = list(gdp_vals[-N_LAGS_RF:])
        x_pred   += list(X_train.iloc[-1].fillna(0).values)
        fc_rf     = rf.predict(scaler.transform([x_pred]))[0]
        forecasts['RF'][target] = fc_rf
    except Exception as e:
        forecasts['RF'][target] = np.nan

    # 4. LSTM
    try:
        gdp_vals    = gdp_train.values.reshape(-1, 1)
        scaler_lstm = StandardScaler()
        gdp_sc      = scaler_lstm.fit_transform(gdp_vals)

        X_lstm, y_lstm = [], []
        for j in range(SEQ_LEN, len(gdp_sc)):
            X_lstm.append(gdp_sc[j-SEQ_LEN:j])
            y_lstm.append(gdp_sc[j])
        X_lstm = np.array(X_lstm)
        y_lstm = np.array(y_lstm)

        model_lstm = build_lstm()
        model_lstm.fit(
            X_lstm, y_lstm,
            epochs=50, batch_size=8, verbose=0,
            callbacks=[EarlyStopping(patience=5, restore_best_weights=True)]
        )
        x_pred_lstm = gdp_sc[-SEQ_LEN:].reshape(1, SEQ_LEN, 1)
        pred_sc     = model_lstm.predict(x_pred_lstm, verbose=0)
        fc_lstm     = scaler_lstm.inverse_transform(pred_sc)[0, 0]
        forecasts['LSTM'][target] = fc_lstm
    except Exception as e:
        forecasts['LSTM'][target] = np.nan

    # 5. DFM
    try:
        dfm_data   = train_data.dropna()
        scaler_dfm = StandardScaler()
        dfm_sc     = pd.DataFrame(
            scaler_dfm.fit_transform(dfm_data),
            index=dfm_data.index, columns=dfm_data.columns
        )
        fitted_dfm = DynamicFactorMQ(dfm_sc, factors=1, factor_orders=1).fit(disp=False)
        fc_dfm     = fitted_dfm.forecast(steps=1)
        pib_idx    = list(dfm_data.columns).index('PIB')
        pred_unsc  = (fc_dfm.iloc[0, pib_idx] * scaler_dfm.scale_[pib_idx]
                      + scaler_dfm.mean_[pib_idx])
        forecasts['DFM'][target] = pred_unsc
    except Exception as e:
        forecasts['DFM'][target] = np.nan

forecasts_df = pd.DataFrame({m: pd.Series(forecasts[m]) for m in forecasts})
forecasts_df.index = pd.PeriodIndex(forecasts_df.index, freq='Q')
forecasts_df['actual'] = gdp_series.reindex(forecasts_df.index)

print("\n=== MAE POR MODELO (QoQ) ===")
for m in ['VAR', 'ARIMA', 'RF', 'LSTM', 'DFM']:
    mae = (forecasts_df[m] - forecasts_df['actual']).abs().mean()
    print(f"  {m:<6}: {mae:.4f}")

# ── CEUI Construction (WINDOW=4) ──────────────────────────────────────────────
WINDOW = 4
MODELS = ['VAR', 'ARIMA', 'RF', 'LSTM', 'DFM']

errors_df = forecasts_df[MODELS].subtract(forecasts_df['actual'], axis=0)
u_within = errors_df.rolling(window=WINDOW).std().mean(axis=1)
u_within.name = 'U_within'

u_between = forecasts_df[MODELS].std(axis=1)
u_between.name = 'U_between'

ensemble_mean = forecasts_df[MODELS].mean(axis=1)
u_temporal = ensemble_mean.rolling(window=WINDOW).std()
u_temporal.name = 'U_temporal'

dims_df = pd.DataFrame({
    'U_within' : u_within,
    'U_between': u_between,
    'U_temporal': u_temporal
}).dropna()

dims_df['CEUI'] = dims_df[['U_within', 'U_between', 'U_temporal']].mean(axis=1)
ceui = dims_df['CEUI']

# ── OLS Regression and Spearman correlation ──────────────────────────────────
import statsmodels.api as sm
from scipy.stats import spearmanr

common_idx = ceui.index.intersection(sigma_rev.index)
y = sigma_rev.loc[common_idx]
x = ceui.loc[common_idx]

def run_ols(y, x, label=''):
    X = sm.add_constant(x)
    res = sm.OLS(y, X).fit(cov_type='HC3')
    rho, p_rho = spearmanr(x, y)
    print(f'\n--- {label} (N={len(y)}) ---')
    print(f'  const     : {res.params.iloc[0]:.4f} (p={res.pvalues.iloc[0]:.4f})')
    print(f'  beta      : {res.params.iloc[1]:.4f} (p={res.pvalues.iloc[1]:.4f})')
    print(f'  R²     : {res.rsquared:.4f}')
    print(f'  rho Spearman: {rho:.4f} (p={p_rho:.4f})')
    return res, rho

res1, rho1 = run_ols(y, x, 'Full sample (QoQ)')

# Sensitivity
covid_excl = pd.period_range('2020Q2', '2020Q4', freq='Q')
mask2 = ~common_idx.isin(covid_excl)
res2, rho2 = run_ols(y[mask2], x[mask2], 'Ex-COVID (2020Q2-Q4) (QoQ)')

crisis_excl = pd.period_range('2020Q1', '2021Q1', freq='Q')
mask3 = ~common_idx.isin(crisis_excl)
res3, rho3 = run_ols(y[mask3], x[mask3], 'Ex-crisis (2020Q1-2021Q1) (QoQ)')

# Save results table
table_content = f"""
Regression results for QoQ Specification:
-------------------------------------------
Full Sample:
  Beta: {res1.params.iloc[1]:.4f} (p={res1.pvalues.iloc[1]:.4f})
  R2: {res1.rsquared:.4f}
  Spearman rho: {rho1:.4f}

Ex-COVID:
  Beta: {res2.params.iloc[1]:.4f} (p={res2.pvalues.iloc[1]:.4f})
  R2: {res2.rsquared:.4f}
  Spearman rho: {rho2:.4f}

Ex-crisis:
  Beta: {res3.params.iloc[1]:.4f} (p={res3.pvalues.iloc[1]:.4f})
  R2: {res3.rsquared:.4f}
  Spearman rho: {rho3:.4f}
"""
with open(os.path.join(PATH_TABLES, 'regression_results_qoq.txt'), 'w') as f:
    f.write(table_content)

# Plot Figure 7: Scatter plot CEUI vs sigma_rev
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(x.values, y.values, color='purple', alpha=0.7, label='Observations')
# Fit line
X_line = np.linspace(x.min(), x.max(), 100)
y_line = res1.params.iloc[0] + res1.params.iloc[1] * X_line
ax.plot(X_line, y_line, color='black', linestyle='--', label='OLS fit')
ax.set_xlabel('CEUI (QoQ)')
ax.set_ylabel('sigma_rev (QoQ)')
ax.set_title(f'Scatter: CEUI vs GDP Revision Volatility (QoQ)\nSpearman rho = {rho1:.3f}')
ax.legend()
ax.grid(True, alpha=0.3)
fig.savefig(os.path.join(PATH_FIGURES, 'fig7_scatter_ceui_sigmarev.pdf'), bbox_inches='tight', dpi=300)
plt.close()

# Plot Figure 2: Ensemble Forecasts
fig, ax = plt.subplots(figsize=(10, 5))
x_dates = forecasts_df.index.to_timestamp()
ax.plot(x_dates, forecasts_df['actual'], color='black', linewidth=2.0, label='GDP realized')
for m in MODELS:
    ax.plot(x_dates, forecasts_df[m], label=m, alpha=0.7, linestyle='--')
ax.set_ylabel('GDP growth rate (% QoQ)')
ax.set_title('Five-Model Ensemble Forecasts vs. Realized GDP growth (QoQ)')
ax.legend()
ax.grid(True, alpha=0.3)
fig.savefig(os.path.join(PATH_FIGURES, 'fig2_ensemble_forecasts.pdf'), bbox_inches='tight', dpi=300)
plt.close()

print("\n=== ANALISIS COMPLETADO ===")
print("Figuras y tablas guardadas en scratch/figures y scratch/tables.")
