
import pytest

from app import app
from inventory import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True
    inventory.clear()

    with app.test_client() as client:
        yield client

    inventory.clear()


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.get_json()


def test_health_route(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_get_empty_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_inventory_item(client):
    response = client.post("/inventory", json={
        "name": "Milk",
        "quantity": 10,
        "price": 3.99
    })

    assert response.status_code == 201
    assert response.get_json()["name"] == "Milk"


def test_get_specific_item(client):
    created = client.post("/inventory", json={
        "name": "Bread",
        "quantity": 5,
        "price": 2.50
    })

    item_id = created.get_json()["id"]

    response = client.get(f"/inventory/{item_id}")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Bread"


def test_get_missing_item(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404


def test_update_item(client):
    created = client.post("/inventory", json={
        "name": "Eggs",
        "quantity": 12,
        "price": 4.99
    })

    item_id = created.get_json()["id"]

    response = client.patch(
        f"/inventory/{item_id}",
        json={"quantity": 20}
    )

    assert response.status_code == 200
    assert response.get_json()["quantity"] == 20
    assert response.get_json()["name"] == "Eggs"


def test_delete_item(client):
    created = client.post("/inventory", json={
        "name": "Cheese",
        "quantity": 3,
        "price": 5.99
    })

    item_id = created.get_json()["id"]

    response = client.delete(f"/inventory/{item_id}")

    assert response.status_code == 204
    assert client.get(f"/inventory/{item_id}").status_code == 404


def test_missing_name_rejected(client):
    response = client.post("/inventory", json={
        "quantity": 10,
        "price": 2.99
    })

    assert response.status_code == 400


def test_negative_quantity_rejected(client):
    response = client.post("/inventory", json={
        "name": "Milk",
        "quantity": -1,
        "price": 3.99
    })

    assert response.status_code == 400


def test_invalid_price_rejected(client):
    response = client.post("/inventory", json={
        "name": "Milk",
        "quantity": 5,
        "price": "expensive"
    })

    assert response.status_code == 400


def test_invalid_json_rejected(client):
    response = client.post("/inventory", json=[])

    assert response.status_code == 400


def test_patch_missing_item(client):
    response = client.patch(
        "/inventory/999",
        json={"price": 4.99}
    )

    assert response.status_code == 404


def test_delete_missing_item(client):
    response = client.delete("/inventory/999")

    assert response.status_code == 404
