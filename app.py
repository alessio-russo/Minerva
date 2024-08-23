from flask import Flask, render_template
from lib.utils.mapper import Mapper
from lib.utils.data.database import Database
from lib.blog.section import Section
from lib.blog.subsection import Subsection
from lib.blog.subsubsection import Subsubsection
from lib.blog.post import Post
import os

CONTENT_FOLDER = 'content'
app = Flask(__name__)
mapper = Mapper()
database = Database()

@app.route('/')
def index():
    return render_template('index.html', site_map=mapper.site_map, content_folder=CONTENT_FOLDER)


# SECTION AREA =====================================
@app.route('/<sec>')
def section(sec):
    section_name = sec.replace("_", " ")
    return render_template('section.html', content_folder=CONTENT_FOLDER, site_map=mapper.site_map,
                           section_name=section_name)


@app.route('/<sec>/post/<post>')
def section_post(sec, post):
    section_name = sec.replace("_", " ")
    post = post.replace("_", " ")
    post_path = mapper.site_map[CONTENT_FOLDER]['subfolders'][section_name]['posts'][post]['path']
    post = Post(title=post, path=post_path)
    return render_template('post.html', site_map=mapper.site_map,
                           title=post.get_title(), data=post.get_m_time(), content=post.get_content())


# END SECTION AREA =========================================

# SUBSECTION AREA =====================================

@app.route('/<sec>/<subsec>')
def subsection(sec, subsec):
    section_name = sec.replace("_", " ")
    subsection_name = subsec.replace("_", " ")
    return render_template('subsection.html', content_folder=CONTENT_FOLDER, site_map=mapper.site_map,
                           section_name=section_name, subsection_name=subsection_name)


@app.route('/<sec>/<subsec>/post/<post>')
def subsection_post(sec, subsec, post):
    section_name = sec.replace("_", " ")
    subsection_name = subsec.replace("_", " ")
    post = post.replace("_", " ")
    post_path = \
    mapper.site_map[CONTENT_FOLDER]['subfolders'][section_name]['subfolders'][subsection_name]['posts'][post]['path']
    post = Post(title=post, path=post_path)
    return render_template('post.html', site_map=mapper.site_map,
                           title=post.get_title(), data=post.get_m_time(), content=post.get_content())


# END SUBSECTION AREA =====================================

# SUBSUBSECTION AREA =====================================

@app.route('/<sec>/<subsec>/<subsubsec>')
def subsubsection(sec, subsec, subsubsec):
    section_name = sec.replace("_", " ")
    subsection_name = subsec.replace("_", " ")
    subsubsection_name = subsubsec.replace("_", " ")
    return render_template('subsubsection.html', content_folder=CONTENT_FOLDER, site_map=mapper.site_map,
                           section_name=section_name, subsection_name=subsection_name,
                           subsubsection_name=subsubsection_name)


@app.route('/<sec>/<subsec>/<subsubsec>/post/<post>')
def subsubsection_post(sec, subsec, subsubsec, post):
    section_name = sec.replace("_", " ")
    subsection_name = subsec.replace("_", " ")
    subsubsection_name = subsubsec.replace("_", " ")
    post = post.replace("_", " ")
    post_path = \
    mapper.site_map[CONTENT_FOLDER]['subfolders'][section_name]['subfolders'][subsection_name]['subfolders'][
        subsubsection_name]['posts'][post]['path']
    post = Post(title=post, path=post_path)
    return render_template('post.html', site_map=mapper.site_map,
                           title=post.get_title(), data=post.get_m_time(), content=post.get_content())


# END SUBSUBSECTION AREA =====================================

@app.route('/sec')
def get_sec():

    return f"{database.print()}"


if __name__ == '__main__':
    mapper.generate_site_map(content_folder=CONTENT_FOLDER)
    app.run(host="0.0.0.0", port=8080, use_reloader=False)
