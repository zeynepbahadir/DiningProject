import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import ingredients

blp = Blueprint("ingredients", __name__, description="Operations on ingredients")

@blp.route("/ingredient")
class IngredientList(MethodView):
    def get(self):
        return {"ingredients": list(ingredients.values())}
    
    def post(self):
        request_ingredient = request.get_json()
        if "name" not in request_ingredient:
            abort(400, message="Bad request. Ensure 'name' is included in JSON payload.")
        for ingredient in ingredients:
            if request_ingredient["name"] == ingredient["name"]:
                abort(400, message="Bad request. Ingredient already exists.")
        ingredient_id = uuid.uuid4().hex
        new_ingredient = {**request_ingredient, "id":ingredient_id}
        
        ingredients[ingredient_id] = new_ingredient
        return new_ingredient, 201

@blp.route("/ingredient/<string:ingredient_id>")
class Ingredient(MethodView):
    def delete(self, ingredient_id):
        try:
            del ingredients[ingredient_id]
            return {"message":"Ingredient deleted."}
        except KeyError:
            abort(404, message="Ingredient not found.")