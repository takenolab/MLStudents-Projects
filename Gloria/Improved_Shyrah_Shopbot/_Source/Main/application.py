import os
import sys
import json
from dotenv import load_dotenv
import streamlit as st
from langchain.agents import initialize_agent, AgentType
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
# from Memory.Conversation import memory
from langchain.memory import ConversationBufferMemory


if "agent_memory" not in st.session_state:
    st.session_state.agent_memory = None 


llm = ChatOpenAI(
    model="glm-4.5V",
    temperature=0,
    api_key="c42373cad52843178efda15cf7864d36.mIgXX6WI2xRHDNIA",
    base_url="https://open.bigmodel.cn/api/paas/v4"
)


# Set up sys.path to include the project root so we can import smart_item_locator
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now safely import your custom tool
try:
    from _Source.AGents.ROuter.AGent_tools.Tools import smart_item_locator
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




# Optional import: folium for maps
try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False

# Dynamically add project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import custom modules (must exist)
# try:
    # from PROMPT_template.Templates import tools
    # from Model.model import llm
# except ModuleNotFoundError as e:
    # print(f"[ERROR] Required module not found: {e}")
    # sys.exit(1)

load_dotenv()

# Initialize agent
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    memory=st.session_state.agent_memory
)


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    memory=memory
)



class ShopBotApp:
    def __init__(self):
        self.history = []

    def get_store_map(self, store_id):
        """Return HTML map of a store if available."""
        if not FOLIUM_AVAILABLE:
            return "<p>Map feature unavailable. Please install 'folium'.</p>"

        json_path = os.path.join(PROJECT_ROOT, "store_maps", f"{store_id}.json")
        if not os.path.exists(json_path):
            return f"<p>Store map for ID '{store_id}' not found.</p>"

        try:
            with open(json_path, "r") as f:
                data = json.load(f)
            m = folium.Map(location=data["center"], zoom_start=18)
            for item, loc in data["locations"].items():
                folium.Marker(location=loc, popup=item).add_to(m)
            return m._repr_html_()
        except Exception as e:
            return f"<p>Failed to load map: {e}</p>"

    def process_query(self, message, history):
        """Run user message through LLM."""
        try:
            response = agent_executor.run(message)
        except Exception as e:
            response = f"Sorry, I encountered an error: {e}"
        history.append({"role":"user", "message":message})
        history.append({"role":"assistant","message":response})
        return response, history
    

    

    # def chat_with_user(self, message, history):
    #     """Handle full user interaction including map rendering."""
    #     response, history = self.process_query(message, history)
    #     if "### Show in-store map:" in response:
    #         store_id = response.split("### Show in-store map:")[-1].strip()
    #         map_html = self.get_store_map(store_id)
    #         return [{"role": "bot", "message": response}, {"role": "map", "html": map_html}], history
    #     return [{"role": "bot", "message": response}], history
    


    def chat_with_user(self, message, history):
        """ 
        Handle full user interaction including  map rendering

        """
        response, history = self.process_query(message, history)
        if "### Show in-store map:" in response:
            store_id = response.split("### Show in-store map:")[-1].strip()
            map_html = self.get_store_map(store_id)
            return [
            {"role": "assistant", "message": response},
            {"role": "assistant", "message": "", "html": map_html}
                     ], history
        return [{"role": "assistant", "message": response}], history


def interface():
    # 🌐 Use wide layout for full-screen experience
    st.set_page_config(page_title="Shyrah Shopbot🩵", layout="wide")

    # 🛍️ Sidebar for navigation or filters
    st.sidebar.title("🧭 Navigation")
    st.sidebar.markdown("Choose your shopping action:")
    action = st.sidebar.radio("What would you like to do?", [
      "Find Products", "Compare Prices", "Buy Online", "Locate In-Store"
    ])

    # 🛒 Main title and caption
    st.title("🛒 Shyrah Shopbot🩵 - Your Smart Shopping Assistant")
    st.caption("Ask me to find products, compare prices, buy online, or locate them in‑store! 🫣😁")

    # 🧱 Use columns for a clean layout
    col1, col2 = st.columns([2, 3])

    with col1:
        st.subheader("🧠 Assistant Panel")
        st.write(f"You're currently exploring: **{action}**")
        st.text_input("What product are you looking for?", placeholder="e.g. wireless headphones")

    with col2:
        st.subheader("📦 Product Display")
        st.info("Results will appear here based on your query and selected action.")




    # st.set_page_config(page_title="Shyrah Shopbot🩵", layout="centered")
    # st.title("🛒 Shyrah Shopbot🩵 - Your Smart Shopping Assistant")
    # st.caption("Ask me to find products, compare prices, buy online, or locate them in‑store! 🫣😁")
    

    if "agent_memory" not in st.session_state:
        st.session_state.agent_memory = ConversationBufferMemory(
             memory_key="chat_history",
             return_messages=True
               )
        agent_executor = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            memory=st.session_state.agent_memor
              )


    bot = ShopBotApp()
    # bot.agent_executor = agent_executor


    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            if "message" in entry and entry["message"]:
                st.markdown(entry["message"])
            elif "html" in entry:
                st.components.v1.html(entry["html"], height=400, scrolling=True)

    user_input = st.chat_input("How can I assist you today, my humble customer🫡🧐?")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        # Call your agent logic
        ui_elements, updated_history = bot.chat_with_user(user_input, st.session_state.chat_history)

        # Display AI responses
        for element in ui_elements:
            with st.chat_message("assistant"):
                if "message" in element and element["message"]:
                    st.markdown(element["message"])
                if "html" in element:
                    st.components.v1.html(element["html"], height=400, scrolling=True)

        # Save updated history
        st.session_state.chat_history = updated_history


if __name__ == "__main__":
    interface()

