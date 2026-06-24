# Instrucciones de revisión — Paper CEUI (Empirical Economics)

> **Para:** la IA de código ("cortita").
> **De:** revisión tipo referee de Empirical Economics.
> **Objetivo:** que cada cifra y cada afirmación del paper se correspondan exactamente con lo que genera `risk_index_v2.py`. No se trata de cambiar el resultado (ρ = 0.729 es sólido), sino de eliminar las contradicciones que provocarían un rechazo por falta de fiabilidad.
> **Archivos de referencia:** `main_final.tex`, `risk_index_v2.py`, y las tablas `.tex` generadas.

**Convención:** cada tarea indica si es **[PROSA]** (editar `main_final.tex`) o **[CÓDIGO]** (tocar `risk_index_v2.py` y regenerar). Donde hace falta una decisión de Manuel, está marcado **[DECISIÓN]**.

---

## BLOQUE A — Coherencia código ↔ paper (lo que más pesa para el rechazo)

### A1. [DECISIÓN + PROSA/CÓDIGO] El reclamo de "tiempo real estricto" no es literalmente cierto

**Qué pasa.** En `risk_index_v2.py`:
- Línea ~614: `gdp_series = df_growth.ffill(axis=1).iloc[:, -1].dropna()` → el PIB usado es el **último vintage** (dato final revisado), no el dato que se conocía en cada momento.
- Los modelos se entrenan con ese PIB final (`gdp_train = train_data['PIB']`).
- Línea ~1063: `errors_df = forecasts_df[MODELS].subtract(forecasts_df['actual'], axis=0)` y `U_within = errors_df.rolling(4).std()`. Como `actual` = PIB final, **`U_within` en el trimestre t usa la realización final de t, que no se conoce en t.**

**Por qué importa.** El abstract, la introducción, la Sección 3 ("Each measure uses only information available up to quarter t, ensuring strict real-time validity") y la nota al pie del protocolo rolling ("No look-ahead information or future revisions are used at any step") afirman tiempo real estricto. Eso es la novedad del paper. El §6.1 actual solo neutraliza el look-ahead de la **normalización**, no este canal del **vintage**. Un referee de EE lo detectará.

**Opciones (elige una con Manuel):**

- **Opción A (recomendada, mínimo riesgo):** reencuadrar honestamente como *quasi-real-time / pseudo-real-time* y añadir una salvaguarda. Concretamente:
  1. **[PROSA]** Sustituir "strict real-time" / "no look-ahead at any step" por una formulación precisa (ver texto propuesto abajo). El protocolo es de **ventana expansiva sobre el último vintage de datos**, que es práctica habitual y aceptable, pero NO es point-in-time.
  2. **[PROSA]** Distinguir explícitamente las dos fuentes de look-ahead: (i) normalización de pleno muestreo — ya resuelta en §6.1; (ii) uso del vintage final — ahora reconocida y acotada.
  3. **[CÓDIGO, opcional pero muy recomendable]** Añadir un check de robustez que recalcule `U_within` SIN usar el dato final: usar la **varianza de los residuos de cada modelo dentro de la ventana de entrenamiento** (disponible en t) o los errores contra el **vintage flash** en lugar del final. Reportar el ρ resultante. Si se mantiene alto, es la mejor defensa posible.

- **Opción B (más limpia conceptualmente, más trabajo):** recalcular `U_within` como la **desviación típica predictiva de cada modelo** (intervalos/residuos del entrenamiento), que SÍ está disponible en tiempo real y SÍ coincide con lo que describe la Proposición 1.(i). Esto haría que código y teoría coincidan exactamente. Cambia el ρ de cabecera → requiere correr de nuevo todo el pipeline una sola vez (disciplina de run canónico) y propagar el nuevo número.

**Texto de prosa propuesto** (reemplaza la frase de la nota al pie del protocolo rolling, ~línea 162):
> *"The ensemble is estimated under an expanding-window protocol: for each quarter t the models are re-estimated using only observations dated up to t−1. Following standard practice in the real-time forecasting literature, the exercise uses the latest available data vintage rather than point-in-time vintages; we therefore describe the index as quasi-real-time. The dependent variable, by contrast, is computed from the genuine vintage triangle. Section 6.1 shows that the headline result is invariant to the normalisation choice, and Appendix [X] reports a stricter variant in which the within-model dimension is computed without using the final realisation of the target quarter."*

