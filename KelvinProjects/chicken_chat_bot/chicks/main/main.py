from pathlib import Path
import sys
path = Path(__file__).resolve().parents[2]
sys.path.append(str(path))
from chicks.model.model import model1
from langchain.agents.agent_types import AgentType
from chicks.prompt.prompts import templates
import tempfile
from chicks.tools.tools import feed_quantity_tool, wrapped_feed_type_tool,wrapped_diseases_tool,wrapped_chicken_guide_tool,wrapped_chicken_support_centers_tool,chicken_choosing_factors_wrapper_tool,wrapped_chicks_booking_malawi_and_feed_provider_tool,wrapped_conversation_clarifier_tool
tools=[feed_quantity_tool,wrapped_feed_type_tool,wrapped_diseases_tool,wrapped_chicken_guide_tool,wrapped_chicken_support_centers_tool,chicken_choosing_factors_wrapper_tool,wrapped_chicks_booking_malawi_and_feed_provider_tool,wrapped_conversation_clarifier_tool]
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.prompts import PromptTemplate
from langchain.prompts import PromptTemplate
import streamlit as st
import re
import base64
from datetime import datetime
from typing import Optional
from langchain.memory import ConversationSummaryMemory
from langchain.agents import create_react_agent, AgentExecutor
import sqlite3,hashlib

from typing import TypedDict, List, Optional
from langchain_core.messages import BaseMessage

from langchain.memory import ConversationSummaryBufferMemory
import streamlit as st
import sqlite3
import hashlib
import base64
from datetime import datetime
from typing import List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from langchain.schema import BaseMessage
# from langchain.agents import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner

# from langchain.agents import PlanAndExecute, load_chat_planner, load_agent_executor
from langchain.chains import LLMChain
# from langgraph.checkpoint import MemorySaver





import os

from langchain.schema import AgentFinish
from langgraph.checkpoint.memory import MemorySaver


import streamlit as st
import sqlite3, hashlib, base64
from datetime import datetime
from typing import List, Optional, TypedDict
from langchain.schema import BaseMessage, AgentFinish
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import AgentExecutor

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None


# -------------------------------
# LLM / AGENT SETUP
# -------------------------------
agent = create_react_agent(tools=tools, llm=model1, prompt=templates)
executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

class AgentState(TypedDict):
    messages: List[BaseMessage]
    image_path: Optional[str]

checkpointer = MemorySaver()

def agent_node(state: AgentState):
    user_message = state["messages"][-1]["content"]
    result = executor.invoke({
        "question": user_message,
        "chat_history": [m["content"] for m in state["messages"][:-1]],
        "image_path": state.get("image_path"),
        "agent_scratchpad": ""
    })
    if isinstance(result, AgentFinish):
        output = result.return_values.get("output", "")
    else:
        output = result.get("output", "")
    state["messages"].append({"role": "assistant", "content": output})
    return state

graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)
app = graph.compile(checkpointer=checkpointer)

