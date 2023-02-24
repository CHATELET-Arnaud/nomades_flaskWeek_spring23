from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from DB_API import *

from flaskweek_functions import authenticate
from flaskweek_functions.forms import FormArticle
from DB_API.schema import Posts

Myposts = Blueprint('posts', __name__, template_folder='templates', static_folder='static', static_url_path='assets')

@Myposts.route('/post',methods=['POST','GET'])
@authenticate
def post():
    form=FormArticle(request.form)
    # TODO: save the posts in the database
    # TODO: save using the Posts class defined in schema.py
    return render_template('posts/post.html',form=form)

@Myposts.route('/myposts')
@authenticate
def myposts():
    posts=[] 
    # TODO: get all posts from the user in session
    return render_template('posts/myposts.html',posts=posts)

@Myposts.route('/delete_post/<string:id>', methods=['POST'])
@authenticate
def delete_post(id):
    # TODO: delete selected post
    return redirect(url_for('posts.myposts'))