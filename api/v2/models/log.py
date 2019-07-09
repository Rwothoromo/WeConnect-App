# app/models/log.py

from api.db import db


class Log(db.Model):
    """Class for database changes logs"""

    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(256), nullable=False)
    table = db.Column(db.String(50), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    author = db.relationship("User")

    def __init__(self, action, message, table, user_id):
        self.action = action
        self.message = message
        self.table = table
        self.created_by = user_id

    def __repr__(self):
        return '<Log: {}>'.format(self.message)

    def log_as_dict(self):
        """Represent the log as a dict"""

        log = {l.name: getattr(self, l.name) for l in self.__table__.columns}
        log['author'] = self.author.first_name + ' ' + self.author.last_name
        return log
