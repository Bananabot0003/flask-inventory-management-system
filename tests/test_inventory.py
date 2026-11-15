
import pytest

from inventory import (
    inventory,
    get_all_items,
    get_item,
    add_item,
    update_item,
    delete_item
)


@pytest.fixture(autouse=True)
def reset_inventory():
    inventory.clear()
    yield
    inventory.clear()


def test_inventory_starts_empty():
    assert get_all_items() == []


def test_add_item():
    item = add_item("Milk", 10, 3.99)

    assert item["id"] == 1
    assert item["name"] == "Milk"
    assert item["quantity"] == 10
    assert item["price"] == 3.99


def test_get_item():
    item = add_item("Bread", 5, 2.50)

    assert get_item(item["id"]) == item


def test_missing_item():
    assert get_item(999) is None


def test_update_item():
    item = add_item("Eggs", 12, 4.99)

    updated = update_item(
        item["id"],
        {"quantity": 20}
    )

    assert updated["quantity"] == 20
    assert updated["name"] == "Eggs"


def test_delete_item():
    item = add_item("Cheese", 3, 5.99)

    assert delete_item(item["id"]) is True
    assert get_item(item["id"]) is None


def test_delete_missing_item():
    assert delete_item(999) is False


def test_unique_ids():
    first = add_item("Milk", 1, 3.00)
    second = add_item("Bread", 2, 4.00)

    assert first["id"] != second["id"]
