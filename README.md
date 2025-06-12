# 📊 ENTROPÍA: Framework Multidimensional de Incertidumbre Económica

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![LaTeX](https://img.shields.io/badge/LaTeX-academic%20paper-green.svg)](https://www.latex-project.org/)

Un framework avanzado para la cuantificación y análisis de la incertidumbre económica basado en modelos DSGE con información imperfecta y aprendizaje adaptativo.

## 🎯 Descripción del Proyecto

**ENTROPÍA** es un proyecto de investigación que desarrolla metodologías innovadoras para medir y analizar la incertidumbre económica a través de múltiples dimensiones. El framework combina teoría económica avanzada con técnicas de machine learning para proporcionar herramientas robustas de análisis de riesgo macroeconómico.

### 🔬 Innovaciones Principales

- **Framework Multidimensional**: Captura tres dimensiones clave de incertidumbre:
  - **Model Dispersion**: Desacuerdo entre diferentes metodologías de forecasting
  - **Within-Model Variability**: Variabilidad intrínseca dentro de cada modelo
  - **Temporal Instability**: Inestabilidad de predicciones a lo largo del tiempo

- **Modelos DSGE con Información Imperfecta**: Incorpora autoridades fiscales que observan señales ruidosas y aprenden adaptativamente

- **Análisis de Resiliencia Post-Crisis**: Evalúa la capacidad de recuperación de modelos después de shocks extremos (COVID-19)

## 📂 Estructura del Proyecto

```
entropia/
├── src/                                    # Código fuente principal
│   ├── dsge model incertidumbre.ipynb    # Modelo DSGE con información imperfecta
│   └── risk index.ipynb                  # Framework de índice de riesgo multidimensional
├── risk_analysis/                         # Análisis y documentación académica
│   ├── paper_tex/                        # Papers en LaTeX
│   │   ├── dsge_model.tex               # Paper modelo DSGE
│   │   ├── dsge_model.pdf               # Versión compilada
│   │   ├── main.tex                     # Paper framework principal
│   │   └── bib.bib                      # Bibliografía
│   └── bibliografía/                     # Literatura de referencia
└── README.md                             # Este archivo
```

## 🤖 Modelos Implementados

### 1. **Vector Autoregression (VAR)**
- Modelo econométrico tradicional para análisis multivariado
- **Fortaleza**: Captura relaciones dinámicas entre variables económicas
- **Uso**: Generación de intervalos de confianza (within-model uncertainty)

### 2. **Random Forest**
- Modelo de machine learning para capturar no-linealidades
- **Fortaleza**: Robusto ante outliers y cambios estructurales
- **Uso**: Modelo alternativo para dispersión entre modelos

### 3. **ARIMA**
- Modelo univariado clásico de series temporales
- **Fortaleza**: Simplicidad y transparencia interpretativa
- **Uso**: Tercer modelo para completar la dispersión multidimensional

### 4. **LSTM (Long Short-Term Memory)**
- Red neuronal para capturar dependencias temporales complejas
- **Fortaleza**: Memoria de largo plazo y manejo de secuencias complejas
- **Uso**: Análisis de patrones temporales no lineales

### 5. **Dynamic Factor Model (DFM)**
- Extracción de factores latentes macroeconómicos
- **Fortaleza**: Reducción dimensional e interpretación económica
- **Uso**: Identificación de fuerzas económicas comunes

## 📊 Ranking de Performance

### Por Precisión (MAE)
🥇 **Random Forest**: 2.34  
🥈 **LSTM**: 2.34  
🥉 **DFM**: 4.01  
🏅 **ARIMA**: 4.26  
🎖️ **VAR**: 6.22  

### Por Resiliencia Post-COVID
🥇 **Random Forest**: Score 1.096 (mejora post-crisis)  
🥈 **LSTM**: Score 0.469  
🥉 **ARIMA**: Score 0.303  
🏅 **DFM**: Score 0.293  
🎖️ **VAR**: Score 0.064 (trauma estructural)  

## 🎨 Características Técnicas

### Análisis de Incertidumbre
- **Intervalos de Confianza**: Generación automática para cada modelo
- **Monte Carlo Dropout**: Para modelos LSTM con incertidumbre epistémica
- **Dispersión entre Modelos**: Medición de desacuerdo entre 5 metodologías
- **Índice Compuesto**: Combinación ponderada de todas las dimensiones

### Evaluación Temporal
- **Rolling Window Analysis**: Evaluación dinámica desde 2019Q1 hasta 2025Q1
- **Out-of-Sample Testing**: Forecasting con ventana móvil
- **Crisis Resilience**: Análisis pre/post-COVID para medir adaptabilidad

### Visualizaciones Avanzadas
- **Dashboards Interactivos**: Series temporales, distribuciones, correlaciones
- **Heatmaps de Dispersión**: Análisis visual de desacuerdo entre modelos
- **Gráficos de Resiliencia**: Comparación de performance pre/post-crisis

## 🚀 Instalación y Uso

### Requisitos
```python
python >= 3.8
pandas >= 1.3.0
numpy >= 1.21.0
matplotlib >= 3.4.0
scikit-learn >= 1.0.0
statsmodels >= 0.13.0
tensorflow >= 2.6.0 (para LSTM)
```

### Instalación Rápida
```bash
git clone https://github.com/mhidper/entropia.git
cd entropia
pip install -r requirements.txt  # (crear este archivo con las dependencias)
```

### Ejecución
```python
# Ejecutar el framework completo
jupyter notebook "src/risk index.ipynb"

# Solo modelo DSGE
jupyter notebook "src/dsge model incertidumbre.ipynb"
```

## 📈 Resultados Principales

### Impacto de la Incertidumbre
- **Pérdidas de Bienestar**: 0.08% en regímenes normales → 1.23% en extremos
- **Multiplicadores de Crisis**: Errores de política se amplifican 2-20x
- **Persistencia**: La incertidumbre se mantiene elevada post-COVID

### Thresholds Empíricos
- 🟢 **Normal** (0-2): Condiciones económicas estables
- 🟡 **Elevada** (2-4): Vigilancia aumentada requerida  
- 🟠 **Alta** (4-8): Medidas proactivas necesarias
- 🔴 **Extrema** (>8): Respuesta de emergencia crítica

## 📚 Publicaciones Académicas

### Papers Incluidos
1. **"Fiscal Policy Errors Under Economic Uncertainty: A DSGE Model with Imperfect Information and Learning"**
   - Modelo teórico con autoridades fiscales que aprenden adaptativamente
   - Análisis de errores sistemáticos de política durante crisis

2. **"A Multidimensional Framework for Economic Uncertainty Quantification"**
   - Framework metodológico para cuantificación de incertidumbre
   - Integración de múltiples fuentes de ambigüedad predictiva

### Bibliografía de Referencia
- **Baker, Bloom & Davis (2016)**: Economic Policy Uncertainty Index
- **Jurado, Ludvigson & Ng (2015)**: Measuring Uncertainty
- **Bloom (2009)**: Impact of Uncertainty Shocks
- **Carriero, Clark & Marcellino (2018)**: Measuring Uncertainty and its Impact
- Y más referencias fundamentales en `/risk_analysis/bibliografía/`

## 🎯 Aplicaciones Prácticas

### Para Policymakers
- **Timing de Intervenciones**: Basado en regímenes de incertidumbre
- **Evaluación de Políticas**: Efectividad bajo diferentes niveles de ambigüedad
- **Early Warning System**: Detección temprana de crisis emergentes

### Para Instituciones Financieras
- **Risk Management**: Asignación de capital basada en incertidumbre
- **Stress Testing**: Escenarios de incertidumbre extrema
- **Due Diligence**: Mejora en decisiones de inversión

### Para Investigadores
- **Framework Replicable**: Metodología extensible a diferentes economías
- **Benchmarking**: Comparación de nuevos modelos de forecasting
- **Análisis Sectorial**: Aplicable a sectores específicos

## 🤝 Contribuciones

### Autores
- **Manuel Hidalgo-Pérez** - Universidad Pablo de Olavide
- **Leandro Airef** - AIREF (Autoridad Independiente de Responsabilidad Fiscal)

### Cómo Contribuir
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guidelines
- Seguir PEP 8 para código Python
- Documentar funciones con docstrings
- Incluir tests para nuevas funcionalidades
- Mantener compatibilidad con versiones anteriores

## 📊 Métricas del Proyecto

### Completitud del Framework
- ✅ **Within-Model Uncertainty**: Implementado
- ✅ **Between-Model Uncertainty**: Implementado  
- ✅ **Model Resilience Analysis**: Implementado
- ⏳ **Temporal Instability**: En desarrollo

**Estado**: 🚧 75% Completo - Operativo para aplicación práctica

### Performance Benchmark
| Modelo | MAE | RMSE | Resilience Score |
|--------|-----|------|------------------|
| Random Forest | 2.34 | 6.54 | 1.096 |
| LSTM | 2.34 | 5.47 | 0.469 |
| DFM | 4.01 | 9.55 | 0.293 |
| ARIMA | 4.26 | 11.27 | 0.303 |
| VAR | 6.22 | 12.30 | 0.064 |

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto

- **Email**: mhidper@upo.es
- **Institución**: Universidad Pablo de Olavide
- **Proyecto**: Crisis Tracker v2 - Risk Index Framework

## 🙏 Agradecimientos

- Universidad Pablo de Olavide por el apoyo institucional
- AIREF por la colaboración en la investigación aplicada
- Comunidad académica por las valiosas contribuciones y feedback

---

### 💡 Nota sobre Reproducibilidad

Este framework está diseñado para ser completamente reproducible. Todos los resultados pueden ser replicados ejecutando los notebooks en el orden especificado. Para cuestiones específicas sobre reproducibilidad, consultar la documentación técnica en los notebooks.

### 🔮 Roadmap Futuro

- [ ] Implementación completa de Temporal Instability
- [ ] Extensión a economías emergentes
- [ ] API REST para integración en sistemas externos
- [ ] Dashboard web interactivo
- [ ] Módulo de alertas en tiempo real

---

*Última actualización: Junio 2025*