import hashlib
import json
import os

DATA_DIR = 'data'
INVENTORY_FILE = os.path.join(DATA_DIR, 'inventory.json')
STORE_MAP_FILE = os.path.join(DATA_DIR, 'store_map.json')
ADMINS_FILE = os.path.join(DATA_DIR, 'admins.json')


# -------------------------
# Utility Functions
# -------------------------

def load_data(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r') as f:
        return json.load(f)

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


# -------------------------
# Admin Authentication
# -------------------------

def load_admins():
    return load_data(ADMINS_FILE)

def authenticate_admin(username, password):
    admins = load_admins()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    return admins.get(username) == hashed_pw


# -------------------------
# Inventory Management
# -------------------------

def add_item(name, aisle, section, price, stock):
    name = name.lower()
    inventory = load_data(INVENTORY_FILE)
    store_map = load_data(STORE_MAP_FILE)

    inventory[name] = {
        "price": price,
        "stock": stock
    }

    store_map[name] = {
        "aisle": aisle,
        "section": section
    }

    save_data(INVENTORY_FILE, inventory)
    save_data(STORE_MAP_FILE, store_map)

    return f"✅ Item '{name}' added with {stock} units at MK{price} in Aisle {aisle}, Section {section}."

def update_stock(name, new_stock):
    name = name.lower()
    inventory = load_data(INVENTORY_FILE)

    if name in inventory:
        inventory[name]["stock"] = new_stock
        save_data(INVENTORY_FILE, inventory)
        return f"✅ Stock for '{name}' updated to {new_stock}."
    else:
        return f"❌ Item '{name}' not found in inventory."

