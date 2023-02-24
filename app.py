from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
#from flaskweek_functions import authenticate
#from flaskweek_functions.forms import ExampleForms, UserLogin

from wtforms import Form, validators, StringField, PasswordField

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

key = {
  "type": "service_account",
  "project_id": "flaskfevrier23",
  "private_key_id": "a2ec14ba011e18b9c39a74ac171ccec07a37f50c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCX7RpV6z2iIe7Z\nkqQEyvbU+18+A+GyAr51YgSMqDHTDPowo0wgPwaVVFgt+IZj1BRIT2NULtWs84rZ\no3AcJgM8k3ww1R9pcYOn5X1+ByynnUNMgZ/S3wjrUUiJFZORIGY3XdR7/98sJiZ0\nhvqOPXL5nY+391kpMUTIjjFSCJGtGyEpogfb00jaM6nVuflGMJgr39o5ufwKibv/\no7oE4Zt0vKBFl4hQJC3kMkUNezHL/c52GC8r+/gpHeeed2jAQfdDFufZuHJGkMd4\nFKJ+V3cdM18GHwSnUBrZ1kAOVw8kFbZKk6lGUvVRzw1XOH9OvyakBAsbignMaVEE\nch8jNjjTAgMBAAECggEAEDfLW+ikx63/pVI2GBzihJHg9OnNKgeI9VblTW6XAwSb\noJ2N/tM7jK1YTG//SKDXGXEAFXh6buAAroL38MlOByVnWH8nv0XS3BVvdAioB6yO\nBpi/yu7sMNKYf6nB+vgOcVKe4C3MURYxfLb8ADsnDuZ29Rh+eBs+UHp9YVhw1J2q\no+it0IMd31RistVn7jQLCCv8jAZT4E31E4wYLlOMWkoMOKKQEwgF8lIeTAhGfwl4\nG/ja2MwgruQdDSxWji5DpXvotpxS4HpA3VYPnBHPBq4muZ55XmHVyw6l8z1QOWuL\n7iDNWzObO2TGxuVrowB/BbHI+rdxXDk5YGkwSF/ugQKBgQDNyLpKPi2DGRNG27Y3\nLHlB3oQVQyPW3WsLNWsB9RiFvA6/VIP6av0JzG2pQuM8Yu6Iu9zRCV3RHKn6JE0O\nziJ5U5Ohrfbx5O9UPkEqI6I15Z+4R1WIF106WzCgiGMDYustseLEk0JhNsczw6jk\nm3alAGh9KPSqY+ABKuCVUTQ2IwKBgQC8/+Mj4mg1yKe0PXy0WyTsLTFxPVL3HrVm\nho5a4dXeCKfJIbcrVIlRrJ+N9Db4N3EUDjZvMzHucIpTAq1confVCNnYJ8QU6rzF\npZfc+n3QWTLZizieMie1uOLEx0LP75LYc+zsdPgLuddSfU47Gw3idJfxm1T3pQnp\nelWl3bWlkQKBgHu1Xfhf5LBZFLOWRbZpcAPfJvw5PoRe24kDde7ZTwKmiR8QSb7z\nLmcDlDEa2sxklQ1yEk9AGDwrxStxQznRRfw1+BxMHpZQkGfOfRI+Fbfc8OWxTIPh\nt9PrGhKHqy5P+x2fQLn35QHYEmzWBORZaTvMQQRs6Ji+Ld3Fzvk0tfSNAoGBAK5F\njR3zkH+3a9vormpneJ5F9cci8rNnH4FQJUdr4haACKaPbiSIKK6k6+KrA1zRUnVZ\nvZu/qxTftMxiNZSrQq+vH6AO2uEmqbXdwTBD0WsiNJ8fnq9QNAl+V6t2yQaPM+pe\nymImYOn/DKrFXDNn+N+M/uYLgsdu6Lre0MbGrs3hAoGAL2l02M7pHZQqOr+4W1e1\nXbkQhy7uoj1M6zyPFEKx6AgvTN9yFwwrtMe6NZ0WKhrsSH/fpGz7wQRkllgVRits\nEIPyVlVNdMsmRZC8B02DRzjTVWnG5ImxK5hKAV3t+reb020RxaItgb+IudECtttt\nAjJfuUENVzUprezaMZcwSEo=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-hdspu@flaskfevrier23.iam.gserviceaccount.com",
  "client_id": "114805183182714813731",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-hdspu%40flaskfevrier23.iam.gserviceaccount.com"
}

cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred)
db = firestore.client()

class loginWTF(Form):
    uid = StringField("Email or username", validators=[validators.InputRequired(), validators.Length(min=5, max=15, message="La longueur doit etre comprise entre 5 et 15 chars")])
    pwd = PasswordField("Password", validators=[validators.InputRequired(), validators.equal_to('pwd2', message='PASSWORDS DONT MATCH')])
    pwd2 = PasswordField("confirm password", validators=[validators.InputRequired()])

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

def authenticate(f):
    @wraps(f) 
    def decorated_func(*args, **kwargs):
        if "loggedin" in session and session["loggedin"]:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))
    return decorated_func

@app.route("/")
def index():
    uid = session.get("uid", "")
    return render_template("index.html.j2", uid=uid)

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

@app.route("/users")
def getAllUsersFromDb():
    users = db.collection(u"Users").stream()
    for user in users:
        print(user.id)
        print(user.to_dict())
    return ""

@app.route("/users/<id>")
def getUserFromDb(id):
    user = db.collection(u"Users").document(id).get()
    if user.exists:
        return jsonify(user.to_dict())
    return f"No user with id {id}"

@app.route("/users/where")
def whereUsers():
    users = db.collection(u"Users").where("pwd", "==", "123").stream()
    ret = {}
    for user in users:
        print(user.to_dict())
        ret[user.id] = user.to_dict()
    return jsonify(ret)

@app.route("/users/delete/<id>")
def deleteUsers(id):
    users = db.collection(u"Users").document(id).delete()
    return "user deleted"

@app.errorhandler(404)
def not_found(e):
  return "<h1>Vous etes perdus</h1><p><a href='"+url_for('index')+"'>retourner sur l'index</a></p>'"

if __name__ == '__main__':
    app.run(debug=True)