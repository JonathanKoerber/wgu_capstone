"""
this test the for the users blueprint

test use GET and POST to url's used in main to check the proper behavior
of the users blueprint
"""
from flask import url_for
import pytest


def test_register(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/register')
    assert response.status_code == 200


def test_valid_register(test_client, init_database):
    """
    given: flask app
    when: /register is posted to (POST)
    then: check response is valid
    """
    response = test_client.post('/register',
                                data=dict(username='username',
                                          email='awesome@sause.com',
                                          password='FlaskIsAwesome',
                                          confirm='FlaskIsAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200


def test_invalid_register(test_client, init_database):
    """
       given: flask app
       when: /register is posted to (POST)
       then: check response is valid
       """
    response = test_client.post('/register',
                                data=dict(username='username',
                                          email='awesome@sause.com',
                                          password='FlaskIsAwesome',
                                          confirm='FlaskIsNotAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200


def test_valid_login_logout(test_client, init_database):
    """
    given: flask app
    when: /register is posted to (POST)
    then: check response is valid
     """
    response = test_client.post('/login',
                                data=dict(email='test1@test.com', password='hello'),
                                follow_redirects=True)
    assert response.status_code == 200

    response = test_client.post('/login',
                                data=dict(email='this in not an email', password='hello'),
                                follow_redirects=True)
    assert response.status_code == 200


def test_invalid_login_logout(test_client, init_database):
    """
    given: flask app
    when: /register is posted to (POST)
    then: check response is valid
     """
    response = test_client.post('/login',
                                data=dict(email='test1@test.com', password='hello'),
                                follow_redirects=True)
    assert response.status_code == 200
    response = test_client.get('/logout')
    assert response.status_code == 302


def test_account(test_client, init_database):
    """
        GIVEN flask app
        WHEN  the '/search' page is requested (GET)
        THEN check the response is valid
        """
    response = test_client.get('/account')
    assert response.status_code == 302


def test_user_post(test_client, init_database):
    """
            GIVEN flask app
            WHEN  the '/search' page is requested (GET)
            THEN check the response is valid
            """
    response = test_client.get(url_for('users.user_posts', username='test1'), follow_redirects=True)

    assert response.status_code == 200


def test_user_find_user(test_client, init_database):
    responce = test_client.get(url_for('users.find_user'))
    assert responce.status_code == 302


def test_user_search_user(test_client, init_database):
    responce = test_client.get(url_for('users.search_user'),
                               data=dict(query='test1'),
                               follow_redirects=True)
    assert responce.status_code == 200
