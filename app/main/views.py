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
    Renders home/landing page based on authentication status.
    """
    try:
        if current_user.is_authenticated:
            return render_template("home.html")
        else:
            return render_template("home.html")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/search", methods=["POST"])
def search_recipes():
    """
    Called dynamically by AJAX to search recipe database with search box input.
    """
    search_text = request.form["query"]
    results = None
    if search_text == None:
        results = Recipe.query.filter_by(is_head=True, private=False).all()
    else:
        results = Recipe.query.filter(Recipe.is_head==True,
                                      Recipe.private==False,
                                      Recipe.title.ilike(f"%{search_text}%")).all()
    return render_template("search_results.html", recipe_query=results, user=User)

@main.route("/u/<un>", methods=["GET"])
def user(un):
    """
    Renders a user profile page based on permissions.
    """
    other = User.query.filter_by(username=un).first_or_404()

    try:
        if not current_user.is_authenticated or current_user.username != un:
            return render_template("view_other_user.html", other=other)
        else:
            return render_template("user.html")
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
    user = User.query.get_or_404(current_user.id)
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

@main.route("/u/<un>/<recipe_id>", methods=["GET"])
def view_recipe(un, recipe_id):
    """
    Displays a recipe page based on permissions.
    """
    recipe = Recipe.query.get_or_404(recipe_id)
    url_user = User.query.filter_by(username=un).first_or_404()

    try:
        if recipe.author_id == url_user.id:
            if current_user.is_authenticated and current_user.username == url_user.username:
                return render_template("recipe.html", recipe=recipe)
            else:
                return render_template("view_public_recipe.html", recipe=recipe, other=url_user)
        else:
            abort(404)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@main.route("/u/<un>/new-recipe", methods=["GET"])
@login_required
def recipe(un):
    """
    Renders form page to create a new recipe.
    """
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
    """
    Retrieves form information, processes data, and add to database before
    returning user to profile.
    """
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
                                        quantity=float(request.form.get(f"quantity{i}")),
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
    recipe = Recipe.query.get_or_404(recipe_id)
    if current_user.username != un and current_user.id != recipe.collab_id:
        abort (401)
    try:
        recipe = Recipe.query.get(recipe_id)
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

    parent_recipe = Recipe.query.get(recipe_id)
    if parent_recipe == None:
        abort(500)

    if current_user.username != user.username or current_user.id != parent_recipe.collab_id:
            abort(401)
        
    try:
        new_recipe = Recipe(id=generate_recipe_id(),
                        title=request.form.get("recipe-name"),
                        description=request.form.get("description"),
                        gf = bool(request.form.get("gluten-free")) if request.form.get("gluten-free") else False,
                        vegan=bool(request.form.get("vegan")) if request.form.get("vegan") else False,
                        private=bool(request.form.get("is-private")) if request.form.get("is-private") else False,
                        instructions=request.form.get("instructions"),
                        version=parent_recipe.version+1,
                        author_id = user.id,
                        collab_id=parent_recipe.collab_id)
        db.session.add(new_recipe)

        if parent_recipe == new_recipe:
            db.session.remove(new_recipe)
            return redirect(f"/u/{un}")

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
        recipe = Recipe.query.get(recipe_id)
        parent_recipe = Recipe.query.filter_by(child_id=recipe_id).first()
        if parent_recipe != None:
            delete_recipe(un, parent_recipe.id)
        
        if recipe and recipe.author_id == current_user.id:
            assoc_igs = Ingredient.query.filter_by(recipe_id=recipe_id).all()
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
    


@main.route("/u/<un>/<recipe_id>/versions", methods=["GET"])
@login_required
def view_versions(un, recipe_id):
    # Ensure that the user requesting the versions is the author
    if current_user.username != un:
        return abort(401)

    try:
        current_recipe = Recipe.query.get_or_404(recipe_id)
        if current_recipe.author_id != current_user.id:
            return abort(401)
        
        while not current_recipe.is_head:
            current_recipe = Recipe.query.get(int(current_recipe.child_id))

        previous_versions = collect_previous_versions(current_recipe.id)
        return render_template("previous_versions.html", recipe=current_recipe, recipe_versions=previous_versions)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=str(ex))

def collect_previous_versions(recipe_id):
    previous_recipes = []
    parent_recipe = Recipe.query.filter_by(child_id=recipe_id).first()
    
    while parent_recipe:
        previous_recipes.append(parent_recipe)
        parent_recipe = Recipe.query.filter_by(child_id=parent_recipe.id).first()
    
    # Return the list in reverse order to start from the first version
    return previous_recipes[::-1]