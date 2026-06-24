# 📊 ENTROPÍA: Composite Economic Uncertainty Index (CEUI)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LaTeX](https://img.shields.io/badge/LaTeX-academic%20paper-green.svg)](https://www.latex-project.org/)

This repository hosts the replication code, vintage data pipeline, and LaTeX manuscript for the paper:
**"A Real-Time Forecasting-Ensemble Index of Economic Uncertainty and the Volatility of GDP Revisions"**

Targeted for submission to *Empirical Economics* (Springer Nature).

---

## 🎯 Project Overview

The **Composite Economic Uncertainty Index (CEUI)** is a model-based, multi-dimensional gauge of real-time macroeconomic uncertainty. It is constructed from the internal properties of a heterogeneous five-model forecasting ensemble. Rather than measuring generalized risk (like the VIX or news-based EPU indices), the CEUI directly measures the ex-ante **informational disorder** of the economic environment to predict the ex-post volatility of GDP data revisions ($\sigma^{rev}_t$).

### 🔬 The 3 Dimensions of the CEUI
1. **Within-Model Uncertainty ($\mathcal{U}^{\text{within}}_t$):** The average trailing forecast noise of the individual models, capturing their intrinsic predictive confidence.
2. **Between-Model Dispersion ($\mathcal{U}^{\text{between}}_t$):** The real-time disagreement (empirical standard deviation) among different modeling paradigms.
3. **Temporal Instability ($\mathcal{U}^{\text{temporal}}_t$):** The rate at which the ensemble updates its beliefs between consecutive periods, captured by the historical volatility of the forecast path.

---

## 📂 Repository Structure

```
Entropía/
├── src/                                    # Main replication pipeline
│   ├── risk_index_v2.py                    # Main YoY Python pipeline (run this to regenerate all tables/figures)
│   ├── risk_index_v2.ipynb                 # Jupyter version of the YoY pipeline
│   └── risk_index_v2_QoQ.py                # Robustness script for the QoQ specification
├── risk_analysis/                         # Academic documentation & LaTeX source
│   └── paper_tex/                          # LaTeX project
│       ├── main_final.tex                  # Main paper text
│       ├── main_final.pdf                  # Compiled PDF version
│       ├── cover_letter.tex                # Cover letter for Empirical Economics
│       ├── cover_letter.pdf                # Compiled Cover Letter
│       ├── figures/                        # Generated charts (.pdf and .png)
│       └── tables/                         # Generated LaTeX tables (.tex)
├── replica_pavia_2018/                     # Replication base database
│   └── datos/
│       └── cntr2.xlsx                      # Real-time CNTR vintage database (INE)
├── claims_new.txt                          # Single source of truth for paper statistics
├── README.md                               # This file
└── claims.txt                              # Old stats log
```

---

## 🤖 Ensemble Models & Indicators

The forecasting ensemble utilizes 10 indicator variables (GDP growth + 9 monthly indicators) to predict Spanish GDP in real time under a rolling, expanding-window protocol (minimum 20 training quarters):

### The 5 Estimating Models
1. **Vector Autoregression (VAR):** Linear multivariate framework. Lags selected recursively via AIC (max 4).
2. **Random Forest (RF):** Non-linear machine learning algorithm. Trained with 100 trees, unlimited depth, and fixed random seed (`random_state=42`).
3. **ARIMA:** Univariate time-series baseline. Configured with a fixed ARIMA(4,0,1) specification.
4. **LSTM (Long Short-Term Memory):** Recurrent neural network capturing temporal sequence dependencies. Univariately trained with sequence length of 8 and 16 hidden units, with early stopping.
5. **Dynamic Factor Model (DFM):** Condenses the indicator set into a single common factor using Kalman filtering.

### The 9 Monthly Indicators
* **Social Security Affiliations** (Employment proxy)
* **Industrial Production Index (IPI)** for Manufacturing
* **Synthetic Construction Indicator** (Investment)
* **Synthetic Capital Goods Indicator** (Investment)
* **Real Interior Sales of Large Enterprises** (Consumption & Services)
* **Manufacturing Purchasing Managers' Index (PMI)** (Expectations)
* **OECD Composite Leading Indicator (CLI)** for Spain (Expectations)

---

## 📈 Canonical Metrics (YoY Specification)

The canonical run of the pipeline produces the following benchmark parameters (saved in `claims_new.txt`):

### Model Accuracy & Resilience (2019Q1--2024Q4)
* **LSTM:** MAE full = 2.15 pp | MAE ratio (Crisis/Normal) = 6.49x | Resilience = 0.154
* **Random Forest:** MAE full = 2.18 pp | MAE ratio = 10.33x | Resilience = 0.097
* **Dynamic Factor Model:** MAE full = 2.42 pp | MAE ratio = 15.83x | Resilience = 0.063
* **ARIMA (4,0,1):** MAE full = 4.46 pp | MAE ratio = 36.30x | Resilience = 0.028
* **VAR:** MAE full = 7.10 pp | MAE ratio = 26.39x | Resilience = 0.038

### Core Regression Results
* **Spearman Rank Correlation ($\rho$):** **0.727** ($p < 0.001$) between the ex-ante CEUI and ex-post revision volatility $\sigma^{rev}_t$.
* **OLS Slope Coefficient ($\hat{\beta}$):** **0.0198** ($p < 0.001$, HC3-robust standard errors).
* **Baseline Goodness-of-Fit ($R^2$):** **0.413**.
* **Robust In-Sample Variant ($U^{\text{within, train}}$):** Spearman correlation of **0.734** (stable within `[0.732, 0.739]` under a leave-one-model-out test).

---

## 🚀 Reproduction Instructions

### Requirements
```
python >= 3.10
pandas >= 1.4.0
numpy >= 1.22.0
scikit-learn >= 1.0.0
statsmodels >= 0.13.0
tensorflow >= 2.8.0
matplotlib >= 3.5.0
openpyxl (for Excel reading)
```

### Quick Run
To run the canonical pipeline, regenerate all tables, figures, and populate `claims_new.txt`:
```bash
# Clone the repository
git clone https://github.com/mhidper/entropia.git
cd entropia/src

# Execute main pipeline
python risk_index_v2.py
```
To run the quarter-on-quarter (QoQ) robustness specification:
```bash
python risk_index_v2_QoQ.py
```

### LaTeX Compilation
To compile the manuscript with the updated tables and cover letter:
```bash
cd ../risk_analysis/paper_tex
pdflatex main_final.tex
pdflatex cover_letter.tex
```

---

## 📚 Declarations & Academic Information

* **JEL Classification:** C53, C82, E01, E32.
* **Keywords:** Economic Uncertainty, Forecast Combinations, Informational Entropy, GDP Revisions, Real-time Data.
* **Funding:** No funding was received for this study.
* **Conflicts of Interest:** None.
* **Replicability:** Data and code pipeline are open-source. Manuel Hidalgo-Pérez is the lead author and investigator.