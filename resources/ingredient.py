import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import IngredientSchema, PlainIngredientSchema,RecipeAndIngredientSchema

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import IngredientModel, RecipeModel

blp = Blueprint("ingredients", __name__, description="Operations on ingredients")


@blp.route("/ingredient")
class IngredientList(MethodView):
    @blp.response(200, PlainIngredientSchema(many=True))
    def get(self):
        return IngredientModel.query.all()
    
    @blp.arguments(IngredientSchema)
    @blp.response(201, IngredientSchema)
    def post(self, request_ingredient):
        ingredient = IngredientModel(**request_ingredient)
        try:
            db.session.add(ingredient)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An Ingredient with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the ingredient.")
        return ingredient

@blp.route("/ingredient/<string:ingredient_id>")
class Ingredient(MethodView):
    @blp.response(202, description="Deletes an ingredient if no recipe is assigned to it.", example={"message":"Tag deleted."})
    @blp.alt_response(404, description="Ingredient not found.")
    @blp.alt_response(400, description="Returned if the ingredient is assigned to one or more recipes. In this case, the ingredient is not deleted.")
    def delete(self, ingredient_id):
        ingredient = IngredientModel.query.get_or_404(ingredient_id)

        if not ingredient.recipe:
            db.session.delete(ingredient)
            db.session.commit()
            return {"message":"Ingredient deleted."}
        abort(400, message="Could not delete ingredient. Make sure ingredient is not associated with a recipe, and try again.")

#according to many-to-many relationships linking and unlinking ingredients to recipes
@blp.route("/recipe/<string:recipe_id>/ingredient/<string:ingredient_id>")
class LinkIngredientToRecipe(MethodView):
    @blp.response(201, RecipeAndIngredientSchema)
    def post(self, recipe_id, ingredient_id):
        ingredient = IngredientModel.query.get_or_404(ingredient_id)
        recipe = RecipeModel.query.get_or_404(recipe_id)
        recipe.ingredient.append(ingredient)

        try:
            db.session.add(recipe)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while linking ingredient.")

        return {"message":"Ingredient added to recipe.", "Ingredient":ingredient, "recipe":recipe}

    @blp.response(200, RecipeAndIngredientSchema)
    def delete(self, recipe_id, ingredient_id):
        recipe = RecipeModel.query.get_or_404(recipe_id)
        ingredient = IngredientModel.query.get_or_404(ingredient_id)

        recipe.ingredient.remove(ingredient)

        try:
            db.session.add(recipe)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while deleting ingredient.")

        return {"message": "Ingredient removed Recipe.", "Ingredient":ingredient, "recipe":recipe}
