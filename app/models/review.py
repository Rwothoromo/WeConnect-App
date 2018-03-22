# app/models/review.py

# from flask import session

from app import db


class Review(db.Model):
    """Class to create a Review class object"""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    business = db.Column(db.Integer, db.ForeignKey('businesses.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name, description, business):
        self.name = name
        self.description = description
        self.business = business
        self.created_by = 1 # session["user_id"]

    def __repr__(self):
        return '<Review: {}>'.format(self.name)
