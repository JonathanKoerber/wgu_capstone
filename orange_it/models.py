from sqlalchemy import ForeignKey

from orange_it import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, TimedSerializer


@login_manager.user_loader
def load_user(user_id_):
    return User.query.get(int(user_id_))


# the id in the user object. Not sure if the Moderator will be ab
moderator_thread = db.Table('moderator_thread',
                            db.Column('moderator_id', db.Integer, db.ForeignKey('moderator.id'), nullable=False),
                            db.Column('thread_id', db.Integer, db.ForeignKey('thread.id'), nullable=False),
                            db.PrimaryKeyConstraint('moderator_id', 'thread_id'))

# # connects thread and owner
# thread_owner = db.Table('thread_owner',
#                         db.Column('owner_id', db.Integer, db.ForeignKey('owner.id'), nullable=False),
#                         db.Column('thread_id', db.Integer, db.ForeignKey('thread.id'), nullable=False),
#                         db.PrimaryKeyConstraint('owner_id', 'thread_id'))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)

    __mapper_arg__ = {'polymorphic_identity': 'user', 'polymorphic_on': type}

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

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# todo moderator
class Moderator(User):
    __tablename__ = 'moderator'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    thread_id = db.relationship('Thread', secondary=moderator_thread, backref='moderator')

    __mapper_arg__ = {'polymorphic_identity':'moderator'}

    def __repr__(self):
        return f"Moderator('{self.username}', '{self.image_file})'"

    def remove_post(self):
        pass

    def tag_user_removal(self):
        pass


class Owner(User):
    __tablename__ = 'owner'
    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    thread_id = db.relationship('Thread', backref='owner', lazy=True)

    __mapper_arg__ = {'polymorphic_identity': 'owner'}

    def __repr__(self):
        return f"Owner('{self.username}', '{self.image_file}')"

    def create_rule(self):
        pass

    def confirm_removal(self):
        pass

    def invite_moderator(self):
        pass

    def transfer_owner(self):
        pass


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # comments = db.relationship('Comment', backref='post_comment', lazy=True)
    up_votes = db.Column(db.Integer, nullable=True)
    down_votes = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# todo add comments to app
# class Comment(Post):
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


# todo many to many relationship with
class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    moderator_id = db.relationship('Moderator', secondary=moderator_thread, backref="thread")
    rule = db.relationship('Rule', backref='rule.thread_id', lazy=True)


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
