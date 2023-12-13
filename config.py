"""
Configuration file for Flask app. Sets necessary environment variables for Flask
and SQLAlchemy.
SET ENVIRON:
export FLASK_APP=gitfood.py
export DB_URI=postgresql://git_food_user:uelFgIGe9GCTYYttir2XHNJ9Y4auBX4G@dpg-clrqa1cm7d1c73f483tg-a.ohio-postgres.render.com/git_food
export SEC_KEY=uelFgIGe9GCTYYttir2XHNJ9Y4auBX4G
export CLIENT_SECRET=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
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# TODO
class Config:
    SECRET_KEY = os.environ.get("SEC_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # connection pooling configurations
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 1800
