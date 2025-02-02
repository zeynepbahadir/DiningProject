import pytest
import requests
import unittest
from flask import request, Flask
from flask_smorest import Blueprint
from flask.views import MethodView
from resources.ingredient import blp as IngredientList


app = Flask(__name__)



app.register_blueprint(IngredientList, url_prefix='')
app.sqlalchemy = 


class TestIngredientList(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
    
    def test_list_ingredients(self):
        list_ingredients = self.app.get('/ingredient')
        print (list_ingredients.data)




if __name__ == '__main__':
    unittest.main()