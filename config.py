# config.py

import os


class Config:
    """
    Common configurations
    """

    SECRET_KEY = os.environ.get('SECRET_KEY', 'some value')

    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True  # protect against CSRF attacks


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    TESTING = False


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
