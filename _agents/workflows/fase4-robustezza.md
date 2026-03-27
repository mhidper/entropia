---
description: Fase 4: Robustez de especificaciones e inconsistencias técnicas.
---

### Workflow: Fase 4 - Robustezza (Tareas 6 y 8)

1.  **Tarea 6: Justificación del Especificación VAR(4)**
    - Perform a BIC/AIC test for VAR(k) in `risk index.ipynb` (comparing k=1, 2, 3, 4).
    - Insert a paragraph in Section 4.3 ("Econometric Specification") explaining the choice of k=4 and how PCA or DFM mitigates overparameterization.
    - Reference the resilience of the 11-variable system in Section 4.5.

2.  **Tarea 8: Consistencia de Umbrales (Threshold Stability)**
    - Identify all mentions of "Regime", "Threshold", "Elevated", "High" in `main.tex`.
    - Correct all values in Section 5.5, 7.1, and Table 8 to use the consolidated thresholds (55/62 or 40.55/66.40 based on the final decision).
    - Ensure Figure 2 shows the same thresholds.

3.  **Compilar y Verificar**
    - Run `pdflatex` to resolve references.
    - Check the Table 10 ("Threshold Stability - Bootstrap") for final synchronization.
