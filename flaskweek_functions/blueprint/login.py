import re
from flask import Blueprint, request, render_template, session, redirect, url_for
from flaskweek_functions import EMAIL_REGEX, authenticate
from flaskweek_functions.forms import UserLogin, UserSignUp

from DB_API import getDocumentDB, insertDb, getDocumentsWhere

MyLogin = Blueprint("login", __name__, template_folder="templates", static_folder="static", static_url_path="assets")

@MyLogin.route("/signup", methods=["GET", "POST"])
def signup():
    if "loggedin" in session and session["loggedin"]:
        return redirect(url_for("secure"))

    form = UserSignUp(request.form)

    if request.method == "POST":
        uid = form.uid.data
        pwd = form.pwd.data
        mail = form.email.data
        name = form.name.data
        firstName = form.firstName.data
        age = int(form.age.data)
        
        # TODO: use object to store data in database
        user = {
            "uid" : uid,
            "pwd" : pwd,
            "name": name,
            "firstName": firstName,
            "age": age,
            "mail": mail
        }


        insertDb(u"Users", None, user)
        """
        # si on garde un email comme id de document firestore
        insertDb(u"Users", mail, user)
        """
        
        session["loggedin"] = True
        session["uid"] = uid
        return redirect(url_for("secure"))
        
    return render_template("login/signup.html.j2", form=form)


@MyLogin.route("/login", methods=["GET", "POST"])
def login():
    if "loggedin" in session and session["loggedin"]:
        return redirect(url_for("secure"))

    formLoginWTF = UserLogin(request.form)

    if request.method == "POST" and formLoginWTF.validate():
        uid = formLoginWTF.uid.data
        pwd = formLoginWTF.pwd.data

        if re.match(EMAIL_REGEX, uid):
            user = getDocumentsWhere(u"Users", u"mail", u"==", uid)
            """
            # si on garde un email comme id de document firestore
            user = getDocumentDB(u"Users", uid)
            """
        else:
            user = getDocumentsWhere(u"Users", u"uid", u"==", uid)

        if len(user) == 1:
            user = user[next(iter(user))]
            if user["pwd"] == pwd:
                session["loggedin"] = True
                session["uid"] = uid
                return redirect(url_for("secure"))

    return render_template("login/login.html.j2", form=formLoginWTF)
    
    

@MyLogin.route("/logout")
@authenticate
def logout():
    session.clear()
    return redirect(url_for("index"))