# GUIA DE PROMPTS - RONDA 2
Correcciones pendientes, incompletas e inconsistencias nuevas detectadas
**"A Multidimensional Framework for Economic Uncertainty Quantification"**

> **ATENCION**: Este documento incluye 3 errores críticos que deben resolverse ANTES de cualquier otro cambio. Un referee rechazaria el paper inmediatamente si detecta las inconsistencias numéricas actuales.

---

## 🔴 BLOQUE 0: ERRORES CRITICOS (Resolver primero)
Estos tres problemas son inconsistencias numéricas internas que invalidan la credibilidad del paper. Deben resolverse ANTES de cualquier otro cambio, porque los demás prompts dependen de que los números base sean correctos.

### R1: Inconsistencia R-cuadrado entre Tabla 5 y Tabla 9
*   **El problema**: La Tabla 5 (entropy_regression), columna (1), reporta la regresión `sigma_rev ~ CEUI` con $R^2 = 0.40$. La Tabla 9 (horserace), columna (1), reporta EXACTAMENTE la misma regresión (CEUI Only, misma muestra, misma variable dependiente) con $R^2 = 0.860$. Es imposible que la misma regresión produzca dos $R^2$ diferentes.
*   **Acción**: Diagnóstico y corrección inmediata. Los números deben ser consistentes.

### R2: Inconsistencia Spearman rho (0.63 vs 0.796)
*   **El problema**: La Tabla 5, columna (5), reporta Spearman $\rho = 0.63$ ($p<0.001$) para la muestra completa. Pero la Sección 5.8 (ex-COVID analysis) dice: *"Spearman rank correlation of rho = 0.704 (compared to rho = 0.796 for the full sample)"*. El 0.796 contradice el 0.63 de la Tabla 5. Ambos se refieren a la muestra completa.
*   **Acción**: Verificar y unificar en todas las menciones del paper y el abstract.

### R3: Inconsistencia coeficiente CEUI (0.008 vs 0.0162)
*   **El problema**: El coeficiente de CEUI sobre `sigma_rev` es 0.008 ($t=3.81$) en Tabla 5 y 0.0162 ($t=11.90$) en Tabla 9. Un factor 2x de diferencia con t-stats tan dispares es inaceptable.
*   **Acción**: Auditar el pipeline completo.

---

## 🟡 BLOQUE A: TAREAS CRITICAS PENDIENTES (Ronda 1 incompleta)

### TAREA 1 (revisada): Análisis de influencia COMPLETO
*   **Qué falta**: La Sección 5.8 actual menciona un Cook's D pero no presenta evidencia auditable (tablas, figuras, leverage plots).
*   **Donde insertar**: Tabla A1 en el Apéndice y figuras Fig A1/A2. Referenciar desde el texto principal.

### TAREA 2 (revisada): Wild Bootstrap IMPLEMENTADO en Tabla 5
*   **Qué falta**: El texto afirma que se hizo, pero la Tabla 5 no muestra los intervalos ni p-values bootstrap.
*   **Criterio de aceptación**: La Tabla 5 debe mostrar visualmente los intervalos bootstrap [entre corchetes].

### TAREA 7: Verificación numérica JSD + corregir Remark
*   **Qué falta**: El Remark afirmaba falsamente que la Sección 6 confirmaba la insensibilidad al supuesto de varianza homogénea, cuando la Sección 6 no contenía tal test.
*   **Acción**: Ejecutar el test numérico real y actualizar el Remark o la sección 6.

---

## 🔵 BLOQUE B: TAREAS MUY RECOMENDABLES

### TAREA 4 (completar): Regresión en escala bruta
*   Comparar la regresión `sigma_rev ~ raw_entropy` con la versión normalizada para justificar empíricamente el uso del "Invariant Filter".

### TAREA 5 (completar): Moderación lenguaje causal
*   Aunque se cambió el Abstract, persisten términos deterministas en el cuerpo del texto (Secciones 3, 4 y 5).

### TAREA 6 (completar): Sobreparamatrización VAR
*   Abordar la robustez del VAR de 495 parámetros frente a versiones más parsimoniosas.

---

## 🏁 BLOQUE D: SECUENCIA DE EJECUCION (Fases)
1.  **Fase 0: Emergencias** (R1, R2, R3).
2.  **Fase 1: Análisis empírico** (Tareas 1 y 2).
3.  **Fase 2: Coherencia teórica** (Tareas 7 y 4).
4.  **Fase 3: Robustez adicional** (Tareas 6 y 14).
5.  **Fase 4: Redacción y pulido** (Tareas 5, 10, 9, 13).

---

## ✅ BLOQUE E: CHECKLIST DE VERIFICACION FINAL
*   Consistencia numérica absoluta en todas las tablas.
*   Evidencia de Cook's D en el apéndice.
*   Intervalos bootstrap visibles en Tabla 5.
*   Actualización de la "Response Letter" para que sea honesta con los cambios realizados.
