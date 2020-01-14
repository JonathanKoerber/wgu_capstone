
import os
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
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.protonmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)


from orange_it import routes