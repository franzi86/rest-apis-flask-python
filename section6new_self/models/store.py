from typing import List
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")

    @classmethod
    def find_by_name(cls, name) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id) -> "StoreModel":
        return cls.query.get_or_404(id)

    @classmethod
    def get_all(cls) -> List["StoreModel"]:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
