from langchain_core.tools import tool,Tool
import joblib
from pathlib import Path
import streamlit as st
import tensorflow as tf
import numpy as np
import os
import sys
# path = Path(__file__).resolve().parents[2]
# sys.path.append(str(path))
import sys
path = Path(__file__).resolve().parents[2]
sys.path.append(str(path))
from chicks.data.load_data import load_data
from langchain.vectorstores import FAISS
from chicks.embeddings.embeddings import embeddings
from chicks.model.model import model1
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chicken_age" not in st.session_state:
    st.session_state.chicken_age = None

if "num_chickens" not in st.session_state:
    st.session_state.num_chickens = None

if "last_disease" not in st.session_state:
    st.session_state.last_disease = None
 
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter




from typing import Union, Dict
import joblib
import streamlit as st
import re
import joblib
import streamlit as st
from typing import Union, Dict

from typing import Union, Dict
from langchain.tools import tool
import joblib
import re

@tool("feed_quantity_and_cost", return_direct=True)
@tool
def feed_quantity_and_cost(question: Union[str, Dict[str, Union[int, float]]]) -> str:
    """
    Predict weekly feed quantity for chickens based on age and number of chickens,
    and calculate the feed cost in MKW (Malawi Kwacha) no other currency except this one based on the quantity.

    Accepts:
    - A string with age and number of chickens (e.g. "I have 50 chicks that are 3 weeks old")
    - A dictionary with keys: "age", "num_chickens", or "kg" (for direct cost estimation)

    Returns:
    - Feed quantity in kg and cost in MKW
    - do not return the cost in any other currency except MKW
    """
    try:
        # Case 1: Dictionary input
        if isinstance(question, dict):
            if "kg" in question:
                # Direct cost estimation
                kg = float(question["kg"])
                cost_model = joblib.load("chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_cost_model.pkl")
                cost = cost_model.predict([[kg]])[0]
                return f"💰 Estimated feed cost for {kg:.2f} kg is **{cost:.2f} MKW**."

            age = int(question.get("age", 0))
            num_chickens = int(question.get("num_chickens", 0))

        # Case 2: String input
        elif isinstance(question, str):
            age_match = re.search(r"(\d+)\s*(?:week|weeks|wk|wks)", question.lower())
            chick_match = re.search(r"(\d+)\s*(?:chicks?|chickens?)", question.lower())
            kg_match = re.search(r"(\d+\.?\d*)\s*kg", question.lower())

            if kg_match:
                kg = float(kg_match.group(1))
                cost_model = joblib.load("chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_cost_model.pkl")
                cost = cost_model.predict([[kg]])[0]
                return f"💰 Estimated feed cost for {kg:.2f} kg is **{cost:.2f} MKW**."

            if age_match and chick_match:
                age = int(age_match.group(1))
                num_chickens = int(chick_match.group(1))
            else:
                return "❌ Couldn't find both age and number of chickens in your input."

        else:
            return "❌ Unsupported input type. Provide a string or dictionary."

        # Model paths for feed quantity prediction
        model_paths = {
            1: "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_1_week_quantity_model.pkl",
            2: "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_2_week_quantity_model.pkl",
            3: "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_3_week_quantity_model.pkl",
            4: "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_4_week_quantity_model.pkl",
            5: "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_5_week_quantity_model.pkl",
            6: "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_6_week_quantity_model.pkl",
        }

        if age not in model_paths:
            return f"⚠️ No model available for age {age} weeks."

        quantity_model = joblib.load(model_paths[age])
        predicted_kg = quantity_model.predict([[num_chickens]])[0]

        cost_model = joblib.load("chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_cost_model.pkl")
        cost = cost_model.predict([[predicted_kg]])[0]

        return (
            f"🐔 For {num_chickens} chickens aged {age} weeks:\n"
            f"📦 Weekly feed required: **{predicted_kg:.2f} kg**\n"
            f"📅 Daily feed: **{predicted_kg / 7:.2f} kg**\n"
            f"💰 Estimated weekly feed cost: **{cost:.2f} MKW**"
        )

    except Exception as e:
        return f"🚨 Unexpected error occurred: {str(e)}"


