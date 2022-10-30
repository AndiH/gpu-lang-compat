# GPU Vendor/Programming Model Compatibility Matrix

Soon, there are three vendors of HPC-grade GPUs (NVIDIA, AMD, Intel), and many different programming models to use the devices for general computing. It's a zoo. For a presentation, I assessed the status of the possible combinations of some more established programming models.

Since I needed this Compatibility Matrix both in PDF form (for presentations) and HTML form (for a blog), I wrote a little Python tool which consumes a definition file and generates HTML and LaTeX from it.

The tool – `render_table.py` – uses Jinja2 templates to create the respective overview tables and descriptions. The data source is `compat.yml`.

Files:

* `render_table.py`: Read in definitions from `compat.yml`, massage data, and generate HTML and/or LaTeX code. Can be either printed to screen and/or written to file. See `render_table.py -h`
* `compat.yml`: All the raw data, in YAML. Starts with SVG code for status icons. Then come the status assessments in form of dictionaries. And finally, a list of descriptions of the assessments.
* `table-template.in.html`/`table-template.in.tex`: The Jinja2 template files generating the respective code from the raw data. While a lot of the content is similar, there are some distinct differences – like how the footnotes are handled, because LaTeX is typeset while HTML is static.
* `gpu-vendor-model-matrix.html`/`gpu-vendor-model-matrix.tex`: Example boilerplate code to augment the generated table. For HTML, this is not much beyond the CSS; but for LaTeX this also includes some important definitions; but I did not want to cascade it any further.
* Pre-compiled examples:
	- `gpu-vendor-model-matrix.table.html`/`gpu-vendor-model-matrix.table.tex`: Generated version of the raw data
	- `gpu-vendor-model-matrix.table.pdf`: Typeset PDF from `gpu-vendor-model-matrix.tex`

Also, `_gen-symbols/` exist, which is part of my exploration for all of this. I just might need it if I change the icons.