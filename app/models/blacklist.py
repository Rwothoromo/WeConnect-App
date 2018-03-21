# app/models/blacklist.py

from app import db
from sqlalchemy.dialects.postgresql import JSON

from datetime import datetime


class Blacklist(db.Model):
    """Class for blacklisted tokens"""

    __tablename__ = 'blacklists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.created_at = datetime.now()

    # Represent the object when it is queried
    def __repr__(self):
        return '<id: token: {}'.format(self.token)