# @tool
# def feed_quantity_and_cost(question: Union[str, Dict[str, Union[int, float]]]) -> str:
#     """
#     Predict weekly feed quantity for chickens based on age and number of chickens,
#     and calculate the feed cost in MKW (Malawi Kwacha).
#     """
#     try:
#         # Case 1: Dictionary input
#         if isinstance(question, dict):
#             if "kg" in question:
#                 kg = float(question["kg"])
#                 cost_model = joblib.load(
#                     "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_cost_model.pkl"
#                 )
#                 cost = cost_model.predict([[kg]])[0]
#                 return f"Estimated feed cost for {kg:.2f} kg is **{cost:.2f} MKW**."

#             age = int(question.get("age", 0))
#             num_chickens = int(question.get("num_chickens", 0))

#         # Case 2: String input
#         elif isinstance(question, str):
#             age_match = re.search(r"(\d+)\s*(?:week|weeks|wk|wks)", question.lower())
#             chick_match = re.search(r"(\d+)\s*(?:chicks?|chickens?)", question.lower())
#             kg_match = re.search(r"(\d+\.?\d*)\s*kg", question.lower())

#             if kg_match:
#                 kg = float(kg_match.group(1))
#                 cost_model = joblib.load(
#                     "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_cost_model.pkl"
#                 )
#                 cost = cost_model.predict([[kg]])[0]
#                 return f"Estimated feed cost for {kg:.2f} kg is **{cost:.2f} MKW**."

#             if age_match and chick_match:
#                 age = int(age_match.group(1))
#                 num_chickens = int(chick_match.group(1))
#             else:
#                 return "Couldn't find both age and number of chickens in your input."

#         else:
#             return "Unsupported input type. Provide a string or dictionary."

#         # Load correct age model
#         model_paths = {
#             1: "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_1_week_quantity_model.pkl",
#             2: "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_2_week_quantity_model.pkl",
#             3: "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_3_week_quantity_model.pkl",
#             4: "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_4_week_quantity_model.pkl",
#             5: "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_5_week_quantity_model.pkl",
#             6: "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_6_week_quantity_model.pkl",
#         }

#         if age not in model_paths:
#             return f"No model available for age {age} weeks."

#         quantity_model = joblib.load(model_paths[age])
#         predicted_kg = quantity_model.predict([[num_chickens]])[0]

#         cost_model = joblib.load(
#             "chicks/tools/saved_models_for_chicks_feed_quantity_Pre/feed_cost_model.pkl"
#         )
#         cost = cost_model.predict([[predicted_kg]])[0]

#         return (
#             f"For {num_chickens} chickens aged {age} weeks:\n"
#             f" Weekly feed required: **{predicted_kg:.2f} kg**\n"
#             f" Daily feed: **{predicted_kg / 7:.2f} kg**\n"
#             f" Estimated weekly feed cost: **{cost:.2f} MKW**"
#         ).strip()

#     except Exception as e:
#         return f"Unexpected error occurred: {str(e)}"


# ✅ Register tool cleanly
feed_quantity_tool = Tool.from_function(
    func=feed_quantity_and_cost,
    name="feed_quantity_and_cost",
    description="Predict feed quantity and cost for chickens. Input can be a string question like 'I have 5000 chicks that are 3 weeks old'.",
    return_direct=True
)





        
        

@tool
def disease_prediction(image_path: str) -> str:
    """
    
    use the image path provided by the  user to pridict the disease name, 
    your work is to predict the disease and return the disease name"""
    try:
        model = tf.keras.models.load_model("./chicks/tools/maize_disease3.keras", compile=False)
        img = tf.keras.utils.load_img(image_path, target_size=(250, 250))
        img_array = tf.keras.utils.img_to_array(img) / 255.0
        image_ = np.expand_dims(img_array, axis=0)

        predictions = model.predict(image_)
        predicted_class = np.argmax(predictions)
        class_name = ["newcastle", "healthy", "concidiosis", "salmonella"]
        disease = class_name[predicted_class]

        # Save into memory
        st.session_state.last_disease = disease

        return (
            f" [TOOL:disease_prediction] The chicken shows signs of **{disease}**.\n\n"
            f" Would you like treatment and prevention guidance for {disease}?"
        )
    except Exception as e:
        return f"An error occurred: {e}"

