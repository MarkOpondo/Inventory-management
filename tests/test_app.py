from models.inventory import InventoryItem
import pytest

# class tests
def test_create_inventory_item():
    # Test the inventory item saves attributes properly
    item = InventoryItem("2", "brush", 3, 20.00)

    assert item.id == "2"
    assert item.name == "brush"
    assert item.quantity == 3
    assert item.price == 20.00

def test_convert_item_to_dictionary():
    # Test that an item converts to a clean dictionary
    item = InventoryItem("3", "shoe", 2, 30.00)
    item_dict = item.to_dict()

    assert item_dict["id"] == "3"
    assert item_dict["name"] == "shoe"

# unit tests
def test_add_item_to_list():
    test_db = []
    new_item = InventoryItem("2", "blanket", 3, 25.50)

    test_db.append(new_item)

    assert len(test_db) == 1
    assert test_db[0].name == "blanket"

def test_delete_item_from_list():
    item1 = InventoryItem("1", "plate", 5, 5.50)
    item2 = InventoryItem("2", "socks", 4, 1.00)
    
    test_db = [item1, item2]

    test_db = [i for i in test_db if i.id != "1"]

    assert len(test_db) == 1
    assert test_db[0].id == "2"