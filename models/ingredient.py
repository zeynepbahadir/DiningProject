from db import db


class IngredientModel(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    #many-to-many relationship with recipe
    recipe = db.relationship("RecipeModel", back_populates="ingredient", secondary="recipe_ingredients")

    #one-to-many relationship with recipe
    """
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), unique=False, nullable=False) #foreign key means id comes from a foreign table recipe
    recipe = db.relationship("RecipeModel", back_populates="ingredients")
    """