from flask_restful import Resource,reqparse
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity
from models.user import UserModel
from models.assets import AssetModel



_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                        type=str,
                        required=True,
                        help = "This cannot be blank."
                        )
_user_parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This cannot be blank."
                        )

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'Message': 'Username already exist.'},400

        user =UserModel(**data)
        user.save_to_db()

        return {'Message':'User sucessfully created.'},200
class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and user.password==data['password']:
            access_token=create_access_token(identity=user.id,fresh=False,)
            return{
                'access_token': access_token,

            },200
        return {'Message':'Invalid credentials'},401
class DeleteUser(Resource):
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and user.password == data['password']:
            AssetModel.delete_all(id=user.id)
            user.delete_from_db()
            return {'Message':'User successfully deleted.'},200
        return {'Message':'User not found.'},404
