# main flask app
from flask import render_template, url_for, flash, redirect, request
from mainApp import app, db, bcrypt
from mainApp.forms import RegistrationForm, LoginForm
from mainApp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/about')
def about_page():
    return render_template('about.html', title='About')


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    """take user input from form and check if it matches with db information"""
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # check if
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_page'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    """Take information enterd in form and create a account in db"""
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # take user input password and hashit
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # create a database entry to register new user
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        # add user to database
        db.session.add(user)
        db.session.commit()
        flash('Account Created, you now can login', 'success')
        return redirect(url_for('login_page'))
    return render_template('register.html', title='Register', form=form)


@app.route('/buy')
def buy_page():
    return render_template('buy.html', title='Buy')


@app.route('/sell')
def sell_page():
    return render_template('sell.html', title='Sell')


@app.route("/logout")
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))


@app.route("/profile")
@login_required
def profile_page():
    return render_template('profile.html', title='Profile')
