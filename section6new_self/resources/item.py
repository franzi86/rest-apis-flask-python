import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schema import ItemSchema, ItemUpdateSchema
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.find_by_id_404(item_id)

        return item

    def delete(self, item_id):
        item = ItemModel.find_by_id_404(item_id)
        item.delete_from_db()

        return {"message": "Item deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.find_by_id(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            if item_data.get("store_id", None) is None:
                abort(400, message="store_id is missing for inserting that item.")
            item = ItemModel(id=item_id, **item_data)

        try:
            item.save_to_db()
        except SQLAlchemyError:
            abort(
                500, message="An error occurred while inserting or updating the item."
            )

        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.get_all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            item.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return item, 201
