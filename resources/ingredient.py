import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import ingredients
from schemas import IngredientSchema



blp = Blueprint("ingredients", __name__, description="Operations on ingredients")

@blp.route("/ingredient")
class IngredientList(MethodView):
    @blp.response(200, IngredientSchema(many=True))
    def get(self):
        return ingredients.values()
    
    @blp.arguments(IngredientSchema)
    @blp.response(201, IngredientSchema)
    def post(self, request_ingredient):
        for ingredient in ingredients:
            if request_ingredient["name"] == ingredient["name"]:
                abort(400, message="Bad request. Ingredient already exists.")
        
        ingredient_id = uuid.uuid4().hex
        new_ingredient = {**request_ingredient, "id":ingredient_id}
        ingredients[ingredient_id] = new_ingredient
        
        return new_ingredient

@blp.route("/ingredient/<string:ingredient_id>")
class Ingredient(MethodView):
    def delete(self, ingredient_id):
        try:
            del ingredients[ingredient_id]
            return {"message":"Ingredient deleted."}
        except KeyError:
            abort(404, message="Ingredient not found.")