import sys
from flask import render_template, redirect, url_for, session
from flask_login import login_required
from . import main
from .. import db
from ..models import User, Ingredient, Recipe

@main.route("/", methods=["GET"])
def index():
    """
    Renders home/landing page
    """
    try:
        if session:
            return render_template("base.html", active=True, username=session["username"])
        else:
            return render_template("base.html", active=False)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/u/<user>", methods=["GET"])
@login_required
def user():
    """
    Renders user page
    """
    user = User.query.get(session["user_id"])
    if user is None:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
    
    try:
        return render_template("user.html", active=True, username=session["username"],
                               name=user.name, pic_url=user.picture, about_me=user.about_me)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)