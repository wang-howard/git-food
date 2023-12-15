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
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_head = db.Column(db.Boolean, default=True)
    child_id = db.Column(db.Integer, default=None)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    collab_id = db.Column(db.Integer, nullable=True, default=None)

    def __repr__(self):
        return f"<Recipe ID: {self.id}, Title: {self.title}>"

    def __eq__(self, other):
        self_ingredients = Ingredient.query.filter_by(recipe_id=self.id).all()
        other_ingredients = Ingredient.query.filter_by(recipe_id=other.id).all()

        if len(self_ingredients) != len(other_ingredients):
            return False
        
        for i in range(len(self_ingredients)):
            if self_ingredients[i] != other_ingredients[i]:
                return False

        return self.title == other.title and self.description == other.description \
            and self.gf == other.gf and self.vegan == other.vegan \
            and self.instructions == other.instructions and self.author_id == other.author_id \
            and self.collab_id == other.collab_id
        

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Double , nullable=False)
    unit = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)

    def __repr__(self):
        return f"<Ingredient {self.name}, Quantity: {self.quantity}, Unit: {self.unit}>"
    
    def __eq__(self, other):
        return self.name == other.name and self.quantity == other.quantity and self.unit == other.unit
