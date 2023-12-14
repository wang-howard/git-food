"""
Commonly used functions in code to avoid repitition
"""
import random
from .. import db
from ..models import User, Recipe, Ingredient

def generate_recipe_id():
    id = str(random.randint(1000000, 9999999))
    while True:
        query = Recipe.query.get(id)
        if query == None:
            return id

def generate_ingredient_id():
    id = str(random.randint(1000000, 9999999))
    while True:
        query = Ingredient.query.get(id)
        if query == None:
            return id
