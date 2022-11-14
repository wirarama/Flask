from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import DataRequired
from os import urandom


app = Flask(__name__)
Bootstrap(app)

SECRET_KEY = urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class MyForm(FlaskForm):
    nama = StringField('nama', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

@app.route("/")
def hello_world():
    form = MyForm()
    return render_template('bswtf.html',form=form)

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()