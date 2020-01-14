class Config(object):
    DEBUG = False
    TESTING = False

    # 'mysql://b9ddc39b3371a7:7329dc96@us-cdbr-iron-east-05.cleardb.net/heroku_e9df929449c4e73'
    # db_username = 'b9ddc39b3371a7'
    # db_password = '7329dc96'
    # db_host = 'us-cdbr-iron-east-05.cleardb.net'
    # db_db = 'heroku_e9df929449c4e73'
    #
    # SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(db_username,
    #                                                        db_password,
    #                                                        db_host,
    #                                                        db_db)


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
