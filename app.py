
from flask import Flask, jsonify, request

from inventory import (
    get_all_items,
    get_item,
    add_item,
    update_item,
    delete_item
)

from openfoodfacts import lookup_product

app = Flask(__name__)


def validate_item(data, partial=False):
    """Validate inventory data."""
    if not isinstance(data, dict) or not data:
        return "A JSON object is required"

    if not partial:
        for field in ("name", "quantity", "price"):
            if field not in data:
                return f"{field} is required"

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return "Name must be a non-empty string"

    if "quantity" in data:
        if type(data["quantity"]) is not int or data["quantity"] < 0:
            return "Quantity must be a non-negative integer"

    if "price" in data:
        if type(data["price"]) not in (int, float) or data["price"] < 0:
            return "Price must be a non-negative number"

    if "barcode" in data:
        barcode = data["barcode"]
        if barcode is not None and (
            not isinstance(barcode, str) or not barcode.isdigit()
        ):
            return "Barcode must be a numeric string"

    return None


@app.get("/")
def home():
    return jsonify({
        "message": "Welcome to the Inventory Management API",
        "endpoints": {
            "inventory": "/inventory",
            "product_lookup": "/products/lookup/<barcode>",
            "product_import": "/inventory/import"
        }
    }), 200


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.get("/inventory")
def get_inventory():
    return jsonify(get_all_items()), 200


@app.get("/inventory/<int:item_id>")
def get_inventory_item(item_id):
    item = get_item(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200


@app.post("/inventory")
def create_inventory_item():
    data = request.get_json(silent=True)
    error = validate_item(data)

    if error:
        return jsonify({"error": error}), 400

    item = add_item(
        data["name"].strip(),
        data["quantity"],
        data["price"],
        data.get("barcode")
    )

    return jsonify(item), 201


@app.patch("/inventory/<int:item_id>")
def patch_inventory_item(item_id):
    item = get_item(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(silent=True)
    error = validate_item(data, partial=True)

    if error:
        return jsonify({"error": error}), 400

    if "name" in data:
        data["name"] = data["name"].strip()

    updated_item = update_item(item_id, data)
    return jsonify(updated_item), 200


@app.delete("/inventory/<int:item_id>")
def remove_inventory_item(item_id):
    if not delete_item(item_id):
        return jsonify({"error": "Item not found"}), 404

    return "", 204


@app.get("/products/lookup/<barcode>")
def get_external_product(barcode):
    try:
        product = lookup_product(barcode)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 503

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product), 200


@app.post("/inventory/import")
def import_external_product():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON data is required"}), 400

    barcode = data.get("barcode")

    if not isinstance(barcode, str) or not barcode.isdigit():
        return jsonify({"error": "Valid barcode required"}), 400

    quantity = data.get("quantity", 0)
    price = data.get("price", 0)

    validation_error = validate_item({
        "name": "External Product",
        "quantity": quantity,
        "price": price,
        "barcode": barcode
    })

    if validation_error:
        return jsonify({"error": validation_error}), 400

    try:
        product = lookup_product(barcode)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 503

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    item = add_item(
        product["name"],
        quantity,
        price,
        product["barcode"]
    )

    return jsonify(item), 201


if __name__ == "__main__":
    app.run(debug=True)
