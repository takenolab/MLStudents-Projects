from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('store.db')
    conn.row_factory = sqlite3.Row
    return conn


    @app.route('/find_item', methods=['GET'])
def find_item():
    item_name = request.args.get('item')
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM inventory WHERE name = ?', (item_name,)).fetchone()
    conn.close()
    if item:
        return jsonify({
            'name': item['name'],
            'price': item['price'],
            'location': item['location']
        })
    else:
        return jsonify({'error': 'Item not found'}), 404

        @app.route('/purchase', methods=['POST'])
def purchase():
    data = request.json
    # Validate face ID (placeholder)
    if not validate_face(data['face_id']):
        return jsonify({'error': 'Face not recognized'}), 403

    # Process payment (mock)
    if process_payment(data['account'], data['amount']):
        return jsonify({'status': 'Purchase successful'})
    else:
        return jsonify({'error': 'Payment failed'}), 400


        -- inventory table
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL,
    location TEXT
);

-- sample entry
INSERT INTO inventory (name, price, location)
VALUES ('Flour', 2500, 'Aisle 5 - Baking Section - Bottom Shelf');


from langchain_core.runnables import Runnable

class SmartItemLocator(Runnable):
    def invoke(self, message: str) -> str:
        # Parse message, query DB, return result
        item = extract_item_name(message)
        result = query_inventory(item)
        return f"🛍️ Item: {item}\n🏷️ Brands: {result['brands']}\n💲 Price: {result['price']}\n🗺️ Location: {result['location']}"
    


class PurchaseDelegate(Runnable):
    def invoke(self, message: str) -> str:
        # Parse message, validate face, process payment
        if not validate_face(message):
            return "❌ Face verification failed"
        success = process_payment(message)
        return "✅ Purchase successful" if success else "❌ Payment failed"
    
from sou_rce.Agent_tools.Tools import (
    SmartItemLocator,
    PurchaseDelegate
    # smart_item_locator,
    # purchase_delegate,
    # face_verifier
)

agent_router: dict[str, Runnable] = {
    "item_locator":  SmartItemLocator,
    "purchase_delegate": PurchaseDelegate,
    # "face_verifier": face_verifier
}
ShyrahShopBot/
├── app.py
├── data/
│   ├── inventory.json
│   ├── users.json
│   └── store_map.json
├── modules/
│   ├── customer.py
│   ├── admin.py
│   ├── face_recognition.py
│   └── payment.py
└── README.md
