from flask import Flask
from flask_restful import Api
from resources.Stock import Stock
from resources.Crypto import Crypto
from resources.User import UserRegister,UserLogin,DeleteUser
from resources.Assets import addAsset,portfolio,remove,balance
from flask_jwt_extended import JWTManager
from db import db

app = Flask(__name__)
url='postgresql://pkajdrxdqpfskl:f7320a226552faf3518021767264eaccf5f15f47adc4d6ff4dd2ec23c6487ce9@ec2-52-207-90-231.compute-1.amazonaws.com:5432/d5jc9a3cj36kdi'
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['PROPAGATE_EXCEPTIONS']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='jdkskhcsoemkfncncwienio'

api = Api(app)
jwt = JWTManager(app)

db.init_app(app)
with app.app_context():
    db.create_all()

api.add_resource(Stock,'/stock/<string:tag>')
api.add_resource(Crypto,'/crypto/<string:name>')
api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin,'/login')
api.add_resource(addAsset,'/add')
api.add_resource(portfolio, '/portfolio')
api.add_resource(remove,'/remove')
api.add_resource(balance,'/balance')
api.add_resource(DeleteUser,'/deleteuser')

if __name__ == '__main__':
    app.run(debug=True)
