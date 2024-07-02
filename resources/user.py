from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from db import db
from models import UserModel
from schemas import UserSchema, PlainUserSchema


blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, PlainUserSchema(many=True))
    def get(self):
        return UserModel.query.all()
    
    @blp.arguments(UserSchema)
    def post(self, request_user):
        if UserModel.query.filter(UserModel.username == request_user["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=request_user["username"],
            password=pbkdf2_sha256.hash(request_user["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, request_user):
        user = UserModel.query.filter(UserModel.username == request_user["username"]).first()

        if user and pbkdf2_sha256.verify(request_user["password"], user.password):
            access_token = create_access_token(identity=user.id) #users id is passed to jwt too (among other infos)
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"User deleted."}, 200