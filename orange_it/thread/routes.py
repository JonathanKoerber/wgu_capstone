from flask import Blueprint
from sqlalchemy import update
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from orange_it.thread.forms import ThreadForm
from orange_it import db, bcrypt
from orange_it.models import Thread, Post, Rule
from orange_it.users.utils import save_picture, send_reset_email

threads = Blueprint('thread', __name__)


@threads.route('/new_thread', methods=['POST', 'GET'])
@login_required
def create_thread():
    form = ThreadForm()
    if form.validate_on_submit():
        new_thread = Thread(title=form.title.data, description=form.title.data, user_id=current_user.id)
        db.session.add(new_thread)
        db.session.commit()
        flash('Your Thread ' + new_thread.title + ' has been created!', 'success')
        return redirect(thread(new_thread.id))
    return render_template('create_thread.html', title='New Thread', form=form, legend="New Thread")


@threads.route('/update_thread<thread_id>', methods=['POST', 'GET'])
@login_required
def update_thread(thread_id):
    form = ThreadForm()
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


@threads.route('/thread/<int:id>')
def thread(id):
    thread = Thread.query.get_or_404(id)
    print(thread.title)
    page = request.args.get('page', 1, type=int)
#    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(thread_id=id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    rules = Rule.query.filter_by(thread_id=id).order_by(Rule.date_created.desc()).all()
    return render_template('thread.html', title=thread.title, thread=thread, posts=posts, rules=rules)
