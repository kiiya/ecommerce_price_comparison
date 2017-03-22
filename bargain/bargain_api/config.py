"""API configuration file."""


class DevConfig(object):
    """Development configurationg."""
    DEBUG = True
    MONGO_DBNAME = 'items'
    MONGO_URI = 'mongodb://localhost:27017/items'


class ProdConfig(object):
    """Production config."""
    DEBUG = False
