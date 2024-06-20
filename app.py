from flask import Flask, request
from db import recipes, ingredients
import uuid
from flask_smorest import abort

app = Flask(__name__)


@app.get("/recipe")
def get_recipes():
    return {"recipes": list(recipes.values())}

@app.post("/recipe")
def add_recipe():
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

@app.get("/recipe/<string:recipe_id>")
def get_recipe_by_id(recipe_id):
    try:
        return recipes[recipe_id]
    except KeyError:
        abort(404, message="Recipe not found.")

@app.put("/recipe/<string:recipe_id>")
def update_recipe(recipe_id):
    request_recipe = request.get_json()
    if "name" not in request_recipe or "ingredients" not in request_recipe:
        abort(400, message="Bad request. Ensure 'name', and 'ingredients' are included in the JSON payload.")
    try:
        recipe = recipes[recipe_id]
        recipe |= request_recipe

        return recipe
    except KeyError:
        abort(404, message="Recipe not found.")

@app.delete("/recipe/<string:recipe_id>")
def del_recipe_by_id(recipe_id):
    try:
        del recipes[recipe_id]
        return {"message":"Recipe deleted."}


@app.get("/ingredient")
def get_ingredients():
    return {"ingredients": list(ingredients.values())}

@app.post("/ingredient")
def add_ingredient():
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

@app.delete("/ingredient/<string:abche >")
def del_ingredient_by_id(ingredient_id):
    try:
        del ingredients[ingredient_id]
        return {"message":"Ingredient deleted."}
    except KeyError:
        abort(404, message="Ingredient not found.")
