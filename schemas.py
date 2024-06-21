from marshmallow import Schema, fields


class IngredientSchema(Schema):
    id = fields.Str(dump_only=True) #it can only be used for returning data
    name = fields.Str(required=True) #this comes with json payload

class RecipeSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    ingredients = fields.Str(required=True)

class RecipeUpdateSchema(Schema):
    ingredients = fields.Str()