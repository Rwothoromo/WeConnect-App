# app/__init__.py
"""Initializes the app module"""

from flask import Flask

# Initialize the app
APP = Flask(__name__, instance_relative_config=True)

# Load the config file
APP.config.from_object('config')
