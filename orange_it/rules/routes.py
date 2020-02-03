from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from orange_it.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                         RequestResetForm, ResetPasswordForm)
from orange_it import db, bcrypt
from orange_it.models import User, Post
from orange_it.users.utils import save_picture, send_reset_email

users = Blueprint('rules', __name__)
