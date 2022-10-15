from db import db
from typing import List


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.String(), db.ForeignKey("stores.id"), nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")

    @classmethod
    def find_by_store_id_and_name(cls, store_id, name) -> "TagModel":
        return cls.query.filter(cls.store_id == store_id, cls.name == name).first()

    @classmethod
    def find_by_id_404(cls, id) -> "TagModel":
        return cls.query.get_or_404(id)

    @classmethod
    def find_by_id(cls, id) -> "TagModel":
        return cls.query.get(id)

    @classmethod
    def get_all(cls) -> List["TagModel"]:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
