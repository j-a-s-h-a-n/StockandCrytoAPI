from flask_restful import Resource,reqparse
from flask_jwt_extended import get_jwt_identity,jwt_required
from models.user import UserModel
from models.assets import AssetModel
from Scraper import *

class Portfolio(Resource):
    @jwt_required()
    def get(self):
        id = get_jwt_identity()
        assets=AssetModel.find_all_assets(id=id)
        if assets:
            dic = {}
            for a in assets:
                if a.type == 'stock':
                    data = getStockStat(a.name)
                    price = float(data['Price'])
                    currentHoldings = price * a.quantity
                else:
                    data = getCryptoStat(a.name)
                    price = float(data['Price'].replace("$", '').replace(",", ''))
                    currentHoldings = price * a.quantity
                change = float(data['Price Change'].replace("$", '').replace(",", '')) * a.quantity
                dic[a.name] = {"Quantity": a.quantity,
                               'Price': f"${price.__round__(2)}",
                               'Value': f"${currentHoldings.__round__(2)}"}
            if dic:
                return dic,200
        return {'Message':'No assets recorded.'}

class AssetManagement(Resource):
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
        if AssetModel.find_asset(id=id,name=data['name'].lower(),type=data['type'].lower()):
            return {'Message':'Asset already exist. Use PATCH method.'},400

        if data['type']=='crypto':
            results=getCrypto(data['name'])
            if 'Message' in results:
                return results,404
        else:
            results = getStock(data['name'])
            if 'Message' in results:
                return results, 404
        asset = AssetModel(name=data['name'].lower(),quantity=data['quantity'],type = data['type'].lower(),owner=id)
        asset.save_to_db()
        return {'Message':'Asset successfully added.'},200

    @jwt_required()
    def patch(self):
        id = get_jwt_identity()
        data = self.parser.parse_args()
        asset_to_update=AssetModel.find_asset(id=id, name=data['name'].lower(),type=data['type'].lower())
        if asset_to_update:
            asset_to_update.delete_from_db()
            asset = AssetModel(name=data['name'].lower(), quantity=data['quantity'], type=data['type'].lower(), owner=id)
            asset.save_to_db()
            return {'Message': 'Asset successfully updated.'},200
        return {'Message': "Asset doesn't exist. Use POST method to add asset."}, 400

class RemoveAsset(Resource):
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
        asset_to_delete=AssetModel.find_asset(id,data['name'].lower(),data['type'].lower())
        if asset_to_delete:
            asset_to_delete.delete_from_db()
            return {'Message':'Successfully Deleted'},400
        return {'Message':'Asset not found.'}, 404

class AccountBalance(Resource):
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
                "24 Hour Balance Change": f'${change.__round__(2)}'}

