from flask import Flask, render_template, url_for
from lib.scanner import Scanner

app = Flask(__name__)
scanner = Scanner('content')
structure = scanner.get_structure()

@app.route('/str')
def get_struct():
    return structure


@app.route('/')
def index():
    return render_template('index.html', structure=structure)


@app.route('/<sec>')
def section(sec):
    return render_template('section.html', structure=structure, section=sec)
@app.route('/<sec>/article/<post>')
def section_post(sec, post):
    return render_template('post.html')


@app.route('/<sec>/<subsec>')
def subsection(sec, subsec):
    return render_template('subsection.html', structure=structure, section=sec, subsection=subsec)

@app.route('/<sec>/<subsec>/<subsubsec>')
def subsubsection(sec, subsec, subsubsec):
    return render_template('subsubsection.html', structure=structure, section=sec, subsection=subsec, subsubsection=subsubsec)





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
