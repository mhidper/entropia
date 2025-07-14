# Makefile para compilar el paper de replicación de Pavia et al. (2017)

# Variables
MAIN = paper_replicacion_pavia
TEX_FILES = $(MAIN).tex referencias.bib tabla_2_latex_interanuales.tex tabla_2_latex_intertrimestrales.tex
OUTPUT_DIR = output
FIGURES_DIR = ../figuras

# Regla principal
all: $(MAIN).pdf

# Compilación completa del paper
$(MAIN).pdf: $(TEX_FILES)
	@echo "=== Compilando paper de replicación ==="
	@mkdir -p $(OUTPUT_DIR)
	pdflatex -output-directory=$(OUTPUT_DIR) $(MAIN).tex
	@echo "=== Procesando bibliografía ==="
	cd $(OUTPUT_DIR) && bibtex $(MAIN)
	@echo "=== Segunda pasada LaTeX ==="
	pdflatex -output-directory=$(OUTPUT_DIR) $(MAIN).tex
	@echo "=== Tercera pasada LaTeX ==="
	pdflatex -output-directory=$(OUTPUT_DIR) $(MAIN).tex
	@echo "=== Copiando PDF final ==="
	cp $(OUTPUT_DIR)/$(MAIN).pdf .
	@echo "✅ Paper compilado exitosamente: $(MAIN).pdf"

# Compilación rápida (sin bibliografía)
quick: $(MAIN).tex
	@echo "=== Compilación rápida ==="
	pdflatex $(MAIN).tex
	@echo "✅ Compilación rápida completada"

# Usar latexmk (método recomendado)
latexmk: $(TEX_FILES)
	@echo "=== Compilando con latexmk ==="
	latexmk -pdf -output-directory=$(OUTPUT_DIR) $(MAIN).tex
	cp $(OUTPUT_DIR)/$(MAIN).pdf .
	@echo "✅ Paper compilado con latexmk: $(MAIN).pdf"

# Verificar que las figuras existen
check-figures:
	@echo "=== Verificando figuras ==="
	@test -f $(FIGURES_DIR)/figura_2_pavia_robusta_2005_2016.png || echo "⚠️  Falta: figura_2_pavia_robusta_2005_2016.png"
	@test -f $(FIGURES_DIR)/figura_2_pavia_robusta_2005_2024.png || echo "⚠️  Falta: figura_2_pavia_robusta_2005_2024.png"
	@test -f $(FIGURES_DIR)/evolucion_estimaciones_2020Q1_robusto.png || echo "⚠️  Falta: evolucion_estimaciones_2020Q1_robusto.png"
	@test -f $(FIGURES_DIR)/analisis_cntr_graficos.png || echo "⚠️  Falta: analisis_cntr_graficos.png"
	@echo "✅ Verificación de figuras completada"

# Limpiar archivos temporales
clean:
	@echo "=== Limpiando archivos temporales ==="
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz
	rm -rf $(OUTPUT_DIR)
	@echo "✅ Archivos temporales eliminados"

# Limpiar todo (incluyendo PDF)
cleanall: clean
	@echo "=== Limpiando todos los archivos generados ==="
	rm -f $(MAIN).pdf
	@echo "✅ Todos los archivos generados eliminados"

# Mostrar estructura del proyecto
structure:
	@echo "=== Estructura del proyecto ==="
	@echo "📂 Directorio actual: $(PWD)"
	@echo "📄 Archivo principal: $(MAIN).tex"
	@echo "📚 Bibliografía: referencias.bib"
	@echo "📊 Tablas LaTeX:"
	@ls -la tabla_2_latex_*.tex 2>/dev/null || echo "   No se encontraron tablas LaTeX"
	@echo "🖼️  Figuras en: $(FIGURES_DIR)"
	@ls -la $(FIGURES_DIR)/*.png 2>/dev/null || echo "   No se encontraron figuras PNG"
	@echo "📁 Directorio de salida: $(OUTPUT_DIR)"

# Mostrar ayuda
help:
	@echo "=== Makefile para Paper de Replicación Pavia et al. (2017) ==="
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make all          - Compilación completa del paper (recomendado)"
	@echo "  make latexmk      - Compilación usando latexmk"
	@echo "  make quick        - Compilación rápida sin bibliografía"
	@echo "  make check-figures- Verificar que todas las figuras existen"
	@echo "  make structure    - Mostrar estructura del proyecto"
	@echo "  make clean        - Limpiar archivos temporales"
	@echo "  make cleanall     - Limpiar todo (incluyendo PDF)"
	@echo "  make help         - Mostrar esta ayuda"
	@echo ""
	@echo "Archivos principales:"
	@echo "  📄 $(MAIN).tex - Documento principal"
	@echo "  📚 referencias.bib - Bibliografía"
	@echo "  📊 tabla_2_latex_*.tex - Tablas generadas"
	@echo ""
	@echo "Ejemplo de uso:"
	@echo "  make check-figures  # Verificar figuras"
	@echo "  make all           # Compilar paper completo"

# Reglas especiales
.PHONY: all quick latexmk check-figures clean cleanall structure help

# Regla por defecto
.DEFAULT_GOAL := help