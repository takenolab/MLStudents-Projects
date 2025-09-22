# app.py
import time
import streamlit as st
from dotenv import load_dotenv
import os
import json
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# LangChain / search
from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatZhipuAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.tools import TavilySearchResults

# Initialize dotenv
load_dotenv()

# -------------------------
# Constants & paths
# -------------------------
IMG_SIZE = 128
EPOCHS = 10
BATCH_SIZE = 16

BASE_DIR = os.path.dirname(os.path.abspath(
    r"C:/Users/students/OneDrive/Desktop/maize detection 2/maize/maize disease"
))
MODEL_PATH = os.path.join(BASE_DIR, "maize_cnn_model.h5")
CLASS_INDICES_PATH = os.path.join(BASE_DIR, "class_indices.json")

# -------------------------
# API keys from .env
# -------------------------
openai_api_key = os.getenv("OPENAI_API_KEY")
zhipu_api_key = os.getenv("ZHIPUAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Check keys and warn user (no hallucination: we only report presence)
if not (openai_api_key or zhipu_api_key):
    st.warning("No LLM API key found in environment. Add OPENAI_API_KEY or ZHIPUAI_API_KEY to .env.")
if not tavily_api_key:
    st.warning("No Tavily API key found. Add TAVILY_API_KEY to .env to enable web search.")

# Initialize Tavily search tool (if key present), increase k=5 for better results
tavily = None
if tavily_api_key:
    try:
        tavily = TavilySearchResults(k=5, tavily_api_key=tavily_api_key)  # increased from 3 to 5
    except Exception as e:
        tavily = None
        st.error(f"Tavily init error: {e}")

# -------------------------
# LangChain chat factory
# -------------------------
def get_langchain_chat(model_choice="OPENAI"):
    """Return a ConversationChain with memory using the chosen LLM."""
    if model_choice == "OPENAI":
        if not openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not found in environment.")
        llm = ChatOpenAI(
            temperature=0.2,
            model_name="gpt-4o-mini",
            openai_api_key=openai_api_key
        )
    else:
        if not zhipu_api_key:
            raise RuntimeError("ZHIPUAI_API_KEY not found in environment.")
        llm = ChatZhipuAI(
            temperature=0.2,
            model="glm-4",
            api_key=zhipu_api_key
        )
    memory = ConversationBufferMemory()
    return ConversationChain(llm=llm, memory=memory)

# -------------------------
# Topic autodetection using LLM
# -------------------------
def detect_topic_with_llm(question, chat):
    topic_prompt = f"""
Classify the following question into exactly one of these:
maize - if it's about maize, agriculture, farming, or crop diseases
other - if it's about anything else
Do not explain. Just return one word: maize or other.

Question: {question}
"""
    try:
        classification = chat.run(topic_prompt).strip().lower()
        if classification == "maize":
            return "maize"
    except Exception:
        pass
    return "other"

# -------------------------
# Web-first responder with strict prompt
# -------------------------
def get_chat_response_with_web(chat, query, retries=3, delay=4):
    """
    Always search the web (Tavily) first, then call the LLM with the search results.
    Returns the model response string or None on failure.
    """
    if chat is None:
        return None

    search_results = ""
    if tavily is not None:
        try:
            search_results = tavily.run(query)
        except Exception as e:
            search_results = f"(Web search unavailable: {e})"
    else:
        search_results = "(Web search disabled: no Tavily key or initialization failed.)"

    # Strict prompt instructing to ONLY use the search results, no hallucination
    context_prompt = (
        "your name is ziley time. You are an AI assistant. Use ONLY the information contained in the following web search results to answer the user's question.\n"
        "If the search results do not contain an answer, respond that you could not find authoritative information rather than guessing or fabricating.\n\n"
        f"Search Results:\n{search_results}\n\n"
        f"Question:\n{query}\n\n"
        "Answer concisely based ONLY on the search results:"
    )

    for attempt in range(retries):
        try:
            return chat.run(context_prompt)
        except Exception as e:
            error_message = str(e).lower()
            if "insufficient_quota" in error_message:
                st.error("You have exceeded your API quota.")
                break
            elif "rate limit" in error_message or "rate_limit_exceeded" in error_message:
                st.warning(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                st.error(f"Unexpected error from LLM: {e}")
                break
    return None

# -------------------------
# Model training & loading
# -------------------------
def train_model():
    st.info("Training CNN model...")
    train_gen = ImageDataGenerator(rescale=1.0 / 255).flow_from_directory(
        BASE_DIR, target_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH_SIZE, class_mode="categorical"
    )
    val_gen = ImageDataGenerator(rescale=1.0 / 255).flow_from_directory(
        BASE_DIR, target_size=(IMG_SIZE, IMG_SIZE), batch_size=BATCH_SIZE, class_mode="categorical"
    )

    num_classes = len(train_gen.class_indices)

    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(num_classes, activation="softmax"),
    ])

    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit(train_gen, epochs=EPOCHS, validation_data=val_gen)

    model.save(MODEL_PATH)
    with open(CLASS_INDICES_PATH, "w") as f:
        json.dump(train_gen.class_indices, f)

    return model, train_gen.class_indices

