import sys
from flask import render_template, abort, redirect, session, request, jsonify
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
            return render_template("home.html")
        else:
            return render_template("home.html")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/u/<un>", methods=["GET"])
@login_required
def user(un):
    """
    Renders user profile page
    """
    user = User.query.get(current_user.id)
    other = User.query.filter_by(username=un).first()
    if user == None or other == None:
        abort(404)

    try:
        if user.username == un:
            return render_template("user.html")
        else:
            return render_template("view_other_user.html", other=other)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/u/<un>/<recipe_id>", methods=["GET"])
@login_required
def view_recipe(un, recipe_id):
    recipe = Recipe.query.get(int(recipe_id))
    other_user = User.query.filter_by(username=un).first()
    if recipe == None or other_user == None:
        abort(404)

    try:
        if current_user.username == un:
            return render_template("recipe.html", recipe=recipe)
        else:
            return render_template("view_public_recipe.html", recipe=recipe, other=other_user)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/u/<un>/edit-user", methods=["POST"])
@login_required
def edit_user(un):
    """
    Called by JS AJAX to update database w/o refreshing page. Does not return a
    template but a JSON file to AJAX method.
    """

    if current_user.username != un:
        abort(401)

    new_data = request.form.get("new_data")
    type = request.form.get("item_changed")
    user = User.query.filter_by(username=un).first()
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
    user = User.query.filter_by(username=un).first()
    if user is None:
        return render_template("error.html", message="User Not Found")
    if current_user.username != un:
        abort(401)

    try:
        return render_template("new_recipe.html")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/u/<un>/submit-recipe", methods=["POST"])
@login_required
def submit_recipe(un):
    user = User.query.filter_by(username=un).first()
    if user is None:
        return render_template("error.html", message="User Not Found")
    if current_user.username != un:
        abort(401)
    
    try:
        new_recipe = Recipe(id=generate_recipe_id(),
                        title=request.form.get("recipe-name"),
                        description=request.form.get("description"),
                        gf = bool(request.form.get("gluten-free")) if request.form.get("gluten-free") else False,
                        vegan=bool(request.form.get("vegan")) if request.form.get("vegan") else False,
                        private=bool(request.form.get("is-private")) if request.form.get("is-private") else False,
                        instructions=request.form.get("instructions"),
                        author_id = user.id)
        db.session.add(new_recipe)
        db.session.commit()

        num_ingredients = request.form.get("ingredient-count")
        for i in range(int(num_ingredients)):
            new_ingredient = Ingredient(id=generate_ingredient_id(),
                                        name=request.form.get(f"ingredient-name{i}"),
                                        quantity=int(request.form.get(f"quantity{i}")),
                                        unit=request.form.get(f"unit{i}"),
                                        recipe_id = new_recipe.id)
            db.session.add(new_ingredient)
        db.session.commit()
        
        return redirect(f"/u/{user.username}")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
    
@main.route("/u/<un>/<recipe_id>/edit", methods=["GET"])
@login_required
def show_edit_recipe(un, recipe_id):
    if current_user.username != un:
        abort (401)
    try:
        recipe = Recipe.query.get(int(recipe_id))
        if current_user.username != un or recipe is None:
            abort(404)
        return render_template("edit_recipe.html", recipe=recipe)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/u/<un>/<recipe_id>/save-recipe-edit", methods=["POST"])
@login_required
def make_recipe_edit(un, recipe_id):
    user = User.query.filter_by(username=un).first()
    if user is None:
        return render_template("error.html", message="User Not Found")
    if current_user.username != un:
        abort(401)

    parent_recipe = Recipe.query.get(int(recipe_id))
    if parent_recipe == None:
        abort(500)

    try:
        new_recipe = Recipe(id=generate_recipe_id(),
                        title=request.form.get("recipe-name"),
                        description=request.form.get("description"),
                        gf = bool(request.form.get("gluten-free")) if request.form.get("gluten-free") else False,
                        vegan=bool(request.form.get("vegan")) if request.form.get("vegan") else False,
                        private=bool(request.form.get("is-private")) if request.form.get("is-private") else False,
                        instructions=request.form.get("instructions"),
                        version=parent_recipe.version+1,
                        author_id = user.id)
        db.session.add(new_recipe)

        parent_recipe.is_head = False
        parent_recipe.child_id = new_recipe.id
        db.session.add(parent_recipe)
        db.session.commit()

        num_ingredients = request.form.get("ingredient-count")
        for i in range(int(num_ingredients)):
            new_ingredient = Ingredient(id=generate_ingredient_id(),
                                        name=request.form.get(f"ingredient-name{i}"),
                                        quantity=request.form.get(f"quantity{i}"),
                                        unit=request.form.get(f"unit{i}"),
                                        recipe_id = new_recipe.id)
            db.session.add(new_ingredient)
        db.session.commit()
        
        return redirect(f"/u/{user.username}")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/u/<un>/<recipe_id>/delete-recipe", methods=["POST"])
@login_required
def delete_recipe(un, recipe_id):
    """
    function called by deleteRecipe() JS function to delete a recipe from a
    user's profile page without needing to refresh.
    """
    if current_user.username != un:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    try:
        recipe = Recipe.query.get(int(recipe_id))
        parent_recipe = Recipe.query.filter_by(child_id=recipe_id).first()
        if parent_recipe == None:
            pass
        else:
            delete_recipe(un, parent_recipe.id)
        
        if recipe and recipe.author_id == current_user.id:
            assoc_igs = Ingredient.query.filter_by(recipe_id=int(recipe_id)).all()
            for ig in assoc_igs:
                db.session.delete(ig)
            db.session.delete(recipe)
            db.session.commit()
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Recipe not found"}), 404
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
    
