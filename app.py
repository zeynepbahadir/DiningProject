import os
import secrets

from flask import Flask
from flask_smorest import Api

from flask_jwt_extended import JWTManager

from resources.recipe import blp as RecipeBlueprint
from resources.ingredient import blp as IngredientBlueprint
from resources.user import blp as UserBlueprint
from resources.user_extensive import blp as UserExtensiveBlueprint

from schemas import RecipeSchema, IngredientSchema

from db import db
import models

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Recipes REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(RecipeBlueprint)
    api.register_blueprint(IngredientBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(UserExtensiveBlueprint)

    return app