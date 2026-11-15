
import requests

API_URL = "http://127.0.0.1:5000"


def send_request(method, endpoint, data=None):
    try:
        response = requests.request(
            method,
            f"{API_URL}{endpoint}",
            json=data,
            timeout=15
        )

        print(f"\nHTTP Status: {response.status_code}")

        if response.content:
            result = response.json()
            return result

        return None

    except requests.RequestException as error:
        print(f"Connection error: {error}")
        return None
    except ValueError:
        print("Server returned an invalid JSON response.")
        return None


def display_product(product):
    print("-" * 40)
    print(f"ID:       {product.get('id', 'N/A')}")
    print(f"Name:     {product.get('name', 'Unknown')}")
    print(f"Quantity: {product.get('quantity', 'N/A')}")
    print(f"Price:    ${product.get('price', 0):.2f}")
    print(f"Barcode:  {product.get('barcode', 'N/A')}")


def list_inventory():
    result = send_request("GET", "/inventory")

    if isinstance(result, list):
        if not result:
            print("\nInventory is empty.")
        else:
            print("\nCURRENT INVENTORY")
            for product in result:
                display_product(product)
    elif result is not None:
        print(result)


def view_product():
    item_id = input("Enter product ID: ").strip()

    if not item_id.isdigit():
        print("Invalid product ID.")
        return

    result = send_request("GET", f"/inventory/{item_id}")

    if isinstance(result, dict):
        if "error" in result:
            print(result["error"])
        else:
            display_product(result)


def add_product():
    try:
        name = input("Product name: ").strip()
        quantity = int(input("Quantity: "))
        price = float(input("Price: "))
        barcode = input("Barcode (optional): ").strip()

        data = {
            "name": name,
            "quantity": quantity,
            "price": price,
            "barcode": barcode or None
        }

        result = send_request("POST", "/inventory", data)

        if result:
            print(result)

    except ValueError:
        print("Quantity must be an integer and price must be a number.")


def update_product():
    item_id = input("Product ID to update: ").strip()

    if not item_id.isdigit():
        print("Invalid product ID.")
        return

    print("Leave fields blank to keep existing values.")

    name = input("New name: ").strip()
    quantity = input("New quantity: ").strip()
    price = input("New price: ").strip()

    data = {}

    try:
        if name:
            data["name"] = name
        if quantity:
            data["quantity"] = int(quantity)
        if price:
            data["price"] = float(price)

    except ValueError:
        print("Invalid quantity or price.")
        return

    if not data:
        print("No updates provided.")
        return

    result = send_request(
        "PATCH",
        f"/inventory/{item_id}",
        data
    )

    if result:
        print(result)


def remove_product():
    item_id = input("Product ID to delete: ").strip()

    if not item_id.isdigit():
        print("Invalid product ID.")
        return

    confirm = input("Delete this product? (y/n): ").lower()

    if confirm == "y":
        result = send_request(
            "DELETE",
            f"/inventory/{item_id}"
        )
        if result is None:
            print("Delete request finished.")


def lookup_barcode():
    barcode = input("Enter product barcode: ").strip()

    if not barcode.isdigit():
        print("Invalid barcode.")
        return

    product = send_request(
        "GET",
        f"/products/lookup/{barcode}"
    )

    if not product or "error" in product:
        print("Product lookup failed.")
        if product:
            print(product)
        return

    print("\nPRODUCT FOUND")
    print(f"Name: {product['name']}")
    print(f"Brand: {product['brand']}")
    print(f"Barcode: {product['barcode']}")


def import_product():
    barcode = input("Enter product barcode: ").strip()

    try:
        quantity = int(input("Inventory quantity: "))
        price = float(input("Selling price: "))

    except ValueError:
        print("Invalid quantity or price.")
        return

    data = {
        "barcode": barcode,
        "quantity": quantity,
        "price": price
    }

    result = send_request("POST", "/inventory/import", data)

    if result:
        if "error" in result:
            print(result["error"])
        else:
            print("\nProduct successfully imported!")
            display_product(result)


def main():
    while True:
        print("\n" + "=" * 40)
        print("INVENTORY MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. View all inventory")
        print("2. View product by ID")
        print("3. Add product")
        print("4. Update product")
        print("5. Delete product")
        print("6. Look up barcode")
        print("7. Import external product")
        print("8. Exit")

        choice = input("\nChoose an option: ").strip()

        actions = {
            "1": list_inventory,
            "2": view_product,
            "3": add_product,
            "4": update_product,
            "5": remove_product,
            "6": lookup_barcode,
            "7": import_product
        }

        if choice == "8":
            print("Goodbye!")
            break

        action = actions.get(choice)

        if action:
            action()
        else:
            print("Invalid selection. Try again.")


if __name__ == "__main__":
    main()
