.PHONY: all all-table pdf svg html paper
all: pdf svg html
all-table: output-fragments/gpu-vendor-model-matrix.table.tex output-fragments/gpu-vendor-model-matrix.table.html
pdf: gpu-vendor-model-matrix.pdf
svg: gpu-vendor-model-matrix.svg
html: gpu-vendor-model-matrix.html
paper: output-fragments/gpu-vendor-model-matrix.table.descriptions.paper.tex

output-fragments/gpu-vendor-model-matrix.table.html: LANG=html
output-fragments/gpu-vendor-model-matrix.table.tex: LANG=latex
output-fragments/gpu-vendor-model-matrix.table.html: templates/table-template.in.html style.css render_table.py compat.yml Makefile
output-fragments/gpu-vendor-model-matrix.table.tex: templates/table-template--legend.in.tex templates/table-template--table.in.tex templates/table-template--descriptions.in.tex render_table.py compat.yml Makefile

output-fragments/gpu-vendor-model-matrix.table.tex output-fragments/gpu-vendor-model-matrix.table.html:
	python3 render_table.py --format ${LANG}

gpu-vendor-model-matrix.pdf: output-fragments/gpu-vendor-model-matrix.skeleton.tex output-fragments/gpu-vendor-model-matrix.table.tex output-fragments/gpu-vendor-model-matrix.table.table.tex output-fragments/gpu-vendor-model-matrix.table.descriptions.tex
	cd output-fragments && latexmk -pdflua $(notdir $<) -jobname=$(basename $@)
	cd output-fragments && latexmk -c -jobname=$(basename $@) $(notdir $<)
	mv output-fragments/$@ $@

gpu-vendor-model-matrix.svg: gpu-vendor-model-matrix.pdf
	inkscape $$(PWD)/$< --export-area-drawing -o $$(PWD)/$@ --export-type=svg --pages=1-4
	svgo -i $@

gpu-vendor-model-matrix.html: output-fragments/gpu-vendor-model-matrix.table.html output-fragments/gpu-vendor-model-matrix.skeleton.html
	sed -i 's/B9D25F/85924E/' output-fragments/gpu-vendor-model-matrix.table.html
	gsed '/<!-- insert_here -->/e cat output-fragments/gpu-vendor-model-matrix.table.html' output-fragments/gpu-vendor-model-matrix.skeleton.html > $@

# SPECIAL RULES

output-fragments/gpu-vendor-model-matrix.table.descriptions.paper.tex: LANG=latex
output-fragments/gpu-vendor-model-matrix.table.descriptions.paper.tex: compat.yml Makefile templates/table-template--descriptions.in.paper.tex
	python3 render_table.py --format ${LANG} --template-latex-descriptions templates/table-template--descriptions.in.paper.tex --output-latex-descriptions $@