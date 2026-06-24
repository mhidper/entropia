# Instrucciones de revisión — RONDA 2 (Paper CEUI, Empirical Economics)

> [!NOTE]
> Para la IA de código ("cortita"). Esta ronda parte de la auditoría de la versión ya corregida. **Lo de modelos (Apéndice C), el rango de correlaciones (0.10–0.82) y la honestidad de §3 (l.196) están BIEN; no los toques.** Quedan abiertos seis puntos. Uno de ellos (el ρ) ha empeorado respecto a la versión anterior, así que va primero.
>
> Archivos: `main_final.tex`, `risk_index_v2.py`, `tabla1_ensemble.tex`, `claims_new.txt`.

---

## P0 — CRÍTICO: el ρ del baseline aparece con DOS valores en el propio paper

**Qué pasa.** El nuevo apéndice del `U_within_train` (l.566) dice *"slightly higher than the baseline $\rho = 0.727$"*, pero el resto del paper dice **0.729**:
- Abstract (l.48): `\rho = 0.729`
- Introducción (l.75): `\rho = 0.729`
- Resultados (l.229): `\rho = 0.729`
- §6.1 (l.296): *"The headline association ($\rho = 0.729$)"* y *"still yields $\rho = 0.729$, identical to the raw-index value"*
- `tab7_sensitivity.tex` (fila Full sample): `0.729`
- Apéndice nuevo (l.566): baseline = **0.727**

Es el mismo objeto (Spearman del CEUI raw vs $\sigma^{rev}$) impreso con dos números. Un referee que pase del §5 al apéndice lo ve. Causa raíz: **no existe fuente única** (`claims_new.txt` está vacío).

**Tarea (en este orden):**
1. **[CÓDIGO]** Ejecutar el pipeline **una sola vez** con las semillas fijadas ANTES del entrenamiento del LSTM (ya está en l.641–645; confirmar que no se re-siembra después). Ese run es el canónico.
2. **[CÓDIGO]** Hacer que `claims_new.txt` se **rellene de verdad** en ese run (ahora sale con 0 líneas). Debe contener, como mínimo: `rho_baseline`, `beta_baseline`, `se_baseline`, `t_baseline`, `p_baseline`, `R2_baseline`, las 4 filas de sensibilidad YoY, las 6 del horse-race, `rho_qoq`/`beta_qoq`, `rho_within_train`, factores de amplificación, umbrales p60/p90, LOO y pesos. Verificar que el archivo del proyecto NO está en otra ruta (`src/claims_new.txt` ≠ `claims_new.txt` raíz): apuntar al que lee la compilación.
3. **[PROSA]** Tomar el `rho_baseline` de `claims_new.txt` y **propagarlo idéntico** a: abstract (l.48), intro (l.75), resultados (l.229), §6.1 (l.296 ×2), `tab7_sensitivity.tex`, y reescribir la frase del apéndice (l.566) para que el "baseline" sea ese mismo número.
   - Si el canónico resulta ser **0.729**, entonces en el apéndice `\rho = 0.727` pasa a comparar `\rho_{within,train}` contra `0.729`.
   - Si resulta ser **0.727**, hay que cambiar los SEIS sitios anteriores a 0.727 (y revisar que β/R²/t de `tab7` correspondan a ese mismo run).
4. **[VERIFICACIÓN]** `grep -noE "0\.72[0-9]" main_final.tex` debe devolver **un único** valor de baseline en todos los contextos no-QoQ.

> Regla de oro: ningún número del `.tex` puede existir si no está en `claims_new.txt`.

---

## P1 — Completar el reencuadre "quasi-real-time" (está a medias)

La nota de §4 (l.162) y el apéndice ya dicen "quasi-real-time", pero estos cinco sitios siguen prometiendo tiempo real estricto. Hay que bajar el tono para que el abstract no contradiga a la nota.

**[PROSA] Sustituciones exactas (buscar → reemplazar):**

1. **Abstract (l.48).**
   - Buscar: `The index, computed strictly from information available in real time, is strongly associated`
   - Poner: `The index, computed under an expanding-window protocol that uses only data dated up to each quarter (a quasi-real-time design), is strongly associated`

2. **Introducción (l.108).**
   - Buscar: `is computable at the moment the flash estimate is published, contains no look-ahead bias, and is designed specifically`
   - Poner: `is computable at the moment the flash estimate is published, is free of the full-sample normalisation bias common to composite indices, and is designed specifically`

3. **§3 (l.199).**
   - Buscar: `Because we seek an index that is strictly valid in real time, avoiding any look-ahead bias that arises from full-sample normalisation, we define the baseline CEUI`
   - Poner: `Because we seek an index that avoids the look-ahead bias arising from full-sample normalisation, we define the baseline CEUI`

4. **§6.1 (l.296).**
   - Buscar: `The headline association ($\rho = 0.729$) is therefore established entirely in real time.`
   - Poner: `The headline association ($\rho = \texttt{[CANÓNICO]}$) is therefore established under the quasi-real-time protocol, free of full-sample normalisation bias.`
   - (El `[CANÓNICO]` es el mismo número fijado en P0.)

5. **Conclusión (l.358).**
   - Buscar: `for Spanish GDP, computed strictly in real time.`
   - Poner: `for Spanish GDP, computed under a quasi-real-time, expanding-window protocol.`

> No toques la palabra "real-time" cuando se refiere a la disponibilidad temporal del índice como herramienta (eso es legítimo). Solo elimina las promesas de "strict / no look-ahead / entirely in real time" que la mecánica del código no cumple.

