# Generate Compatibility Symbols

In my quest to generate the compatibility table from one source file, I also tried LaTeXML. While the result is pretty good, I wasn't entirely satisfied (like, the referenced did not work properly). Surely, that could have been somehow fixed within the LaTeXML conversion process, but I feared diving too deep into the realm. So I eventually ended up writing Jinja code (which probably was not worth it in the end…)

At least I could take the SVG graphics out of the HTML document which LaTeXML created from the TikZ code. Should I (or someone else, of course) ever need to generate the SVG icons again, I list here the necessary files and commands.

With the Jinja generation in place, one can surely also use the same approach on the generated LaTeX code.

In order to use LaTeXML to generate the HTML version of the Compatibility Matrix in LaTeX, use

```
make
```

with will launch `latexmlc`.

I used LaTeXML with the following version

```
latexml (LaTeXML version 0.8.6; revision ae17857a)
```

as I needed basic Beamer support, which only landed in LaTeXML recently. For installation, I used `brew install latexml --head`.