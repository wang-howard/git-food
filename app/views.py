import sys
from flask import Blueprint, render_template, url_for
from flask import session, request
from flask_login import login_required
from . import db
from .models import User, Recipe, Ingredient

bp = Blueprint("main", __name__, template_folder="/templates")

@bp.route("/", methods=["GET"])
def index():
    """
    Renders home/landing page
    """
    try:
        return render_template("index.html")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500