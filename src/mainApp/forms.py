# login and registration form validation to make sure user doesn't enter invalid information
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from mainApp.models import User, Post, Review
from flask_wtf.file import FileField, FileRequired


class RegistrationForm(FlaskForm):
    '''Registration form validation'''
    username = StringField('Username', validators=[
        DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    profile_picture = FileField(validators=[FileRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        '''check and handle if user is trying to make a account with a taken username'''
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        '''check and handle if user is trying to make a account with a taken email'''
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    '''Login form validation'''
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SellForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=200)])
    isbn = IntegerField('ISBN', validators=[DataRequired()])
    book_price = IntegerField('Book Price', validators=[DataRequired()])
    book_condition = SelectField(u'Book Condition', choices=[('Poor', 'Poor'), ('Good', 'Good'), ('New', 'New')],
                                 validators=[DataRequired()])
    contact = StringField('Email for Contact', validators=[DataRequired(), Email()])
    cover_page = FileField(validators=[FileRequired()])
    submit = SubmitField('Add Post')

    def validate_title(self, title):
        '''check and handle if title is already taken'''
        post = Post.query.filter_by(title=title.data).first()
        if post:
            raise ValidationError(
                'Please choose a different Title.')

    def validate_isbn(self, isbn):
        '''check and handle if title is already taken'''
        post = Post.query.filter_by(isbn=isbn.data).first()
        if post:
            raise ValidationError(
                'Please choose a different isbn.')

    def __repr__(self):
        return f"Post('{self.title}', '{self.isbn}', '{self.book_price}', '{self.book_condition}', '{self.contact}')"

class ReviewForm(FlaskForm):
    ''' check review form '''
    review = StringField('Review', validators=[DataRequired(), Length(min=1, max=250)])
    rating = IntegerField('Rating', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __repr__(self):
        return f"Review('{self.review}', '{self.rating}', '{self.user_id}')"
