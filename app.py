from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post')
def post():
    return render_template('post-template.html')

if __name__ == '__main__':
    app.run()
