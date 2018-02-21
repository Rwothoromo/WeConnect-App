# app/__init__.py
"""Initializes the app module"""

from flask import Flask

# Initialize the app
app = Flask(__name__)

# Load the config file
app.config.from_object('config')
