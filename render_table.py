#!/usr/bin/env python
# GPU-Vendor-Programming-Model-Compatibility Matrix Generator
# Andreas Herten, Oct 2022

import argparse
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
def render_tex(data, args):
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
    template = environment.get_template(args.template_latex)
    return template.render(data=data)

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
        rendered_tex = render_tex(data=table, args=args)
        if args.print:
            print(rendered_tex)
        if args.write:
            with open(args.output_latex, mode="w", encoding="utf-8") as output:
                output.write(rendered_tex)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Generate GPU Vendor-Programming Compatibility Matrix raw files. Files need to be input to proper documents.''')
    parser.add_argument('--format', '-f', choices=['html', 'latex'], nargs='+', help='Generate table in this format(s)', required=True)
    parser.add_argument('--input', help='YAML input with all the info', default="compat.yml")
    parser.add_argument('--template-latex',  help='Jinja template for LaTeX', default="table-template.in.tex")
    parser.add_argument('--output-latex',  help='File to write for LaTeX', default="gpu-vendor-model-matrix.table.tex")
    parser.add_argument('--template-html', help='Jinja template for HTML', default="table-template.in.html")
    parser.add_argument('--output-html', help='File to write for HTML', default="gpu-vendor-model-matrix.table.html")
    parser.add_argument('--print', '-p', help='Print generated code to screen', default=False, action='store_true')
    parser.add_argument('--write', '-w', help='Write generated code to file (set for disabling writing)', default=True, action='store_false')
    args = parser.parse_args()
    main(args)