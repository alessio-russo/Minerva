from flask import Flask, render_template, url_for
from lib.scanner import Scanner
from lib.post import Post

root = 'content'
app = Flask(__name__)
scanner = Scanner(root)
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
    post = Post(filename=f"{root}/{sec}/{post}.md")
    return render_template('post.html', structure=structure,
                           title=post.get_title(), data=post.get_m_time(), content=post.get_content())

## END SECTION AREA

## SUBSECTION AREA
@app.route('/<sec>/<subsec>')
def subsection(sec, subsec):
    return render_template('subsection.html', structure=structure, section=sec, subsection=subsec)

@app.route('/<sec>/<subsec>/article/<post>')
def subsection_post(sec, subsec, post):
    post = post.replace("_", " ")
    sec = sec.replace("_", " ")
    subsec = subsec.replace("_", " ")
    post = Post(filename=f"{root}/{sec}/{subsec}/{post}.md")
    return render_template('post.html', structure=structure,
                           title=post.get_title(), data=post.get_m_time(), content=post.get_content())

## END SUBSECTION AREA

## SUBSUBSECTION AREA

@app.route('/<sec>/<subsec>/<subsubsec>')
def subsubsection(sec, subsec, subsubsec):
    return render_template('subsubsection.html', structure=structure, section=sec, subsection=subsec, subsubsection=subsubsec)

@app.route('/<sec>/<subsec>/<subsubsec>/article/<post>')
def subsubsection_post(sec, subsec, subsubsec, post):
    post = post.replace("_", " ")
    sec = sec.replace("_", " ")
    subsec = subsec.replace("_", " ")
    subsubsec = subsubsec.replace("_", " ")
    post = Post(filename=f"{root}/{sec}/{subsec}/{subsubsec}/{post}.md")
    return render_template('post.html', structure=structure,
                           title=post.get_title(), data=post.get_m_time(), content=post.get_content())

## END SUBSUBSECTION AREA

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
