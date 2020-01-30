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

    users = db.session.query(User.id, User.first_name, User.last_name).all()

    print(users)
    return render_template('users.html', title=title, header=header, users=users)

@app.route('/users/new')
def add_new_user():
    title = 'Create a user'
    header = title
    return render_template('create_user.html', title=title, header=header)

@app.route('/users/new', methods=["POST"])
def process_new_user():

    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    image_url = request.form.get('image-url')

    new_user_record = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user_record)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):

    selected_user = User.query.get(user_id)
    title = f"{selected_user.first_name} {selected_user.last_name}"
    header = title
    image_url = selected_user.image_url

    return render_template('user_detail.html', title=title, header=header, image_url=image_url, user_id=user_id)

@app.route('/users/<int:user_id>/edit')
def edit_user_detail(user_id):

    selected_user = User.query.get(user_id)
    first_name = selected_user.first_name
    last_name = selected_user.last_name
    image_url = selected_user.image_url

    return render_template('user_edit.html', first_name=first_name, last_name=last_name, image_url=image_url, user_id=user_id)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_edit_user_detail(user_id):

    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    image_url = request.form.get('image-url')

    selected_user = User.query.get(user_id)

    selected_user.first_name = first_name
    selected_user.last_name = last_name
    selected_user.image_url = image_url

    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def process_delete_user(user_id):

    User.query.filter(User.id==user_id).delete()
    db.session.commit()

    return redirect('/users') 


