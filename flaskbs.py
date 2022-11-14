from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def hello_world():
    return render_template('bs.html')

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()