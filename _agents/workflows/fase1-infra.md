---
description: Fase 1: Infraestructura de datos y estadísticas descriptivas del ensemble.
---

### Workflow: Fase 1 - Infraestructura (Tareas 9 y 14)

1.  **Tarea 9: Tabla de Estadísticos Descriptivos (Ensemble)**
    - Read `risk index.ipynb` (specifically the cell with forecasts).
    - Aggregate mean, standard deviation, min, and max for each model (VAR, RF, ARIMA, LSTM, DFM).
    - Extract descriptive stats for $\sigma^{\text{rev}}$ and CEUI.
    - Create a LaTeX table in a new `risk_analysis/paper_tex/tables/descriptive_stats.tex` or directly in `main.tex` at the beginning of Section 5.
    - Insert the reference in the text.

2.  **Tarea 14: Cuantificación del Sesgo de Madurez (Vintages)**
    - Read `cntr.csv` if possible or use available summary info.
    - Check the number of revisions for 2024Q4 and 2025Q1 compared to historical average.
    - Add a footnote in the paper mentioning potential bias in the most recent periods.

3.  **Compilar y Verificar**
    - Run `pdflatex` to ensure the new table is rendered correctly.
    - Update `revision_tracking.md`.
