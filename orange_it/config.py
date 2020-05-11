import dictionary_profile
import os


class Config(object):
    DEBUG = False
    TESTING = False

    # 'mysql://b9ddc39b3371a7:7329dc96@us-cdbr-iron-east-05.cleardb.net/heroku_e9df929449c4e73'
    # db_username = 'b9ddc39b3371a7'
    # db_password = '7329dc96'
    # db_host = 'us-cdbr-iron-east-05.cleardb.net'
    # db_db = 'heroku_e9df929449c4e73'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    MAIL_USERNAME = dictionary_profile.email_profile.get('EMAIL_USER')
    MAIL_PASSWORD = dictionary_profile.email_profile.get('EMAIL_PASS')

    SECRET_KEY = dictionary_profile.app_key.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = dictionary_profile.app_key.get('DB_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'site.db')
    # SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(dictionary_profile.db_profile.get('DB_USER_NAME'),
    #                                                        dictionary_profile.db_profile.get('DB_PASSWORD'),
    #                                                        dictionary_profile.db_profile.get('DB_HOSE'),
    #                                                        dictionary_profile.db_profile.get('DB_DB'))
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WHOOSH_BASE = 'whoosh'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True



class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(DevelopmentConfig):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4
    TESTING = True
    WTF_CSRE_ENABLE = False