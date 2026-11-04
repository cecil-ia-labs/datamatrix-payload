PYTHON ?= python3

.PHONY: test experiments tables paper markdown all
test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

experiments:
	$(PYTHON) experiments/extended.py

tables:
	$(PYTHON) experiments/build_tables.py

paper: tables
	cd paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex
	cd paper && bibtex main
	cd paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex
	cd paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex
	cp paper/main.pdf paper/datamatrix-payload-paper-v0.1.pdf
	cp paper/main.pdf output/pdf/datamatrix-payload-paper-v0.1.pdf

markdown:
	$(PYTHON) experiments/build_markdown.py

all: test experiments paper markdown
