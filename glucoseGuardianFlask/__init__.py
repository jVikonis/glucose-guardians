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

from .views import *
