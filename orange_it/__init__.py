
import os
import dictionary_profile
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from orange_it.config import DevelopmentConfig
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

# todo change db using environ var
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SECRET_KEY'] = '838a2fbb0c5f33c28d77e8f9c69932ba'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = dictionary_profile.email_profile.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = dictionary_profile.email_profile.get('EMAIL_PASS')

mail = Mail(app)

from orange_it.users.routes import users
from orange_it.posts.routes import posts
from orange_it.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)

