import sys
import os
from langchain.agents import Tool

# Set up sys.path to include the project root so we can import smart_item_locator
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now safely import your custom tool
try:
    from AGents.ROuter.AGent_tools.Tools import smart_item_locator
except ModuleNotFoundError as e:
    raise ImportError(f"Failed to import 'smart_item_locator'. Check path or casing. Error: {e}")

# Define the tool for LangChain
tools = [
    Tool(
        name="item_locator",
        func=smart_item_locator,
        description=(
            "Locate an item in-store or online based on input like: "
            "'item_name=soap, user_query=where is it?, shop=store_a, mode=physical'."
        )
    )
]















# from langchain.agents import Tool
# from AGents.ROuter.AGent_tools.Tools import smart_item_locator

# tools = [
#     Tool(
#         name="item_locator",
#         func=smart_item_locator,
#         description=(
#             "Locate an item in-store or online based on input like: "
#             "'item_name=soap, user_query=where is it?, shop=store_a, mode=physical'."
#         )
#     )
# ]



# from langchain.agents import Tool
# from AGENTS.router.agent_tools.Tools import (
#     soapy_items,
#     cooking_ingredients,
#     snacks,
#     game_accessories,
#     clothes_and_beddings,
#     shoes,
#     baby_care,
#     suggest_related_items
# )
# tools = [
#     Tool(
#         name="Soapy Items",
#         func=soapy_items,
#         description="Find hygiene items like soap and shampoo."
#     ),
#     Tool(
#         name="Cooking Ingredients",
#         func=cooking_ingredients,
#         description="Locate cooking ingredients like salt and flour."
#     ),
#     Tool(
#         name="Snacks",
#         func=snacks,
#         description="Find snacks like chips and candy."
#     ),
#     Tool(
#         name="Game Accessories",
#         func=game_accessories,
#         description="Locate gaming accessories."
#     ),
#     Tool(
#         name="Clothes and Beddings",
#         func=clothes_and_beddings,
#         description="Find clothes and bedding items."
#     ),
#     Tool(
#         name="Shoes",
#         func=shoes,
#         description="Locate footwear items."
#     ),
#     Tool(
#         name="Baby Care",
#         func=baby_care,
#         description="Find baby care products."
#     ),
#     Tool(
#         name="Suggest Related Items",
#         func=suggest_related_items,
#         description="Suggest alternatives or related items."
#     ),
# ]
