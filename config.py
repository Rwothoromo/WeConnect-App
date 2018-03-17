# config.py
"""Weconnect app configurations"""

class Config(object):
    """
    Common configurations
    """

    SECRET_KEY = 'really secret, is it'
    CC_TEST_REPORTER_ID = 'b1291fa23eaa46259ebf81dedc73ffb661fc2bc3d67378004cef34bf375ad739'

    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    SECRET_KEY = 'whispers in the dark'


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


class TestingConfig(Config):
    """
    Testing configurations
    """

    SECRET_KEY = 'some value'
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
