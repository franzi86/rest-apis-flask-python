from db import db
from typing import List


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=True)
    price = db.Column(db.Float(precision=2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")

    @classmethod
    def find_by_name(cls, name) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id_404(cls, id) -> "ItemModel":
        return cls.query.get_or_404(id)

    @classmethod
    def find_by_id(cls, id) -> "ItemModel":
        return cls.query.get(id)

    @classmethod
    def get_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
