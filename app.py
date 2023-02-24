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

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        uid = request.form.get("uid", "")
        pwd:int = int(request.form.get("pwd", ""))
        name = request.form.get("name", "")
        mail = request.form.get("mail", "")

        user = {
            "uid" : uid,
            "pwd" : pwd,
            "name": name
        }

        db.collection(u"Users").document(mail).set(user)

        # get the data
        # check data
        # store data in database
        # redirect to homepage
        return "Données insérées avec succes"
    else : # when GET
        return render_template("login/signup.html.j2")

@app.route("/login", methods=["GET", "POST", "PUT"])
def login():
    if "loggedin" in session and session["loggedin"]:
        return redirect("secure")


    if request.method == "POST":
        uid = request.form.get("uid", "")
        pwd = request.form.get("pwd", "")

        if uid == "anto" and pwd == "1234":
            # user is logged_in
            session["loggedin"] = True
            session["uid"] = uid

            return redirect(url_for("secure"))

        
    return render_template("login/login.html.j2")


@app.route("/loginwtf", methods=["GET", "POST"])
def loginwtf():
    formLoginWTF = loginWTF(request.form)

    if request.method == "POST" and formLoginWTF.validate():
        uid = formLoginWTF.uid.data
        pwd = formLoginWTF.pwd.data
        print(uid)
        print(pwd)

        user = db.collection(u"Users").where("uid", "==", uid).get()
        if user != None:
            user = user[0].todict()

        if user.exists and user.id == uid and user.pwd == pwd :
            session["loggedin"] = True
            session["uid"] = uid

            return redirect(url_for("secure"))

    return render_template("login/login.html.j2", form=formLoginWTF)
    
    

@app.route("/logout")
@authenticate
def logout():
    session.clear()
    return redirect(url_for("index"))

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