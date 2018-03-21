# instance/config.py
"""Weconnect app configurations"""

class Config(object):
    """
    Common configurations
    """

    DEBUG = True
    CSRF_ENABLED = True # protect against CSRF attacks

    SECRET_KEY = 'really secret, is it'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/weconnect_db'


class DevelopmentConfig(Config):
    """
    Development configurations
    """

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
