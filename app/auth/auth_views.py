import sys, os, pathlib, requests, random
from flask import session, abort, redirect, url_for, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from flask_login import login_user, logout_user, login_required

from . import auth
from gitfood import app
from ..models import User, Recipe, Ingredient
from .. import db

app.secret_key = os.environ.get("CLIENT_SECRET")
GOOGLE_CLIENT_ID = "213256229846-rappmhrpskr8hj7pp3lekhpiki14id7g.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    # TODO
    redirect_uri="http://127.0.0.1:5553/callback"
)

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

        id = id_info.get("sub")
        session["user_id"] = id
        user = None
        # new user, first time logging in w/ Google
        if User.query.get(id) is None:
            user = User(id=id,
                        username=_generate_username(id_info),
                        email=id_info.get("email"),
                        picture=id_info.get("picture"))
            db.session.add(user)
            db.session.commit()
        login_user(User.query.get(id))
        return redirect(url_for("main.index"))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

def _generate_username(id_info):
    while True:
        un = id_info.get("given_name")[0] + id_info.get("family_name") + str(random.randint(100, 999))
        if User.query.filter_by(username=un) is None:
            return un

@auth.route("/logout")
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("main.index"))