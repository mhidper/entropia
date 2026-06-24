# Plan de FINALIZACIÓN — *Entropía* (Empirical Economics)

Lee esto entero antes de empezar. Ejecuta las fases **en orden**. Es la lista para dejar el paper
listo para enviar.

## REGLAS DE ORO (no las rompas nunca)
- **No inventes ningún número.** Toda cifra sale de `claims.txt` (salida del pipeline) o de un
  fragmento de tabla generado por el código.
- **No borres contenido ni dejes secciones vacías.** Si no puedes completar algo, deja un comentario
  `% TODO: ...` visible.
- **Una sola corrida.** Todas las figuras, tablas y cifras del texto deben proceder de la MISMA
  ejecución del pipeline.
- Cuando una figura/tabla esté comentada, **activar = quitar el `%`**, nunca borrar el bloque.

---

## FASE 0 — Fijar el número central (prerrequisito, lo más importante)

El estadístico central ha cambiado en cada corrida (0.708 → 0.715 → 0.736 → 0.729 → 0.714).
No se puede enviar un paper cuyo resultado principal no se reproduce.

1. Ejecuta el pipeline dos veces seguidas, guardando la correlación de rangos de cada una:
   ```bash
   python risk_index_v2.py 2>&1 | tee run1.txt
   python risk_index_v2.py 2>&1 | tee run2.txt
   grep -i "spearman" run1.txt run2.txt
   ```
2. **SI las dos corridas dan exactamente el mismo ρ:** perfecto. Usa esa corrida como canónica,
   guarda su `claims.txt`, y continúa.
3. **SI difieren:** el determinismo del LSTM no está funcionando. Antes de seguir, revisa que en el
   código estén activos y ANTES del entrenamiento: `random.seed`, `np.random.seed(42)`,
   `tf.random.set_seed(42)` y `tf.config.experimental.enable_op_determinism()`, y fuerza ejecución
   en un solo hilo si hace falta. Repite hasta que dos corridas seguidas coincidan. **No continúes
   hasta lograrlo.**
4. Congela esa corrida: a partir de aquí, todas las cifras del texto se verifican contra su
   `claims.txt`.

---

## FASE 1 — Corregir errores concretos

### 1.1 Tabla del ensemble rota (BLOQUEANTE)
La línea ~133 hace `\input{tables/tabla1_ensemble.tex}`, pero ese fichero **no existe**. En el
proyecto está `tab1_panel_a_descriptive.tex`.
- Comprueba con `ls tables/` el nombre real.
- Corrige el `\input` para que apunte al fichero correcto.
- **Verifica que la tabla incluye el Panel B (matriz de correlación entre modelos).** Si no existe
  un fragmento para el Panel B, genéralo con el pipeline e inclúyelo. El texto (§3.3) describe Panel
  A y Panel B; ambos deben estar.

### 1.2 §7.1 con número obsoleto
La §7.1 (Real-Time Validity) dice "ρ = 0.729 for the raw index versus ρ = 0.736 for the normalised".
- Sustituye `0.729` por el valor de ρ del índice bruto de `claims.txt` (la corrida de la Fase 0).
- Sustituye `0.736` por el valor de ρ del índice normalizado de **esa misma** corrida. Si no está en
  `claims.txt`, añade una línea al pipeline que lo imprima. No lo dejes con el valor viejo.

### 1.3 Frase rota en §3.3 (línea ~126)
Dice: "The high pairwise correlations (all above 0.0) indicate a strong shared signal".
- "all above 0.0" no dice nada y, además, es falso según la matriz de correlación (hay pares casi
  nulos o negativos).
- Sustitúyela por el **rango real** de correlaciones del Panel B (p. ej. "ranging from X to Y").
- Matiza la frase que justifica la invarianza a pesos: la invarianza no se debe a que todas las
  correlaciones sean altas, sino a que las tres dimensiones comparten la señal dominante de crisis.

