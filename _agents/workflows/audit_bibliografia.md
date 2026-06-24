---
description: Audita la bibliografía (PDFs vs main.tex) y sugiere nuevas citas.
---

### Bibliografía Audit Agent

Este agente automatiza la verificación de integridad entre los archivos PDF de la carpeta `risk_analysis/bibliografía` y las entradas en `bib.bib` y `main.tex`.

#### Pasos para ejecutar:

1.  **Asegúrate de tener instalada la librería `pypdf`**:
    ```bash
    pip install pypdf
    ```

2.  **Ejecuta el script de auditoría**:
    ```bash
    python _agents/scripts/bib_audit.py
    ```

3.  **Revisa los resultados**:
    El agente generará un informe detallado en `risk_analysis/audit_bibliografia_report.md`.

#### Qué hace este agente:

*   **Verificación Cruzada**: Compara los autores y el año detectados en los metadatos de los PDFs con las entradas de BibTeX.
*   **Detección de Inconsistencias**: Avisa si los PDFs en la carpeta no tienen una clave correspondiente en `bib.bib`.
*   **Identificación de Referencias Internas**: Escanea la sección "References" de cada PDF para identificar obras que se citan allí pero que aún no están incorporadas en el proyecto "Entropía".
*   **Sugerencia de Citas**: Genera una lista de candidatas a ser incorporadas en futuras revisiones.
