
import requests

BASE_URL = "https://world.openfoodfacts.org"

HEADERS = {
    "User-Agent": (
        "FlaskInventoryManagement/1.0 "
        "(https://github.com/Bananabot0003/flask-inventory-management-system)"
    )
}


def lookup_product(barcode):
    """Look up a food product using its barcode."""

    barcode = str(barcode).strip()

    if not barcode.isdigit():
        raise ValueError("Barcode must contain only numbers")

    url = f"{BASE_URL}/api/v2/product/{barcode}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params={"fields": "code,product_name,brands"},
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

    except requests.RequestException as error:
        raise RuntimeError(
            "Open Food Facts is currently unavailable"
        ) from error

    except ValueError as error:
        raise RuntimeError(
            "Open Food Facts returned invalid JSON"
        ) from error

    if data.get("status") != 1:
        return None

    product = data.get("product", {})

    return {
        "barcode": barcode,
        "name": product.get("product_name") or "Unknown Product",
        "brand": product.get("brands") or "Unknown Brand"
    }
