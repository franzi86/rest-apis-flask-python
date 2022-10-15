from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="Every item needs a store_id."
    )

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {"message": "An item with name {} already exists".format(name)}, 400
        data = Item.parser.parse_args()
        new_item = ItemModel(name, **data)

        try:
            new_item.save_to_db()
        except:
            return {
                "message": "An error occurred inserting an item to the database."
            }, 500

        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item is None:
            return {"message": "An item with name {} does not exist".format(name)}, 400

        item.delete_from_db()
        return {"message": "Item deleted"}

    def put(self, name):
        item = ItemModel.find_by_name(name)
        data = Item.parser.parse_args()
        updated_item = ItemModel(name, **data)
        if item is None:
            try:
                updated_item.save_to_db()
            except:
                return {"message": "An error occurred inserting an item."}, 500
        else:
            try:
                updated_item.save_to_db()
            except:
                return {"message": "An error occurred updating an item."}, 500
        return updated_item.json()


class ItemList(Resource):
    def get(self):

        return {"Items": [item.json() for item in ItemModel.get_all()]}, 200
