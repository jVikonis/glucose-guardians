from datetime import datetime
from flask_login import UserMixin
from . import db, login
from werkzeug.security import check_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    #__tablename__ = "User"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), index = True, nullable = False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(256), nullable = False)
    birthday = db.Column(db.DateTime, nullable = False)
    distance = db.Column(db.Integer, default = 10, nullable = False)
    gender = db.Column(db.String(12), nullable = False)
    preference = db.Column(db.String(12), nullable = False)
    min = db.Column(db.Integer, nullable = False)
    max = db.Column(db.Integer, nullable = False)

    pictures = db.relationship('Picture', backref = 'user', lazy = True)

class Picture(db.Model):
    #__tablename__ = "picture"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable = False)
    image = db.Column(db.String(1024), nullable = False)
    order = db.Column(db.Integer, nullable = False)

class Swipe(db.Model):
    #__tablename__ = "Swipe"

    id = db.Column(db.Integer, primary_key=True)
    matcher_id = db.Column(db.Integer, nullable = False)
    matched_id = db.Column(db.Integer, nullable = False)
    match_date = db.Column(db.DateTime, default=datetime.utcnow)
    match = db.Column(db.Boolean, nullable = False)

class Match(db.Model):
    #__tablename__ = "Match"

    id = db.Column(db.Integer, primary_key=True)
    matcher_id = db.Column(db.Integer, nullable = False)
    matched_id = db.Column(db.Integer, nullable = False)
    send_date = db.Column(db.DateTime, default=datetime.utcnow)