### 1.4 Prefijo "Figure N:" en los títulos de las figuras (REGRESIÓN)
Las figuras vuelven a llevar incrustado en la imagen "Figure 6: ...", "Figure 5: ...", etc., que
choca con la numeración que asigna LaTeX. En el código que dibuja las figuras, **elimina el prefijo
"Figure N:" del título de CADA figura** (deja solo la parte descriptiva), y regenera. Verifica
después:
```bash
grep -nE "Figure [0-9]|Figure A1|Figure D1" risk_index_v2.py
```
No debe quedar ningún "Figure N:" dentro de un `set_title`/`suptitle`.

### 1.5 Leyenda de las figuras del CEUI (menor)
En `fig5` y `fig6` el eje X ya empieza en 2016, pero la leyenda sigue listando "Financial Crisis" y
"Sovereign Debt", cuyas bandas (2008–2013) ya no aparecen. Quita esas dos entradas de la leyenda de
estas dos figuras (deja solo COVID-19, que sí está en rango).

### 1.6 Verificar bibliografía y que no falten ficheros (BLOQUEANTE)
- Comprueba que existe `bib.bib` con las 14 claves usadas: `aruoba2008`, `asimakopoulos2023`,
  `baker2016measuring`, `bloomuncer`, `carriero2018`, `clark2017`, `croushore2011`, `ellsberg1961`,
  `haussler1997`, `heskes1998`, `jurado2015`, `mankiw1986`, `orphanides2001`, `pavia2018`.
- Comprueba que TODOS los `\input{tables/...}` y `\includegraphics{figures/...}` apuntan a ficheros
  que existen:
  ```bash
  grep -oE "tables/[a-zA-Z0-9_]+" main.tex | sort -u
  grep -oE "figures/[a-zA-Z0-9_]+" main.tex | sort -u
  ls tables/ figures/
  ```
  Cualquier referencia sin fichero: genérala o coméntala y repórtala. No dejes referencias rotas.
- Cambia `\cite{carriero2018}` y `\cite{clark2017}` por `\citep{...}`.

---

## FASE 2 — Profundizar el texto delgado

Regla para toda esta fase: **amplía con contenido sustantivo y cifras reales (de `claims.txt` o las
tablas)**, no con relleno. No inventes valores.

### 2.1 §6.1 Resultado central (PRIORIDAD MÁXIMA — hoy son 5 frases)
Amplía a 2–3 párrafos que incluyan, además de lo que ya hay:
- **Contexto de magnitud.** Indica que, a lo largo del rango observado del índice (de ~0 a ~18.9,
  según la tabla de influencia), el efecto implica un cambio de ≈ 0.37 pp en la volatilidad de las
  revisiones (= β × rango), y compáralo con los valores reales de $\sigma^{rev}$ de los trimestres
  tranquilos (~0.1 pp) frente a los más turbulentos de la COVID (~0.6 pp). Usa los valores de
  $\sigma^{rev}$ que aparecen en la tabla de influencia / `claims.txt`.
- **Error estándar en el texto**, no solo los asteriscos: SE ≈ β / t = 0.0197 / 3.107 (toma t de la
  tabla de sensibilidad).
- **Interpretación de la nube de puntos** (Figura del scatter): di si la relación es aproximadamente
  lineal o si la tracciona el racimo de alta incertidumbre de la COVID, y conecta con que la Tabla
  de sensibilidad muestra que el signo y la significatividad **sobreviven** al excluir esos
  trimestres (da las cifras de la fila "Ex-COVID" y "Ex-most influential").
- **Una frase sobre el carácter adelantado**: el índice usa solo información hasta $t$ y predice
  revisiones que se materializan en los dos años siguientes.

### 2.2 §8 Discusión (PRIORIDAD ALTA — hoy es un párrafo + dos de 3 frases)
Desarrolla en párrafos separados:
- **Mecanismo.** Por qué el desacuerdo entre modelos predice que la cifra oficial se revise: ambos
  responden al mismo deterioro del entorno informativo; cuando los datos primarios entran
  desordenados, los modelos divergen Y la triangulación estadística del INE es más frágil.
- **Cierre con la literatura del §2.** Conecta con Aruoba (revisiones "mal comportadas",
  heterocedásticas) y con la medición de incertidumbre de Jurado: tu índice es el eslabón que faltaba
  entre incertidumbre ex-ante y calidad ex-post.
