"""
this test the for the thread blueprint

test use GET and POST to url's used in thread to check the proper behavior
of the main blueprint
"""
from flask import url_for


def test_thread(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get(url_for('thread.thread', thread_id=1))
    assert response.status_code == 200


def test_search_thread(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/search' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get(url_for('thread.search_thread', thread_id=1))
    assert response.status_code == 302

def test_new_thread(test_client, init_database):
    current_user = test_client.post('/register',
                                data=dict(username='username',
                                          email='awesome@sause.com',
                                          password='FlaskIsAwesome',
                                          confirm='FlaskIsAwesome'),
                                follow_redirects=True)
    response = test_client.post(url_for('thread.create_thread'))
    assert response.status_code ==302

def test_manage_threadt(test_client, init_database):
    response = test_client.post('/login',
                                data=dict(email='test1@test.com', password='hello'),
                                follow_redirects=True)
    response = test_client.get(url_for('thread.manage_thread', thread_id=1))
    assert response.status_code == 302


def test_delete(test_client, init_database):
    response = test_client.post(url_for('thread.delete', thread_id=1, object_id=2, object_str='post'))
    assert response.status_code == 302

def test_update_thread(test_client, init_database):
    response = test_client.get(url_for('thread.update_thread', thread_id=2))
    assert response.status_code == 302


def test_mod_thread(test_client, init_database):
    response = test_client.post(url_for('thread.mod_thread', thread_id=1))
    assert response.status_code == 302

def test_search_mod(test_client, init_database):
    response = test_client.get(url_for('thread.search_mod', thread_id=1,
                                       data=dict(query='hello world'),
                                       follow_redirects=True))
    assert response.status_code == 302




