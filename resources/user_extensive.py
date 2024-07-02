import regex as re

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from db import db
from models import UserModel, IngredientModel, RecipeModel
from schemas import RecipeSchema, UserAndIngredientSchema, UserAndRecipeSchema

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("User_extensive", "user_extensive", description="Extended operations on users")


@blp.route("/user/<int:user_id>/ingredient/<int:ingredient_id>")
class PostAndDeleteUserIngredients(MethodView):
    @jwt_required()
    #@blp.arguments(UserAndIngredientSchema)
    @blp.response(201, UserAndIngredientSchema)
    def post(self, user_id, ingredient_id):
        user = UserModel.query.get_or_404(user_id)
        ingredient = IngredientModel.query.get_or_404(ingredient_id)

        ilist = [int(re.sub("[^\d\.]", "", str(x))) for x in user.ingredient]

        if ingredient_id not in ilist:
            user.ingredient.append(ingredient)
            try:
                db.session.add(user)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="An error occured while adding ingredient to user.")

            return {"message":"Ingredient added to user."}
        abort(404, message="User has these ingredient already.")
    
    @jwt_required()
    @blp.response(200, UserAndIngredientSchema)
    def delete(self, user_id, ingredient_id):
        user = UserModel.query.get_or_404(user_id)
        ingredient = IngredientModel.query.get_or_404(ingredient_id)

        ilist = [int(re.sub("[^\d\.]", "", str(x))) for x in user.ingredient]

        if ingredient_id in ilist:
            user.ingredient.remove(ingredient)
            try:
                db.session.add(user)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="An error occured while removing ingredient from user.")

            return {"message": "Ingredient removed from user."}
        abort(404, message="User doesnt have these ingredient.")
    
@blp.route("/user/<int:user_id>/ingredient")
class ListWhatIngredientUserHas(MethodView):
    @blp.response(200, RecipeSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
            
        return user
    
@blp.route("/user/<int:user_id>/recipe")
class ListWhichRecipesPasses(MethodView):
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        sql = text('select ingredients_id from user_ingredients where users_id = :val')
        result = db.session.execute(sql, {"val":user_id})
        ingredient_ids = [row[0] for row in result]
        if len(ingredient_ids) == 1:
            sql1 = text('SELECT recipes_id FROM recipe_ingredients WHERE ingredients_id = :val')
            result1 = db.session.execute(sql1, {"val":ingredient_ids[0]})
        else:
            sql1 = text('SELECT recipes_id FROM recipe_ingredients WHERE ingredients_id IN {}'.format(tuple(ingredient_ids)))
            result1 = db.session.execute(sql1)
        recipe_ids = [row[0] for row in result1]
        r = set(recipe_ids)
        ri = list(r)
        return {"message": "Recipes which has users ingredients", "recipes": ri, "ingredients":ingredient_ids}

@blp.route("/user/<int:user_id>/recipe/<int:recipe_id>")
class UsersRecipe(MethodView):
    def get(self, user_id, recipe_id):
        user = UserModel.query.get_or_404(user_id)
        recipe = RecipeModel.query.get_or_404(recipe_id)
        sql = text('select ingredients_id from user_ingredients where users_id = :val')
        result = db.session.execute(sql, {"val":user_id})
        user_ingredients_ids = [row[0] for row in result]

        sql1 = text('select ingredients_id from recipe_ingredients where recipes_id = :val')
        result1 = db.session.execute(sql1, {"val":recipe_id})
        recipe_ingredients_ids = [row[0] for row in result1]

        return {"missed ingredients": list(set(recipe_ingredients_ids).difference(user_ingredients_ids))}
    
    @jwt_required()
    #@blp.arguments(UserAndRecipeSchema)
    @blp.response(201, UserAndRecipeSchema)
    def post(self, user_id, recipe_id):
        user = UserModel.query.get_or_404(user_id)
        recipe = RecipeModel.query.get_or_404(recipe_id)
        
        relist = [int(re.sub("[^\d\.]", "", str(x))) for x in user.recipe]

        #user.recipe is a list of RecipeModel 1, RecipeModel 2...
        if recipe_id not in relist:
            recipe.user.append(user)
            try:
                db.session.add(recipe)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="An error occured while linking recipe to users meal plan.")

            return {"message":"Recipe added to users meal plan."}#, "user":user, "recipe":recipe}
        abort(400, message="User has these recipe already.")
    
    @jwt_required()
    @blp.response(201, UserAndRecipeSchema)
    def delete(self, user_id, recipe_id):
        user = UserModel.query.get_or_404(user_id)
        recipe = RecipeModel.query.get_or_404(recipe_id)
        
        relist = [int(re.sub("[^\d\.]", "", str(x))) for x in user.recipe]

        #user.recipe is a list of RecipeModel 1, RecipeModel 2...
        if recipe_id in relist:
            user.recipe.remove(recipe)
            try:
                db.session.add(user)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="An error occured while deleing recipe from users meal plan.")

            return {"message":"Recipe removed from to users meal plan."}#, "user":user, "recipe":recipe}
        abort(400, message="User doesnt have these Recipe")
    
@blp.route("/user/<int:user_id>/mealplan")
class UsersMealplan(MethodView):
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        sql = text('select recipes_id from user_recipes where users_id = :val')
        result = db.session.execute(sql, {"val":user_id})
        recipes_id = [row[0] for row in result]
        return recipes_id


@blp.route("/user/<int:user_id>/mealplan/ingredient")
class UsersMealplanMissedIngredients(MethodView):
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        #get what user has
        sql = text('SELECT ingredients_id from user_ingredients where users_id = :val')
        result = db.session.execute(sql, {"val":user_id})
        user_ingredients_ids = [row[0] for row in result]
        
        #get what recipes user has
        sql1 = text('SELECT recipes_id from user_recipes where users_id = :val')
        result1 = db.session.execute(sql1, {"val":user_id})
        recipes_ids = [row[0] for row in result1]
        
        #get what ingredients has the recipes which user has
        if len(recipes_ids) == 1:
            sql2 = text('SELECT ingredients_id from recipe_ingredients where recipes_id = :val')
            result2 = db.session.execute(sql2, {"val":recipes_ids[0]})
        else:
            sql2 = text('SELECT ingredients_id from recipe_ingredients where recipes_id IN {}'.format(tuple(recipes_ids)))
            result2 = db.session.execute(sql2)
        recipe_ingredients_ids = [row[0] for row in result2]
        
        return {"missed ingredients": list(set(recipe_ingredients_ids).difference(user_ingredients_ids))}