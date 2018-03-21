# app/models/category.py

from flask import session

from app.db import db


class Category:
    """Class to create a Category class object"""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    businesses = db.relationship(
        'Business', backref='category', cascade='all, delete-orphan')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.businesses = {}
        self.created_by = session["user_id"]

    def __repr__(self):
        return '<Category: {}>'.format(self.name)
