# config.py


class Config(object):
    """
    Common configurations
    """
    
    SECRET_KEY = 'really secret, is it'
    
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
