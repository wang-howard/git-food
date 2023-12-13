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
        if "google_token" in session:
            me = google.get("userinfo")
            return jsonify({"data": me.data})
        return render_template("landing.html")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
