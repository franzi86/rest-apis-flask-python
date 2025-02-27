from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404
    
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {
                'name': row[1],
                'price': row[2]
            }}
    
    def post(self, name):
        item = self.find_by_name(name)
        if item:
            return {'message': "An item with name {} already exists".format(name)}, 400
        data = Item.parser.parse_args()
        new_item = {'name':name, 'price': data['price']}
        
        try:
            Item.insert(new_item)
        except:
            return {'message':'An error occurred inserting an item to the database.'},500

        return new_item, 201
    
    @classmethod
    def insert(cls,new_item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (NULL,?,?)"
        cursor.execute(query,(new_item['name'],new_item['price']))

        connection.commit()
        connection.close()
    
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))

        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}
    
    def put(self, name):
        item = self.find_by_name(name)
        data = Item.parser.parse_args()
        updated_item = {'name':name, 'price': data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message':'An error occurred inserting an item.'},500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message':'An error occurred updating an item.'},500
        return updated_item
    
    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name = ?"
        cursor.execute(query,(item['price'],item['name']))

        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        items = []
        query = "SELECT * FROM items"
        result = cursor.execute(query)

        for row in result:
            items.append(
                {
                'name': row[1],
                'price': row[2]
                }
            )

        connection.close()
        return {'Items':items}