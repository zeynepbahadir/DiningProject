import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import IngredientSchema, PlainIngredientSchema

from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import IngredientModel



blp = Blueprint("ingredients", __name__, description="Operations on ingredients")

@blp.route("/ingredient")
class IngredientList(MethodView):
    @blp.response(200, PlainIngredientSchema(many=True))
    def get(self):
        return IngredientModel.query.all()
    
    @blp.arguments(IngredientSchema)
    @blp.response(201, IngredientSchema)
    def post(self, request_ingredient):
        ingredient = IngredientModel(**request_ingredient)
        
        try:
            db.session.add(ingredient)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the ingredient.")
        
        #return ingredient

@blp.route("/ingredient/<string:ingredient_id>")
class Ingredient(MethodView):
    def delete(self, ingredient_id):
        ingredient = IngredientModel.query.get_or_404(ingredient_id)
        db.session.delete(ingredient)
        db.session.commit()
        return {"message":"Ingredient deleted."}