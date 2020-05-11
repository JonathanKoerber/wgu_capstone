import os
from orange_it import models
import pytest

user_test = models.User

"""
GIVEN a User model
WHEN a new User is created
THEN check the email, hashed_password, authentication

"""


def test_new_user(new_user):
    assert new_user.username == 'test'
    assert new_user.email == 'test@test.com'
    assert new_user.password == 'hello'


def test_moderator(new_mod):
    assert new_mod.user_id == 3
    assert new_mod.thread_id == 4


def test_post(new_post):
    assert new_post.title == 'hello world'
    assert new_post.content == 'world hello'
    assert new_post.user_id == 1


def test_post_thread(new_thread_post):
    assert new_thread_post.title == 'hello world'
    assert new_thread_post.content == 'world hello'
    assert new_thread_post.user_id == 1
    assert new_thread_post.thread_id == 1


def test_comment(new_comment):
    assert new_comment.title == 'hello world'
    assert new_comment.content == 'world hello'
    assert new_comment.user_id == 1
    assert new_comment.post_id == 1


def test_thread(new_thread):
    assert new_thread.title == 'thread test'
    assert new_thread.description == 'this is a dummy thread to be used for testing'
    assert new_thread.user_id == 1


def test_rule(new_rule):
    assert new_rule.title == 'Rules are awesome'
    assert new_rule.content == 'Science proves that rules are awesome'
    assert new_rule.thread_id == 1


def test_vote(new_vote):
    assert new_vote.user_id == 1
    assert new_vote.post_id == 1
    assert True == new_vote.vote


def test_message(new_message):
    assert new_message.sender_id == 2
    assert new_message.recipient_id == 1
    assert new_message.title == 'this is a test message'
    assert new_message.body == 'I sure hope this works'


def test_notification(new_notification):
    # todo figure how this object works and write a test
    pass

