from db import db

class AssetModel(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    quantity = db.Column(db.FLOAT)
    type = db.Column(db.String)
    owner = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __init__(self, name, quantity,type,owner):
        self.name = name
        self.quantity = quantity
        self.type=type
        self.owner=owner
    def json(self):
        return {
            'name': self.name,
            'quantity': self.quantity
        }
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def find_all_assets(cls, id):
        return cls.query.filter_by(owner=id)

    @classmethod
    def find_asset(cls,id,name,type):
        return cls.query.filter_by(owner=id,name=name,type=type).first()
