---
description: Fase 2: Análisis empírico central y robustez de influencia bajo protocolos de RA Senior.
---

### Workflow: Fase 2 - Análisis Central (Tareas 1, 2 y 3)

> [!IMPORTANT]
> **Protocolo de Rigor Senior RA**: No te limites a borrar datos. Analiza si la estructura de los residuos cambia. Si el horse-race con VIX/EPU no da significatividad, propón una interpretación basada en el "valor de la información" que el CEUI aporta por su descomposición.

1.  **Tarea 1: Análisis de Correlación sin COVID (Influece)**
    - Read `risk index.ipynb` (specifically the CEUI vs $\sigma^{\text{rev}}$ regression).
    - Recompute OLS excluding 2020Q2, 2020Q3, 2020Q4.
    - Compute Cook's D for all periods (2019Q1--2025Q1).
    - Generate a Figure (Apendice) with leverage plots.
    - Write a new section in Section 6 ("Robustness to outliers") reporting coefficients.

2.  **Tarea 2: Bootstrap Completo para Tabla 5 (OLS)**
    - Implement Wild Bootstrap in the notebook.
    - Recompute Table 5 (regressions (1)--(4)) with 1,000 bootstrap iterations.
    - Format Table 5 in LaTeX to include bootstrap confidence intervals.

3.  **Tarea 3: Horse-race con VIX y EPU (Benchmark)**
    - Use `browser_subagent` if needed to find VIX (VIXCLS) or Baker et al. (EPU) data for Spain/Europe.
    - Perform a joint regression $\sigma^{\text{rev}}_t \sim CEUI_t + VIX_t + EPU_t$.
    - Report Wald tests for incremental $R^2$.

4.  **Compilar y Verificar**
    - Ensure all new figures exist in `figures/`.
    - Run final `pdflatex` sequence.
