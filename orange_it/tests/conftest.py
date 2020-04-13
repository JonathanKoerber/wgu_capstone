import pytest
from orange_it.models import User, Owner, Post, Moderator, Comment, Thread, Rule, Vote, Message, Notification


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
