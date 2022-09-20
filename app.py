from flask import Flask
from flask_restful import Api
from resources.Stock import Stock
from resources.Crypto import Crypto
from resources.User import UserRegister,UserLogin,DeleteUser
from resources.Assets import AssetManagement,Portfolio,RemoveAsset,AccountBalance
from flask_jwt_extended import JWTManager
from db import db

app = Flask(__name__)
url = '' #enter database URL
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key=''#enter secret key

api = Api(app)
jwt = JWTManager(app)

db.init_app(app)
with app.app_context():
    db.create_all()

api.add_resource(Stock,'/stock/<string:tag>')
api.add_resource(Crypto,'/crypto/<string:name>')
api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin,'/login')
api.add_resource(AssetManagement, '/adjustasset')
api.add_resource(Portfolio, '/portfolio')
api.add_resource(RemoveAsset, '/removeasset')
api.add_resource(AccountBalance, '/balance')
api.add_resource(DeleteUser,'/deleteuser')

if __name__ == '__main__':
    app.run(debug=True)
