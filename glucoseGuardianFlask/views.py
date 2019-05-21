"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import request, render_template, session, redirect, url_for, jsonify
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from sqlalchemy import func, desc
from . import app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from .models import *
import hashlib
import os


PIC_PATH = "pics/"
ALLOWED_EXT = ["jpg", "jpeg", "png"]

def is_pic(filename):
    return '.' in filename and filename.split(".", 1)[1].lower() in ALLOWED_EXT

def _min(one, two):
    if one < two:
        return one
    return two

M_TO_INT = {"Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
            }

@app.context_processor
def inject_year():
    return { "year": datetime.utcnow().year }

@app.route("/swipe")
def swipe():
    return render_template("swipe.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/")
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/PerformLogin", methods=["POST"])
def PerformLogin():
    email = request.form["email"]
    password = request.form["password"]
    user = User.query.filter(func.lower(User.email) == func.lower(email)).first()
    if user is None or not user.check_password(password):
        return jsonify("Incorrect email or password")
    login_user(user)
    return jsonify(success=True, redirect=url_for("swipe"))

@app.route('/PerformRegister', methods=["POST"])
def PerformRegister():
    u = User()
    try:
        u.email = request.form["name"]
        u.password = generate_password_hash(request.form["password"])
        u.name = request.form["name"]
        u.preference = request.form["preference"]
        u.gender = request.form["gender"]
        u.bio = request.form["bio"]
        u.birthday = datetime(int(request.form["year"]), M_TO_INT[request.form["month"]], int(request.form["day"]))
        u.min = _min(int(request.form["year"]) - 40, 18)
        u.max = int(request.form["year"]) + 20
        u.lat = float(request.form["lat"])
        u.long = float(request.form["long"])
        User.query.filter(func.lower(User.email) == func.lower(u.email)).first()
        if User.query.filter(func.lower(User.email) == func.lower(u.email)).first() is not None:
            return jsonify(success = False, reason="This email is already in use.")

        file = request.files["picture"] 
        if not is_pic(file.filename):
            return jsonify(success = False, reason="Invalid picture, it must be a png or a jpg.")
        filename = secure_filename(file.filename)
        fname = os.path.join(PIC_PATH, hashlib.md5((u.email + filename).encode("utf-8")).hexdigest() + ".png")
        file.save(fname)

        db.session.add(u)
        db.session.commit()
        pic = Picture()
        pic.user_id = u.id
        pic.image = fname
        pic.order = 1
        db.session.add(pic)
        login_user(User.query.filter(func.lower(User.email) == func.lower(u.email)).first())
        print("*" * 10 + " Successfully created user " + "*" * 10)
        return jsonify(success="true", redirect=url_for("swipe"))
    except Exception as e:
        import traceback
        print(traceback.format_exc())


@app.route('/adw')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/swipe/getpotentialsoulmate', methods = ["POST"])
def getPotentialSoulmates():
    """Renders the swipe page"""
    current_user.distance()
    potential = User.query.filter_by(current_user.preference == "both" or current_user.preference == User.gender).all()
    return jsonify(potential)

