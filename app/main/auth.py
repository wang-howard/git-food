import os, pathlib, requests
from flask import Flask, Blueprint, session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from .. import db
from gitfood import app

app.secret_key = os.environ.get("CLIENT_SECRET")
GOOGLE_CLIENT_ID = "213256229846-rappmhrpskr8hj7pp3lekhpiki14id7g.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    # TODO
    redirect_uri="http://localhost/callback"
)

auth = Blueprint("auth", __name__, template_folder="/templates")

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Unauthorized
        else:
            return function(*args, **kwargs)
    wrapper.__name__ = function.__name__
    return wrapper

@auth.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@auth.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/home")

# TODO
@auth.route("/signup")
def signup():
    return "Signup"

@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@auth.route("/home")
@login_is_required
def protected_area():
    return render_template("index.html")