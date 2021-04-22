from mainApp import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """user sessions"""
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """User database model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """User post model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), nullable=False)
    book_price = db.Column(db.String(4), nullable=False)
    book_condition = db.Column(db.String(10), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    contact = db.Column(db.String(100), nullable=False)
    cover_photo = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.isbn}', '{self.date_posted}', '{self.book_price}', '{self.book_condition}', '{self.contact}', '{self.cover_photo}', '{self.user_id}')"


class Review(db.Model):
    """User review model"""
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Review('{self.review}', '{self.rating}', '{self.user_id}')"

db.create_all()
db.session.commit()