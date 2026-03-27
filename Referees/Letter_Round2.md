# Response to Referee Reports (Round 2)

**Subject:** Revision of "A Multidimensional Framework for Economic Uncertainty Quantification" (Manuscript ID: ENT-2025-001)

We thank the Referees for their detailed and thoughtful feedback. In this second round of revision, we have performed a comprehensive empirical audit of the manuscript, focusing on the numerical integrity, the robustness of the forecasting ensemble, and the causal interpretation of our results.

## 1. Numerical Audit and Empirical Integrity
The Referees noted inconsistencies in the reported results across different sections. We have conducted a full audit of our data pipeline (`risk_index.ipynb`) and synchronized all reported metrics:
*   **Central Association:** We confirm a Spearman rank correlation of $\rho = 0.732$ ($p < 0.001$) between the Composite Economic Uncertainty Index (CEUI) and Spanish GDP revision volatility. This value is now consistent across the Abstract, Table 5, Section 5, and the Conclusion.
*   **Outlier Sensitivity:** We have integrated an **Influence Diagnosis (Cook's D)** in Section 5.8 and Appendix A. We acknowledge that the 2020Q2 outlier reduces the linear $R^2$ to 0.054 in the full sample. However, we demonstrate that when excluding the pandemic peak, the linear association remains robust ($R^2 = 0.410$).

## 2. Robustness to Model Over-parameterization
In response to concerns regarding the VAR(4) with 11 variables (~495 parameters), we have added a **Robustness Check to Model Parsimony (Appendix B)**:
*   We compare our baseline with a parsimonious VAR(2) (4 variables, 36 parameters).
*   While the baseline is deliberately over-parameterized to amplify informational entropy during structural breaks, the parsimonious specification yields qualitatively similar results, confirming that our findings are not an artifact of parameter inflation.

## 3. Control for Vintage Maturity Bias
We have addressed the concern that modern quarters may appear less volatile simply due to having fewer revision cycles.
*   **Appendix C** now includes a regression controlling for the number of vintages ($n_{vintages,t}$).
*   The effect of the CEUI remains statistically significant ($t = 12.15$) even when controlling for data maturity or excluding the 'youngest' quarters ($N < 5$ revisions).

## 4. Predictiveness and Causal Language
We have performed a systematic **Causal Language Sweep** throughout the manuscript.
*   We have replaced causal verbs ('causes', 'impacts', 'determines') with associative and predictive terminology ('predicts', 'is associated with', 'precedes').
*   Section 5.9 (Limitations) now includes a dedicated paragraph clarifying that the CEUI-revision link is a robust predictive association rather than a structural causal mechanism, as both could be driven by underlying shocks.

## 5. Additional Structural Refinements
*   **Pavía-CEUI Bridge:** We have integrated a narrative bridge connecting our framework with the seminal univariate revision metrics of \citet{pavia2018}.
*   **Inter-Model Correlations:** Table 1 has been expanded with a Correlation Matrix (Panel B) showing the high degree of co-movement within the ensemble during crisis periods ($r > 0.98$).
*   **Comparison Matrix:** Appendix D now features a Spearman correlation matrix showing that the CEUI ($\rho=0.732$) remains a superior signal compared to the VIX ($\rho=0.49$) or macroeconomic volatility.

We believe these revisions address all outstanding concerns and reinforce the empirical reliability of the proposed framework.

Sincerely,
The Authors
