from marshmallow import Schema, fields


class PlainIngredientSchema(Schema):
    id = fields.Str(dump_only=True) #it can only be used for returning data
    name = fields.Str(required=True) #this comes with json payload


class PlainRecipeSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    ingredients = fields.Str(required=True)


class IngredientSchema(PlainIngredientSchema):
    recipe_id = fields.Int(required=True, load_only=True)
    recipe = fields.Nested(PlainRecipeSchema(), dump_only=True)


class RecipeSchema(PlainRecipeSchema):
    ingredients = fields.List(fields.Nested(PlainIngredientSchema()), dump_only=True)


class RecipeUpdateSchema(Schema):
    name = fields.Str()
    ingredients = fields.Str()