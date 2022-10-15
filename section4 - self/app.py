from flask import Flask, request
from flask_restful import Resource, Api,reqparse
from flask_jwt import JWT, jwt_required, current_identity

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)
jwt = JWT(app, authenticate, identity)
items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda i: i['name'] == name,items),None)
     
        return {'item': item}, 200 if item else 404
    
    def post(self, name):
        if next(filter(lambda i: i['name'] == name,items),None) is not None:
            return {'message': "An item with name {} already exists".format(name)}, 400
        data = Item.parser.parse_args()
        new_item = {'name':name, 'price': data['price']}
        items.append(new_item)
        return new_item, 201
    
    def delete(self, name):
        global items

        items = list(filter(lambda i: i['name'] != name,items))
        return {'message': 'Item deleted'}
    
    def put(self, name):
        item = next(filter(lambda i: i['name'] == name,items),None)
        data = Item.parser.parse_args()
        if item is None:
            
            item = {'name':name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'Items':items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


app.run(port=5000, debug=True)