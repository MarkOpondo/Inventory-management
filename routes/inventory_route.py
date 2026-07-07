from flask import Blueprint, jsonify, request
from models.inventory import InventoryItem
from services.database import load_db, save_db

inventory = Blueprint("inventory", __name__)

@inventory.route("/inventory", methods=["GET"])
def get_all_items():
    inventory = load_db()
    return jsonify([item.to_dict() for item in inventory]), 200

# GET /inventory/<id>
@inventory.route("/inventory/<string:id>", methods=["GET"])
def get_item(id):
    inventory = load_db()
    item = next((i for i in inventory if i.id == id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item.to_dict()), 200

# POST /inventory - Add item and write updates straight to disk
@inventory.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json()
    
    if not data or not all(k in data for k in ("id", "name", "quantity", "price")):
        return jsonify({"error": "Missing required fields"}), 400
        
    inventory = load_db()
    if any(i.id == data["id"] for i in inventory):
        return jsonify({"error": f"Item with ID '{data['id']}' already exists"}), 400

    new_item = InventoryItem(
        id=data["id"],
        name=data["name"],
        quantity=int(data["quantity"]),
        price=float(data["price"])
    )
    
    inventory.append(new_item)
    save_db(inventory) # Write down changes permanently
    return jsonify(new_item.to_dict()), 201

# PATCH /inventory/<id>
@inventory.route("/inventory/<string:id>", methods=["PATCH"])
def update_item(id):
    data = request.get_json()
    inventory = load_db()
    item = next((i for i in inventory if i.id == id), None)
    
    if not item:
        return jsonify({"error": "Item not found"}), 404

    if "name" in data:
        item.name = data["name"]
    if "quantity" in data:
        item.quantity = int(data["quantity"])
    if "price" in data:
        item.price = float(data["price"])

    save_db(inventory)
    return jsonify(item.to_dict()), 200

# DELETE /inventory/<id>
@inventory.route("/inventory/<string:id>", methods=["DELETE"])
def delete_item(id):
    inventory = load_db()
    item = next((i for i in inventory if i.id == id), None)
    
    if not item:
        return jsonify({"error": "Item not found"}), 404
        
    updated_inventory = [i for i in inventory if i.id != id]
    save_db(updated_inventory)
    return "", 204


