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
llm = ChatOpenAI(model="glm-4.5V", temperature=0, ...)

tools = [Tool(name="item_locator", func=smart_item_locator, ...)]
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