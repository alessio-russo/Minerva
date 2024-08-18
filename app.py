from flask import Flask, render_template, url_for
import os
import json


def scan(root: str):
    parent = root.split("/")[-1]
    parent = parent.replace(' ', '_')
    parent = parent.lower()
    result = f"\"{parent}\": "
    result += "{ \"dir\" : ["
    folder = os.listdir(root)
    try:
        folder.remove("description")
    except:
        pass
    subfolders = []

    for i, elem in enumerate(folder):
        if not elem.startswith("_"):

            if os.path.isdir(f"{root}/{elem}"):
                subfolders.append(f"{root}/{elem}")

            elem = elem.replace(' ', '_')
            elem = elem.lower()

            result += f"\"{elem}\""

            if i != len(folder) - 1:
                result += ","
    result += "]"
    try:
        with open(f"{root}/description", "r") as f:

            result += ", \"description\":"
            result += f"\"{f.read()}\""
            result += "}"
    except:
        result += "}"

    if len(subfolders) != 0:
        result += ","

        for i, dir in enumerate(subfolders):
            result += scan(dir)

            if i != len(subfolders) - 1:
                result += ","

    return result


root = f"{os.getcwd()}/content"
content = "{"
content += scan(root)
content += "}"
structure = json.loads(content)

app = Flask(__name__)


@app.route('/str')
def get_struct():
    return structure


@app.route('/')
def index():
    return render_template('index.html', structure=structure)


@app.route('/<sec>')
def section(sec):
    return render_template('section.html', structure=structure, section=sec)


@app.route('/<sec>/<subsec>')
def subsection(sec, subsec):
    return render_template('subsection.html', structure=structure, section=sec, subsection=subsec)


@app.route('/post')
def post():
    return render_template('post.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
