import os, sys, requests
from flask import render_template, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
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
        if "google_id" in session:
            return render_template(url_for("auth.home"))
        else:
            return render_template("index.html", name="Anon")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
