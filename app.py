from flask import Flask, render_template, url_for
from pygments.formatters import HtmlFormatter

import os
import time
from datetime import datetime

from lib.scanner import Scanner
import markdown
import markdown.extensions.fenced_code
import markdown.extensions.codehilite

app = Flask(__name__)
scanner = Scanner('content')
structure = scanner.get_structure()

@app.route('/str')
def get_struct():
    return structure


@app.route('/')
def index():
    return render_template('index.html', structure=structure)

## SECTION AREA

@app.route('/<sec>')
def section(sec):
    return render_template('section.html', structure=structure, section=sec)
@app.route('/<sec>/article/<post>')
def section_post(sec, post):
    post = post.replace("_", " ")
    sec = sec.replace("_", " ")
    with open(f"content/{sec}/{post}.md", "r") as file:
        content = markdown.markdown(file.read(),  extensions=["fenced_code", "codehilite", 'mdx_math'], extension_configs={
        'mdx-math': {'enable_dollar_delimiter': True}
    })
    formatter = HtmlFormatter(style="emacs", full=True, cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = "<style>" + css_string + "</style>"
    content = md_css_string + content

    data = os.path.getmtime(f"content/{sec}/{post}.md")
    data = time.ctime(data)
    data = datetime.strptime(data, "%a %b %d %H:%M:%S %Y")
    return render_template('post.html', structure=structure, title=post, data=data, content=content)

## END SECTION AREA

## SUBSECTION AREA
@app.route('/<sec>/<subsec>')
def subsection(sec, subsec):
    return render_template('subsection.html', structure=structure, section=sec, subsection=subsec)

@app.route('/<sec>/<subsec>/article/<post>')
def subsection_post(sec, subsec, post):
    return render_template('post.html', structure=structure)

## END SUBSECTION AREA

## SUBSUBSECTION AREA

@app.route('/<sec>/<subsec>/<subsubsec>')
def subsubsection(sec, subsec, subsubsec):
    return render_template('subsubsection.html', structure=structure, section=sec, subsection=subsec, subsubsection=subsubsec)

@app.route('/<sec>/<subsec>/<subsubsec>/article/<post>')
def subsubsection_post(sec, subsec, subsubsec, post):
    return render_template('post.html', structure=structure)

## END SUBSUBSECTION AREA

if __name__ == '__main__':
    Markdown(app)
    app.run(host="0.0.0.0", port=8080, debug=True)
