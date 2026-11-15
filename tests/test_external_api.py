
import pytest

import app as app_module
import openfoodfacts
from inventory import inventory


class FakeResponse:
    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise openfoodfacts.requests.HTTPError(
                "External API error"
            )

    def json(self):
        return self.data


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True
    inventory.clear()

    with app_module.app.test_client() as client:
        yield client

    inventory.clear()


@pytest.fixture
def mock_product(monkeypatch):
    def fake_get(url, headers=None, params=None, timeout=None):
        return FakeResponse({
            "status": 1,
            "product": {
                "product_name": "Nutella",
                "brands": "Ferrero"
            }
        })

    monkeypatch.setattr(openfoodfacts.requests, "get", fake_get)


def test_external_lookup(mock_product):
    product = openfoodfacts.lookup_product("3017620422003")

    assert product["name"] == "Nutella"
    assert product["brand"] == "Ferrero"
    assert product["barcode"] == "3017620422003"


def test_lookup_route(client, mock_product):
    response = client.get(
        "/products/lookup/3017620422003"
    )

    assert response.status_code == 200
    assert response.get_json()["name"] == "Nutella"


def test_import_product(client, mock_product):
    response = client.post("/inventory/import", json={
        "barcode": "3017620422003",
        "quantity": 5,
        "price": 6.99
    })

    assert response.status_code == 201

    item = response.get_json()

    assert item["name"] == "Nutella"
    assert item["quantity"] == 5
    assert item["price"] == 6.99

    inventory_response = client.get("/inventory")
    assert len(inventory_response.get_json()) == 1


def test_product_not_found(client, monkeypatch):
    monkeypatch.setattr(
        app_module,
        "lookup_product",
        lambda barcode: None
    )

    response = client.get("/products/lookup/999999999")

    assert response.status_code == 404


def test_external_service_error(client, monkeypatch):
    def fail_lookup(barcode):
        raise RuntimeError("External API unavailable")

    monkeypatch.setattr(
        app_module,
        "lookup_product",
        fail_lookup
    )

    response = client.get(
        "/products/lookup/3017620422003"
    )

    assert response.status_code == 503


def test_invalid_barcode(client):
    response = client.post("/inventory/import", json={
        "barcode": "invalid",
        "quantity": 5,
        "price": 6.99
    })

    assert response.status_code == 400


def test_invalid_import_quantity(client):
    response = client.post("/inventory/import", json={
        "barcode": "3017620422003",
        "quantity": -5,
        "price": 6.99
    })

    assert response.status_code == 400


def test_invalid_lookup_barcode():
    with pytest.raises(ValueError):
        openfoodfacts.lookup_product("bad-barcode")
