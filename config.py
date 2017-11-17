import os
basedir = os.path.abspath(os.path.dirname(__file__))

__APP_NAME__ = "Rhino Radio CMS"
LIQUIDSOAP_TOKEN = os.environ.get('LIQUIDSOAP_TOKEN') or 'hijackmyradio'
AIRTIME_API_KEY = os.environ.get('AIRTIME_API_KEY')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hackme'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'radiorhino.eu'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # SQLite :
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # PostgreSQL :
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'postgresql://localhost/rhino'

class TestingConfig(Config):
    TESTING = True
    MAIL_SERVER = 'radiorhino.eu'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'postgresql://localhost/rhino'

class ProductionConfig(Config):
    MAIL_SERVER = 'radiorhino.eu'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/rhino'

config = {
        'development':   DevelopmentConfig,
        'testing':       TestingConfig,
        'production':    ProductionConfig,

        'default': DevelopmentConfig
        }
