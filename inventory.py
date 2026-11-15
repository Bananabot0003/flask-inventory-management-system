
# In-memory inventory database
inventory = []


def get_all_items():
    """Return all inventory items."""
    return inventory


def get_item(item_id):
    """Find an inventory item by its ID."""
    for item in inventory:
        if item["id"] == item_id:
            return item

    return None


def add_item(name, quantity, price, barcode=None):
    """Create a new inventory item."""
    new_id = max(
        (item["id"] for item in inventory),
        default=0
    ) + 1

    new_item = {
        "id": new_id,
        "name": name,
        "quantity": quantity,
        "price": price,
        "barcode": barcode
    }

    inventory.append(new_item)
    return new_item


def update_item(item_id, updates):
    """Update an existing inventory item."""
    item = get_item(item_id)

    if item is None:
        return None

    for key in ["name", "quantity", "price", "barcode"]:
        if key in updates:
            item[key] = updates[key]

    return item


def delete_item(item_id):
    """Remove an inventory item."""
    item = get_item(item_id)

    if item is None:
        return False

    inventory.remove(item)
    return True
