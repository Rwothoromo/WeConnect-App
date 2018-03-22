# app/__init__.py
"""Initializes the app module"""

import os

# third-party imports
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# local imports
from config import app_config

app = Flask(__name__)
app.config.from_object(app_config[os.environ['FLASK_CONFIG']])
db = SQLAlchemy(app)
# db.init_app(app)
Migrate(app, db)
db.create_all()

# temporary route
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()