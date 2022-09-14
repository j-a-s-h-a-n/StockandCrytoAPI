from flask_restful import Resource
from Scraper import getCrypto

class Crypto(Resource):
    def get(self,name):
        info= getCrypto(name)
        if 'Message' in info:
            return (info,404)
        else:
            return (info, 200)