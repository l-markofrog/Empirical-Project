# Makefile

# Code files
SCRAPE_PY = code/scrape.py
ANALYSIS_QMD = code/analysis.qmd

# Files created by code
DATA_FILE = data/listings.csv

PLOT_FILES = \
	plots/bar_region_mean_price.png \
	plots/barh_bedrooms_combined.png \
	plots/barh_type_count.png \
	plots/barh_type_mean_price.png \
	plots/hist_price_bins.png \
	plots/scatt_crime_price.png

# ----- Tasks -----

# run: create missing files
run: $(DATA_FILE) $(PLOT_FILES) ## Run code to generate missing files

$(DATA_FILE): $(SCRAPE_PY)  ## Generate listings.csv if scrape.py is modified
	@echo "Running scrape.py to create listings.csv..."
	python3 $(SCRAPE_PY)

$(PLOT_FILES): $(ANALYSIS_QMD) $(DATA_FILE)  ## Generate plots if analysis.qmd or listings.csv is modified
	@echo "Running analysis.qmd to generate plots..."
	quarto render $(ANALYSIS_QMD) --execute-dir="$(PWD)"
	rm -f code/analysis.html; \
	rm -rf code/analysis_files; \

# clean: delete generated files
clean:
	rm -f $(DATA_FILE) $(PLOT_FILES)

# force_run: clean everything and rerun
force_run: clean run

# help: show available commands
help:
	@echo "Available commands:"
	@echo "  make run        - Run code to generate missing files"
	@echo "  make clean      - Remove generated files and plots directory"
	@echo "  make force_run  - Clean everything and rerun"
	@echo "  make help       - Show available commands"