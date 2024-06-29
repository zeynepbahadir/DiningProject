from db import db

class UserIngredients(db.Model):
    __tablename__ = "user_ingredients"

    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    ingredients_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"))