def disease_prediction_wrapper(image_path: str) -> str:
    return disease_prediction(image_path)

wrapped_diseases_tool = Tool.from_function(
    func=disease_prediction_wrapper,
    name="disease_prediction",
    description="Predicts chicken disease from an image path"
)


def load_and_chunk_pdfs(path: str):
    loader = PyPDFLoader(path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_documents(documents)

def build_vectorstore(pdf_path: str, index_path: str):
    """Create FAISS index with batching and save locally (run once)."""
    docs = load_and_chunk_pdfs(pdf_path)
    texts = [d.page_content for d in docs]
    metadatas = [d.metadata for d in docs]

    # Batch embeddings (≤64 items per API call)
    batch_size = 64
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = embeddings.embed_documents(batch)
        all_embeddings.extend(batch_embeddings)

    vectorstore = FAISS.from_embeddings(
        list(zip(texts, all_embeddings)),
        embedding=embeddings,
        metadatas=metadatas
    )
    vectorstore.save_local(index_path)
    print(f"✅ FAISS index saved at: {index_path}")

# Run this once to build and save
build_vectorstore(
    "chicks/data/Poultry-AgriBusiness-Course-Training-Manual-for-trainers_MW_EN_09.2023.pdf",
    "faiss_index"
)
def get_vectorstore(index_path: str):
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

@tool
def chicken_farming_guide(question: str = None) -> str:
    """
    Provide general farming guidance in Malawi, ONLY using the Malawi poultry training manual.
    If answer not found, use your own general knowledge this must happens when the manual failed
    summerise and reason before answering the user's question."
    """
    if not question:
        return "Please provide a farming question."

    db = get_vectorstore("faiss_index")
    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 3})

    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
    You are a poultry expert for Malawi farmers. Use ONLY the context below (from the official Malawi poultry training manual) and
    If the answer is not in the context, use your own general knowledge this must happens when the manual failed,never tell the farmer your source of informatio.

    Context:
    {context}

    Farmer's question: {question}
    Answer (in simple farmer language):
    """
    return model1.predict(prompt)

def chicken_guide_wrapper(question: str) -> str:
    return chicken_farming_guide(question)

wrapped_chicken_guide_tool = Tool.from_function(
    func=chicken_guide_wrapper,
    name="chicken_farming_guide",
    description="Provide general farming guidance to a farmer in Malawi for example how to raise chickens, disease management and etc.",
    return_direct=True 
)




@tool("conversation_clarifier", return_direct=True)
def conversation_clarifier(question: str) -> str:
    """
    Helps maintain smooth conversation flow when farmer gives short replies,
    disagreements, or asks for clarification or when he is giving his thoughts.
    Uses last topic from chat history to generate a clarifying question.
    """
    # Very simple rule-based flow (you can extend with LLM later if needed)
    question= question.strip().lower()
    
    if question in ["not sure", "maybe", "i don't think so"]:
        return ("I hear you are not certain. "
                "About our last topic, are you more concerned about feed cost, disease, "
                "or egg production?")
    elif "more" in question:
        return "Would you like me to explain more about feed, housing, or disease management?"
    elif "mortality" in question:
        return "I understand. Do you want me to explain common causes of mortality or how to prevent it?"
    else:
        return "Could you please clarify which part you want me to expand on — feed, housing, disease, or market?"

def wrapped_conversation_clarifier(question: str) -> str:
    return conversation_clarifier(question)
wrapped_conversation_clarifier_tool = Tool.from_function(
    func=wrapped_conversation_clarifier,
    name="conversation_clarifier",
    description="Use this tool to clarify farmer's short or ambiguous replies and keep the conversation flowing smoothly or when he is giving his thoughts"
)



import re
import streamlit as st
from typing import Union, Dict


from typing import Union, Dict
import re
from langchain.tools import tool


def build_feed_info_index(pdf_path: str, index_path: str):
    if os.path.exists(index_path):
        print(f"✅ Feed info index already exists: {index_path}")
        return

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
    vectorstore.save_local(index_path)
    print(f"⚡ Feed info FAISS index saved at: {index_path}")

# Run once
build_feed_info_index("chicks/data/Chicken_Nutrient_Requirements.pdf", "feed_info_index")
build_feed_info_index("chicks/data/chicken_feed_by_age.pdf", "feed_types_index")

def get_feed_info_index(index_path: str):
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

@tool
# ("chicken_feed_info", return_direct=True)
def chicken_feed_info(question: str):
    """
    Provide feed type or nutrient requirements for chickens using prebuilt FAISS.
    """
    # Determine PDF type
    if "feed type" in question.lower():
        db = get_feed_info_index("feed_types_index")
    else:
        db = get_feed_info_index("feed_info_index")

    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"Summarize feed info in simple bullet points:\n{context}"
    return model1.predict(prompt)

def feed_type_wrapper(question: str) -> str:
    return chicken_feed_info.invoke(question)
wrapped_feed_type_tool = Tool.from_function(
    func=feed_type_wrapper,
    name="chicken_feed_info",
    description="Provides feed type based on the user's question and feed nutrient requirements",
    return_direct=True )


build_vectorstore("chicks/data/chicken_support_centers_districts_with_contacts (1).pdf","support_centers_index")

def get_support_centers_index():
    return FAISS.load_local("support_centers_index", embeddings, allow_dangerous_deserialization=True)

@tool
def chicken_support_centers(question: str) -> str:
    """
    Help the farmer find physical locations, offices, or contacts 
    where they can get chicken farming support in Malawi.
    """
    
    db = get_support_centers_index()
    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 5})
    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"Extract and summarize the most relevant chicken support centers info:\n{context}"
    return model1.predict(prompt)



def chicken_support_centers_wrapper(question: str) -> str:
    return chicken_support_centers(question)
wrapped_chicken_support_centers_tool = Tool.from_function(
    func=chicken_support_centers_wrapper,
    name="chicken_support_centers",
    description="Give farmer contact information and locations where they can get **physical help** about chicken farming ",
    return_direct=True )



build_vectorstore("chicks/data/Farmers_Guide_Proto_CentralPoultry.pdf",
                  "chicks_booking_index")

def get_chicks_booking_index():
    return FAISS.load_local("chicks_booking_index", embeddings, allow_dangerous_deserialization=True)

@tool
def chicks_booking_malawi_and_feed_provider(question: str) -> str:
    """
    Help a farmer with information where he can book chicks and buy nutritious feed
    near his location in Malawi using the Farmers_Guide_Proto_CentralPoultry.pdf.
    Only return results from 'proto' or 'central_poultry'.
    """

    db = get_chicks_booking_index()
    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 5})
    docs = retriever.get_relevant_documents(question)
    
    # Filter only Proto or Central Poultry entries
    filtered = [d.page_content for d in docs if "proto" in d.page_content.lower() or "central" in d.page_content.lower()]
    context = "\n\n".join(filtered)

    prompt = f"Provide booking and feed provider info in Malawi:\n{context}"
    return model1.predict(prompt)

def chicks_booking_malawi_and_feed_provider_wrapper(question: str) -> str:
    return chicks_booking_malawi_and_feed_provider(question)

wrapped_chicks_booking_malawi_and_feed_provider_tool = Tool.from_function(
    func=chicks_booking_malawi_and_feed_provider_wrapper,
    name="chicks_booking_malawi_and_feed_provider",
    description="Help the farmer find where to book chicks and buy feed in Malawi",
    return_direct=True 
)




@tool("chicken_farming_advisor", return_direct=True)
def chicken_farming_advisor(input_str: str) -> str:
    """
    Help a farmer decide which type of chicken to farm.
    - If cost inputs are provided, calculate profitability and recommend best option.
    - If cost inputs are missing, just give advice from PDF.
    """
    try:
        # Parse question and optional parameters
        parts = dict(item.strip().split("=", 1) for item in input_str.split(",") if "=" in item)
        question = parts.get("question", input_str)  # fallback to raw input
        num_chickens = parts.get("num_chickens")  # optional

        # ----------- (1) PDF qualitative advice ----------
        pdf = load_data("chicks/data/factors_to_consider_chickens.pdf")
        embed = embeddings.embed_query(question)
        embeddings_vectore = FAISS.from_documents(pdf, embeddings)
        pdf_result = embeddings_vectore.max_marginal_relevance_search(embed, k=3)
        pdf_advice = "\n".join([d.page_content for d in pdf_result])

        # ----------- (2) Profitability Calculation ----------
        cost_keys = [
            "broiler_chick_price", "broiler_feed_price_per_bag", "broiler_feed_bags", "broiler_vaccine_cost",
            "broiler_selling_price", "layer_chick_price", "layer_feed_price_per_bag", "layer_feed_bags",
            "layer_vaccine_cost", "egg_price", "eggs_per_day", "laying_days",
            "local_chick_price", "local_feed_price_per_bag", "local_feed_bags", "local_vaccine_cost",
            "local_selling_price", "mikolongwe_chick_price", "mikolongwe_feed_price_per_bag",
            "mikolongwe_feed_bags", "mikolongwe_vaccine_cost", "mikolongwe_selling_price"
        ]

        can_calculate = all(k in parts for k in cost_keys) and num_chickens is not None

        if can_calculate:
            num_chickens = int(num_chickens)
            results = {}

            # Broilers
            broiler_cost = (num_chickens * float(parts["broiler_chick_price"]) +
                            int(parts["broiler_feed_bags"]) * float(parts["broiler_feed_price_per_bag"]) +
                            num_chickens * float(parts["broiler_vaccine_cost"]))
            broiler_revenue = num_chickens * float(parts["broiler_selling_price"])
            broiler_profit = broiler_revenue - broiler_cost
            results["Broiler"] = (broiler_profit / broiler_cost * 100) if broiler_cost > 0 else 0

            # Layers
            layer_cost = (num_chickens * float(parts["layer_chick_price"]) +
                          int(parts["layer_feed_bags"]) * float(parts["layer_feed_price_per_bag"]) +
                          num_chickens * float(parts["layer_vaccine_cost"]))
            layer_revenue = int(parts["eggs_per_day"]) * int(parts["laying_days"]) * float(parts["egg_price"])
            layer_profit = layer_revenue - layer_cost
            results["Layer"] = (layer_profit / layer_cost * 100) if layer_cost > 0 else 0

            # Local
            local_cost = (num_chickens * float(parts["local_chick_price"]) +
                          int(parts["local_feed_bags"]) * float(parts["local_feed_price_per_bag"]) +
                          num_chickens * float(parts["local_vaccine_cost"]))
            local_revenue = num_chickens * float(parts["local_selling_price"])
            local_profit = local_revenue - local_cost
            results["Local"] = (local_profit / local_cost * 100) if local_cost > 0 else 0

            # Mikolongwe
            mik_cost = (num_chickens * float(parts["mikolongwe_chick_price"]) +
                        int(parts["mikolongwe_feed_bags"]) * float(parts["mikolongwe_feed_price_per_bag"]) +
                        num_chickens * float(parts["mikolongwe_vaccine_cost"]))
            mik_revenue = num_chickens * float(parts["mikolongwe_selling_price"])
            mik_profit = mik_revenue - mik_cost
            results["Mikolongwe"] = (mik_profit / mik_cost * 100) if mik_cost > 0 else 0

            best = max(results, key=results.get)

            profitability_msg = f"""
💰 Profitability Results:
- Broilers: {results['Broiler']:.2f}%
- Layers: {results['Layer']:.2f}%
- Local Chickens: {results['Local']:.2f}%
- Mikolongwe: {results['Mikolongwe']:.2f}%
✅ Recommendation based on profitability: **{best} farming**
"""
        else:
            profitability_msg = "\n💡 Profitability could not be calculated due to missing cost inputs. " \
                                "Based on the factors, please consider the advice above to choose a suitable chicken type."

        # ----------- (4) Final Response ----------
        return f"""
🐔 Chicken Farming Advisor
============================

📖 Advice from Factors (PDF):
{pdf_advice}

{profitability_msg}
""".strip()

    except Exception as e:
        return f"⚠️ Error in chicken_farming_advisor: {str(e)}"
    
def chicken_choosing_factors_wrapper(question: str) -> str:
    return chicken_farming_advisor(question)

chicken_choosing_factors_wrapper_tool = Tool.from_function(
    func=chicken_choosing_factors_wrapper,
    name="chicken_farming_advisor",
    description="Use this to help the farmer decide which type of chicken to raise based on cost and farming factors."
)