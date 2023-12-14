from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    picture = db.Column(db.String)
    about_me = db.Column(db.String, default="")
    recipes = db.relationship("Recipe", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User ID: {self.id}, Username: {self.username}>"
    
    def is_active(self):
        """
        True, as all users are active.
        """
        return True

    def get_id(self):
        """
        Return the email address to satisfy Flask-Login's requirements.
        """
        return self.email

    def is_authenticated(self):
        """
        Return True if the user is authenticated.
        """
        return self.authenticated

    def is_anonymous(self):
        """
        False, as anonymous users aren't supported.
        """
        return False

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    gluten_free = db.Column(db.Boolean, default=False)
    vegan = db.Column(db.Boolean, default=False)
    instructions = db.Column(db.Text, nullable=False)
    version = db.Column(db.Integer, default=1)
    parent_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ingredients = db.relationship("Ingredient", backref="recipe")

    def save_version(self):
        pass

    def revert_to_version(self, version):
        pass

    def __repr__(self):
        return f"<Recipe ID: {self.id}, Title: {self.title}>"

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)

    def __repr__(self):
        return f"<Ingredient {self.name}, Quantity: {self.quantity}, Unit: {self.unit}>"