from flask import Flask, render_template, url_for
from lib.mapper import Mapper
from lib.post import Post
import os

CONTENT_FOLDER = 'content'
app = Flask(__name__)
mapper = Mapper(CONTENT_FOLDER)
site_map = mapper.get_site_map()


@app.route('/')
def index():
    return render_template('index.html', site_map=site_map)


# SECTION AREA =====================================
@app.route('/<sec>')
def section(sec):
    sec = sec.replace("_", " ")
    return render_template('section.html', site_map=site_map, section=sec)


@app.route('/<sec>/post/<post>')
def section_post(sec, post):
    sec = sec.replace("_", " ")
    post = post.replace("_", " ")
    post = Post(filename=CONTENT_FOLDER + os.sep + sec + os.sep + post + ".md")
    return render_template('post.html', site_map=site_map,
                           title=post.get_title(), data=post.get_m_time(), content=post.get_content())


# END SECTION AREA =========================================

# SUBSECTION AREA =====================================

@app.route('/<sec>/<subsec>')
def subsection(sec, subsec):
    sec = sec.replace("_", " ")
    subsec = subsec.replace("_", " ")
    return render_template('subsection.html', site_map=site_map, section=sec, subsection=subsec)


@app.route('/<sec>/<subsec>/post/<post>')
def subsection_post(sec, subsec, post):
    sec = sec.replace("_", " ")
    subsec = subsec.replace("_", " ")
    post = post.replace("_", " ")
    post = Post(filename=CONTENT_FOLDER + os.sep + sec + os.sep + subsec + os.sep + post + ".md")
    return render_template('post.html', site_map=site_map,
                           title=post.get_title(), data=post.get_m_time(), content=post.get_content())


# END SUBSECTION AREA =====================================

# SUBSUBSECTION AREA =====================================

@app.route('/<sec>/<subsec>/<subsubsec>')
def subsubsection(sec, subsec, subsubsec):
    sec = sec.replace("_", " ")
    subsec = subsec.replace("_", " ")
    subsubsec = subsubsec.replace("_", " ")

    return render_template('subsubsection.html', site_map=site_map,
                           section=sec, subsection=subsec, subsubsection=subsubsec)


@app.route('/<sec>/<subsec>/<subsubsec>/post/<post>')
def subsubsection_post(sec, subsec, subsubsec, post):
    sec = sec.replace("_", " ")
    subsec = subsec.replace("_", " ")
    subsubsec = subsubsec.replace("_", " ")
    post = post.replace("_", " ")

    post = Post(filename=CONTENT_FOLDER + os.sep + sec + os.sep + subsec + os.sep + subsubsec + os.sep + post + ".md")
    return render_template('post.html', site_map=site_map,
                           title=post.get_title(), data=post.get_m_time(), content=post.get_content())


# END SUBSUBSECTION AREA =====================================

@app.route('/map')
def get_site_map():
    return site_map


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
