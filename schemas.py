from marshmallow import Schema, fields


class PlainIngredientSchema(Schema):
    id = fields.Str(dump_only=True) #it can only be used for returning data
    name = fields.Str(required=True) #this comes with json payload


class PlainRecipeSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class IngredientSchema(PlainIngredientSchema):
    #recipe_id = fields.Int(required=True, load_only=True)
    #recipe = fields.Nested(PlainRecipeSchema(), dump_only=True)
    recipe = fields.List(fields.Nested(PlainRecipeSchema()), dump_only=True)
    user = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)


class RecipeSchema(PlainRecipeSchema):
    ingredient = fields.List(fields.Nested(PlainIngredientSchema()), dump_only=True)
    #user = fields.List(fields.Nested(PlainUserSchema()), dump_only=True)


class UserSchema(PlainUserSchema):
    recipe = fields.List(fields.Nested(PlainRecipeSchema()), dump_only=True)
    ingredient = fields.List(fields.Nested(PlainIngredientSchema()), dump_only=True)


class RecipeAndIngredientSchema(Schema):
    message = fields.Str()
    ingredient = fields.Nested(IngredientSchema)
    recipe = fields.Nested(RecipeSchema)


class UserAndRecipeSchema(UserSchema):
    message = fields.Str()
    user = fields.Nested(UserSchema)
    recipe = fields.Nested(RecipeSchema)


class UserAndIngredientSchema(UserSchema):
    message = fields.Str()
    user = fields.Nested(UserSchema)
    ingredient = fields.Nested(IngredientSchema)