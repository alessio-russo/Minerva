from flask import Flask, render_template, url_for
from lib.mapper import Mapper
from lib.post import Post

content_folder = 'content'
app = Flask(__name__)
mapper = Mapper(content_folder)
site_map = mapper.get_site_map()

@app.route('/map')
def get_site_map():
    return site_map


@app.route('/')
def index():
    return render_template('index.html', site_map=site_map)

## SECTION AREA

@app.route('/<sec>')
def section(sec):
    sec = sec.replace("_", " ")
    return render_template('section.html', site_map=site_map, section=sec)

@app.route('/<sec>/article/<post>')
def section_post(sec, post):
    post = post.replace("_", " ")
    sec = sec.replace("_", " ")
    post = Post(filename=f"{content_folder}/{sec}/{post}.md")
    return render_template('post.html', site_map=site_map,
                           title=post.get_title(), data=post.get_m_time(), content=post.get_content())

## END SECTION AREA

## SUBSECTION AREA
@app.route('/<sec>/<subsec>')
def subsection(sec, subsec):
    return render_template('subsection.html', structure=structure, section=sec, subsection=subsec)

@app.route('/<sec>/<subsec>/post/<post>')
def subsection_post(sec, subsec, post):
    post = post.replace("_", " ")
    sec = sec.replace("_", " ")
    subsec = subsec.replace("_", " ")
    post = Post(filename=f"{content_folder}/{sec}/{subsec}/{post}.md")
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
    post = Post(filename=f"{content_folder}/{sec}/{subsec}/{subsubsec}/{post}.md")
    return render_template('post.html', structure=structure,
                           title=post.get_title(), data=post.get_m_time(), content=post.get_content())

## END SUBSUBSECTION AREA

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
