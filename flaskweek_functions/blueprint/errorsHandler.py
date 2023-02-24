from flask import Blueprint, url_for

MyErrors = Blueprint("errors", __name__)

@MyErrors.app_errorhandler(404)
def not_found(e):
  return "<h1>Vous etes perdus</h1><p><a href='"+url_for('index')+"'>retourner sur l'index</a></p>"