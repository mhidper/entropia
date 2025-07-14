# 📄 Paper de Replicación: Pavia et al. (2017)

## 🎯 Descripción

Este directorio contiene el paper académico de replicación y extensión del trabajo de Pavia et al. (2017) "*Evaluación del sesgo en las estimaciones de Contabilidad Nacional Trimestral: Estudio de las añadas en España*".

## 📂 Estructura de Archivos

```
tex/
├── paper_replicacion_pavia.tex     # Documento principal del paper
├── referencias.bib                 # Bibliografía en formato BibTeX
├── tabla_2_latex_interanuales.tex  # Tabla 2 - Tasas interanuales
├── tabla_2_latex_intertrimestrales.tex # Tabla 2 - Tasas trimestrales
└── README_PAPER.md                 # Este archivo
```

## 🚀 Compilación del Paper

### Requisitos

- LaTeX (TeX Live, MikTeX, o similar)
- BibTeX para la bibliografía
- Paquetes LaTeX requeridos (ver preámbulo del documento)

### Instrucciones de Compilación

1. **Compilación básica:**
```bash
cd replica_pavia_2018/tex/
pdflatex paper_replicacion_pavia.tex
bibtex paper_replicacion_pavia
pdflatex paper_replicacion_pavia.tex
pdflatex paper_replicacion_pavia.tex
```

2. **Usando latexmk (recomendado):**
```bash
latexmk -pdf paper_replicacion_pavia.tex
```

3. **Limpieza de archivos temporales:**
```bash
latexmk -c
```

## 📊 Contenido del Paper

### Secciones Principales

1. **Introducción**
   - Contexto y motivación
   - Objetivos de replicación y extensión

2. **Revisión de Literatura**
   - Marco teórico de revisiones de cuentas nacionales
   - Contribuciones de Pavia et al. (2017)

3. **Metodología**
   - Replicación exacta del marco original
   - Extensiones metodológicas

4. **Resultados de Replicación**
   - Validación de hallazgos originales
   - Confirmación de patrones estacionales

5. **Extensión del Análisis**
   - Período 1995-2025
   - Análisis de crisis (COVID-19, Crisis Financiera, etc.)

6. **Conclusiones**
   - Síntesis de hallazgos
   - Implicaciones para política económica

### Tablas y Figuras

- **Tabla 2**: Errores de revisión por vintage (replicación exacta)
- **Tabla de Crisis**: Factores de amplificación por período
- **Figuras**: Evolución temporal de errores de revisión
  - Figura 2005-2016 (replicación)
  - Figura 2005-2024 (extensión)
  - Análisis específico COVID-19

## 🔗 Enlaces a Datos y Código

El paper hace referencia a:

- **Notebook principal**: `../src/pavia replication.ipynb`
- **Datos procesados**: `../tablas/`
- **Figuras**: `../figuras/`
- **Datos brutos**: `../datos/cntr.csv`

## 📈 Resultados Principales

### Replicación Exitosa

✅ **Validación completa** de Pavia et al. (2017):
- Patrón Q4 ≈ Q3 < Q1 confirmado
- Metodología exactamente replicada
- Resultados estadísticamente coherentes

### Extensiones Originales

🆕 **Nuevos hallazgos**:
- **COVID-19**: Factor de amplificación 2.94x
- **Crisis Deuda Soberana**: Factor de amplificación 3.59x (máximo)
- **Crisis Financiera**: Factor de amplificación 1.80x
- **Período Normal**: Baseline 1.00x

## 👥 Autores

- **Manuel A. Hidalgo-Pérez** - Universidad Pablo de Olavide
- **Leandro Navarro Pablo** - AIReF (Autoridad Independiente de Responsabilidad Fiscal)

## 📚 Cita Recomendada

```
Hidalgo-Pérez, M.A. y Navarro Pablo, L. (2025). 
"Replicación y Extensión de Pavia et al. (2017): 
Evaluación de la Calidad de las Añadas de la Contabilidad Nacional 
Trimestral Española con Análisis del COVID-19". 
Working Paper, Universidad Pablo de Olavide y AIReF.
```

## 🔄 Reproducibilidad

Este paper es **completamente reproducible**:

1. ✅ **Código abierto** en Python
2. ✅ **Datos disponibles** en el repositorio
3. ✅ **Metodología documentada** paso a paso
4. ✅ **Resultados verificables** ejecutando el notebook

## 📧 Contacto

- **Manuel A. Hidalgo-Pérez**: mhidper@upo.es
- **Leandro Navarro Pablo**: lnavarro@airef.es

## 📄 Licencia

Este trabajo se distribuye bajo licencia MIT. Ver archivo LICENSE en el repositorio principal.

---

*Última actualización: Julio 2025*