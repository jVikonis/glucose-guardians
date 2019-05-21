"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

app.secret_key = "Aduw\yahuwAHDWUAd21adBHJK"

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_login import LoginManager
login = LoginManager()
login.init_app(app)

from .models import *

db.create_all()

from werkzeug.security import generate_password_hash

u = User(name="Adam", 
         email="test@gmail.com", 
         password = generate_password_hash("password"),
         bio="",
         birthday=datetime.now(),
         distance=10,
         gender="male",
         preference="female",
         min=40,
         max=100,
         lat=1.0,
         long=1.0)

db.session.add(u)
db.session.commit()

from .views import *
