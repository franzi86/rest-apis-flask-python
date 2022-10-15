from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

from models.store import StoreModel

class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'store not found'}, 404
     
    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message': "An store with name {} already exists".format(name)}, 400
        
        new_store = StoreModel(name)
        
        try:
            new_store.save_to_db()
        except:
            return {'message':'An error occurred inserting an store to the database.'},500

        return new_store.json(), 201

    
    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store is None:
            return {'message': "An store with name {} does not exist".format(name)}, 400

        store.delete_from_db()
        return {'message': 'store deleted'}


class StoreList(Resource):
    def get(self):    
        return {'stores':[store.json() for store in StoreModel.get_all()]}