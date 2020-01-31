"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post
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
    
    users = db.session.query(User.id, User.first_name, User.last_name).all()
    return render_template('users.html', title=title, header=title, users=users)

@app.route('/users/new')
def add_new_user():
    title = 'Create a user'
    
    return render_template('create_user.html', title=title, header=title)

@app.route('/users/new', methods=["POST"])
def process_new_user():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    image_url = request.form.get('image-url')

    if image_url == '':
        image_url = None

    new_user_record = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user_record)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    selected_user = User.query.get_or_404(user_id)
    title = f"{selected_user.first_name} {selected_user.last_name}"
    
    image_url = selected_user.image_url

    posts = Post.query.filter(Post.user_id_fk == user_id).all()
    
    return render_template('user_detail.html', title=title, header=title, image_url=image_url, user_id=user_id, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user_detail(user_id):
    selected_user = User.query.get_or_404(user_id)
    first_name = selected_user.first_name
    last_name = selected_user.last_name
    image_url = selected_user.image_url

    return render_template('user_edit.html', first_name=first_name, last_name=last_name, image_url=image_url, user_id=user_id)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_edit_user_detail(user_id):
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    image_url = request.form.get('image-url')

    selected_user = User.query.get_or_404(user_id)

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

@app.route('/users/<int:user_id>/posts/new')
def create_new_post(user_id): 
    selected_user = User.query.get_or_404(user_id)
    first_name = selected_user.first_name
    last_name = selected_user.last_name

    return render_template('new_post.html', first_name=first_name, last_name=last_name, id=selected_user.id)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def process_new_post(user_id): 

    title = request.form.get('title')
    content = request.form.get('content')

    new_post = Post(title=title, content=content, user_id_fk=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):
    selected_post = Post.query.get_or_404(post_id)
    
    title = selected_post.title
    content = selected_post.content

    user_id = selected_post.user_id_fk

    author = f'{User.query.get_or_404(user_id).first_name} {User.query.get_or_404(user_id).last_name}'
    
    return render_template('post_detail.html', title=title, header=title, content=content, author=author, user_id=user_id, post_id=post_id)


@app.route('/posts/<int:post_id>/edit')
def edit_post_detail(post_id):
    selected_post = Post.query.get_or_404(post_id)
    user_id = selected_post.user_id_fk

    return render_template('post_edit.html', title='Edit Post', post_title=selected_post.title, content=selected_post.content, id=user_id, post_id=post_id)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def process_edit_post_detail(post_id):

    title = request.form.get('title')
    content = request.form.get('content')

    selected_post = Post.query.get_or_404(post_id)
    selected_post.title = title
    selected_post.content = content

    db.session.commit()

    return redirect(f'/posts/{post_id}')

# TO DO - COMPLETE ROUTE
# @app.route('/posts/<int:post_id>/delete', methods=["POST"])
# def process_delete_post(post_id):