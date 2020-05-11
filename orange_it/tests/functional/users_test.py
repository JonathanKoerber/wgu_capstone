"""
this test the for the users blueprint

test use GET and POST to url's used in main to check the proper behavior
of the users blueprint
"""


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
                                data = dict(email='test1@test.com', password='hello'),
                                follow_redirects=True)
    assert response.status_code == 200

    response = test_client.post('/login',
                                data = dict(email='this in not an email', password='hello'),
                                follow_redirects=True)
    assert response.status_code == 200

    assert b"Login Unsuccessful. Please check email and password" in response


def test_invalid_login_logout(test_client, init_database):
    """
    given: flask app
    when: /register is posted to (POST)
    then: check response is valid
     """
    response = test_client.post('/login',
                                data = dict(email='test1@test.com', password='hello'),
                                follow_redirects=True)
    assert response.status_code == 200

def test_search(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/search' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/search')
    assert response.status_code == 200