**Texto propuesto** para la frase de Sección 3 (~línea 196, "ensuring strict real-time validity"):
> *"Each measure is backward-looking and computed under the expanding-window protocol described in Section 4. The between-model and temporal dimensions use only forecasts available at t; the within-model dimension is discussed in Appendix [X], where we also report a variant that avoids any use of the target's final realisation."*

---

### A2. [PROSA] El Apéndice C de especificaciones contradice al código (y al texto principal)

El Apéndice "Model Specifications and Resilience" (~líneas 449–466) está **desfasado**. La verdad del código es:

| Modelo | Código (`risk_index_v2.py`) | Apéndice C dice (MAL) | Texto principal §4 |
|---|---|---|---|
| VAR | AIC hasta 4 lags, sistema de 10 var. (`select_order(maxlags=4).aic`, l.700) | "4 lags fijos y 10 variables" | correcto (AIC hasta 4) |
| ARIMA | **ARIMA(4,0,1) fijo** (`order=(4,0,1)`, l.712) | "ARIMA automático, hasta orden 3" | correcto |
| RF | **100 árboles, sin tope de profundidad**, `random_state=42`, 6 lags GDP + predictores (l.736) | "50 árboles, prof. máx 3" | casi (ver A3) |
| LSTM | **1 capa, 16 unidades, seq=8**, epochs=50, batch=8, patience=5 (l.662–668) | "2 capas 24+24, seq 6, dropout 20%" | correcto |
| DFM | **1 factor** (`factors=1, factor_orders=1`, l.789) | "2 factores" | correcto |

**Tarea:** reescribir el Apéndice C para que coincida con el código y con la nota al pie de §4. Texto propuesto:

> 1. **VAR:** sistema de 10 variables; el número de lags se selecciona recursivamente por AIC hasta un máximo de 4.
> 2. **Random Forest:** 100 árboles, semilla fija (`random_state=42`); usa 6 retardos del crecimiento del PIB más los predictores contemporáneos.
> 3. **ARIMA:** especificación fija ARIMA(4,0,1) sobre el crecimiento del PIB.
> 4. **LSTM:** una capa LSTM de 16 unidades, longitud de secuencia de 8 trimestres, entrenada con early stopping (patience = 5).
> 5. **DFM:** un único factor común estimado por filtro de Kalman y algoritmo EM.

> ⚠️ Quitar las ecuaciones del Apéndice C que afirmen "2 common factors" en el DFM y "two LSTM layers". Dejar solo lo que corresponde a la implementación real.

---

### A3. [PROSA] Corregir hiperparámetros del RF en la nota al pie de §4

En la nota al pie del protocolo (~línea 162) dice: *"Random Forest is trained with 100 trees, a maximum depth of 3, and minimum split samples of 2."*

El código (l.736) es `RandomForestRegressor(n_estimators=100, random_state=42)` → **sin `max_depth`** (profundidad ilimitada por defecto) y sin fijar `min_samples_split`.

**Opción 1 [PROSA]:** corregir el texto → *"100 trees with default depth and a fixed random seed."*
**Opción 2 [CÓDIGO] [DECISIÓN]:** si Manuel prefiere árboles regularizados (depth=3 es razonable con N pequeño), añadir `max_depth=3, min_samples_split=2` al código y **volver a correr el pipeline**. Si se hace esto, hay que revalidar ρ y todas las cifras dependientes.
> Recomendación: Opción 1 (corregir texto) salvo que quieras tocar resultados; lo barato es alinear la prosa con el código.

---

### A4. [PROSA] `U_within`: la descripción teórica no coincide con el cálculo

- Sección 3 (~línea 191) y Proposición 1.(i): describen *within* como *"average log-predictive standard deviation, directly observable from the confidence intervals produced by each model."*
- Código (l.1063–1066): `U_within = std móvil (4 trim.) de los errores de pronóstico (forecast − actual)`, promediada entre modelos. **No hay intervalos de confianza** (RF y LSTM no los producen aquí).

**Tarea [PROSA]:** describir `U_within` por lo que de verdad calcula. Texto propuesto para §3:
> *"Within-model variability ($\mathcal{U}^{within}_t$): the average, across models, of the trailing 4-quarter standard deviation of each model's recent forecast errors. It proxies how noisy each model has been about its own predictions. (As discussed in Appendix A, under a Gaussian approximation this dispersion is monotonically related to the average predictive entropy of the ensemble; the operational measure is the error-based standard deviation, not the theoretical quantity.)"*

