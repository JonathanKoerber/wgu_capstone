
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from orange_it.thread.forms import Thread_Form
from orange_it import db, bcrypt
from orange_it.models import Thread, Post
from orange_it.users.utils import save_picture, send_reset_email

thread = Blueprint('thread', __name__)


@thread.route('/new_thread', methods=['POST', 'GET'])
@login_required
def create_thread():
    form = Thread_Form()
    if form.validate_on_submit():
        new_thread = Thread(title=form.title, content=form.content, owner=current_user)
        db.session.add(new_thread)
        db.session.commit()
        flash('Your Thread has been created!', 'success')
        return redirect(url_for('thread<thread.id>'))
    return render_template('thread.html', title='Thread', content='What is this tread about?', form=form)


@thread.route('/thread<thread.id>', methods=['POST', 'GET'])
@login_required
def view_thread():
    form = Thread_Form()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Thread has been created!', 'success')
        return redirect(url_for('thread.'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    print(url_for('static', filename='profile_pics/' + current_user.image_file))
    return render_template('account.html', title='Account', image_file=image_file, form=form)
