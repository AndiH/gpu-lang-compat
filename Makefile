.PHONY: all all-table pdf svg html
all: pdf svg html
all-table: gpu-vendor-model-matrix.table.tex gpu-vendor-model-matrix.table.html
pdf: gpu-vendor-model-matrix.pdf
svg: gpu-vendor-model-matrix.svg
html: gpu-vendor-model-matrix.html

gpu-vendor-model-matrix.table.html: LANG=html
gpu-vendor-model-matrix.table.tex: LANG=latex
gpu-vendor-model-matrix.table.html: table-template.in.html style.css render_table.py compat.yml Makefile
gpu-vendor-model-matrix.table.tex: table-template.in.tex render_table.py compat.yml Makefile

gpu-vendor-model-matrix.table.tex gpu-vendor-model-matrix.table.html:
	python3 render_table.py --format ${LANG}

gpu-vendor-model-matrix.pdf: gpu-vendor-model-matrix.tex gpu-vendor-model-matrix.table.tex
	latexmk -pdfxe gpu-vendor-model-matrix.tex
	latexmk -c

gpu-vendor-model-matrix.svg: gpu-vendor-model-matrix.pdf
	inkscape $$(PWD)/$< --export-area-drawing -o $$(PWD)/$@ --export-type=svg
	svgo -i $@

gpu-vendor-model-matrix.html: gpu-vendor-model-matrix.table.html gpu-vendor-model-matrix.skeleton.html
	gsed '/<!-- insert_here -->/e cat gpu-vendor-model-matrix.table.html' gpu-vendor-model-matrix.skeleton.html > $@