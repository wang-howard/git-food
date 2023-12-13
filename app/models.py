from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    recipes = db.relationship("Recipe", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User ID: {self.id}, Username: {self.username}>"

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