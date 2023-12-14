import sys
from flask import render_template, abort, redirect, url_for, session, request, jsonify
from flask_login import login_required, current_user
from . import main
from .. import db
from ..models import User, Ingredient, Recipe
from .common import generate_recipe_id, generate_ingredient_id

@main.route("/", methods=["GET"])
def index():
    """
    Renders home/landing page
    """
    try:
        if current_user.is_authenticated:
            return render_template("base.html")
        else:
            return render_template("base.html")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/u/<un>", methods=["GET"])
@login_required
def user(un):
    """
    Renders user profile page
    """
    user = User.query.get(session["user_id"])

    if user.username != un:
        abort(401)
    if user is None:
        return render_template("error.html", message="User Not Found")
    
    try:
        return render_template("user.html", name=user.name, pic_url=user.picture, about_me=user.about_me)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/edit-user", methods=["POST"])
def edit_user():
    """
    Called by JS AJAX to update database w/o refreshing page. Does not return a
    template but a JSON file to AJAX method.
    """
    new_data = request.form.get("new_data")
    type = request.form.get("item_changed")
    
    user = User.query.get(session["user_id"])
    if user:
        if type == "display-name":
            user.name = new_data
        elif type == "about-me":
            user.about_me = new_data
        else:
            return jsonify({"status": "error", "message": "Improperly formatted response."}), 400
        db.session.commit()
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "User not found."}), 400

@main.route("/u/<un>/new-recipe", methods=["GET"])
@login_required
def recipe(un):
    """
    Renders create new recipe page
    """
    user = User.query.get(session["user_id"])

    if user.username != un:
        abort(401)
    if user is None:
        return render_template("error.html", message="User Not Found")

    try:
        return render_template("new_recipe.html")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/u/<un>/submit_recipe", methods=["POST"])
@login_required
def submit_recipe(un):
    user = User.query.get(session["user_id"])

    if user.username != un:
        abort(401)
    if user is None:
        return render_template("error.html", message="User Not Found")
    new_recipe = Recipe(id=generate_recipe_id(),
                    title=request.form.get("recipe-name"),
                    description=request.form.get("description"),
                    gf = bool(request.form.get("gluten-free")) if request.form.get("gluten-free") else False,
                    vegan=bool(request.form.get("vegan")) if request.form.get("vegan") else False,
                    private=bool(request.form.get("is-private")) if request.form.get("is-private") else False,
                    instructions=request.form.get("instructions"),
                    author_id = user.id)

    num_ingredients = request.form.get("ingredient-count")
    for i in range(int(num_ingredients)):
        new_ingredient = Ingredient(id=generate_ingredient_id(),
                                    name=request.form.get(f"ingredient-name{i}"),
                                    quantity=int(request.form.get(f"quantity{i}")),
                                    unit=request.form.get(f"unit{i}"),
                                    recipe_id = new_recipe.id)
        db.session.add(new_ingredient)
    
    db.session.add(new_recipe)
    db.session.commit()
    return redirect(f"/u/{user.username}")
    # try:
        
    # except Exception as ex:
    #     print(ex, file=sys.stderr)
    #     return render_template("error.html", message=ex)
