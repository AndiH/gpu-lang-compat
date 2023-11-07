#!/usr/bin/env python
# GPU-Vendor-Programming-Model-Compatibility Matrix Generator
# Andreas Herten, 2022, 2023

import argparse
import sys
import subprocess
import yaml
from jinja2 import Environment, FileSystemLoader

def preprocess_html(data):
    '''
    Since HTML is not typeset (like LaTeX) we need to take care of handling multiple of the same footnotes manually.
    '''
    _footnotes = data['descriptions']
    footnotes = {}
    i = 1
    for shortname, description in _footnotes.items():
        footnotes[shortname] = {
            'index': i,
            'description': description
        }
        i += 1
    return footnotes
def preprocess_tex(data):
    '''
    In the YAML overview document, links are written in HTML.
    Convert them to LaTeX with Pandoc. Pandoc needs to be installed, obviously.
    '''
    for shortname, description in data['descriptions'].items():
        echo = subprocess.Popen(['echo', description], stdout=subprocess.PIPE)
        new_description = subprocess.check_output(['pandoc', '--from=html', '--to=latex', '--wrap=none'], stdin=echo.stdout).strip().decode('utf-8')
        data['descriptions'][shortname] = new_description
def render_html(data, footnotes, args):
    environment = Environment(loader=FileSystemLoader('.'))
    template = environment.get_template(args.template_html)
    return template.render(data=data, footnotes=footnotes)
def render_tex(data, file, flat_dict):
    '''
    Since LaTeX uses a lot of curly braces, it's useful to define custom Jinja strings.
    '''
    environment = Environment(
        block_start_string='((*',
        block_end_string='*))',
        variable_start_string='(((',
        variable_end_string=')))',
        comment_start_string='((=',
        comment_end_string='=))',
        # line_statement_prefix='%%',
        # line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=FileSystemLoader(".")
    )
    template = environment.get_template(file)
    return template.render(data=data, flat_dict=flat_dict)

def main(args):
    with open(args.input, 'r') as f:
        try:
            table = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
    if 'html' in args.format:
        footnotes = preprocess_html(data=table)
        rendered_html = render_html(data=table, footnotes=footnotes, args=args)
        if args.print:
            print(rendered_html)
        if args.write:
            with open(args.output_html, mode="w", encoding="utf-8") as output:
                output.write(rendered_html)
    if 'latex' in args.format:
        preprocess_tex(data=table)
        flat_dict = {}
        for vendor, models in table['vendors'].items():
            for model, languages in models.items():
                for language, tagstatuses in languages.items():
                    for tag, status in tagstatuses.items():
                        _this_flat_dict = {
                                'vendor': vendor,
                                'model': model,
                                'language': language,
                                'status': status
                            }
                        if tag in table['references']:
                            _this_flat_dict['reference'] = table['references'][tag]
                        if tag not in flat_dict:
                            flat_dict[tag] = []
                        flat_dict[tag].append(_this_flat_dict)
                        import pprint
        for (infile, outfile) in zip([args.template_latex_legend, args.template_latex_table, args.template_latex_descriptions], [args.output_latex_legend, args.output_latex_table, args.output_latex_descriptions]):
            rendered_tex = render_tex(data=table, file=infile, flat_dict=flat_dict)
            if args.print:
                print(rendered_tex)
            if args.write:
                with open(outfile, mode="w", encoding="utf-8") as output:
                    print(f'Writing to {outfile}', file=sys.stderr)
                    output.write(rendered_tex)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Generate GPU Vendor-Programming Compatibility Matrix raw files. Files need to be input to proper documents.''')
    parser.add_argument('--format', '-f', choices=['html', 'latex'], nargs='+', help='Generate table in this format(s)', required=True)
    parser.add_argument('--input', help='YAML input with all the info', default="compat.yml")
    parser.add_argument('--template-latex-legend',  help='Jinja template for LaTeX (legend part)', default="templates/table-template--legend.in.tex")
    parser.add_argument('--template-latex-table',  help='Jinja template for LaTeX (table part)', default="templates/table-template--table.in.tex")
    parser.add_argument('--template-latex-descriptions',  help='Jinja template for LaTeX (descriptions part)', default="templates/table-template--descriptions.in.tex")
    parser.add_argument('--output-latex-legend',  help='File to write for LaTeX (legend part)', default="output-fragments/gpu-vendor-model-matrix.table.legend.tex")
    parser.add_argument('--output-latex-table',  help='File to write for LaTeX (table part)', default="output-fragments/gpu-vendor-model-matrix.table.table.tex")
    parser.add_argument('--output-latex-descriptions',  help='File to write for LaTeX (descriptions part)', default="output-fragments/gpu-vendor-model-matrix.table.descriptions.tex")
    parser.add_argument('--template-html', help='Jinja template for HTML', default="templates/table-template.in.html")
    parser.add_argument('--output-html', help='File to write for HTML', default="output-fragments/gpu-vendor-model-matrix.table.html")
    parser.add_argument('--print', '-p', help='Print generated code to screen', default=False, action='store_true')
    parser.add_argument('--write', '-w', help='Write generated code to file (set for disabling writing)', default=True, action='store_false')
    args = parser.parse_args()
    main(args)