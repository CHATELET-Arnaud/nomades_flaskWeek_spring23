from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flaskweek_functions import authenticate
from flaskweek_functions.blueprint.posts import Myposts
from flaskweek_functions.forms import ExampleForms
from flaskweek_functions.blueprint.errorsHandler import MyErrors
from flaskweek_functions.blueprint.login import MyLogin

from DB_API import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

app.register_blueprint(MyLogin, url_prefix="/")
app.register_blueprint(Myposts, url_prefix="/")
app.register_blueprint(MyErrors)

@app.route("/")
def index():
    uid = session.get("uid", "")
    return render_template("index.html.j2", uid=uid), 200

@app.route("/account")
def account():
    l = ["Conrad", "Fabrice", "Monica", "Arnaud"]
    return render_template("account.html.j2", eleves=l)


@app.route("/secure")
@authenticate
def secure():
    return render_template("secure.html.j2")

@app.route("/form_example")
def form_example():
    form = ExampleForms(request.form)
    return render_template("forms/forms_without_macro.html.j2", form=form)

if __name__ == '__main__':
    app.run(debug=True)