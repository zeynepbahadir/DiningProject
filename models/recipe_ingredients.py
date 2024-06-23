from db import db

class RecipesIngredients(db.Model):
    __tablename__ = "recipe_ingredients"

    id = db.Column(db.Integer, primary_key=True)
    recipes_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))
    ingredients_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"))