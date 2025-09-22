import json
import os

USERS_FILE = 'data/users.json'  # Path to users.json

def load_users():
    """Loads users from the JSON file."""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Saves updated user data to the JSON file."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def charge_account(customer_id, amount, users=None):
    """
    Charges a customer’s account for a purchase.

    Parameters:
        customer_id (str): The ID of the customer
        amount (float): The total cost of the items
        users (dict, optional): Preloaded users data. If None, it will be loaded from file.

    Returns:
        bool: True if payment succeeded, False otherwise.
    """
    if users is None:
        users = load_users()

    customer = users.get(customer_id)
    if not customer:
        print(f"❌ Customer ID '{customer_id}' not found.")
        return False

    if customer['balance'] >= amount:
        customer['balance'] -= amount
        users[customer_id] = customer
        save_users(users)
        print(f"💰 Charged {amount} MK from '{customer_id}'. New balance: {customer['balance']} MK")
        return True
    else:
        print(f"⚠️ Insufficient funds for '{customer_id}'. Balance: {customer['balance']} MK")
        return False
