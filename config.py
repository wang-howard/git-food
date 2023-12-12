"""
Configuration file for Flask app. Sets necessary environment variables
for Flask and SQLAlchemy.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# TODO
class Config:
    SECRET_KEY = os.environ.get("SEC_KEY") or "------"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI') or \
        "postgres://git_food_user:uelFgIGe9GCTYYttir2XHNJ9Y4auBX4G@dpg-clrqa1cm7d1c73f483tg-a.ohio-postgres.render.com/git_food"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # connection pooling configurations
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 1800
