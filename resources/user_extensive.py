from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import UserModel, IngredientModel, RecipeModel
from schemas import RecipeSchema, UserAndIngredientSchema, UserAndRecipeSchema

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp = Blueprint("User_extensive", "user_extensive", description="Extended operations on users")


@blp.route("/user/<int:user_id>/ingredient/<int:ingredient_id>")
class PostAndDeleteUserIngredients(MethodView):
    #@blp.arguments(UserAndIngredientSchema)
    @blp.response(201, UserAndIngredientSchema)
    def post(self, user_id, ingredient_id):
        user = UserModel.query.get_or_404(user_id)
        ingredient = IngredientModel.query.get_or_404(ingredient_id)
        user.ingredient.append(ingredient)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="User has this ingredient already.")
        except SQLAlchemyError:
            abort(500, message="An error occured while adding ingredient to user.")

        return {"message":"Ingredient added to user.", "Ingredient":ingredient, "user":user}
    
    @blp.response(200, UserAndIngredientSchema)
    def delete(self, user_id, ingredient_id):
        user = UserModel.query.get_or_404(user_id)
        ingredient = IngredientModel.query.get(ingredient_id)

        user.ingredient.remove(ingredient)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while removing ingredient from user.")

        return {"message": "Ingredient removed from user.", "Ingredient":ingredient, "user":user}
    
@blp.route("/user/<int:user_id>/ingredient")
class ListWhatIngredientUserHas(MethodView):
    @blp.response(200, RecipeSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
            
        return user
    
@blp.route("/user/<int:user_id>/recipe")
class ListWhichRecipesPasses(MethodView):
    def get(self, user_id):
        sql = text('select ingredients_id from user_ingredients where users_id = :val')
        result = db.session.execute(sql, {"val":user_id})
        ingredient_ids = [row[0] for row in result]

        sql1 = text('SELECT recipes_id FROM recipe_ingredients WHERE ingredients_id IN {}'.format(tuple(ingredient_ids)))
        result1 = db.session.execute(sql1)
        recipe_ids = [row[0] for row in result1]
        r = set(recipe_ids)
        ri = list(r)
        return {"message": "Recipes which has users ingredients", "recipes": ri}

@blp.route("/user/<int:user_id>/recipe/<int:recipe_id>")
class UsersRecipe(MethodView):
    def get(self, user_id, recipe_id):
        sql = text('select ingredients_id from user_ingredients where users_id = :val')
        result = db.session.execute(sql, {"val":user_id})
        user_ingredients_ids = [row[0] for row in result]

        sql1 = text('select ingredients_id from recipe_ingredients where recipes_id = :val')
        result1 = db.session.execute(sql1, {"val":recipe_id})
        recipe_ingredients_ids = [row[0] for row in result1]

        return {"missed ingredients": list(set(recipe_ingredients_ids).difference(user_ingredients_ids))}
    
    #@blp.arguments(UserAndRecipeSchema)
    @blp.response(201, UserAndRecipeSchema)
    def post(self, user_id, recipe_id):
        user = UserModel.query.get_or_404(user_id)
        recipe = RecipeModel.query.get_or_404(recipe_id)
        recipe.user.append(user)

        try:
            db.session.add(recipe)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Users has this recipe already.")
        except SQLAlchemyError:
            abort(500, message="An error occured while linking recipe to users meal plan.")

        return {"message":"Recipe added to users meal plan."}#, "user":user, "recipe":recipe}
    

    @blp.response(201, UserAndRecipeSchema)
    def delete(self, user_id, recipe_id):
        user = UserModel.query.get_or_404(user_id)
        recipe = RecipeModel.query.get_or_404(recipe_id)
        
        user.recipe.remove(recipe)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="error occured.")
        except SQLAlchemyError:
            abort(500, message="An error occured while deleing recipe from users meal plan.")

        return {"message":"Recipe removed from to users meal plan."}#, "user":user, "recipe":recipe}
    
@blp.route("/user/<int:user_id>/mealplan")
class UsersMealplan(MethodView):
    def get(self, user_id):
        sql = text('select recipes_id from user_recipes where users_id = :val')
        result = db.session.execute(sql, {"val":user_id})
        recipes_id = [row[0] for row in result]
        return recipes_id


@blp.route("/user/<int:user_id>/mealplan/ingredient")
class UsersMealplanMissedIngredients(MethodView):
    def get(self, user_id):
        sql = text('select recipes_id from user_recipes where users_id = :val')
        result = db.session.execute(sql, {"val":user_id})
        recipes_ids = [row[0] for row in result]
        #r = set(recipes_ids)
        #ri = list(r)

        #sql1 = text('SELECT ingredients_id FROM recipe_ingredients WHERE recipes_id IN {}'.format(tuple(recipes_ids)))
        sql1 = text('SELECT ingredients_id FROM recipe_ingredients WHERE recipes_id IN :val')
        result1 = db.session.execute(sql1, {"val":tuple(recipes_ids)})
        ingredients_ids = [row[0] for row in result1]
        return {"message": "Ingredients which users recipes has:", "recipes": ingredients_ids}