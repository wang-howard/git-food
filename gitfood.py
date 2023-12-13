"""
Defines application instance.
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app import create_app, db
from app.models import User, Recipe, Ingredient

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,
                User=User,
                Recipe=Recipe,
                Ingredient=Ingredient)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5553", debug=True)
