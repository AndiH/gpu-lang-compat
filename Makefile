.PHONY: all all-table pdf svg html paper
all: pdf svg html
all-table: gpu-vendor-model-matrix.table.tex gpu-vendor-model-matrix.table.html
pdf: gpu-vendor-model-matrix.pdf
svg: gpu-vendor-model-matrix.svg
html: gpu-vendor-model-matrix.html
paper: gpu-vendor-model-matrix.table.descriptions.paper.tex

gpu-vendor-model-matrix.table.html: LANG=html
gpu-vendor-model-matrix.table.tex: LANG=latex
gpu-vendor-model-matrix.table.html: templates/table-template.in.html style.css render_table.py compat.yml Makefile
gpu-vendor-model-matrix.table.tex: templates/table-template--legend.in.tex templates/table-template--table.in.tex templates/table-template--descriptions.in.tex render_table.py compat.yml Makefile

gpu-vendor-model-matrix.table.tex gpu-vendor-model-matrix.table.html:
	python3 render_table.py --format ${LANG}

gpu-vendor-model-matrix.pdf: gpu-vendor-model-matrix.tex gpu-vendor-model-matrix.table.tex gpu-vendor-model-matrix.table.table.tex gpu-vendor-model-matrix.table.descriptions.tex
	latexmk -pdflua gpu-vendor-model-matrix.tex
	latexmk -c

gpu-vendor-model-matrix.svg: gpu-vendor-model-matrix.pdf
	inkscape $$(PWD)/$< --export-area-drawing -o $$(PWD)/$@ --export-type=svg --pages=1-4
	svgo -i $@

gpu-vendor-model-matrix.html: gpu-vendor-model-matrix.table.html gpu-vendor-model-matrix.skeleton.html
	sed -i 's/B9D25F/85924E/' gpu-vendor-model-matrix.table.html
	gsed '/<!-- insert_here -->/e cat gpu-vendor-model-matrix.table.html' gpu-vendor-model-matrix.skeleton.html > $@

# SPECIAL RULES

gpu-vendor-model-matrix.table.descriptions.paper.tex: LANG=latex
gpu-vendor-model-matrix.table.descriptions.paper.tex: compat.yml Makefile templates/table-template--descriptions.in.paper.tex
	python3 render_table.py --format ${LANG} --template-latex-descriptions templates/table-template--descriptions.in.paper.tex --output-latex-descriptions $@