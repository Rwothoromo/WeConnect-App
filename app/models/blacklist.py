# app/models/blacklist.py

from app.db import db


class Blacklist(db.Model):
    """Class for blacklisted tokens"""

    __tablename__ = 'blacklists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, token):
        self.token = token

    # Represent the object when it is queried
    def __repr__(self):
        return '<Token: {}'.format(self.token)
    
    def token_as_dict(self):
        return {t.name: getattr(self, t.name) for t in self.__table__.columns}
