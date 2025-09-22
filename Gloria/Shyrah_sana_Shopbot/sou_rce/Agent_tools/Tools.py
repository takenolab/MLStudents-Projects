from langchain_core.runnables import Runnable
import sqlite3

# === Smart Item Locator ===
class SmartItemLocator(Runnable):
    def invoke(self, message: str) -> str:
        item_name = self.extract_item_name(message)
        result = self.query_inventory(item_name)
        if result:
            return (
                f"🛍️ Item: {item_name.title()}\n"
                f"💲 Price: MWK {result['price']}\n"
                f"🗺️ Location: {result['location']}"
            )
        return f"❌ Item '{item_name}' not found in inventory."

    def extract_item_name(self, message: str) -> str:
        # Simple keyword extraction (can be replaced with NLP)
        return message.split()[0]

    def query_inventory(self, item_name: str) -> dict | None:
        conn = sqlite3.connect("store_inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT price, location FROM inventory WHERE name = ?", (item_name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"price": row[0], "location": row[1]}
        return None

# === Purchase Delegate ===
class PurchaseDelegate(Runnable):
    def invoke(self, message: str) -> str:
        # Simulate extracting item and account info
        item_name = message.split()[0]
        account = "user_account_123"  # Placeholder

        result = self.query_inventory(item_name)
        if not result:
            return f"❌ Item '{item_name}' not found."

        if self.process_payment(account, result['price']):
            return (
                f"✅ Purchase successful!\n"
                f"🛍️ Item: {item_name.title()}\n"
                f"💲 Charged: MWK {result['price']}\n"
                f"📦 Pickup Location: {result['location']}"
            )
        return "❌ Payment failed. Please check your account."

    def query_inventory(self, item_name: str) -> dict | None:
        conn = sqlite3.connect("store_inventory.db")
        cursor = conn.cursor()
        cursor.execute("SELECT price, location FROM inventory WHERE name = ?", (item_name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"price": row[0], "location": row[1]}
        return None

    def process_payment(self, account: str, amount: float) -> bool:
        print(f"[Payment] Charging MWK {amount} to account {account}")
        return True  # Simulate success