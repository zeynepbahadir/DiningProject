from db import db


class RecipeModel(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    #ingredients = db.Column(db.String(80), nullable=True)

    #many-to-many relationship with ingredients
    ingredient = db.relationship("IngredientModel", back_populates="recipe", secondary="recipe_ingredients")

    #many-to-many relationship with users
    user = db.relationship("UserModel", back_populates="recipe", secondary="user_recipes")


    #one-to-many relationship with ingredients
    """
    ingredients = db.relationship("IngredientModel", back_populates="recipe", lazy="dynamic") #lazy dynamic means 
                                                                                            #it will not get ingredients 
                                                                                        #of recipe until they called
    """
    ####################################################
    #calling all
    #recipe.ingredients.all()
    #calling by name
    #recipe.ingredients.filter_by(name=="onion").first()
    ####################################################