
"""
this test the for the post blueprint

test use GET and POST to url's used in main to check the proper behavior
of the post blueprint
"""
from flask import url_for


def test_new_post(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get(url_for('posts.new_post'))
    assert response.status_code == 302

def test_new_thread_post(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/search' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get(url_for('posts.new_post', thread_id=1))
    assert response.status_code == 302

def test_post(test_client, init_database):
    response = test_client.get(url_for('posts.post', post_id=1))
    assert response.status_code == 200

def test_comment(test_client, init_database):
    response = test_client.get(url_for('posts.comment', post_id=1))
    assert response.status_code == 302

def test_update_post(test_client, init_database):
    response = test_client.get(url_for('posts.update_post', post_id=1))
    assert response.status_code == 302

# todo need to mock the current users
def test_invalit_delete_post(test_client, init_database):
    response = test_client.get(url_for('posts.delete_post', post_id=1, thread_id=1))
    assert response.status_code == 405

def delete_comment(test_client, init_database):
    login = test_client.post('/login',
                             data=dict(email='test1@test.com', password='hello'),
                             follow_redirects=True)
    response = test_client.get(url_for('posts.delete_comment', comment_id=1))
    assert response.status_code == 302

