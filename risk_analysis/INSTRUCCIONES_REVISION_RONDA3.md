# Instrucciones de revisión — RONDA 3 (Paper CEUI, Empirical Economics)

> [!NOTE]
> Para la IA de código ("cortita"). La ronda 2 quedó bien: ρ=0.727 propagado, β=0.0198/R²=0.413/t=3.108 cuadrados, quasi-real-time en los 5 sitios, Panel A en YoY, nota del EPU corregida, LOO del `within_train` y caveat de madurez en §5. **No toques nada de eso.** Solo quedan cuatro retoques, casi todos de una línea.
>
> Archivos: `main_final.tex`, `risk_index_v2.py`, `claims_new.txt`.

---

## P1 — [PROSA] Número obsoleto en el horse-race (prioritario)

El run canónico movió el $R^2$ de la especificación "All three" de 0.570 a **0.565** (confirmado en `tab_horserace.tex`, fila (6): `0.565`). El texto se quedó con el valor viejo.

En `main_final.tex`, l.277:
- Buscar: `driving the $R^2$ up to $0.570$ when all three are combined`
- Poner: `driving the $R^2$ up to $0.565$ when all three are combined`

> Mientras tanto, verificar de paso que el resto de cifras inline del párrafo (VIX $R^2=0.057$, EPU $R^2=0.041$) siguen coincidiendo con la tabla (sí coinciden ahora mismo).

---

## P2 — [PROSA + VERIFICACIÓN] Cuerpo y nota del horse-race dan razones distintas

La **nota** (l.286) ya da la razón verdadera (madurez de $\sigma^{rev}$, y aclara que VIX/EPU están disponibles más allá). Pero el **cuerpo** (l.277) sigue con la razón vieja y contradictoria ("jointly available").

En `main_final.tex`, l.277:
- Buscar: `over the overlapping sample for which the CEUI, the VIX and the Spanish EPU index are jointly available ($N = 26$, 2015Q4--2022Q1)`
- Poner: `over the sample for which $\sigma^{rev}_t$ has a complete two-year forward revision window ($N = 26$, 2015Q4--2022Q1)`

**Verificación obligatoria antes de cerrar P2:** si el límite fuera pura madurez de 2 años (8 trimestres) desde el final de la muestra (2024Q4), el último trimestre maduro sería ~2022Q4, **no 2022Q1**. Confirmar en el código qué restricción fija realmente el corte en 2022Q1:
- Si es la madurez de $\sigma^{rev}$ pero con un umbral distinto (p. ej. exige ventana completa + algún margen), ajustar la redacción de la nota (l.286) y del cuerpo para que diga el criterio exacto.
- Si en realidad lo que corta es otra cosa (fin del fichero de predictores, solapamiento del VIX/EPU descargado, etc.), entonces tanto la nota como el cuerpo deben decir esa razón real.
- En cualquier caso, cuerpo (l.277) y nota (l.286) deben dar **la misma** razón.

---

## P3 — [CÓDIGO + VERIFICACIÓN] `claims_new.txt` debe existir y estar poblado

El bloque de escritura existe (`risk_index_v2.py`, ~l.2467), pero el archivo aparece a **0 bytes** / sin sincronizar. Es la fuente única para el check de pre-envío.

**Tareas:**
1. Confirmar que el run canónico llega hasta el bloque de escritura sin abortar antes (que ninguna excepción previa corte el script en l.~1900–2400).
2. Verificar la **ruta**: `claims_path = dirname(dirname(abspath(__file__)))` escribe en el directorio padre del padre del script. Asegurarse de que ése es el repo root real y de que el archivo resultante no está vacío (`os.path.getsize(claims_path) > 0`).
3. Que `claims_new.txt` contenga, como mínimo, todas las cifras inline del paper para poder cruzarlas: `rho_baseline` (0.727), `beta_baseline` (0.0198), `t_baseline` (3.108), `R2_baseline` (0.413), `rho_qoq` (0.777), `rho_within_train` (0.734) + rango LOO, $R^2$ del horse-race (incl. all-three = 0.565), factores de amplificación (1.5/1.7/2.8), umbrales (p60≈1.69, p90≈13.62), correlaciones de normalización (0.891/0.997) y concordancias (43.2–59.5).
4. Dejar el archivo accesible (que no quede solo en `.gitignore` sin generar).

---

## P4 — [PROSA] Cosmético: "strict quasi-real-time"

En `main_final.tex`, l.581, "strict" y "quasi" se contradicen.
- Buscar: `As a robustness check for the strict quasi-real-time implementation of the CEUI`
- Poner: `As a robustness check for the quasi-real-time implementation of the CEUI`

---

## P5 — [VERIFICACIÓN] Confirmar que TODAS las tablas salen del mismo run

El YoY se movió a 0.727 pero el QoQ sigue en ρ=0.777. Tabla y prosa del QoQ concuerdan entre sí (no hay inconsistencia visible), pero conviene descartar que `tab_robustness_qoq.tex` haya quedado de un run anterior.

**Tarea:** confirmar que en el run canónico se regeneraron TODAS las tablas que usa el paper, no solo las del bloque principal. Lista a verificar (fecha de modificación reciente y coherencia con `claims_new.txt`):
`tabla1_ensemble`, `tab4_model_performance`, `tab5_ceui_regimes`, `tab7_sensitivity`, `tab_horserace`, `tab_robustness_qoq`, `tab_robustness_norm`, `tab_robustness_weights`, `tab_robustness_loo`, `tab_crisis_amplification`, `tab_revision_errors`, `tab_appendix_maturity`, `tab_appendix_influence`, `tab_appendix_parsimony`, `tab5_ceui_regimes`.

Si alguna tiene fecha anterior al run canónico, regenerarla en el mismo run.

---

## Orden y checklist final

1. **P1** (0.570 → 0.565) y **P2** (alinear cuerpo/nota + verificar el porqué de 2022Q1).
2. **P3** (`claims_new.txt` poblado) y **P5** (todas las tablas del mismo run).
3. **P4** (cosmético).
4. Compilar y revisar refs cruzadas.

- [ ] `tab_horserace` all-three = 0.565 también en el texto (l.277).
- [ ] Cuerpo y nota del horse-race con la misma razón; corte 2022Q1 verificado.
- [ ] `claims_new.txt` existe, no vacío, y contiene todas las cifras inline.
- [ ] Todas las tablas regeneradas del run canónico (sin restos de runs viejos).
- [ ] "strict quasi-real-time" → "quasi-real-time".
- [ ] `pdflatex` sin refs rotas ni overfull.

> Tras esta ronda, el manuscrito queda internamente consistente en todo lo que podía motivar un rechazo por fiabilidad. Lo que reste es ya criterio editorial (encuadre, contribución), no errores.
