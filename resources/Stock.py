from flask_restful import Resource
from Scraper import getStock

class Stock(Resource):
    def get(self,tag):
        info=getStock(tag)
        if 'Message' in info:
            return (info,404)
        else:
            return (info, 200)