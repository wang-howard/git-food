import os, sys, requests
from flask import render_template, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
from flask_login import login_required
from . import main
from .. import db
from ..models import User, Ingredient, Recipe

# google_client_id = "213256229846-rappmhrpskr8hj7pp3lekhpiki14id7g.apps.googleusercontent.com"
# google_client_secret = os.environ.get("CLIENT_SECRET")
# google_redirect_uri = "http://localhost/callback"

# oauth = OAuth(app)
# google = oauth.remote_app(
#     "google",
#     consumer_key=google_client_id,
#     consumer_secret=google_client_secret,
#     request_token_params={
#         "scope": "email",
#     },
#     base_url="https://www.googleapis.com/oauth2/v1/",
#     request_token_url=None,
#     access_token_method="POST",
#     access_token_url="https://accounts.google.com/o/oauth2/token",
#     authorize_url="https://accounts.google.com/o/oauth2/auth",
# )

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
    
# @main.route("/login", methods=["GET"])
# def login():
#     try:
#         return google.authorize(callback=url_for('authorized', _external=True))
#     except Exception as ex:
#         print(ex, file=sys.stderr)
#         return render_template("error.html", message=ex)

# @main.route("/login/authorized", methods=["GET"])
# def authorized():
#     response = google.authorized_response()
#     if response is None or response.get("access_token") is None:
#         return "Login failed."

#     session["google_token"] = (response["access_token"], "")
#     me = google.get("userinfo")
#     # Here, "me.data" contains user information.
#     # You can perform registration process using this information if needed.

#     return redirect(url_for("index"))

# @main.route("/logout")
# def logout():
#     session.pop("google_token", None)
#     return redirect(url_for("index"))

# @oauth.tokengetter
# def get_google_oauth_token():
#     return session.get("google_token")
