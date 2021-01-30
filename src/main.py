# main flask app, handles routes for now

from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ma3b33ipq3pqr21739cf9a8'


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/about')
def about_page():
    return render_template('about.html', title='About')


@app.route('/login')
def login_page():
    form = RegistrationForm()
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home_page'))
    return render_template('register.html', title='Register', form=form)


@app.route('/buy')
def buy_page():
    return render_template('buy.html', title='Buy')


@app.route('/sell')
def sell_page():
    return render_template('sell.html', title='Sell')


if __name__ == '__main__':
    app.run(debug=True)
