import uuid
import regex as re
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt

from schemas import IngredientSchema, PlainIngredientSchema,RecipeAndIngredientSchema
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import IngredientModel, RecipeModel

blp = Blueprint("ingredients", __name__, description="Operations on ingredients")


@blp.route("/ingredient")
class IngredientList(MethodView):
    @blp.response(200, PlainIngredientSchema(many=True))
    def get(self):
        return IngredientModel.query.all()
    
    @jwt_required()
    @blp.arguments(IngredientSchema)
    @blp.response(201, IngredientSchema)
    def post(self, request_ingredient):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        
        ingredient = IngredientModel(**request_ingredient)
        try:
            db.session.add(ingredient)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An Ingredient with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the ingredient.")
        return ingredient

@blp.route("/ingredient/<int:ingredient_id>")
class Ingredient(MethodView):
    @jwt_required()
    @blp.response(202, description="Deletes an ingredient if no recipe is assigned to it.", example={"message":"Tag deleted."})
    @blp.alt_response(404, description="Ingredient not found.")
    @blp.alt_response(400, description="Returned if the ingredient is assigned to one or more recipes. In this case, the ingredient is not deleted.")
    def delete(self, ingredient_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        ingredient = IngredientModel.query.get_or_404(ingredient_id)

        if not ingredient.recipe:
            db.session.delete(ingredient)
            db.session.commit()
            return {"message":"Ingredient deleted."}
        abort(400, message="Could not delete ingredient. Make sure ingredient is not associated with a recipe, and try again.")

#according to many-to-many relationships linking and unlinking ingredients to recipes
@blp.route("/recipe/<int:recipe_id>/ingredient/<int:ingredient_id>")
class LinkIngredientToRecipe(MethodView):
    @jwt_required()
    @blp.response(201, RecipeAndIngredientSchema)
    def post(self, recipe_id, ingredient_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        ingredient = IngredientModel.query.get_or_404(ingredient_id)
        recipe = RecipeModel.query.get_or_404(recipe_id)
        
        ingrlist = [int(re.sub("[^\d\.]", "", str(x))) for x in recipe.ingredient]

        if ingredient_id not in ingrlist:
            recipe.ingredient.append(ingredient)
            try:
                db.session.add(recipe)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="An error occured while linking ingredient.")

            return {"message":"Ingredient added to recipe.", "Ingredient":ingredient, "recipe":recipe}
        abort(400, message="Recipe has these ingredient already.")

    @jwt_required()
    @blp.response(200, RecipeAndIngredientSchema)
    def delete(self, recipe_id, ingredient_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        recipe = RecipeModel.query.get_or_404(recipe_id)
        ingredient = IngredientModel.query.get_or_404(ingredient_id)

        ingrlist = [int(re.sub("[^\d\.]", "", str(x))) for x in recipe.ingredient]

        if ingredient_id in ingrlist:
            recipe.ingredient.remove(ingredient)
            try:
                db.session.add(recipe)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="An error occured while deleting ingredient.")

            return {"message": "Ingredient removed Recipe.", "Ingredient":ingredient, "recipe":recipe}
        abort(400, message="Recipe doesnt have these ingredient.")