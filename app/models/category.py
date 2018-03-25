# app/models/category.py

from flask import session

from app.db import db


class Category(db.Model):
    """Class to create a Category class object"""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.created_by = session["user_id"]

    def __repr__(self):
        return '<Category: {}>'.format(self.name)

    def category_as_dict(self):
        """Represent the category as a dict"""

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
