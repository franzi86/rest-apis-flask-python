from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schema import TagSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.find_by_id(store_id)

        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.find_by_store_id_and_name(store_id, tag_data["name"]):
            abort(400, message="A tag with that name already exists in that store.")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            tag.save_to_db()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.find_by_id_404(item_id)
        tag = TagModel.find_by_id_404(tag_id)

        if item.store.id != tag.store.id:
            abort(
                400,
                message="Make sure item and tag belong to the same store before linking.",
            )

        item.tags.append(tag)

        try:
            item.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.find_by_id_404(item_id)
        tag = TagModel.find_by_id_404(tag_id)

        item.tags.remove(tag)

        try:
            item.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Item removed from tag", "item": item, "tag": tag}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.find_by_id_404(tag_id)
        return tag

    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self, tag_id):
        tag = TagModel.find_by_id_404(tag_id)

        if not tag.items:
            tag.delete_from_db()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",
        )
