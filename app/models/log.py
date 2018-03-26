# app/models/log.py

from app.db import db


class Log(db.Model):
    """Class for database changes logs"""

    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    table = db.Column(db.String(50), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '<Log: {}'.format(self.message)

    def log_as_dict(self):
        """Represent the log as a dict"""

        return {t.id: getattr(self, t.id) for t in self.__table__.columns}
