"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
# app.config['SECRET_KEY'] = "never-tell!"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)
# toolbar = DebugToolbarExtension(app)

# app.debug = False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def root():

    return redirect('/users')

@app.route('/users')
def show_users():

    title = 'Users'
    header = title
    return render_template('users.html', title=title, header=header)

@app.route('/users/new')
def add_new_user():

    title = 'Create a user'
    header = title
    return render_template('create_user.html', title=title, header=header)

@app.route('/users/new', methods=["POST"])
def process_new_user():

    # request.form ...
    return redirect('/users/new')

@app.route('/users/<int: user-id>')
def show_user_detail():

    return render_template('user_detail.html')

@app.route('/users/<int: user-id>/edit')
def edit_user_detail():

    return render_template('user_edit.html')

@app.route('/users/<int: user-id>/edit', methods=["POST"])
def process_edit_user_detail():

    # request.form ...
    return redirect('/users')

@app.route('/users/<int: user-id>/delete', methods=["POST"])
def process_delete_user():

    # request.form ...
    return redirect('/users') # maybe somewhere else ?


