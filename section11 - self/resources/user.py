from hmac import compare_digest
from flask_restful import Resource,reqparse
from models.user import UserModel
from flask_jwt_extended import (
    create_access_token, create_refresh_token,jwt_required,get_jwt_identity,get_jwt)
from blocklist import BLOCKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
_user_parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user is None:
            user = UserModel(data['username'],data['password'])

            user.save_to_db()

            return {"message": "User created successfully"},201
        return {"message": "User already exists"}, 400

class User(Resource):

    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)

        if user is None:
            return {'message':'User not found'},404
        
        return user.json(),200

    @classmethod
    def delete(cls,user_id):
        user = UserModel.find_by_id(user_id)

        if user is None:
            return {'message':'User not found'},404

        user.delete_from_db()
        return{'message': 'User deleted'}

class UserLogin(Resource):
 
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {'access_token': access_token,
                    'refresh_token': refresh_token},200
        
        return {'message': 'Invalid credentials'},401

class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
