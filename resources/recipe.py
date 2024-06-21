import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import recipes


blp = Blueprint("recipes", __name__, description="Operations on recipes")

@blp.route("/recipe")
class RecipeList(MethodView):
    def get(self):
        return {"recipes": list(recipes.values())}

    def post(self):
        request_recipe = request.get_json()
        if "name" not in request_recipe or "ingredients" not in request_recipe:
            abort(400, message="Bad request. Ensure 'name' or 'ingredients' are included in the JSON payload.")
        for recipe in recipes.values():
            if request_recipe["name"] == recipe["name"]:
                abort(400, message="Recipe already exists.")

        recipe_id = uuid.uuid4().hex
        new_recipe = {**request_recipe, "id":recipe_id}
    
        recipes[recipe_id] = new_recipe
        return new_recipe, 201

@blp.route("/recipe/<string>:recipe_id")
class Recipe(MethodView):
    def get(self, recipe_id):
        try:
            return recipes[recipe_id]
        except KeyError:
            abort(404, message="Recipe not found.")
    
    def put(self, recipe_id):
        request_recipe = request.get_json()
        if "name" not in request_recipe or "ingredients" not in request_recipe:
            abort(400, message="Bad request. Ensure 'name', and 'ingredients' are included in the JSON payload.")
        try:
            recipe = recipes[recipe_id]
            recipe |= request_recipe

            return recipe
        except KeyError:
            abort(404, message="Recipe not found.")

    def delete(self, recipe_id):
        try:
            del recipes[recipe_id]
            return {"message":"Recipe deleted."}
        except KeyError:
            abort(404, message="Recipe not found.")