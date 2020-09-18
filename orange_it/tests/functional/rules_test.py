"""
this test the for the rules blueprint

test use GET and POST to url's used in main to check the proper behavior
of the rules blueprint
"""
from flask import url_for


def test_new_rule(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.post(url_for('rules.new_rule', thread_id=1))
    assert response.status_code == 302


def test_update_rule(test_client, init_database):
    """
    GIVEN flask app
    WHEN  the '/search' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get(url_for('rules.update_post', rule_id=1))
    assert response.status_code == 302


def test_delete_rule(test_client, init_database):
    response = test_client.post(url_for('rules.delete_post', rule_id=1))
    assert response.status_code == 302