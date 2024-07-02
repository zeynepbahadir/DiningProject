import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt

from schemas import RecipeSchema

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import RecipeModel

blp = Blueprint("recipes", __name__, description="Operations on recipes")


@blp.route("/recipe/<int:recipe_id>")
class Recipe(MethodView):
    @blp.response(200, RecipeSchema)
    def get(self, recipe_id):
        recipe = RecipeModel.query.get_or_404(recipe_id)
        return recipe
    
    @jwt_required(fresh=True)
    def delete(self, recipe_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        
        recipe = RecipeModel.query.get_or_404(recipe_id)
        db.session.delete(recipe)
        db.session.commit()
        return {"message":"Recipe deleted."}

@blp.route("/recipe")
class RecipeList(MethodView):
    @blp.response(200, RecipeSchema(many=True))
    def get(self):
        return RecipeModel.query.all()

    @jwt_required()
    @blp.arguments(RecipeSchema)
    @blp.response(201, RecipeSchema)
    def post(self, request_recipe):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        recipe = RecipeModel(**request_recipe)
        try:
            db.session.add(recipe)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A Recipe with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occured while adding the recipe.")
        return recipe