> Mantener el Apéndice A como **motivación** (ya dice explícitamente que es aproximación, no identidad), pero asegurar que la frase de §3 no prometa "intervalos de confianza". Coherencia con el principio de transparencia teoría→proxy que ya aplicáis.

---

## BLOQUE B — Errores numéricos verificables (los revisores los pillan)

### B1. [PROSA] Rango de correlaciones inventado/desfasado

Texto (~línea 164): *"The pairwise correlations between forecasts range from −0.009 to 0.871."*

La tabla real (`tabla1_ensemble.tex`, Panel B) tiene mínimo **0.096** (VAR–LSTM) y máximo **0.819** (RF–DFM). Ni −0.009 ni 0.871 existen.

**Tarea:** sustituir por *"range from 0.10 to 0.82"* (o las cifras exactas 0.096–0.819). Verificar contra el Panel B antes de fijar el número.

---

### B2. [PROSA] Frase autocontradictoria sobre "regime agreement"

Sección 6 (~línea 326): primero dice *"the discrete regime agreement varies significantly (from 18.9% to 59.5%)"* y a continuación concluye *"The high degree of regime agreement across normalization techniques suggests..."*. Es contradictorio: 18.9 % es **bajo**.

**Tarea:** reemplazar la frase final por algo coherente con los datos (`tab_robustness_norm.tex`):
> *"Although the continuous correlations across normalisation methods are high, the discrete regime classification is sensitive to the chosen scale (agreement ranges from 18.9% to 59.5% relative to the min-max baseline). This sensitivity reinforces our decision to rely on the continuous, unscaled index for all core regressions rather than on discrete regime thresholds."*

---

### B3. [PROSA] Tabla 1 Panel A mal etiquetada como "QoQ"

`tabla1_ensemble.tex` (Panel A) lleva el encabezado **"Summary Statistics (QoQ % Growth)"**, pero el baseline del paper es **YoY** (§3, línea 117), y las cifras (PIB min −21.45, max 19.77) son consistentes con YoY, no con QoQ.

**Tarea [CÓDIGO]:** en el bloque que genera `tabla1_ensemble.tex`, cambiar el rótulo del Panel A a **"Summary Statistics (YoY % Growth)"** (o "% Growth" a secas). Verificar que la serie usada es efectivamente la YoY del baseline.

---

### B4. [CÓDIGO] Run canónico único: `claims_new.txt` vacío y `regression_results_qoq.txt` desfasado

- `claims_new.txt` está **vacío**. Debe ser el ancla canónica de TODAS las cifras del paper.
- `regression_results_qoq.txt` da β=0.0082, p=0.0386, ρ=0.7745; pero `tab_robustness_qoq.tex` y el texto dan β=0.0081, p=0.0392, ρ=0.777. Provienen de runs distintos.

**Tarea:**
1. Hacer que el pipeline **vuelque a `claims_new.txt`** todas las cifras de cabecera: ρ baseline, β/SE/t/p/R² baseline, las 4 filas de sensibilidad YoY, las 6 filas del horse-race, ρ y β QoQ, factores de amplificación, umbrales, LOO, pesos, normalización.
2. Regenerar `regression_results_qoq.txt` en el **mismo run** que las tablas, para que 0.0081/0.0392/0.777 sean idénticos en los tres sitios (txt, tabla, prosa).
3. Tras el run, **una pasada de verificación**: cada número inline del `.tex` debe existir en `claims_new.txt`.

---

## BLOQUE C — Claridad y encuadre (generan preguntas del revisor)

### C1. [DECISIÓN + PROSA] Justificación del corte muestral del horse-race (2022Q1)

La nota de `tab_horserace` dice que el corte en **2022Q1 (N=26)** se debe a *"periods where the CEUI, VIX and EPU are jointly available."* Pero VIX y el EPU español de policyuncertainty.com llegan mucho más allá de 2022. La razón real probablemente es la **madurez de σ_rev** (necesita ventana de 2 años hacia adelante; el último trimestre con ventana completa es ~2022Q4).

**Problema de coherencia:** el baseline usa σ_rev hasta 2024Q4 (N=37, con vintages inmaduros) pero el horse-race corta en 2022Q1. El revisor preguntará por qué dos criterios distintos.

