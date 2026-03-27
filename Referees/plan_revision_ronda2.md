# 🗺️ Hoja de Ruta: Revisión Entropía (Ronda 2)

Este documento establece la secuencia lógica y cronológica para resolver las inconsistencias detectadas y cumplir con las demandas del referee, basándose en la guía de prompts interna.

## 🔴 FASE 0: Auditoría de Integridad Numérica (Bloque R)
**Objetivo**: Eliminar las contradicciones fatales antes de generar nueva evidencia. Deben ser los mismos números en todas las tablas y secciones.

1. **Tarea R1 & R3: Unificación de la Regresión Central (Tabla 5 vs Tabla 9)**
   * **Problema**: Discrepancia masiva en R2 (0.40 vs 0.86) y Coeficientes (0.008 vs 0.016).
   * **Prompt**: `Auditar el pipeline de datos en risk index.ipynb. Localizar la regresión sigma_rev ~ CEUI en el bloque de Tabla 5 y en el de Tabla 9. Identificar diferencias en la muestra (N=25?), transformaciones de variables o exclusión de observaciones (ej. outliers). Fijar la versión correcta (la que tenga t-stat ~11 si es la muestra completa) y propagarla a ambas tablas.`

2. **Tarea R2: Sincronización de Spearman Rho**
   * **Problema**: 0.63 en Tabla 5 vs 0.796 en Sección 5.8 (Audit).
   * **Prompt**: `Recalcular Spearman Rho para la muestra completa en el Notebook. Actualizar el valor en el Abstract, Tabla 5, Sec 5.8 y Conclusión para que sea idéntico (0.XX).`

## 🟡 FASE 1: Evidencia Empírica "Auditable" (Bloque A)
**Objetivo**: Sustituir afirmaciones narrativas por tablas y figuras reales en el manuscrito.

3. **Tarea 1-R2: Análisis de Influencia Completo (Cook's D)**
   * **Detalle**: Crear Tabla A1 (Cook's D por trimestre) y Leverage Plots.
   * **Prompt**: `Generar tabla de diagnóstico de influencia desglosada por período. Crear figuras Fig A1 (Leverage vs Residuals) y Fig A2 (Cook's D threshold plot). Insertar en Apéndice y referenciar desde Sec 5.8 en lugar del párrafo actual.`

4. **Tarea 2-R2: Integración de Wild Bootstrap en Tabla 5**
   * **Detalle**: Mostrar los intervalos [p5, p95] físicamente en la Tabla 5.
   * **Prompt**: `Modificar la función de generación de Tabla 5 en el Notebook para que calcule e incluya los intervalos Wild Bootstrap. Actualizar el código LaTeX de la Tabla 5 para mostrar estos intervalos entre corchetes debajo de los coeficientes de las 5 especificaciones.`

## 🔵 FASE 2: Coherencia Teórica y de Escala (Bloque B)
**Objetivo**: Validar supuestos y robustez metodológica.

5. **Tarea 7-R2: Validación de la JSD (Jensen-Shannon Divergence)**
   * **Prompt**: `Realizar test numérico de sensibilidad a la aproximación de varianzas homogéneas. Si los resultados son estables, añadir una breve nota en Sec 6.5. Si no, ELIMINAR la afirmación del Remark en Sec 3.4 que afirma falsamente que la Sección 6 lo confirma.`

6. **Tarea 4-R2: Test de Robustez en Escala Bruta**
   * **Prompt**: `Ejecutar la regresión sigma_rev ~ raw_entropy (usando los bits de Shannon sin la normalización 0-100). Comparar R2 y significatividad con la versión normalizada para dar soporte empírico a la elección del "Invariant Filter".`

## 🟢 FASE 3: Estética, Robustez y Pulido (Bloques C y D)
**Objetivo**: Robustez del VAR y refinamiento estilístico.

7. **Tarea 6-R2: Test de Parsimonia del VAR**
   * **Prompt**: `Ejecutar una versión reducida del VAR (menos variables o menos lags) para comprobar si la sobreparametrización (495 parámetros) invalida los resultados. Reportar brevemente en Sec 6.`

8. **Tarea 14-R2: Control por madurez de vintages**
   * **Prompt**: `Evaluar si la menor volatilidad de los periodos recientes (2024Q4, 2025Q1) se debe a que han sido menos revisados (maturity bias). Incluir variable de control en la regresión si es necesario.`

9. **Tarea 5-R2: Barrido Final de Lenguaje Causal**
   * **Prompt**: `Revisar todas las instancias de "predicts", "leads to", "consequence" en las secciones 3, 4 y 5 del .tex y sustituirlas por términos relacionales ("associated with", "precedes").`

10. **Tarea 9, 10, 13-R2: Panel de Correlaciones y Puentes Narrativos**
    * **Detalle**: Matriz de correlación entre modelos y puente Pavia-Entropía.

## 🏁 FASE 4: Verificación Final y Carta Actualizada
11. **Checklist Manual (Bloque E)**: Verificación de consistencia numérica cruzada (Tabla 5 vs Abstract vs Conclusión).
12. **Sincronización de Response Letter**: Reescribir la carta de respuesta para que sea coherente con lo que REALMENTE se ha cambiado en esta segunda ronda de edición.
