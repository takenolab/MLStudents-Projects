from langchain.agents import tool
import json

# --- Base Utilities ---

def parse_input(input_str: str) -> dict:
    """
    Parse input like: "item_name=soap, user_query=where is it?, shop=store_a, mode=physical"
    """
    parts = [part.strip() for part in input_str.split(",")]
    data = {}
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            data[key.strip()] = value.strip()
    return data


def fetch_map(shop: str, item_name: str) -> str:
    """
    Simulate fetching a map or map coordinates for an item in a store.
    In a real scenario, you'd return map data (e.g., Folium HTML or image URL).
    """
    try:
        with open(f"store_maps/{shop}.json") as f:
            map_data = json.load(f)
        location = map_data["locations"].get(item_name.lower(), "Not mapped.")
        return f"🗺️ Map Location: {location}"
    except FileNotFoundError:
        return f"🗺️ Map for shop '{shop}' not found."


def suggest_best_shop(item_name: str) -> str:
    """
    Stimulate online price comparison or API integration.
    This would call e-commerce APIs (Amazon, Walmart, etc.) in production.
    """
    comparisons = {
        "soap": [
            {"shop": "Amazon", "price": "K2,499.99", "rating": "4.5⭐", "link": "https://amazon.com/soap"},
            {"shop": "Walmart", "price": "K1,899.99", "rating": "4.3⭐", "link": "https://walmart.com/soap"}
        ],
        "shampoo": [
            {"shop": "Target", "price": "K5,499.99", "rating": "4.6⭐", "link": "https://target.com/shampoo"},
            {"shop": "Amazon", "price": "K5,999.99", "rating": "4.4⭐", "link": "https://amazon.com/shampoo"}
        ]
    }
    results = comparisons.get(item_name.lower())
    if not results:
        return "🔎 No online comparison data available."
    
    best = min(results, key=lambda x: float(x["price"].strip("K")))
    details = "\n".join([f"- {r['shop']}: {r['price']} ({r['rating']}) [Link]({r['link']})" for r in results])
    return f"🌐 Online Price Comparison:\n{details}\n\n✅ Recommended: **{best['shop']}** for best value."


# --- Dynamic Item Tool Example ---

@tool
def smart_item_locator(input_str: str) -> str:
    """
    Locate an item either in-store or online with mapping and price suggestions.
    """
    data = parse_input(input_str)
    item_name = data.get("item_name", "").lower()
    shop = data.get("shop", "default_store")
    mode = data.get("mode", "physical")  # 'physical' or 'online'

    # Simulated in-store data for each shop
    store_items = {
        "default_store": {
            "soap": {
                "location": "Aisle 1 - Hygiene",
                "suggestions": ["Dettol", "Dove", "Lifebuoy"],
                "price": "K1,999.99 - K3,999.99"
            },
            "shampoo": {
                "location": "Aisle 1 - Hair Care",
                "suggestions": ["Pantene", "Tresemme", "Head & Shoulders"],
                "price": "K4,999.99 - K8,999.99"
            }
        },
        "store_b": {
            "soap": {
                "location": "Section A - Personal Care",
                "suggestions": ["Lux", "Palmolive", "Safeguard"],
                "price": "K2,299.99 - K4,499.99"
            }
        }
    }

    item_info = store_items.get(shop, {}).get(item_name)

    if not item_info:
        return f"⚠️ Item '{item_name}' not found in shop '{shop}'."

    response = (
        f"🛍️ **Item:** {item_name.title()}\n"
        f"🏷️ **Brands:** {', '.join(item_info['suggestions'])}\n"
        f"💲 **Price Range:** {item_info['price']}\n"
    )

    if mode == "physical":
        map_info = fetch_map(shop, item_name)
        response += f"{map_info}\n"
    elif mode == "online":
        comparison = suggest_best_shop(item_name)
        response += f"{comparison}\n"

    return response


