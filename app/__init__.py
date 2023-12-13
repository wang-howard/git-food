"""
Initializes the GitFood app, db, and CAS auth client to be used by various files
within app/ and the main directory. The only function, create_app, creates the
Flask app, initializes the SQLAlchemy object and returns the app. db and
cas_client global variables are imported by other files.
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from app.cas import CASClient
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

# TODO
# cas_client = CASClient(version=3, service_url=os.getenv("SERVICE_URL"),
#                        server_url="https://fed.princeton.edu/cas/")

# TODO
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Flask extensions
    db.init_app(app)
    login_manager.init_app(app)

    # register blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    
    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint)

    return app
