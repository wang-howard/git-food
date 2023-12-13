"""
Creates Flask blueprint to be used by view functions to direct routes. Views
and errors must be imported after bp is initialized due to circular
dependencies.
"""

from flask import Blueprint

main = Blueprint("main", __name__)

# TODO
from . import views_main, views_user, errors
