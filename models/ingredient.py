from db import db


class IngredientModel(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    
    #one-to-many relationship with ingredients
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), unique=False, nullable=False)
    recipe = db.relationship("RecipeModel", back_populates="ingredients")