# app/models/location.py

from flask import session

from app.db import db


class Location(db.Model):
    """Class to create a Location class object"""

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.businesses = {}
        self.created_by = session["user_id"]

    def __repr__(self):
        return '<Location: {}>'.format(self.name)

    def location_as_dict(self):
        """Represent the location as a dict"""

        return {l.name: getattr(self, l.name) for l in self.__table__.columns}
