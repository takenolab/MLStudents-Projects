from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from Model.model import llm

# === Router Prompt (Unified Logic) ===
router_prompt_template = """
You are Shyrah❤️🩵, the witty😉 and helpful AI shopping assistant working across multiple stores.

When a customer asks for an item, your job is to do the following depending on their need:

1. **If they are in a physical shop**, provide the exact **location/map** of the item.
2. **If they are shopping online**, compare **prices** of the item across different stores (e.g., Walmart, ShopRite, Amazon).
3. **If multiple options exist**, recommend the **best quality** item and justify why.
4. **If they ask to buy**, guide them through **online purchase** steps.

Respond in a friendly, helpful, and professional way.

---

Customer Message: {message}

Your Response:
"""

# === Build the LLM chain ===
router_prompt = PromptTemplate(
    template=router_prompt_template.strip(),
    input_variables=["message"]
)

router_chain: Runnable = router_prompt | llm | StrOutputParser()

# === Main Router Function ===
def route_take(message: str) -> str:
    """
    Routes the message through the unified AI logic chain.
    """
    try:
        cleaned = message.strip()
        return router_chain.invoke({"message": cleaned})
    except Exception as e:
        return f"❌ Error while processing your request: {e}"

# === Example CLI Test ===
if __name__ == "__main__":
    print("🛒 Welcome to ShopBot AI — Ask me about any product!")
    while True:
        try:
            user_input = input("\n💬 You: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            result = route_take(user_input)
            print(f"\n🤖 ShopBot: {result}")
        except KeyboardInterrupt:
            print("\n👋 Exiting ShopBot.")
            break
