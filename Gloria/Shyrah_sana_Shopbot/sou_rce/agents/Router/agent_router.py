from langchain_core.runnables import Runnable
from sou_rce.Agent_tools.Tools import (
    SmartItemLocator,
    PurchaseDelegate
)

# === Router Registry ===
agent_router: dict[str, Runnable] = {
    "item_locator": SmartItemLocator(),
    "purchase_delegate": PurchaseDelegate()
}

# === Simulated Router Chain ===
def router_chain(message: str) -> str:
    message = message.lower()
    if "buy" in message or "purchase" in message:
        return "purchase_delegate"
    elif "where" in message or "locate" in message:
        return "item_locator"
    return "item_locator"  # Default fallback

# === Routing Function ===
def route_take(message: str) -> str:
    try:
        clean_message = message.strip().lower()
        category = router_chain(clean_message).strip()
        print(f"[Router] Selected tool: '{category}'")

        tool = agent_router.get(category)
        if not tool:
            return f"⚠️ No tool found for category: '{category}'"

        result = tool.invoke(clean_message)
        return str(result)

    except Exception as e:
        return f"❌ Error during routing: {e}"

# === CLI Entry Point ===
if __name__ == "__main__":
    try:
        print("🧠 Smart ShopBot CLI (type 'exit' to quit)")
        while True:
            user_input = input("\n>> ")
            if user_input.lower() in ("exit", "quit"):
                print("👋 Exiting...")
                break
            result = route_take(user_input)
            print(f"\n📦 Response:\n{result}")
    except KeyboardInterrupt:
        print("\n👋 Exiting...")