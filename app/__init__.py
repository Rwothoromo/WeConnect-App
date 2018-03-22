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
