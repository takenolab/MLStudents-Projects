# === Imports ===
from langchain_core.runnables import Runnable
from AGents.llm_router import router_chain
from AGents.ROuter.AGent_tools.Tools import smart_item_locator  # ✅ This must be exposed in that module

# === Router registry ===
agent_router: dict[str, Runnable] = {
    "item_locator": smart_item_locator  # Router must return this string
}

# === Routing Function ===
def route_take(message: str) -> str:
    """
    Routes a user message to the appropriate tool using a router.
    """
    try:
        clean_message = message.strip().lower()

        # Predict which tool should handle the message
        category = router_chain.invoke({"message": clean_message}).strip()
        print(f"[Router] Selected tool: '{category}'")

        # Get the appropriate tool
        tool = agent_router.get(category)
        if not tool:
            return f"⚠️ Sorry, no tool found for category: '{category}'"

        # Call the tool with the original message
        result = tool.invoke(clean_message)
        return str(result)

    except Exception as e:
        return f"❌ Error during routing: {e}"

# === CLI Entry Point ===
if __name__ == "__main__":
    try:
        print("🧠 Smart Item Locator CLI (type 'exit' to quit)")
        while True:
            user_input = input("\n>> ")
            if user_input.lower() in ("exit", "quit"):
                print("👋 Exiting...")
                break
            result = route_take(user_input)
            print(f"\n📦 Response:\n{result}")
    except KeyboardInterrupt:
        print("\n👋 Exiting...")






# # === Import tools ===
# from AGENTS.router.tools import tools  # Adjust import path as needed

# # Build router registry from tools
# agent_router: dict[str, callable] = {tool.name: tool.func for tool in tools}

# # === route_take() stays the same ===
# def route_take(message: str) -> str:
#     try:
#         clean_message = message.strip().lower()

#         # Route using classifier
#         category = router_chain.invoke({"message": clean_message}).strip()

#         print(f"[Router] Selected tool: '{category}'")

#         tool_func = agent_router.get(category)
#         if not tool_func:
#             return f"⚠️ No matching tool found for category '{category}'"

#         result = tool_func.invoke(clean_message)  # Or just: tool_func(clean_message)
#         return str(result)

#     except Exception as e:
#         return f"❌ Routing Error: {e}"






# Input: item_name=soap, user_query=where is it?, shop=default_store, mode=physical

# [Router] Selected tool: 'item_locator'

# 📦 Response:
# 🛍️ Item: Soap
# 🏷️ Brands: Dettol, Dove, Lifebuoy
# 💲 Price Range: K1,999.99 - K3,999.99
# 🗺️ Map Location: Aisle 1 - Hygiene
