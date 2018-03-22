# app/models/user.py

# Third party imports
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """Class to create a User class object"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    businesses = db.relationship(
        'Business', backref='user', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user',
                              cascade='all, delete-orphan')
    categories = db.relationship(
        'Category', backref='user', cascade='all, delete-orphan')
    locations = db.relationship(
        'Review', backref='user', cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.businesses = {}
        self.reviews = {}
        self.categories = {}
        self.locations = {}

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# Set up user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
