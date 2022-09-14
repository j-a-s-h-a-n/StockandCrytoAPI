from flask_restful import Resource,reqparse
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity,jwt_required
from models.user import UserModel
from models.assets import AssetModel
from Scraper import *

class portfolio(Resource):
    @jwt_required()
    def get(self):
        id = get_jwt_identity()
        assets=AssetModel.find_all_assets(id=id)
        if assets:
            accounts = {}
            for a in assets:
                accounts[a.name]=float(a.quantity)
            return accounts,200
        else:
            return {'Message':'No assets recorded.'}

class addAsset(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help = 'This cannot be blank.'
                        )
    parser.add_argument('quantity',
                        type=float,
                        required=True,
                        help='This cannot be blank.'
                        )
    parser.add_argument('type',
                        type=str,
                        required=True,
                        choices=['crypto', 'stock'],
                        help="Enter 'crypto' or 'stock'.")

    @jwt_required()
    def post(self):
        id=get_jwt_identity()
        data=self.parser.parse_args()
        if AssetModel.find_asset(id=id,name=data['name'],type=data['type']):
            return {'Message':'Asset already exist. Use PATCH method.'},400

        if data['type']=='crypto':
            results=getCrypto(data['name'])
            if 'Message' in results:
                return results,404
        else:
            results = getStock(data['name'])
            if 'Message' in results:
                return results, 404
        asset = AssetModel(name=data['name'],quantity=data['quantity'],type = data['type'],owner=id)
        asset.save_to_db()
        return {'Message':'Asset successfully added.'},200

    @jwt_required()
    def patch(self):
        id = get_jwt_identity()
        data = self.parser.parse_args()
        asset_to_update=AssetModel.find_asset(id=id, name=data['name'],type=data['type'])
        if asset_to_update:
            asset_to_update.delete_from_db()
            asset = AssetModel(name=data['name'], quantity=data['quantity'], type=data['type'], owner=id)
            asset.save_to_db()
            return {'Message': 'Asset successfully updated.'},200
        return {'Message': "Asset doesn't exist. Use POST method to add asset."}, 400

class remove(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help = 'This cannot be blank.'
                        )
    parser.add_argument('type',
                        type=str,
                        required=True,
                        choices=['crypto', 'stock'],
                        help="Enter 'crypto' or 'stock'.")
    @jwt_required()
    def delete(self):
        id = get_jwt_identity()
        data = self.parser.parse_args()
        asset_to_delete=AssetModel.find_asset(id,data['name'],data['type'])
        if asset_to_delete:
            asset_to_delete.delete_from_db()
            return {'Message':'Successfully Deleted'},400
        return {'Message':'Asset not found.'}, 404

class balance(Resource):
    @jwt_required()
    def get(self):
        id = get_jwt_identity()
        assets = AssetModel.find_all_assets(id=id)
        total=0
        change=0
        for a in assets:
            if a.type =='stock':
                data=getStockStat(a.name)
                price = float(data['Price'])
                currentPrice= price * a.quantity
            else:
                data = getCryptoStat(a.name)
                price = float(data['Price'].replace("$",'').replace(",",''))
                currentPrice = price * a.quantity
            change+=float(data['Price Change'].replace("$",'').replace(",",''))*a.quantity
            total += float(currentPrice)
        return {"Portfolio Balance:": f"${total.__round__(2)}",
                "24 Hour Price Change": f'${change.__round__(2)}'}

