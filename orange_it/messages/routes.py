from datetime import datetime
from flask import render_template, url_for, redirect, request, Blueprint, flash, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from orange_it.messages.forms import MessageForm
from orange_it.models import Post, User, Message, Thread, Notification
from orange_it import db

messages = Blueprint('messages', __name__)


@messages.route('/send_message/<int:recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    print(('send mesage'))
    user = User.query.filter_by(id=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(sender_id=current_user.id, recipient_id=user.id, title=form.title.data, body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash('You message has been sent.')
        return redirect(url_for('messages.message'))
    return render_template('send_message.html', form=form, user=user)


@messages.route('/message', methods=['GET', 'POST'])
@login_required
def message():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('uread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc())
    threads = Thread.query.order_by(Thread.date_created.desc()).all()
    return render_template('messages.html', messages=messages, threads=threads)



@messages.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
