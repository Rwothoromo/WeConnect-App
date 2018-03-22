# instance/config.py
"""Weconnect app configurations"""

import os

class Config(object):
    """
    Common configurations
    """

    SECRET_KEY = 'some value'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    
    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True # protect against CSRF attacks
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
