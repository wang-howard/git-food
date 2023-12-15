from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    picture = db.Column(db.String)
    about_me = db.Column(db.String, default="")
    recipes = db.relationship("Recipe", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User ID: {self.id}, Name: {self.name}>"
    
    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True
        
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    gf = db.Column(db.Boolean, default=False)
    vegan = db.Column(db.Boolean, default=False)
    private = db.Column(db.Boolean, default=False)
    ingredients = db.relationship("Ingredient", backref="recipe")
    instructions = db.Column(db.String, nullable=False)
    version = db.Column(db.Integer, default=1)
    child_id = db.Column(db.Integer, default=None)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_head = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Recipe ID: {self.id}, Title: {self.title}>"

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)

    def __repr__(self):
        return f"<Ingredient {self.name}, Quantity: {self.quantity}, Unit: {self.unit}>"