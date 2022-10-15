from sqlite3 import IntegrityError
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from models import StoreModel
from schema import StoreSchema
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("stores", __name__, description="Operations on store")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.find_by_id(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.find_by_id(store_id)
        store.delete_from_db()

        return {"message": "Store deleted."}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.get_all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            store.save_to_db()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store.")
        return store, 201
