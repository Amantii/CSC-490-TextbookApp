# main flask app
from flask import render_template, url_for, flash, redirect, request
from mainApp import app, db, bcrypt
from mainApp.forms import RegistrationForm, LoginForm, SellForm
from mainApp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
import os

basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

admin=Admin(app)
admin.add_view(ModelView(User, db.session))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/amd')
@login_required
def admin_page():
    if(current_user.email=="admin@admin.admin"):
        class MyModelView(sqla.ModelView):
            def is_accessible(self):
                return True
        return redirect('/admin')
    else:
       return redirect('/home')

@app.route('/')
@app.route('/home')
def home_page():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/about/')
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
        f = form.profile_picture.data
        if allowed_file(f.filename):
            filename = secure_filename(f.filename)
            if os.path.exists('./static/uploads/' + filename) != True:
                f.save(os.path.join(basedir, 'static/uploads', filename))
            else:
                flash('File with same name already Existss')
                return render_template('register.html', title='Register', form=form)
        else:
            flash('This extension is not allowed')
            return render_template('register.html', title='Register', form=form)

        # create a database entry to register new user
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password, image_file=filename)
        # add user to database
        db.session.add(user)
        db.session.commit()
        flash('Account Created, you now can login', 'success')
        return redirect(url_for('login_page'))
    return render_template('register.html', title='Register', form=form)


@app.route('/buy/')
def buy_page():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=8)
    return render_template('buy.html', title='Buy', posts=posts)


@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell_page():
    form = SellForm()
    if form.validate_on_submit():
        f = form.cover_page.data
        if allowed_file(f.filename):
            filename = secure_filename(f.filename)
            if os.path.exists('./static/posts/' + filename) != True:
                f.save(os.path.join(basedir, 'static/posts', filename))
                post = Post(title=form.title.data, isbn=form.isbn.data, book_condition=form.book_condition.data,
                            book_price=form.book_price.data, contact=form.contact.data, cover_photo=filename,
                            user_id=current_user.get_id())
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('home_page'))
            else:
                flash('File with same name already Exists')
                return render_template('sell.html', title='Sell', form=form)
        else:
            flash('This extension is not allowed')
            return render_template('sell.html', title='Sell', form=form)
    return render_template('sell.html', title='Sell', form=form)


@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))


@app.route("/delete_post/<id>", methods=['GET', 'POST'])
@login_required
def delete_post(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Post Deleted Successfully')
    return redirect(url_for('profile_page'))


# TO-DO (ALEX) --> ADD A EDIT ROUTE FOR USERS TO UPDATE POSTS
"""
@app.route("/edit_post/<id>", methods=['GET', 'POST'])
@login_required
def edit_post(id):
"""


@app.route("/profile")
@login_required
def profile_page():
    '''All posts of a logged in user are fetching from data base'''
    posts = Post.query.filter_by(user_id=current_user.get_id())
    profile = User.query.filter_by(username=current_user.username).first()
    print(profile)
    return render_template('profile.html', title='Profile', posts=posts, profile=profile)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
