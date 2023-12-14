import sys
from flask import render_template, abort, redirect, url_for, session
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import User, Ingredient, Recipe

@main.route("/", methods=["GET"])
def index():
    """
    Renders home/landing page
    """
    try:
        if current_user.is_authenticated:
            return render_template("base.html", username=session["username"])
        else:
            return render_template("base.html")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/u/<un>", methods=["GET"])
@login_required
def user(un):
    """
    Renders user profile page
    """
    user = User.query.get(session["user_id"])

    if user.username != un:
        abort(401)

    if user is None:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
    
    try:
        return render_template("user.html", username=user.username,
                               name=user.name, pic_url=user.picture, about_me=user.about_me)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
    
@main.route("/u/<un>/new-recipe", methods=["GET"])
@login_required
def recipe(un):
    """
    Renders create new recipe page
    """
    user = User.query.get(session["user_id"])

    if user.username != un:
        abort(401)

    if user is None:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
    try:
        return render_template("recipe.html", username=un)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)