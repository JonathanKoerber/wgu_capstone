"""
this test the for the messages blueprint

test use GET and POST to url's used in main to check the proper behavior
of the messages blueprint
"""
from flask import url_for


def test_send_message(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get(url_for('messages.send_message', recipient=1))
    assert response.status_code == 302

def test_message(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/search' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get(url_for('messages.message'))
    assert response.status_code == 302

def test_notifications(test_client, init_database):

    response = test_client.get(url_for('messages.notifications'))
    assert response.status_code == 302