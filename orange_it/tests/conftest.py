import pytest

from orange_it import create_app, db as _db
from orange_it.config import TestingConfig
from orange_it.models import User, Post, Moderator, Comment, Thread, Rule, Vote, Message, Notification


# Create all objects to be used when testing
@pytest.fixture(scope='module')
def new_user():
    user = User(username='test', email='test@test.com', password='hello')
    return user


@pytest.fixture(scope='module')
def new_mod():
    mod = Moderator(user_id=3, thread_id=4)
    return mod


@pytest.fixture(scope='module')
def new_post():
    post = Post(title='hello world', content='world hello', user_id=1)
    return post


@pytest.fixture(scope='module')
def new_thread_post():
    post = Post(title='hello world', content='world hello', user_id=1, thread_id=1)
    return post


@pytest.fixture(scope='module')
def new_comment():
    comment = Comment(title='hello world', content='world hello', user_id=1, post_id=1)
    return comment


@pytest.fixture(scope='module')
def new_thread():
    thread = Thread(title='thread test',
                    description='this is a dummy thread to be used for testing',
                    user_id=1)
    return thread


@pytest.fixture(scope='module')
def new_rule():
    rule = Rule(title='Rules are awesome', content='Science proves that rules are awesome', thread_id=1)
    return rule


@pytest.fixture(scope='module')
def new_vote():
    vote = Vote(user_id=1, post_id=1, vote=True)
    return vote


@pytest.fixture(scope='module')
def new_message():
    message = Message(sender_id=2, recipient_id=1, title='this is a test message', body='I sure hope this works')
    return message


@pytest.fixture(scope='module')
def new_notification():
    notification = Notification(name='notification test', user_id=1, payload_json='I sure hope this works')

# creates database
@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(TestingConfig)
    test_client = flask_app.test_client()
    ctx = flask_app.test_request_context()
    print(flask_app.app_context())
    ctx.push()
    yield test_client
    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    # create db and tables
    _db.create_all()

    # Insert data
    # User,
    user1 = User(username='test1', email='test1@test.com', password='hello')
    user2 = User(username='test2', email='test2@test.com', password='hello')
    user3 = User(username='test3', email='test3@test.com', password='hello')
    _db.session.add(user1)
    _db.session.add(user2)
    _db.session.add(user3)
    # Thread,
    thread1 = Thread(title='thread test',
                    description='this is a dummy thread to be used for testing',
                    user_id=1)
    thread2 = Thread(title='thread test',
                    description='this is a dummy thread to be used for testing',
                    user_id=2)
    _db.session.add(thread1)
    _db.session.add(thread2)
    # Moderator,
    mod1 = Moderator(user_id=3, thread_id=1)
    mod2 = Moderator(user_id=3, thread_id=2)
    mod3 = Moderator(user_id=1, thread_id=2)
    mod4 = Moderator(user_id=2, thread_id=1)
    _db.session.add(mod1)
    _db.session.add(mod2)
    _db.session.add(mod3)
    _db.session.add(mod4)
    # Post,
    post1 = Post(title='hello world', content='world hello', user_id=1)
    post2 = Post(title='hello world', content='world hello', user_id=1)
    post3 = Post(title='hello world', content='world hello', user_id=1)
    post4 = Post(title='hello world', content='world hello', user_id=1)
    post5 = Post(title='hello world', content='world hello', user_id=1)
    post6 = Post(title='hello world', content='world hello', user_id=1)
    _db.session.add(post1)
    _db.session.add(post2)
    _db.session.add(post3)
    _db.session.add(post4)
    _db.session.add(post5)
    _db.session.add(post6)
    thread_post1 = Post(title='hello world', content='world hello', user_id=1, thread_id=2)
    thread_post2 = Post(title='hello world', content='world hello', user_id=2, thread_id=2)
    thread_post3 = Post(title='hello world', content='world hello', user_id=3, thread_id=1)
    thread_post4 = Post(title='hello world', content='world hello', user_id=1, thread_id=1)
    thread_post5 = Post(title='hello world', content='world hello', user_id=2, thread_id=2)
    thread_post6 = Post(title='hello world', content='world hello', user_id=3, thread_id=1)
    _db.session.add(thread_post1)
    _db.session.add(thread_post2)
    _db.session.add(thread_post3)
    _db.session.add(thread_post4)
    _db.session.add(thread_post5)
    _db.session.add(thread_post6)
    # Comment,
    comment1 = Comment(title='hello world', content='world hello', user_id=1, post_id=1)
    comment2 = Comment(title='hello world', content='world hello', user_id=2, post_id=1)
    comment3 = Comment(title='hello world', content='world hello', user_id=1, post_id=1)
    comment4 = Comment(title='hello world', content='world hello', user_id=2, post_id=1)
    comment5 = Comment(title='hello world', content='world hello', user_id=1, post_id=1)
    _db.session.add(comment1)
    _db.session.add(comment2)
    _db.session.add(comment3)
    _db.session.add(comment4)
    _db.session.add(comment5)
    # Rule,
    rule1 = Rule(title='Rules are awesome', content='Science proves that rules are awesome', thread_id=1)
    rule2 = Rule(title='Rules are awesome', content='Science proves that rules are awesome', thread_id=2)
    _db.session.add(rule1)
    _db.session.add(rule2)
    # Vote,
    vote = Vote(user_id=1, post_id=1, vote=True)
    vote2 = Vote(user_id=2, post_id=4, vote=False)
    vote3 = Vote(user_id=1, post_id=3, vote=True)
    vote4 = Vote(user_id=2, post_id=8, vote=False)
    vote5 = Vote(user_id=3, post_id=3, vote=True)
    _db.session.add(vote)
    _db.session.add(vote2)
    _db.session.add(vote3)
    _db.session.add(vote4)
    _db.session.add(vote5)
    _db.session.add(vote)
    # Message,
    message1 = Message(sender_id=2, recipient_id=1, title='this is a test message', body='I sure hope this works')
    message2 = Message(sender_id=1, recipient_id=2, title='this is a test message', body='I sure hope this works')
    message3 = Message(sender_id=2, recipient_id=1, title='this is a test message', body='I sure hope this works')
    _db.session.add(message1)
    _db.session.add(message2)
    _db.session.add(message3)
    # Notification
    notification = Notification(name='notification test', user_id=1, payload_json='I sure hope this works')

    _db.session.commit()

    yield _db

    _db.drop_all()

