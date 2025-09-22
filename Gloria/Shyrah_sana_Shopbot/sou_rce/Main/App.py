import face_recognition
import cv2

# Load a reference image of a registered user
known_image = face_recognition.load_image_file("known_faces/user123.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]
known_faces = [known_encoding]
known_names = ["Alice"]

def identify_face(frame):
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    for encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_faces, encoding, tolerance=0.5)
        if matches[0]:
            return known_names[0]
    return None


import os, json, cv2, face_recognition
import streamlit as st
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import folium

# Constants
STORE = "sana"
Crowd_THRESHOLD = 10      # Customize sensor threshold
KNOWN_FACE_DIR = "known_faces"

# Load known face encodings
known_faces, known_names = [], []
for fname in os.listdir(KNOWN_FACE_DIR):
    img = face_recognition.load_image_file(os.path.join(KNOWN_FACE_DIR, fname))
    enc = face_recognition.face_encodings(img)
    if enc:
        known_faces.append(enc[0])
        known_names.append(os.path.splitext(fname)[0])

def recognize_user():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    name = identify_face(frame)
    return name or "Unknown"

def is_crowded():
    # Hook to actual sensors in real deployment:
    return True  # Simulated as always busy for demo

# LangChain tool stays mostly the same; focus only on in-store mode.

# Streamlit interface
st.set_page_config(layout="wide", page_title="SANA ShopBot (Malawi)")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = ChatOpenAI(model="glm-4.5V", temperature=0, api_key="your_key", max_tokens=1000)

tools = [
    Tool(
        name="item_locator",
        func=smart_item_locator,
        description="Locates items in the shop",
        return_direct=True
    )
]
agent = initialize_agent(tools, llm, AgentType.ZERO_SHOT_REACT_DESCRIPTION, memory=memory, verbose=True)

if is_crowded():
    st.warning("Store is currently crowded. I can help you purchase items directly. Please ensure you've consented to facial recognition.")

user = recognize_user()
if user != "Unknown":
    st.success(f"Hello, {user}! You're recognized.")
else:
    st.info("Welcome! For assistance, I’ll need your account details for payment.")

# Query input UI...

# Map rendering using folium and genuine JSON store layout:
def render_map():
    path = f"store_maps/{STORE}.json"
    if not os.path.exists(path): return st.error("Store map missing.")
    data = json.load(open(path))
    m = folium.Map(location=data["center"], zoom_start=18)
    for item, loc in data["locations"].items():
        folium.Marker(location=loc, popup=item).add_to(m)
    st.components.v1.html(m._repr_html_(), height=500)

if "### Show in-store map:" in agent_response:
    render_map()


import streamlit as st
import json
import os
import hashlib

STORE_FILE = "store_maps/sana.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Replace with secure loading from secrets or database
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("sana1234")  # store this securely

def check_login():
    st.title("🔐 SANA Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH:
            st.session_state["admin_logged_in"] = True
            st.success("✅ Logged in successfully.")
        else:
            st.error("❌ Invalid credentials.")

def admin_panel():
    st.title("🛠️ SANA Admin Panel")
    with open(STORE_FILE, "r") as f:
        store_data = json.load(f)

    item_keys = list(store_data["locations"].keys())
    selected_item = st.selectbox("Select Item to Manage", item_keys)

    # Existing values
    item_location = store_data["locations"].get(selected_item, "")
    item_price = store_data["prices"].get(selected_item, "")
    available = store_data["availability"].get(selected_item, True)

    st.subheader(f"Editing: **{selected_item.title()}**")
    new_location = st.text_input("Location", item_location)
    new_price = st.text_input("Price Range", item_price)
    is_available = st.checkbox("Available?", available)

    if st.button("💾 Save Changes"):
        store_data["locations"][selected_item] = new_location
        store_data["prices"][selected_item] = new_price
        store_data["availability"][selected_item] = is_available

        with open(STORE_FILE, "w") as f:
            json.dump(store_data, f, indent=2)
        st.success("✅ Changes saved!")

    st.markdown("---")
    st.subheader("➕ Add New Item")
    new_item = st.text_input("New Item Name")
    new_item_location = st.text_input("New Item Location")
    new_item_price = st.text_input("New Item Price")
    if st.button("Add Item"):
        if new_item:
            new_key = new_item.lower()
            store_data["locations"][new_key] = new_item_location
            store_data["prices"][new_key] = new_item_price
            store_data["availability"][new_key] = True
            with open(STORE_FILE, "w") as f:
                json.dump(store_data, f, indent=2)
            st.success(f"✅ Item '{new_item}' added.")
        else:
            st.error("Item name is required.")

# Main app logic
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

if not st.session_state["admin_logged_in"]:
    check_login()
else:
    admin_panel()
{
  "center": [-13.9634, 33.7741],
  "locations": {
    "soap": "Aisle 1 - Hygiene",
    "milk": "Fridge section near back wall"
  },
  "prices": {
    "soap": "K2,999.99 - K4,999.99",
    "milk": "K3,299.99 - K4,099.99"
  },
  "availability": {
    "soap": true,
    "milk": true
  }
}

def fetch_item_info(item_name: str, store_file="store_maps/sana.json"):
    with open(store_file, "r") as f:
        data = json.load(f)
    
    item = item_name.lower()
    location = data["locations"].get(item)
    price = data["prices"].get(item)
    available = data["availability"].get(item, False)

    if not available:
        return f"❌ Sorry, {item_name.title()} is currently unavailable in SANA."

    return {
        "location": location,
        "price": price,
        "available": available
    }
