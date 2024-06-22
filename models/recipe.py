from db import db


class RecipeModel(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    #ingredients = db.Column(db.String(80), nullable=True)

    #one-to-many relationship with ingredients
    ingredients = db.relationship("IngredientModel", back_populates="recipe", lazy="dynamic") #lazy dynamic means 
                                                                                            #it will not get ingredients 
                                                                                        #of recipe until they called
    ####################################################
    #calling all
    #recipe.ingredients.all()
    #calling by name
    #recipe.ingredients.filter_by(name=="onion").first()
    ####################################################