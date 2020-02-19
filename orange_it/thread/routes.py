from flask import Blueprint, abort
from sqlalchemy import update
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from orange_it.thread.forms import ThreadForm
from orange_it import db, bcrypt
from orange_it.models import Thread, Post, Rule, Moderator, Owner
from orange_it.users.utils import save_picture, send_reset_email

threads = Blueprint('thread', __name__)


@threads.route('/new_thread', methods=['POST', 'GET'])
@login_required
def create_thread():
    form = ThreadForm()
    if form.validate_on_submit():
        new_thread = Thread(title=form.title.data, description=form.description.data, user_id=current_user.id)
        db.session.add(new_thread)
        db.session.commit()
        flash('Your Thread ' + new_thread.title + ' has been created!', 'success')
        return redirect(url_for('thread.thread', thread_id=new_thread.id))
    return render_template('create_thread.html', title='New Thread', form=form, legend="New Thread")


@threads.route('/update_thread/<int:thread_id>', methods=['POST', 'GET'])
@login_required
def update_thread(thread_id):
    # todo create owner object
    # todo create view
    thread = Thread.query.get_or_404(thread_id)
    if current_user.id != thread.user_id:
        abort(403)
    owner = Owner(current_user)
    form = ThreadForm()
    if form.validate_on_submit():
        thread.title = form.title.data
        thread.description = form.desciption.data
        db.session.add(thread)
        db.session.commit()
        flash('Your Thread has been created!', 'success')
        return redirect(url_for('thread.'))
    elif request.method == 'GET':
        form.title.data = thread.title
        form.description.data = thread.description
        rules = Rule.query.filter_by(thread_id=thread_id).order_by(Rule.date_created.desc()).all()
        moderators = Moderator.query.filter_by(thread_id=thread_id).all()
    return render_template('update_thread.html', thread=thread, owner=owner, rules=rules,
                           moderators=moderators, form=form)


@threads.route('/thread/<int:thread_id>')
def thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    print(thread.title, thread.description)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(thread_id=thread_id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    rules = Rule.query.filter_by(thread_id=thread_id).order_by(Rule.date_created.desc()).all()
    moderators = Moderator.query.filter_by(thread_id=thread_id).all()
    return render_template('thread.html', title=thread.title, thread=thread, posts=posts,
                           rules=rules, moderators=moderators)
