# instance/config.py
"""Weconnect app configurations"""

import os

class Config(object):
    """
    Common configurations
    """

    SECRET_KEY = 'some value'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/weconnect_db'
    
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

    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_weconnect_db'
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
