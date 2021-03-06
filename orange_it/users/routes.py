from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from orange_it.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from orange_it import db
from orange_it.models import User, Post, Thread
from orange_it.users.utils import save_picture, send_reset_email
import bcrypt

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        password = form.password.data.encode('utf_8')
        hashed_password = bcrypt.hashpw(password, salt)
        print(hashed_password)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created you can now log in!', 'success')
        return redirect(url_for('users.login'))
    # todo this is not redirecting to login screen :(

    return render_template('auth/reg.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf_8'), user.password):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = current_user.update_image(form.picture.data)
            old_image = current_user.image_file
            if old_image != 'default.svg':
                current_user.delete_image(old_image)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    print(url_for('static', filename='profile_pics/' + current_user.image_file))
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/user/<string:username>', methods=['POST', 'GET'])
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())
    threads = Thread.query.order_by(Thread.date_created.desc()).all()
    return render_template('user_posts.html', posts=posts, user=user, threads=threads)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('auth/reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('auth/reset_token.html', title='Reset Password', form=form)

@users.route('/find_user', methods=['GET', 'POST'])
@login_required
def find_user():
    users = db.session.query(User).order_by(User.username.desc())
    return render_template('users.html',  users=users)

@users.route('/search_user',methods=['POST', 'GET'])
@login_required
def search_user():

    num_usr = min(request.args.get('limit', 50), 50)
    search_str = request.args.get('query', '')
    users = User.query.search(search_str, num_usr)

    return render_template('users.html',  users=users)
