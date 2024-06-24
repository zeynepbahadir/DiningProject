from marshmallow import Schema, fields


class PlainIngredientSchema(Schema):
    id = fields.Str(dump_only=True) #it can only be used for returning data
    name = fields.Str(required=True) #this comes with json payload


class PlainRecipeSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class IngredientSchema(PlainIngredientSchema):
    #recipe_id = fields.Int(required=True, load_only=True)
    #recipe = fields.Nested(PlainRecipeSchema(), dump_only=True)
    recipe = fields.List(fields.Nested(PlainRecipeSchema()), dump_only=True)


class RecipeSchema(PlainRecipeSchema):
    ingredient = fields.List(fields.Nested(PlainIngredientSchema()), dump_only=True)


class RecipeAndIngredientSchema(Schema):
    message = fields.Str()
    ingredient = fields.Nested(IngredientSchema)
    recipe = fields.Nested(RecipeSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    #owned = 
    #mealplan = 