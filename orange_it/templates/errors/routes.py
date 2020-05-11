
from flask import Blueprint, make_response, render_template

error = Blueprint('users', __name__)

@error.errorhandler(403)
def not_found():
    return make_response(render_template('403.html'))

@error.errorhandler(404)
def not_found():
    return make_response(render_template('404.html'))

@error.errorhandler(500)
def not_found():
    return make_response(render_template('500.html'))