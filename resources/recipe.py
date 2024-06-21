import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import recipes
from schemas import RecipeSchema, RecipeUpdateSchema

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import RecipeModel

blp = Blueprint("recipes", __name__, description="Operations on recipes")


@blp.route("/recipe/<string:recipe_id>")
class Recipe(MethodView):
    @blp.response(200, RecipeSchema)
    def get(self, recipe_id):
        try:
            return recipes[recipe_id]
        except KeyError:
            abort(404, message="Recipe not found.")
    
    @blp.arguments(RecipeUpdateSchema)
    @blp.response(200, RecipeSchema)
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
    @blp.response(200, RecipeSchema(many=True))
    def get(self):
        return recipes.values()

    @blp.arguments(RecipeSchema)
    @blp.response(201, RecipeSchema)
    def post(self, request_recipe):
        recipe = RecipeModel(**request_recipe)
        try:
            db.session.add(recipe)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A Recipe with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occured while adding the recipe.")
        
        """
        for recipe in recipes.values():
            if request_recipe["name"] == recipe["name"]:
                abort(400, message="Recipe already exists.")

        recipe_id = uuid.uuid4().hex
        new_recipe = {**request_recipe, "id":recipe_id}
        recipes[recipe_id] = new_recipe

        return new_recipe
        """