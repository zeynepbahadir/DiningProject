import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import recipes
from schemas import RecipeSchema, RecipeUpdateSchema

blp = Blueprint("recipes", __name__, description="Operations on recipes")


@blp.route("/recipe/<string:recipe_id>")
class Recipe(MethodView):
    def get(self, recipe_id):
        try:
            return recipes[recipe_id]
        except KeyError:
            abort(404, message="Recipe not found.")
    
    @blp.arguments(RecipeUpdateSchema)
    def put(self, request_recipe, recipe_id):
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

@blp.route("/recipe")
class RecipeList(MethodView):
    def get(self):
        return {"recipes": list(recipes.values())}

    @blp.arguments(RecipeSchema)
    def post(self, request_recipe):
        for recipe in recipes.values():
            if request_recipe["name"] == recipe["name"]:
                abort(400, message="Recipe already exists.")

        recipe_id = uuid.uuid4().hex
        new_recipe = {**request_recipe, "id":recipe_id}
    
        recipes[recipe_id] = new_recipe
        return new_recipe, 201

