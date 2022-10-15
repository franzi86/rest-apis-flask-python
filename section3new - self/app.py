from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [{"name": "My Store", "items": [{"name": "Chair", "price": 15.99}]}]


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.route("/store/<string:name>", methods=["GET"])
def get_store(name):

    for store in stores:
        if store["name"] == name:
            return jsonify(store)
    return jsonify({"message": "Store not found"})


@app.get("/store")
def get_stores():
    return {"Stores": stores}


@app.post("/store/<string:name>/item")
def create_item_in_store(name):
    request_data = request.get_json()
    new_item = {"name": request_data["name"], "price": request_data["price"]}
    for store in stores:
        if store["name"] == name:
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404


@app.get("/store/<string:name>/item")
def get_items_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404


app.run(port=5000)
