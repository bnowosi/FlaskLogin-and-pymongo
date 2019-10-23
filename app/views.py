from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, RegistrationForm
from .user import User
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # This allows the user to login to the system.
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = app.config['USERS_COLLECTION'].find_one({"_id": form.email.data})
        # If the user is validated, it will flash successful.
        if email and User.validate_login(email['password'], form.password.data):
            email_obj = User(email['_id'])
            login_user(email_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("write"))
        # Else it will deny access
        flash("Wrong email or password!", category='error')
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        collection = MongoClient()["blog"]["users"]
        email = form.email.data
        password = form.password.data
        pass_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        try:
            collection.insert_one({"_id": email, "password": pass_hash})
            flash("Account created!", category='success')
            return redirect(url_for('login'))
        except DuplicateKeyError:
            flash("Email already exists!", category='warning')
            return redirect(url_for('register'))
    return render_template('register.html', form=form)

@app.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    return render_template('write.html')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')


@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
