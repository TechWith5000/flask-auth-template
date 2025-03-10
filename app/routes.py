from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.models import User, TokenBlocklist
from app import db

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# ✅ Register a new user
class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            return {"message": "User already exists"}, 400

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201

# ✅ Login & get JWT token
class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=username)
        return {"access_token": access_token}, 200

# ✅ Protected route
class Protected(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {"message": f"Hello, {current_user}! You accessed a protected route."}, 200


# ✅ Logout & revoke token
class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]  # Get the token ID
        db.session.add(TokenBlocklist(jti=jti))
        db.session.commit()
        return {"message": "Successfully logged out"}, 200

# Add routes to API
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Protected, '/protected')
api.add_resource(Logout, '/logout')