**Tarea [DECISIÓN]:** confirmar la causa real del corte y:
- Si es madurez de σ_rev → cambiar la nota a esa explicación y **aplicar el mismo criterio de madurez al baseline** (o justificar por qué el baseline puede incluir vintages inmaduros, apoyándose en el Apéndice de "Vintage Maturity Control").
- Si es disponibilidad de datos → verificar las fechas finales reales de VIX/EPU y dejar constancia.

---

### C2. [PROSA] σ_rev de los trimestres recientes (madurez) — subir el caveat al cuerpo

El Apéndice de "Vintage Maturity Control" ya muestra que el resultado sobrevive al control por madurez. Pero en los **resultados principales** (§5) no se advierte que los últimos ~8 trimestres tienen σ_rev basada en una ventana de revisión incompleta.

**Tarea:** añadir una frase en §5 remitiendo al apéndice de madurez:
> *"For the most recent quarters the two-year revision window is not yet complete; Appendix [X] shows that controlling for vintage maturity leaves the association essentially unchanged ($\hat\beta = 0.0187$, $t = 2.89$)."*

---

### C3. [PROSA] Lenguaje causal vs. asociación

El paper alterna "is associated with" (correcto) con "predicts" / "leading indicator" (sugiere causalidad). Las Limitaciones ya mencionan el confusor común, pero el cuerpo se inclina a veces a lo causal.

**Tarea:** revisar abstract, introducción y discusión para que las afirmaciones fuertes sean de **asociación/predicción in-sample**, no de causalidad. Mantener "leading indicator" solo donde se justifique por la disponibilidad temporal real (ver A1).

---

### C4. [DECISIÓN + PROSA] Párrafos DSGE en Discusión y Conclusión

Hay dos pasajes (Discusión ~línea 347 y Conclusión ~línea 360) que proyectan el índice hacia modelos DSGE. Como el paper DSGE está fuera de alcance, un referee de EE puede leerlo como relleno especulativo.

**Tarea [DECISIÓN]:** recortar a **una sola frase** de "future research" al final de la Conclusión y eliminar el párrafo DSGE de la Discusión, o dejarlo muy breve. Decisión de Manuel.

---

## BLOQUE D — Cosméticos (rápidos)

- **D1. [CÓDIGO]** `tab5_ceui_regimes.tex`: decimales inconsistentes (`0.3`, `0.087`, `0.403`). Unificar a 3 decimales (`0.300`).
- **D2. [PROSA]** `tab4_model_performance.tex` se titula "(2019Q1–2024Q4)" pero las columnas son "pre/post-COVID" y la Figura 4 habla de "crisis/normal". Unificar terminología (pre/post-COVID en ambos, o crisis/normal en ambos).
- **D3. [CÓDIGO/LIMPIEZA]** `tab6_ceui_descriptive.tex` y `tabla2_amplification.tex` **no se referencian** en `main_final.tex`. Decidir: incluirlos o borrarlos para no dejar tablas huérfanas en el repo.
- **D4. [PROSA]** Verificar que todas las `\includegraphics` apuntan a `.pdf` existentes (en el repo hay `.png`). Confirmar que la compilación final encuentra los `.pdf`.

---

## Orden de ejecución sugerido

1. **A1** (decisión de Manuel sobre tiempo real — es lo que define el encuadre de todo lo demás).
2. **A2, A3, A4** (alinear especificaciones y descripción de dimensiones con el código).
3. **B4** (run canónico único → `claims_new.txt` poblado), y **sobre ese run** corregir **B1, B2, B3**.
4. **C1, C2, C3, C4** (claridad y encuadre).
5. **D1–D4** (cosméticos) y compilación final limpia (sin refs rotas ni overfull).

## Checklist final antes de enviar a Empirical Economics

- [ ] Cada cifra inline del `.tex` aparece idéntica en `claims_new.txt`.
- [ ] Apéndice C, nota al pie de §4 y código dicen lo mismo de los 5 modelos.
- [ ] El reclamo de tiempo real es defendible y consistente con el código (A1 cerrado).
- [ ] `U_within` se describe por lo que calcula (A4).
- [ ] Rango de correlaciones, frase de regímenes y rótulo Panel A corregidos.
- [ ] Corte muestral del horse-race justificado y coherente con el baseline.
- [ ] LaTeX compila sin referencias rotas ni overfull boxes.
