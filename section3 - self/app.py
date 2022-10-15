from flask import Flask,jsonify,request

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]

@app.route('/store',methods=['Post'])
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return jsonify(new_store)

@app.route('/store/<string:name>',methods=['GET'])
def get_store(name):

    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'Store not found'})

@app.route('/store',methods=['GET'])
def get_stores():
    return jsonify({'Stores': stores})

@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    new_item = {"name": request_data["name"], "price":request_data["price"]}
    for store in stores:
        if store['name'] == name:
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'Store not found'})

@app.route('/store/<string:name>/item', methods=['GET'])
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})
    return jsonify({'message': 'Store not found'})

app.run(port=5000)