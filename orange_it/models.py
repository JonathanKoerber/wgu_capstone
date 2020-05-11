import json
from time import time
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from orange_it import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask_authorize import RestrictionsMixin, AllowancesMixin, PermissionsMixin, OwnerPermissionsMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, TimedSerializer
import secrets
import os
from PIL import Image
from flask import current_app
from flask_mail import Message


@login_manager.user_loader
def load_user(user_id_):
    return User.query.get(int(user_id_))


class User(db.Model, UserMixin):
    __tablename__='user'
    __searchable__ = ['username']
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.svg')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)
    comment = db.relationship('Comment', backref='author', lazy=True)
    moderator = db.relationship('Moderator', backref='moderator', lazy=True)
    owner = db.relationship('Thread', backref='owner', lazy=True)
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def update_image(self, form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn

    def delete_image(self, old_image):
        if old_image is 'default.svg':
            return True
        else:
            picture_path = os.path.join(current_app.root_path, 'static/profile_pics', old_image)
            os.remove(picture_path)

    def add_notification(self, name, data):
        # todo check to see if this works with
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def up_vote(self, post_id):
        vote = Vote(user_id=self.id, post_id=post_id, vote=True)
        if Vote.query.filter_by(user_id=self.id, post_id=post_id).first():
            return
        db.session.add(vote)
        db.session.commit()

    def down_vote(self, post_id):
        vote = Vote(user_id=self.id, post_id=post_id, vote=False)
        if Vote.query.filter_by(user_id=self.id, post_id=post_id).first():
            return
        db.session.add(vote)
        db.session.commit()

    def comment_vote(self, comment_id, vote):
        com_vote = CommentVote(user_id=self.id, post_id=comment_id, vote=vote)
        if CommentVote.query.filter_by(user_id=self.id, post_id=comment_id).first():
            return
        db.session.add(com_vote)
        db.session.commit()

    def has_permission(self, thread):
        if thread.user_id == self.id:
            return True
        for m in thread.moderator:
            if m.user_id == self.id:
                return True
        else:
            return False



    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Moderator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)

    def __repr__(self):
        return f"Moderator('{self.id}', '{self.user_id}', '{self.thread_id}')"


class Post(db.Model):
    __searchable__ = ['title', 'content']
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=True)
    comments = db.relationship('Comment', backref='comment', lazy=True, cascade="all, delete-orphan")
    votes = db.relationship('Vote', backref='votes', lazy=True, cascade="all, delete-orphan")
    def __repr__(self):
        return f"Post('{self.title}','{self.content} '{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    votes = db.relationship('CommentVote', backref='votes', lazy=True, cascade="all, delete-orphan")
    def __repr__(self):
        return f"Comment('{self.title}', '{self.date_posted}')"

    def delete_post(self, comment_id):
        com = Comment.query().filter(comment_id)
        db.session.delete(com)

# todo many to many relationship with
class Thread(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    moderator = db.relationship('Moderator', backref='moderator_id', lazy=True, cascade="all, delete-orphan")
    rule = db.relationship('Rule', backref='rule', lazy=True, cascade="all, delete-orphan")
    posts = db.relationship('Post', backref='posts', lazy=True, cascade="all, delete-orphan")


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    vote = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Comment('{self.id}', '{self.user_id}', '{self.post_id}', {self.vote}')"


class CommentVote(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    vote = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Comment('{self.id}', '{self.user_id}', '{self.post_id}', {self.vote}')"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))
