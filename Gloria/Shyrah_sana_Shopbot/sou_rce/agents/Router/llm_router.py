# === Imports ===
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from Model.model import llm 
from sou_rce.Agent_tools.Tools import SmartItemLocator, PurchaseDelegate

# === Router Prompt ===
router_prompt_template = """
You are Shyrah❤️🩵, a witty😉 and helpful AI assistant working inside a physical store in Malawi.

Your job is to decide which internal tool should handle a customer's request. You must choose **only one** of the following tools:

1. **item_locator** — Use this when the customer is asking where an item is located in the store, what shelf or aisle it’s on, or wants to compare prices or quality of different options.
2. **purchase_delegate** — Use this when the customer wants you to buy the item for them, assist with payment, or handle the purchase while they wait.

Respond with **only the tool name**: `item_locator` or `purchase_delegate`. Do not explain your reasoning. Do not include any extra text.

---
Customer Message: {message}
Tool Name:
"""

# === Build the LLM Chain ===
router_prompt = PromptTemplate(
    template=router_prompt_template.strip(),
    input_variables=["message"]
)

router_chain: Runnable = router_prompt | llm | StrOutputParser()

# === Tool Registry ===
agent_router: dict[str, Runnable] = {
    "item_locator": SmartItemLocator(),
    "purchase_delegate": PurchaseDelegate()
}

# === Routing Function ===
def route_take(message: str) -> str:
    """
    Routes a user message to the appropriate tool using the LLM router.
    """
    try:
        clean_message = message.strip()
        category = router_chain.invoke({"message": clean_message}).strip()
        print(f"[Router] Selected tool: '{category}'")

        tool = agent_router.get(category)
        if not tool:
            return f"⚠️ Sorry, no tool found for category: '{category}'"

        result = tool.invoke(clean_message)
        return str(result)

    except Exception as e:
        return f"❌ Error during routing: {e}"

# === CLI Entry Point ===
if __name__ == "__main__":
    print("🛒 Welcome to Shyrah AI — Ask me about any product!")
    while True:
        try:
            user_input = input("\n💬 You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Exiting Shyrah.")
                break
            result = route_take(user_input)
            print(f"\n🤖 Shyrah: {result}")
        except KeyboardInterrupt:
            print("\n👋 Exiting Shyrah.")
            break