- **Uso práctico.** Cómo lo usaría una agencia: un nivel del índice como semáforo de cautela sobre la
  estimación flash antes de decisiones importantes.
- **Limitaciones honestas** (amplía la actual): el dominio de la COVID en la muestra; la posible
  causalidad inversa o factor común; y la brecha teoría–medida (la entropía es motivación, las
  medidas operativas son desviaciones típicas).

### 2.3 §7.2–7.4 Robustez (hoy leen como pies de tabla)
En cada subsección, añade **la cifra clave en el propio texto**, no solo "la Tabla X lo confirma":
- LOO: indica el rango de correlación con el ensemble completo y el mayor $\Delta\rho$ (de
  `tab_robustness_loo.tex`).
- Sensibilidad de normalización: di qué porcentaje de acuerdo de régimen se obtiene (de
  `tab_robustness_norm.tex`).
- Pesos: ya da las cifras; déjalo.

### 2.4 §6.2 Horse-race (añade un párrafo)
Explica **por qué** fallan la VIX y el EPU: capturan riesgo generalizado (mercado, política),
mientras el CEUI mide el desorden interno del sistema de previsión. Añade el $R^2$ incremental al
pasar de "solo VIX/EPU" a "incluir CEUI" (compara los $R^2$ de las filas de `tab_horserace.tex`).

### 2.5 Introducción: RECORTAR, no ampliar
El párrafo que dice que "la entropía diferencial se descompone en tres componentes (aleatoria,
epistémica, temporal)" promete un resultado teórico que el paper no demuestra. Reescríbelo en clave
**empírica**: que el índice agrega tres dimensiones observables de ambigüedad predictiva. Mueve
cualquier formalismo al Apéndice A (que ya existe). Mantén el párrafo de contribución.

### 2.6 Menores
- §3.3: añade una frase sobre la heterogeneidad de comportamiento entre modelos (unos siguen al PIB,
  otros divergen), que es lo que motiva la dimensión de dispersión entre modelos.
- §5 (Estrategia): una frase justificando HC3 y Spearman (muestra pequeña, colas pesadas) y otra
  justificando la ventana de revisión de dos años.

---

## FASE 3 — VERIFICACIÓN FINAL (todo debe ser SÍ)

### Cifras
- [ ] Dos corridas seguidas dan el mismo ρ; el texto usa ese valor en TODOS los sitios (resumen,
  introducción, §6.1, §7.1, tabla de sensibilidad).
- [ ] §7.1 ya no dice 0.729; usa el ρ bruto y el normalizado de la corrida canónica.
- [ ] La D de Cook del texto coincide con la tabla de influencia.
- [ ] Ningún número del texto contradice su tabla.

### Ficheros y compilación
- [ ] `bib.bib` con las 14 claves; Referencias se renderiza; sin "Citation undefined".
- [ ] Todos los `\input` y `\includegraphics` apuntan a ficheros existentes.
- [ ] Sin prefijo "Figure N:" en los títulos de las imágenes.
- [ ] Compila sin errores:
  ```bash
  latexmk -pdf main.tex
  grep -iE "error|undefined|warning: citation|undefined reference" main.log
  pdfinfo main.pdf
  ```

### Texto
- [ ] §6.1 ampliado (magnitud en contexto, SE, interpretación de la nube, carácter adelantado).
- [ ] §8 Discusión con mecanismo, cierre con literatura, uso práctico y limitaciones honestas.
- [ ] §7.2–7.4 con la cifra clave dentro del texto.
- [ ] §6.2 con el párrafo de por qué fallan VIX/EPU.
- [ ] Introducción recortada (sin sobre-promesa teórica).
- [ ] Ninguna sección vacía; ningún número inventado; ningún contenido borrado.

## Entregable
`main.tex` y `main.pdf` finales, `claims.txt` y los dos logs de corrida (`run1.txt`, `run2.txt`)
como prueba de reproducibilidad, y una nota corta con cualquier `% TODO` pendiente y su motivo.
