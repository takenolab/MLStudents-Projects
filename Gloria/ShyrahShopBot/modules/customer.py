# modules/customer.py

import json
from modules.payment import charge_account
from modules.face_recognition import recognize_face


# --------------------------
# Utility
# --------------------------

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


# --------------------------
# Locate Item
# --------------------------

def locate_item(item_name):
    store_map = load_json('data/store_map.json')
    item = store_map.get(item_name.lower())

    if item:
        return f"🗺️ '{item_name.title()}' is in Aisle {item['aisle']} — {item['section']}."
    return f"❌ Sorry, '{item_name}' is not in our store."


# --------------------------
# Purchase Item
# --------------------------

def purchase_item(item_name, qty, customer_id):
    inventory = load_json('data/inventory.json')
    users = load_json('data/users.json')
    item_name = item_name.lower()
    item = inventory.get(item_name)

    if not item:
        return f"❌ Item '{item_name}' not found."

    if item['stock'] < qty:
        return f"⚠️ Insufficient stock for '{item_name}'. Only {item['stock']} left."

    total_cost = item['price'] * qty

    if charge_account(customer_id, total_cost, users):
        # Deduct stock
        item['stock'] -= qty
        inventory[item_name] = item
        save_json('data/inventory.json', inventory)
        return f"✅ Purchase successful! '{item_name}' x{qty} purchased for {total_cost} MK."
    else:
        return "❌ Payment failed. Please check your account balance."


# --------------------------
# Identify

def identify_and_purchase(live_input, item_name, qty, customer_id):
    recognized = recognize_face(live_input)
    if recognized and recognized == customer_id:
        return purchase_item(item_name, qty, customer_id)
    else:
        return "❌ Face not recognized. Purchase not authorized."
