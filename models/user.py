from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    #many-to-many relationship with recipe
    recipe = db.relationship("RecipeModel", back_populates="user", secondary="user_recipes")
    
    #many-to-many relationship with ingredients
    ingredient = db.relationship("IngredientModel", back_populates="user", secondary="user_ingredients", lazy="dynamic")
    
    #to add
    #owned =