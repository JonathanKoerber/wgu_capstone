"""
this test the for the rules blueprint

test use GET and POST to url's used in main to check the proper behavior
of the rules blueprint
"""


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
    response = test_client.get('/search')
    assert response.status_code == 200