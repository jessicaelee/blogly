"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):  
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(db.Text, default='https://www.axiumradonmitigations.com/wp-content/uploads/2015/01/icon-user-default.png')

    posts = db.relationship('Post')


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User')


# CREATE TABLE users_tes (
#     id SERIAL PRIMARY KEY,
#     first_name TEXT NOT NULL,
#     last_name TEXT NOT NULL,
#     image_url TEXT DEFAULT 'https://www.axiumradonmitigations.com/wp-content/uploads/2015/01/icon-user-default.png'
# )