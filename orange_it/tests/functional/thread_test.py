"""
this test the for the thread blueprint

test use GET and POST to url's used in thread to check the proper behavior
of the main blueprint
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