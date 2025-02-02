import unittest
from flask import request, Flask
from flask_smorest import Blueprint
from flask.views import MethodView


from schemas import IngredientSchema, PlainIngredientSchema,RecipeAndIngredientSchema
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import IngredientModel, RecipeModel

app = Flask(__name__)

#app.register_blueprint(IngredientBlp, url_prefix='')

class TestIngredientList(unittest.TestCase):

    """
    class AppTestCase(unittest.TestCase):
        def setUp(self):
            self.ctx = app.app_context()
            self.ctx.push()
            self.client = app.test_client()

        def tearDown(self):
            self.ctx.pop()

        def test_home(self):
            response = self.client.post("/", data={"content": "hello world"})
            assert response.status_code == 200
            assert "POST method called" == response.get_data(as_text=True)
    

    def setUp(self):
        self.app = app.app_context()
        self.app.push()
        self.client = app.test_client()
        
    
    def tearDown(self):
        self.app.pop()
    
    def test_list_ingredients(self):
        
        
        list_ingredients = self.client.get('/ingredient')
        db.init_app(app)
        #with app.app_context():
        assert True
        #self.assertEqual(list_ingredients.get_data(as_text=True) == IngredientModel.query.all())
    """

    def test_1(self):
        assert True

if __name__ == '__main__':
    unittest.main()