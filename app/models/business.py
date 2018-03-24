# app/models/business.py

from flask import session

from app.db import db


class Business(db.Model):
    """Class to create a Business class object"""

    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    location = db.Column(db.Integer, db.ForeignKey('locations.id'))
    photo = db.Column(db.String(256))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name, description, category, location, photo):
        self.name = name
        self.description = description
        self.category = category
        self.location = location
        self.photo = photo
        self.reviews = {}
        self.created_by = session["user_id"]

    def __repr__(self):
        return '<Business: {}>'.format(self.name)

    def business_as_dict(self):
        """Represent the business as a dict"""

        return {b.name: getattr(self, b.name) for b in self.__table__.columns}
