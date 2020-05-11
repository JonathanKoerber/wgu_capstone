from flask import Blueprint, abort
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from orange_it.thread.forms import ThreadForm, Update_Thread
from orange_it import db, bcrypt
from orange_it.models import Thread, Post, Rule, Moderator, User, Comment
from orange_it.users.utils import save_picture, send_reset_email

threads = Blueprint('thread', __name__)


@threads.route('/thread/<int:thread_id>')
def thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    posts = Post.query.filter_by(thread_id=thread_id).order_by(Post.date_posted.desc())
    rules = Rule.query.filter_by(thread_id=thread_id).order_by(Rule.date_created.desc()).all()
    moderators = db.session.query(User).join(Moderator, User.id == Moderator.user_id).filter(Moderator.thread_id==thread.id).all()
    return render_template('thread.html', title=thread.title, thread=thread, posts=posts,
                           rules=rules, moderators= moderators)


@threads.route('/search_thread/<int:thread_id>/', methods=['GET'])
@login_required
def search_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    posts = Post.query.whoosh_search(request.args.get('query')).filter_by(thread_id=thread.id).all()
    rules = Rule.query.filter_by(thread_id=thread_id).order_by(Rule.date_created.desc()).all()
    moderators = db.session.query(User).join(Moderator, User.id == Moderator.user_id).filter(Moderator.thread_id==thread.id).all()
    return render_template('thread.html', title=thread.title, thread=thread, posts=posts,
                           rules=rules, moderators=moderators)


@threads.route('/new_thread', methods=['POST', 'GET'])
@login_required
def create_thread():
    form = ThreadForm()
    if form.validate_on_submit():
        new_thread = Thread(title=form.title. data, description=form.description.data, user_id=current_user.id)
        db.session.add(new_thread)
        db.session.commit()

        flash('Your Thread ' + new_thread.title + ' has been created!', 'success')
        return redirect(url_for('thread.thread', thread_id=new_thread.id))
    return render_template('create_thread.html', title='New Thread', form=form, legend="New Thread")

@threads.route('/manage_thread/<int:thread_id>')
@login_required
def manage_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    if current_user.has_permission(thread):
        posts = Post.query.filter_by(thread_id=thread_id).order_by(Post.date_posted.desc())
        rules = Rule.query.filter_by(thread_id=thread_id).order_by(Rule.date_created.desc()).all()
        moderators = db.session.query(User).join(Moderator, User.id == Moderator.user_id).filter(Moderator.thread_id==thread.id).all()
        return render_template('manage_thread.html', title=thread.title, thread=thread, posts=posts,
                           rules=rules, moderators= moderators)
    else:
        abort(403)
#todo error with all users are added to the moderators card
@threads.route('/manage_thread/<thread_id>/<user_id>', methods=['POST','GET'])
@login_required
def add_moderator(thread_id, user_id):
    cu = db.session.query(Moderator).filter(Moderator.thread_id == thread_id & Moderator.user_id == user_id)
    print ('found current usser/ moderator')
    thread = Thread.query.get_or_404(thread_id)
    if current_user.id != thread.user_id:
        abort(403)
    mod = Moderator(thread_id=thread_id, user_id=user_id)
    db.session.add(mod)
    db.session.commit()
    posts = Post.query.whoosh_search(request.args.get('query')).filter_by(thread_id=thread.id).all()
    rules = Rule.query.filter_by(thread_id=thread_id).order_by(Rule.date_created.desc()).all()
    moderators = db.session.query(User).join(Moderator, User.id == Moderator.user_id).filter(Moderator.thread_id==thread.id).all()

    return render_template('manage_thread.html', posts=posts, rules=rules, moderators=moderators, thread=thread, title=thread.title)


@threads.route('/manage_thread/<thread_id>/<object_id>/<object_str>/delete', methods=['POST','GET'])
@login_required
def delete(thread_id, object_id, object_str):
    thread = Thread.query.get_or_404(thread_id)
    if object_str == 'rule':
        rule = Rule.query.get_or_404(object_id)
        db.session.delete(rule)
        db.session.commit()
    elif object_str == 'post':
        post = Post.query.get_or_404(object_id)
        db.session.delete(post)
        db.session.commit()
    elif object_str == 'comment':
        comment = Comment.query.get_or_404(object_id)
        db.session.delete(comment)
        db.session.commit()
    elif object_str == 'moderator':
        mod = Moderator.query.get_or_404(object_id)
        db.session.delete(mod)
        db.session.commit()
    elif object_str == 'thread':
        thread = Thread.query.get_or_404(object_id)
        db.session.delete(thread)
        db.session.commit()
        return redirect(url_for('main.index'))
        #needs a redirect to index.html
    posts = Post.query.filter_by(thread_id=thread_id).order_by(Post.date_posted.desc())
    rules = Rule.query.filter_by(thread_id=thread_id).order_by(Rule.date_created.desc()).all()
    moderators = db.session.query(User).join(Moderator, User.id == Moderator.user_id).filter(Moderator.thread_id==thread.id).all()
    return render_template('manage_thread.html', posts=posts, rules=rules, moderators=moderators, thread=thread, title=thread.title)


@threads.route('/update_thread/<int:thread_id>', methods=['POST', 'GET'])
@login_required
def update_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    form = Update_Thread()
    if form.validate_on_submit():
        thread.title = form.title.data
        thread.description = form.description.data
        db.session.add(thread)
        db.session.commit()
        flash('Thread '+thread.title+' has been updated!', 'success')
        return redirect(url_for('thread.thread', thread_id=thread_id))
    elif request.method == 'GET':
        form.title.data = thread.title
        form.description.data = thread.description
        rules = Rule.query.filter_by(thread_id=thread_id).order_by(Rule.date_created.desc()).all()
        moderators = db.session.query(User).join(Moderator, User.id == Moderator.user_id).filter(Moderator.thread_id==thread.id).all()
    return render_template('update_thread.html', thread=thread, form=form, rules=rules, moderators=moderators)


@threads.route('/thread/<int:thread_id>/pick_moderator', methods=['POST', 'GET'])
@login_required
def mod_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    if current_user.id != thread.user_id:
        abort(403)
    users = db.session.query(User).order_by(User.username.desc())
    rules = Rule.query.filter_by(thread_id=thread_id).order_by(Rule.date_created.desc()).all()
    moderators = db.session.query(User).join(Moderator, User.id == Moderator.user_id).filter(Moderator.thread_id==thread.id).all()
    filter_user = set(users).difference(moderators)

    return render_template('moderators.html', title=thread.title, thread=thread, users=filter_user, rules=rules,
                           moderators=moderators)



@threads.route('/thread/<int:thread_id>/search_moderator',methods=['POST', 'GET'])
@login_required
def search_mod(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    users = User.query.whoosh_search(request.args.get('query')).all()
    moderators = db.session.query(User).join(Moderator, User.id == Moderator.user_id).filter(Moderator.thread_id==thread.id).all()
    return render_template('moderators.html', title=thread.title, thread=thread, users=users, moderators=moderators)
