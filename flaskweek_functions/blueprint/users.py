from flask import Blueprint, jsonify

from DB_API import *

MyUsers = Blueprint("users", __name__, template_folder="templates", static_folder="static", static_url_path="assets")

@MyUsers.route("/users")
def getAllUsersFromDb():
    users = getAllDocumentsDB(u"Users")
    for key, value in users.items():
        print(key, value)
    return jsonify(users)

@MyUsers.route("/users/<id>")
def getUserFromDb(id):
    user = getDocumentDB(u"Users", id)
    if user != None:
        return jsonify(user.to_dict())
    return f"No user with id {id}"

@MyUsers.route("/users/where")
def whereUsers():
    users = getDocumentsWhere(u"Users", u"uid", u"==", "antoo")
    return jsonify(users), 200

@MyUsers.route("/users/delete/<id>")
def deleteUsers(id):
    deleteDB(u"Users", id)
    return "user deleted"