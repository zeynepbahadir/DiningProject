from db import db

class UserRecipes(db.Model):
    __tablename__ = "user_recipes"

    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    recipes_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))