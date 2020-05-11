from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, jsonify
from flask_login import current_user, login_required
from sqlalchemy import func

from orange_it import db
from orange_it.models import Post, Thread, Moderator, Comment, Vote, User, Rule
from orange_it.posts.forms import (PostForm)

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/posts/new_thread_post/<thread_id>', methods=['POST', 'GET'])
@login_required
def new_thread_post(thread_id):
    form = PostForm()
    if form.validate_on_submit():
        # creates a post on a specific thread
        post = Post(title=form.title.data, content=form.content.data, author=current_user, thread_id=thread_id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('thread.thread', thread_id=thread_id))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/comment/<int:post_id>', methods=['POST', 'GET'])
@login_required
def comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        print('post.comment validated')
        com = Comment(title=form.title.data, content=form.content.data, author=current_user, post_id=post_id)
        db.session.add(com)
        db.session.commit()
        return redirect(url_for('posts.post', post_id=post_id))
    return render_template('comment.html', title=post.title, post=post, form=form)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend="Update Post")


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id, thread_id=None):
    post = Post.query.get_or_404(post_id)
    if post.thread_id is not None:
        thread = Thread.query.get_or_404(post.thread_id)
    mod = db.session.query(Moderator).filter_by(
        Moderator.user_id == current_user.id and Moderator.thread_id == thread.id)
    if post.author != current_user or thread.owner != current_user.id \
            or mod.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    if thread_id:
        return redirect(url_for('thread.thread', thread_id=thread_id))
    return redirect(url_for('main.index'))


@posts.route("/post/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id, thread_id=None):
    comment = Comment.query.get_or_404(comment_id)
    thread = None if comment.thread_id is not None else Thread.query.get_or_404(comment.thread_id)
    mod = db.session.query(Moderator).filter_by(user_id=current_user.id)
    if post.author != current_user or thread.owner != current_user.id \
            or mod.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    if thread.id:
        return redirect(url_for('/thread/<int:' + thread_id + '>'))
    return redirect(url_for('main.index'))


@posts.route('/up_votes/<int:post_id>/<thread_id>', methods=['POST', 'GET'])
@login_required
def up_vote(post_id, thread_id):
    current_user.up_vote(post_id)
    if (thread_id == 'post'):
        return redirect(url_for('posts.post', post_id=post_id))
    elif (thread_id == 'index'):
        return redirect(url_for('main.index'))
    else:
        return redirect(url_for('thread.thread', thread_id=thread_id))


@posts.route('/down_vote/<int:post_id>/<thread_id>', methods=['GET'])
@login_required
def down_vote(post_id, thread_id):
    current_user.down_vote(post_id)
    if (thread_id == 'post'):
        print(post_id)
        return redirect(url_for('posts.post', post_id=post_id))
    elif (thread_id == 'index'):
        return redirect(url_for('main.index'))
    else:
        return redirect(url_for('thread.thread', thread_id=thread_id))

@posts.route('/comment/down_vote/<int:post_id>/<int:comment_id>/<vote>', methods=['GET'])
@login_required
def comment_vote(post_id, comment_id, vote):
    if(vote == 'True'):
        current_user.comment_vote(comment_id, True)
    else:
        current_user.comment_vote(comment_id, False)
    return redirect(url_for('posts.post', post_id=post_id))