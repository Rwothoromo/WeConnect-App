# app/models/user.py

# Third party imports
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from api.db import db


class User(UserMixin, db.Model):
    """Class to create a User class object"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    businesses = db.relationship(
        'Business', order_by='Business.id', cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def user_as_dict(self):
        """Represent the user as a dict"""

        return {u.name: getattr(self, u.name) for u in self.__table__.columns}
