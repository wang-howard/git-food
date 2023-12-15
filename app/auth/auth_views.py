"""
View functions that pertain specifically to user authentification,
login, and logout.
"""

import sys, os, pathlib, requests, random, zlib
from flask import session, request, abort, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests

from . import auth
from .. import db
from ..models import User, Recipe, Ingredient

GOOGLE_CLIENT_ID = "213256229846-rappmhrpskr8hj7pp3lekhpiki14id7g.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    # TODO
    redirect_uri=os.environ["CALLBACK_URI"]
)

def crc32_hash(num):
    # Convert the integer to bytes
    num_bytes = num.to_bytes((num.bit_length() + 7) // 8, "big")
    
    # Calculate the CRC32 hash and ensure it's positive
    hash_value = zlib.crc32(num_bytes) & 0xffffffff
    
    return hash_value

@auth.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@auth.route("/callback")
def callback():
    try:
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

        id = crc32_hash(int(id_info.get("sub")))
        user = User.query.get(id)

        # new user, first time logging in w/ Google
        if user is None:
            session["username"] = id_info.get("family_name")+id_info.get("given_name")[0]+str(id)[0:4]
            user = User(id=id,
                        name=id_info.get("name"),
                        username=session["username"],
                        email=id_info.get("email"),
                        picture=id_info.get("picture"))
            db.session.add(user)
            db.session.commit()
        
        session["user_id"] = id
        session["username"] = user.username
        login_user(User.query.get(id))
        return redirect(f"/u/{user.username}")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@auth.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("main.index"))