# -------------------------------
# DATABASE SETUP
# -------------------------------
conn = sqlite3.connect('chat_history.db', check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS user_table (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)""")
c.execute("""CREATE TABLE IF NOT EXISTS chat_history (
    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    question TEXT,
    answer TEXT,
    timestamp DATETIME,
    FOREIGN KEY (user_id) REFERENCES user_table (user_id)
)""")
conn.commit()

# -------------------------------
# AUTH FUNCTIONS
# -------------------------------
def add_user_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username: str, password: str) -> str:
    try:
        c.execute(
            "INSERT INTO user_table (username, password) VALUES (?, ?)",
            (username, add_user_password(password))
        )
        conn.commit()
        return f"Username '{username}' registered successfully!"
    except sqlite3.IntegrityError:
        return f"Username '{username}' already exists. Please choose a different username."

def login_user(username: str, password: str) -> Optional[int]:
    c.execute("SELECT user_id, password FROM user_table WHERE username = ?", (username,))
    result = c.fetchone()
    if result:
        user_id, stored_password = result
        if stored_password == add_user_password(password):
            return user_id
    return None

def save_conversation(user_id: int, question: str, answer: str):
    timestamp = datetime.now()
    c.execute(
        "INSERT INTO chat_history (user_id, question, answer, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, question, answer, timestamp)
    )
    conn.commit()

def get_user_conversation(user_id: int):
    c.execute(
        "SELECT question, answer, timestamp FROM chat_history WHERE user_id = ? ORDER BY timestamp ASC",
        (user_id,)
    )
    return c.fetchall()


st.set_page_config(
    page_title="EQC Farms Chicken Assistant",
    page_icon="chicks/data/ChatGPT Image Sep 4, 2025, 01_46_49 PM.png",
    layout="wide"
)

def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .login-card {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0px 3px 10px rgba(0,0,0,0.2);
            max-width: 300px;
            width: 100%;
            text-align: center;
        }}
        /* Compact input fields */
        input[type="text"], input[type="password"] {{
            height: 35px;
            font-size: 14px;
            padding: 5px 10px;
        }}
        /* Login/Register buttons */
        div.stButton > button {{
            background-color: #1877f2;
            color: white;
            font-size: 14px;
            padding: 6px 16px;
            border-radius: 6px;
            border: none;
            cursor: pointer;
        }}
        div.stButton > button:hover {{
            background-color: #145dbf;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
# -------------------------------
# FRONT PAGE (Login/Register)
# -------------------------------
if st.session_state.user_id is None:
    set_background("chicks/data/backs.jpg")

    # App name at the top
    st.markdown(
        "<h1 style='text-align:center; color:#1877f2; margin-top:20px;'>🐥 EQC Farms Chicken Assistant</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:gray; font-size:16px;'>Login or register to continue</p>",
        unsafe_allow_html=True
    )

    # Login card in center
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    auth_choice = st.radio("Choose an option:", ["Login", "Register"], horizontal=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if auth_choice == "Register":
        if st.button("Register"):
            st.success(register_user(username, password))
    else:
        if st.button("Login"):
            user_id = login_user(username, password)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.username = username

                # Generate a unique session_id for this login
                st.session_state.session_id = f"user_{user_id}_{datetime.now().timestamp()}"

                # Reset in-memory history for this session
                st.session_state.chat_history = []

                # Load only this user's DB history
                past_chats = get_user_conversation(user_id)
                for q, a, t in past_chats:
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    st.session_state.chat_history.append({"role": "assistant", "content": a})

                st.success(f"✅ Welcome, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
            # if user_id:
            #     st.session_state.user_id = user_id
            #     st.session_state.username = username

            #     # Clear LangGraph memory each time user logs in
            #     st.session_state.chat_history = []

            #     # Reload history from DB
            #     past_chats = get_user_conversation(user_id)
            #     for q, a, t in past_chats:
            #         st.session_state.chat_history.append({"role": "user", "content": q})
            #         st.session_state.chat_history.append({"role": "assistant", "content": a})

            #     st.success(f"✅ Welcome, {username}!")
            #     st.rerun()
            # else:
            #     st.error("❌ Invalid username or password")

        

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


else:
    set_background("chicks/data/backgroundk.jpg")

    # Sidebar user info
    st.sidebar.markdown(f"👤 **{st.session_state.username}**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.chat_history = []
        st.session_state.session_id = None
        st.rerun()

    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("chicks/data/ChatGPT Image Sep 4, 2025, 01_46_49 PM.png", width=200)
        st.markdown(
            "<p style='text-align:center; color:gray; font-size:14px;'>"
            "💬 Your trusted guide for broilers, layers, and local chickens."
            "</p>",
            unsafe_allow_html=True
        )
    
    # Route & respond
    # def route_and_respond(user_input: str, image_path: Optional[str] = None):
    #     st.session_state.chat_history.append({"role": "user", "content": user_input})
        
    #     state = {
    #         "messages": st.session_state.chat_history.copy(),
    #         "image_path": image_path
    #     }

    #     # Always use transient session (not long-lived LangGraph memory)
    #     config = {
    #         "configurable": {
    #             "thread_id": f"user_{st.session_state.user_id or 'anonymous'}",
    #             "checkpoint_ns": None,   # disable shared checkpoint
    #             "checkpoint_id": None
    #         }
    #     }

    #     new_state = app.invoke(state, config=config)
    #     reply = new_state["messages"][-1]["content"]

    #     # Save only to DB
    #     save_conversation(st.session_state.user_id, user_input, reply)

    #     # Keep chat history alive in session state
    #     st.session_state.chat_history = new_state["messages"]
    #     return reply

def route_and_respond(user_input: str, image_path: Optional[str] = None):
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    state = {
        "messages": st.session_state.chat_history.copy(),
        "image_path": image_path
    }

    config = {
        "configurable": {
            "thread_id": st.session_state.session_id,   # unique per user
            "checkpoint_ns": "chat_memory",
            "checkpoint_id": st.session_state.session_id
        }
    }

    new_state = app.invoke(state, config=config)
    reply = new_state["messages"][-1]["content"]

    # Persist in DB (per user, safe for concurrency)
    save_conversation(st.session_state.user_id, user_input, reply)

    st.session_state.chat_history = new_state["messages"]
    return reply



user_input = st.chat_input("Type your question about chicken farming...")
if user_input:
    reply = route_and_respond(user_input)
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            role = msg.get("role", "assistant")
            content = msg.get("content", "")
            timestamp = datetime.now().strftime("%H:%M")
            with st.chat_message(role, avatar=("🧑" if role == "user" else "🤖")):
                st.markdown(
                    f"{content}<br/><small style='opacity:0.6;font-size:12px;'>{timestamp}</small>",
                    unsafe_allow_html=True
                )


# 




# -------------------------------
# SESSION STATE INIT
# -------------------------------
# if "user_id" not in st.session_state:
#     st.session_state.user_id = None
# if "username" not in st.session_state:
#     st.session_state.username = None
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "session_id" not in st.session_state:
#     st.session_state.session_id = None

# # -------------------------------
# # LLM / AGENT SETUP
# # -------------------------------
# agent = create_react_agent(tools=tools, llm=model1, prompt=templates)
# executor = AgentExecutor.from_agent_and_tools(
#     agent=agent,
#     tools=tools,
#     verbose=True,
#     handle_parsing_errors=True,
# )

# class AgentState(TypedDict):
#     messages: List[BaseMessage]
#     image_path: Optional[str]

# checkpointer = MemorySaver()

# def agent_node(state: AgentState):
#     user_message = state["messages"][-1]["content"]
#     result = executor.invoke({
#         "question": user_message,
#         "chat_history": [m["content"] for m in state["messages"][:-1]],
#         "image_path": state.get("image_path"),
#         "agent_scratchpad": ""
#     })
#     if isinstance(result, AgentFinish):
#         output = result.return_values.get("output", "")
#     else:
#         output = result.get("output", "")
#     state["messages"].append({"role": "assistant", "content": output})
#     return state

# graph = StateGraph(AgentState)
# graph.add_node("agent", agent_node)
# graph.set_entry_point("agent")
# graph.add_edge("agent", END)
# app = graph.compile(checkpointer=checkpointer)

# # -------------------------------
# # DATABASE SETUP
# # -------------------------------
# conn = sqlite3.connect('chat_history.db', check_same_thread=False)
# c = conn.cursor()
# c.execute("""CREATE TABLE IF NOT EXISTS user_table (
#     user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT UNIQUE,
#     password TEXT
# )""")
# c.execute("""CREATE TABLE IF NOT EXISTS chat_history (
#     chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER,
#     question TEXT,
#     answer TEXT,
#     timestamp DATETIME,
#     FOREIGN KEY (user_id) REFERENCES user_table (user_id)
# )""")
# conn.commit()

# # -------------------------------
# # AUTH FUNCTIONS
# # -------------------------------
# def add_user_password(password: str) -> str:
#     return hashlib.sha256(password.encode()).hexdigest()

# def register_user(username: str, password: str) -> str:
#     try:
#         c.execute(
#             "INSERT INTO user_table (username, password) VALUES (?, ?)",
#             (username, add_user_password(password))
#         )
#         conn.commit()
#         return f"Username '{username}' registered successfully!"
#     except sqlite3.IntegrityError:
#         return f"Username '{username}' already exists. Please choose a different username."

# def login_user(username: str, password: str) -> Optional[int]:
#     c.execute("SELECT user_id, password FROM user_table WHERE username = ?", (username,))
#     result = c.fetchone()
#     if result:
#         user_id, stored_password = result
#         if stored_password == add_user_password(password):
#             return user_id
#     return None

# def save_conversation(user_id: int, question: str, answer: str):
#     timestamp = datetime.now()
#     c.execute(
#         "INSERT INTO chat_history (user_id, question, answer, timestamp) VALUES (?, ?, ?, ?)",
#         (user_id, question, answer, timestamp)
#     )
#     conn.commit()

# def get_user_conversation(user_id: int):
#     c.execute(
#         "SELECT question, answer, timestamp FROM chat_history WHERE user_id = ? ORDER BY timestamp ASC",
#         (user_id,)
#     )
#     return c.fetchall()

# # -------------------------------
# # PAGE CONFIG
# # -------------------------------
# st.set_page_config(
#     page_title="EQC Farms Chicken Assistant",
#     page_icon="chicks/data/ChatGPT Image Sep 4, 2025, 01_46_49 PM.png",
#     layout="wide"
# )

# def set_background(image_file):
#     with open(image_file, "rb") as f:
#         data = f.read()
#     encoded = base64.b64encode(data).decode()
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: url("data:image/jpg;base64,{encoded}");
#             background-size: cover;
#             background-position: center;
#             background-attachment: fixed;
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             min-height: 100vh;
#         }}
#         .login-card {{
#             background-color: rgba(255, 255, 255, 0.9);
#             padding: 1rem;
#             border-radius: 10px;
#             box-shadow: 0px 3px 10px rgba(0,0,0,0.2);
#             max-width: 300px;
#             width: 100%;
#             text-align: center;
#         }}
#         input[type="text"], input[type="password"] {{
#             height: 35px;
#             font-size: 14px;
#             padding: 5px 10px;
#         }}
#         div.stButton > button {{
#             background-color: #1877f2;
#             color: white;
#             font-size: 14px;
#             padding: 6px 16px;
#             border-radius: 6px;
#             border: none;
#             cursor: pointer;
#         }}
#         div.stButton > button:hover {{
#             background-color: #145dbf;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # -------------------------------
# # FRONT PAGE (Login/Register)
# # -------------------------------
# if st.session_state.user_id is None:
#     set_background("chicks/data/backs.jpg")

#     st.markdown(
#         "<h1 style='text-align:center; color:#1877f2; margin-top:20px;'>🐥 EQC Farms Chicken Assistant</h1>",
#         unsafe_allow_html=True
#     )
#     st.markdown(
#         "<p style='text-align:center; color:gray; font-size:16px;'>Login or register to continue</p>",
#         unsafe_allow_html=True
#     )

#     st.markdown('<div class="login-card">', unsafe_allow_html=True)

#     auth_choice = st.radio("Choose an option:", ["Login", "Register"], horizontal=True)
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if auth_choice == "Register":
#         if st.button("Register"):
#             st.success(register_user(username, password))
#     else:
#         if st.button("Login"):
#             user_id = login_user(username, password)
#             if user_id:
#                 st.session_state.user_id = user_id
#                 st.session_state.username = username
#                 st.session_state.session_id = f"user_{user_id}_{datetime.now().timestamp()}"
#                 st.session_state.chat_history = []

#                 past_chats = get_user_conversation(user_id)
#                 for q, a, t in past_chats:
#                     st.session_state.chat_history.append({"role": "user", "content": q})
#                     st.session_state.chat_history.append({"role": "assistant", "content": a})

#                 st.success(f"✅ Welcome, {username}!")
#                 st.rerun()
#             else:
#                 st.error("❌ Invalid username or password")

#     st.markdown('</div>', unsafe_allow_html=True)
#     st.stop()

# else:
#     set_background("chicks/data/backgroundk.jpg")

#     # -------------------------------
#     # WELCOME POPUP (FIRST QUESTION)
#     # -------------------------------
#     if "welcome_shown" not in st.session_state:
#         st.session_state.welcome_shown = False

#     @st.dialog("Welcome")
#     def welcome_popup():
#         st.write(f"👋 Welcome, **{st.session_state.username}**!")
#         st.write("How can I help you today?")

#         first_question = st.text_input("Type your first question about chicken farming...")

#         if st.button("Ask"):
#             if first_question.strip():
#                 reply = route_and_respond(first_question)
#                 st.session_state.welcome_shown = True
#                 st.rerun()
#             else:
#                 st.warning("Please enter a question before continuing.")

#     if not st.session_state.welcome_shown:
#         welcome_popup()

#     # -------------------------------
#     # SIDEBAR
#     # -------------------------------
#     st.sidebar.markdown(f"👤 **{st.session_state.username}**")
#     if st.sidebar.button("🚪 Logout"):
#         st.session_state.user_id = None
#         st.session_state.username = None
#         st.session_state.chat_history = []
#         st.session_state.session_id = None
#         st.session_state.welcome_shown = False
#         st.rerun()

#     # Header
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.image("chicks/data/ChatGPT Image Sep 4, 2025, 01_46_49 PM.png", width=200)
#         st.markdown(
#             "<p style='text-align:center; color:gray; font-size:14px;'>"
#             "💬 Your trusted guide for broilers, layers, and local chickens."
#             "</p>",
#             unsafe_allow_html=True
#         )

# # -------------------------------
# # CHAT HANDLER
# # -------------------------------
# def route_and_respond(user_input: str, image_path: Optional[str] = None):
#     st.session_state.chat_history.append({"role": "user", "content": user_input})

#     state = {
#         "messages": st.session_state.chat_history.copy(),
#         "image_path": image_path
#     }

#     config = {
#         "configurable": {
#             "thread_id": st.session_state.session_id,
#             "checkpoint_ns": "chat_memory",
#             "checkpoint_id": st.session_state.session_id
#         }
#     }

#     new_state = app.invoke(state, config=config)
#     reply = new_state["messages"][-1]["content"]

#     save_conversation(st.session_state.user_id, user_input, reply)

#     st.session_state.chat_history = new_state["messages"]
#     return reply

# user_input = st.chat_input("Type your question about chicken farming...")
# if user_input:
#     reply = route_and_respond(user_input)
#     chat_container = st.container()
#     with chat_container:
#         for msg in st.session_state.chat_history:
#             role = msg.get("role", "assistant")
#             content = msg.get("content", "")
#             timestamp = datetime.now().strftime("%H:%M")
#             with st.chat_message(role, avatar=("🧑" if role == "user" else "🤖")):
#                 st.markdown(
#                     f"{content}<br/><small style='opacity:0.6;font-size:12px;'>{timestamp}</small>",
#                     unsafe_allow_html=True
#                 )
