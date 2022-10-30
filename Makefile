.PHONY: all latex-pdf
all: gpu-vendor-model-matrix.tex gpu-vendor-model-matrix.html
latex-pdf: gpu-vendor-model-matrix.pdf

gpu-vendor-model-matrix.html: LANG=html
gpu-vendor-model-matrix.tex: LANG=latex
gpu-vendor-model-matrix.html: gpu-vendor-model-matrix.table.html table-template.in.html style.css render_table.py compat.yml Makefile
gpu-vendor-model-matrix.tex: gpu-vendor-model-matrix.table.tex table-template.in.tex render_table.py compat.yml Makefile

gpu-vendor-model-matrix.tex gpu-vendor-model-matrix.html:
	python3 render_table.py --format ${LANG}

gpu-vendor-model-matrix.pdf: gpu-vendor-model-matrix.tex
	latexmk -pdfxe $<