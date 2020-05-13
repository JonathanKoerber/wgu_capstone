"""
this test the for the main blueprint

test use GET and POST to url's used in main to check the proper behavior
of the main blueprint
"""
from flask import url_for


def test_index(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_search(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/search' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get(url_for('main.search'),
                               data=dict(query='hello world'),
                               follow_redirects=True)

    assert response.status_code == 200


def test_about(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/search' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get(url_for('main.about'))

    assert response.status_code == 200
