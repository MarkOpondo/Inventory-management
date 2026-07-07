import json
import os
from models import InventoryItem

DB_FILE = "inventory.json"

def load_db():
    """Reads JSON from storage and instantiates list items."""
    if not os.path.exists(DB_FILE):
        # Create an empty file structure if it does not exist yet
        with open(DB_FILE, "w") as f:
            json.dump([], f)
        return []
        
    with open(DB_FILE, "r") as f:
        try:
            raw_data = json.load(f)
            return [InventoryItem.from_dict(item) for item in raw_data]
        except json.JSONDecodeError:
            # Fallback if file is corrupted
            return []

def save_db(inventory_list):
    """Converts objects to serializable dictionaries and commits them to the JSON file."""
    with open(DB_FILE, "w") as f:
        serialized_data = [item.to_dict() for item in inventory_list]
        json.dump(serialized_data, f, indent=4)