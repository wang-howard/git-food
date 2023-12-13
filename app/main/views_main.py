import sys
from flask import render_template, url_for
from flask import session, request
from flask_login import login_required
from . import bp
from .. import db
from ..models import User, Recipe, Ingredient

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
