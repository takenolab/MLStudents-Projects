import os
import sys
from langchain.agents import Tool

# Determine project root so custom modules can be imported
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from Agent_tools.Tools import SmartItemLocator
    # from Agent_tools.Tools import InventoryManager
    # from Agent_tools.Tools import TheftDetector
    # from Agent_tools.Tools import FaceRecognitionAuth
    # from Agent_tools.Tools import PurchaseHandler
except ModuleNotFoundError as e:
    raise ImportError(f"Failed to import required components from Agent_tools.Tools: {e}")

# Define tools for the LangChain agent
TOOLS = [
    Tool(
        name="smart_item_locator",
        func=SmartItemLocator().locate_item,
        description="Locate items in the store inventory by name or SKU."
    ),
    Tool(
        name="inventory_manager",
        func=InventoryManager().check_and_update_stock,
        description="Check inventory levels and update when items get purchased."
    ),
    Tool(
        name="theft_detector",
        func=TheftDetector().monitor,
        description="Monitor store zones and alert on suspicious behavior."
    ),
    Tool(
        name="face_recognition_auth",
        func=FaceRecognitionAuth().recognize,
        description="Recognize customers or flagged individuals for theft prevention."
    ),
    Tool(
        name="purchase_handler",
        func=PurchaseHandler().process_purchase,
        description="Process purchase transactions, update inventory, handle payments."
    ),
]

def initialize_shopbot(agent_class, **agent_kwargs):
    """
    Initialize the ShopBot with all tools for store operation:
    locating items, inventory, theft prevention, face recognition, and purchases.
    """
    return agent_class(tools=TOOLS, **agent_kwargs)

# Example usage:
if __name__ == "__main__":
    from langchain.agents import AgentExecutor, LLMAgent, create_openai_functions_agent
    from langchain.chat_models import ChatOpenAI

    # You can choose whichever style of agent you prefer
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    agent = create_openai_functions_agent(tools=TOOLS, llm=llm)
    shopbot = AgentExecutor.from_agent_and_tools(agent=agent, tools=TOOLS, verbose=True)

    # Example agent call
    response = shopbot.run("Locate toothpaste in aisle 3, then process purchase for 2 units.")
    print(response)

