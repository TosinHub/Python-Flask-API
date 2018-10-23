from flask_restful import  Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exist".format(name)}, 400   
        store = StoreModel(name)
        store.save_to_db()
        return store.json(),200

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'store': 'Store Deleted'}      

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}