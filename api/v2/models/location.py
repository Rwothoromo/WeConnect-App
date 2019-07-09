# app/models/location.py

from flask import session

from api.db import db


class Location(db.Model):
    """Class to create a Location class object"""

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    author = db.relationship("User")

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.created_by = session["user_id"]

    def __repr__(self):
        return '<Location: {}>'.format(self.name)

    def location_as_dict(self):
        """Represent the location as a dict"""

        location = {l.name: getattr(self, l.name) for l in self.__table__.columns}
        location['author'] = self.author.first_name + ' ' + self.author.last_name
        return location
