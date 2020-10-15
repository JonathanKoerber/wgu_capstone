
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from elasticsearch import Elasticsearch
from flask_authorize import Authorize

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()



def create_app(Config):
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    #migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from orange_it.models import Post, User
    from orange_it.users.routes import users
    from orange_it.posts.routes import posts
    from orange_it.main.routes import main
    from orange_it.errors.handlers import errors
    from orange_it.rules.routes import rules
    from orange_it.thread.routes import threads
    from orange_it.messages.routes import messages

    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(rules)
    app.register_blueprint(threads)
    app.register_blueprint(messages)
    app.register_blueprint(users)

    return app
