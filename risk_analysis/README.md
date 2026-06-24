# Academic Paper: A Real-Time Forecasting-Ensemble Index of Economic Uncertainty and the Volatility of GDP Revisions

This directory holds the LaTeX source, compiled documents, figures, and tables for the paper.

## 📝 Abstract

Statistical agencies face a fundamental trade-off between timeliness and accuracy, particularly during economic crises when real-time data becomes structurally disordered. We ask whether the dispersion and instability of a real-time forecasting ensemble anticipate the magnitude of subsequent revisions in official GDP figures, and whether this signal adds information beyond established uncertainty proxies. We construct a Composite Economic Uncertainty Index (CEUI) from three real-time dimensions of a five-model ensemble (VAR, Random Forest, ARIMA, LSTM, and Dynamic Factor Models)—within-model variability, between-model dispersion, and temporal instability—applied to Spanish GDP growth over 2015Q4--2024Q4. The index, computed under an expanding-window protocol that uses only data dated up to each quarter (a quasi-real-time design), is strongly associated with the magnitude of subsequent revisions ($\rho = 0.727$, $p < 0.001$). In a horse-race against the VIX and the Economic Policy Uncertainty (EPU) index for Spain, the CEUI carries predictive information about data quality that the external proxies do not: it remains significant at the 1% level while the VIX and EPU become insignificant once it is included. The results suggest that the internal disorder of a forecasting system is a useful real-time leading indicator of the reliability of official statistics.

---

## 🔬 Theoretical Framework

The paper interprets a forecasting ensemble as an information-processing system. Under information-theoretic foundations (Shannon entropy), ex-ante economic uncertainty is mapped into three observable dimensions of ensemble predictive ambiguity:

1. **Within-Model Uncertainty ($\mathcal{U}^{\text{within}}_t$):** Measures the average predictive noise (standard deviation of trailing out-of-sample forecast errors) across the ensemble components, reflecting ex-ante parameter and shock uncertainty.
2. **Between-Model Dispersion ($\mathcal{U}^{\text{between}}_t$):** Measures the cross-sectional disagreement (standard deviation of point forecasts) among different modeling paradigms (linear benchmarks, multivariate state-space models, non-linear machine learning, recurrent neural networks).
3. **Temporal Instability ($\mathcal{U}^{\text{temporal}}_t$):** Measures the rate at which beliefs are updated over time, captured by the historical volatility of the forecast path.

### The Composite Economic Uncertainty Index (CEUI)
$$\text{CEUI}_t = \tfrac{1}{3}\, \mathcal{U}^{\text{within}}_t + \tfrac{1}{3}\, \mathcal{U}^{\text{between}}_t + \tfrac{1}{3}\, \mathcal{U}^{\text{temporal}}_t$$

Calculated strictly on the raw scale of percentage-point GDP deviations to preserve absolute interpretation and real-time validity (without full-sample normalisation bias).

---

## 📊 Core Empirical Findings

### 1. Revision Volatility Correlation
* The CEUI is strongly correlated with ex-post revision volatility $\sigma^{rev}_t$ with a Spearman rank correlation of **$\rho = 0.727$** ($p < 0.001$).
* The baseline OLS specification yields a slope of **$\hat{\beta} = 0.0198$** (HC3-robust standard error $\approx 0.0064$, $p < 0.001$) and an **$R^2$ of $0.413$**.
* Results are highly robust across subsamples: excluding the COVID-19 pandemic peak yields a slope of $\hat{\beta} = 0.0297$ ($p < 0.001$) and omitting the single most influential observation (2020Q3) yields $\hat{\beta} = 0.0239$ ($p < 0.01$).

### 2. Robustness to In-Sample Uncertainty ($U^{\text{within, train}}$)
* Reconstructing the within-model dimension using only in-sample training residuals yields a robust Spearman correlation of **$\rho = 0.734$** ($p < 0.001$).
* A leave-one-model-out (LOO) stability test shows this correlation is stable within **`[0.732, 0.739]`**, confirming it is not driven by any single model.

### 3. Predictor Horse-Race (CEUI vs. VIX vs. EPU Spain)
When standardising all predictors over the joint evaluation sample ($N = 26$, 2015Q4--2022Q1), OLS horse-race regressions demonstrate:
* The CEUI is the strongest predictor of revision volatility, driving the joint regression $R^2$ up to **$0.565$**.
* In the joint model, the standardized coefficient of the CEUI remains highly significant at the 1% level ($\hat{\beta}_{\text{CEUI}} = 0.1346$, $t = 3.06$), while both the VIX ($\hat{\beta}_{\text{VIX}} = 0.0030$, $t = 0.12$) and the Spanish EPU index ($\hat{\beta}_{\text{EPU}} = -0.0326$, $t = -1.02$) become statistically insignificant.

---

## 📈 Key Figures & Tables inside `paper_tex/`

* **`fig1_revision_volatility.pdf`:** Long-term timeline of Spanish GDP revision volatility $\sigma^{rev}_t$ showing spikes during GFC (1.5x), Sovereign Debt (1.7x), and COVID-19 (2.8x).
* **`fig5_ceui_dimensions.pdf`:** Path of the three raw uncertainty dimensions and the composite index.
* **`fig7_scatter_ceui_sigmarev.pdf`:** Scatter plot and OLS fit line of CEUI vs. revision volatility.
* **`tab_horserace.tex`:** Regression results for the Horse-Race specifications.
* **`tab7_sensitivity.tex`:** Regression sensitivity across different subsamples.
* **`tab_robustness_norm.tex`:** Regime agreement concordance matrix across scaling methods.