def load_or_train_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(CLASS_INDICES_PATH):
        model = load_model(MODEL_PATH)
        with open(CLASS_INDICES_PATH, "r") as f:
            class_indices = json.load(f)
        return model, class_indices
    else:
        return train_model()

# -------------------------
# UI template
# -------------------------
template = """
<style>
h1, h2, label, .stRadio > label {
    text-align: center !important;
    width: 100%;
    display: block;
    color: maroon;
    font-weight: 700;
}
div[data-testid="stTextInput"] > div > input {
    width: 100% !important;
    max-width: 100% !important;
    border: 2px solid maroon !important;
    color: maroon !important;
    font-weight: 600;
    font-size: 18px;
}
.stButton > button {
    background-color: maroon;
    color: white;
}
</style>
"""

# -------------------------
# Main app
# -------------------------
def main():
    st.set_page_config(page_title="Ziley TimeHUB", layout="wide")

    st.markdown(template, unsafe_allow_html=True)
    st.markdown("<h1> 👨‍💻👨‍💻👨‍💻 Ziley TimeHUB👨‍💻👨‍💻👨‍💻 </h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px; text-align:center;'>Your reliable assistant than ever...!</p>", unsafe_allow_html=True)
    st.markdown("---")

    try:
        model, class_indices = load_or_train_model()
    except Exception as e:
        st.error(f"Model load/train error: {e}")
        model, class_indices = None, {}

    model_choice_input = st.radio("CHOOSE THE LANGUAGE MODEL:", ["OpenAI GPT", "ZhipuAI"], index=0, horizontal=True)
    model_choice = "OPENAI" if "OpenAI" in model_choice_input else "ZHIPUAI"

    if "chat" not in st.session_state or st.session_state.get("model_choice") != model_choice:
        try:
            st.session_state["chat"] = get_langchain_chat(model_choice)
            st.session_state["model_choice"] = model_choice
        except RuntimeError as re:
            st.error(str(re))
            st.stop()

    chat = st.session_state["chat"]

    user_question = st.text_input(
        "Ask me anything else for assistance...",
        placeholder="Type your question here...",
        max_chars=300000
    )

    if user_question and user_question.strip():
        topic = detect_topic_with_llm(user_question, chat)

        if topic == "maize":
            context = "Context: This is about maize crops. Last detected disease: unknown.\n"
        else:
            context = ""

        full_query = context + user_question.strip()

        answer = get_chat_response_with_web(chat, full_query)

        if not answer or len(answer.strip()) < 20 or "could not find" in answer.lower():
            st.warning("Sorry, i din't get the corrrect info for your requirement.")
        else:
            simple_answer = answer.strip()
            max_length = 300000
            if len(simple_answer) > max_length:
                simple_answer = simple_answer[:max_length - 3].rsplit(" ", 1)[0] + "..."
            st.write(simple_answer)

if __name__ == "__main__":
    main()




