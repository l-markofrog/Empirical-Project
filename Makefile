# Makefile

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
run:
	@if [ ! -f $(DATA_FILE) ]; then \
		echo "Running scrape.py to create listings.csv..."; \
		python3 code/scrape.py; \
	else \
		echo "listings.csv already exists."; \
	fi
	@if [ ! -f plots/bar_region_mean_price.png ] || [ ! -f plots/barh_bedrooms_combined.png ] || [ ! -f plots/barh_type_count.png ] || [ ! -f plots/barh_type_mean_price.png ] || [ ! -f plots/hist_price_bins.png ] || [ ! -f plots/scatt_crime_price.png ]; then \
		echo "Running analysis.qmd to generate plots..."; \
		quarto render code/analysis.qmd --execute-dir="$(PWD)"; \
		rm -f code/analysis.html; \
		rm -rf code/analysis_files; \
	else \
		echo "All plots already exist."; \
	fi

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