---

## P2 — Frase duplicada en §6 (regime agreement)

En l.326 la corrección anterior dejó **dos frases que dicen lo mismo** seguidas (una versión vieja + la nueva).

**[PROSA]** Borrar la primera y dejar solo la segunda. Resultado final del pasaje:
> *"Table~\ref{tab:robustness_normalization} compares this approach with alternative scaling methods. Although the continuous correlations across normalisation methods are high ($0.841$ for percentile rank, $1.000$ for Z-score), the discrete regime classification is sensitive to the chosen scale (agreement ranges from $18.9\%$ to $59.5\%$ relative to the min-max baseline). This sensitivity reinforces our decision to rely on the continuous, unscaled index for all core regressions rather than on discrete regime thresholds."*

(Eliminar la frase que empieza por *"While the continuous correlations with the min-max baseline are high ... reinforcing our choice to rely on the unscaled index for the core empirical regressions."*)

---

## P3 — Etiqueta de la Tabla 1, Panel A (sigue mal)

`tabla1_ensemble.tex`, línea 3, sigue diciendo **"(QoQ % Growth)"** en un paper cuyo baseline es YoY.

**[CÓDIGO]** En el bloque que genera `tabla1_ensemble.tex`, cambiar:
- Buscar: `Panel A: Summary Statistics (QoQ \% Growth)`
- Poner: `Panel A: Summary Statistics (YoY \% Growth)`

Y confirmar que las cifras del Panel A provienen efectivamente de la serie YoY (PIB min ≈ −21.45, max ≈ 19.77 → coherente con YoY; si fueran QoQ, no cuadraría).

---

## P4 — Razón FALSA del corte del horse-race (verificada)

La nota de `tab_horserace` (l.286) afirma: *"The evaluation window ends in 2022Q1 due to the end of the available data series for the Spanish EPU index."*

**Esto es falso y comprobable.** El EPU español de Ghirelli, Pérez y Urtasun (2019) se publica desde 1997 **hasta el presente** en policyuncertainty.com, y la versión de Baker–Bloom–Davis en FRED (`SPEPUINDXM`) llega hasta septiembre de 2025. Un referee lo verifica en 30 segundos. El corte real es por la **madurez de $\sigma^{rev}$** (necesita ventana de 2 años hacia delante).

**[DECISIÓN + PROSA/CÓDIGO]** Dos salidas, elige con Manuel:

- **Opción A (preferida, más fuerte):** re-descargar el EPU español actualizado y **extender el horse-race** hasta donde llegue $\sigma^{rev}$ con ventana madura (alineándolo con el criterio del baseline). Más observaciones = horse-race más creíble. Luego reescribir la nota con la razón verdadera.
- **Opción B (mínimo esfuerzo):** dejar N=26 pero **cambiar la razón** a la verdadera:
  > *"Note: ... Sample restricted to periods for which $\sigma^{rev}_t$ has a complete two-year forward revision window in our vintage sample ($N = 26$, 2015Q4--2022Q1). The VIX and the Spanish EPU index are available beyond this window."*

> En cualquier caso, **eliminar la afirmación de que el EPU se acaba en 2022Q1.** Y si se aplica el criterio de madurez al horse-race, reconciliarlo con el baseline (que usa $\sigma^{rev}$ hasta 2024Q4): o se añade el caveat de madurez ya presente en el Apéndice de Vintage Maturity, o se explica por qué el baseline puede incluir vintages inmaduros.

---

## P5 — Blindar el apéndice `U_within_train` (cautela técnica)

Los residuos **in-sample** de RF y LSTM pueden ser ≈0 por sobreajuste, de modo que `U_within_train` podría estar dominada por VAR/ARIMA. Que el texto diga *"virtually identical to the baseline"* es coherente con eso, pero conviene demostrar que no la mueve un solo modelo.

**[CÓDIGO, opcional pero recomendable]** Añadir un mini leave-one-model-out **sobre la variante** `U_within_train`: recomputar `rho_within_train` excluyendo cada modelo y comprobar que el rango de $\rho$ se mantiene estrecho. Reportar una frase en el mismo apéndice:
> *"This result is not driven by any single model: leave-one-model-out recomputations of the in-sample variant keep the Spearman correlation within [X, Y]."*

---

## Orden de ejecución

1. **P0** (run canónico + `claims_new.txt` + propagar ρ). Es la base de todo.
2. **P1** (quasi-real-time en los 5 sitios) y **P2** (duplicado).
3. **P3** (etiqueta YoY) y **P4** (razón del horse-race).
4. **P5** (blindaje del apéndice).
5. Compilar y verificar refs cruzadas.

## Checklist final

- [ ] `claims_new.txt` no está vacío y contiene todas las cifras de cabecera.
- [ ] Un único valor de ρ baseline en todo el paper (abstract, intro, §5, §6.1, tabla, apéndice).
- [ ] Abstract, intro, §3, §6.1 y conclusión no prometen "strict / no look-ahead / entirely in real time".
- [ ] Pasaje de regime agreement sin duplicar.
- [ ] Tabla 1 Panel A etiquetada como YoY.
- [ ] Nota del horse-race con la razón verdadera; afirmación falsa del EPU eliminada.
- [ ] (Opcional) LOO del `U_within_train` reportado.
- [ ] LaTeX compila sin refs rotas ni overfull.
