# from document.document import document_base
import streamlit as st
import tensorflow as tf
import numpy as np
# from template.template import prompt_query
import json
from langchain.callbacks.tracers import ConsoleCallbackHandler
import os
import sys
import asyncio
llmode=os.path.dirname(os.path.abspath(__file__))
folder=os.path.dirname(llmode)
sys.path.append(folder)
from embeddings.embeddings import embedding
from model.model import model1
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from template.template import prompt_template
from langchain.agents import create_react_agent,AgentExecutor
from tools.tools import get_treatment_advice_tool,disease_analysis_tool
from langchain_core.tools import tool
from io import StringIO
from embeddings.embeddings import embedding
from embeddings.embeddings import embedding
from langchain_core.vectorstores import InMemoryVectorStore
import tensorflow as tf
import numpy as np
import os
from PyPDF2 import PdfReader
from langchain_core.documents import Document

from PyPDF2 import PdfReader
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from embeddings.embeddings import embedding

from PyPDF2 import PdfReader
from langchain_core.documents import Document




@tool
def disease_analysis_tool(image_path):
    """
    use the uploaded image path to predict the disease of maize"""
    try:
        image_path = image_path.strip().split("\n")[0].replace('"', '').replace("'", "")
        model = tf.keras.models.load_model('maize_diseases.keras')
        img = tf.keras.utils.load_img(image_path, target_size=(128, 128))
        img_array = tf.keras.utils.img_to_array(img)
        norm = img_array / 255.0
        batch = np.expand_dims(norm, axis=0)
        prediction = model.predict(batch)
        class_names = os.listdir('data')
        output = np.argmax(prediction)
        final_ = class_names[output]
        return final_
    except Exception as e:
        return f"Error occurred: {e}"
@tool    
def get_treatment_advice_tool(disease_name:str)->str:
    """
    use the {disease_name} from the prediction to search for treatment ways in the document base and give to the farmer"""
    disease_name = disease_name.strip()
    pdf=PdfReader('maize disease control.pdf')
    document_base=[
    Document(page_content=page.extract_text())
    for page in pdf.pages
    if page.extract_text()
    ]
    embedding_vector_store=InMemoryVectorStore(embedding)
    vector=embedding_vector_store.add_documents(document_base)

    result=embedding_vector_store.similarity_search(disease_name,k=4)

    filtered = [
            doc.page_content for doc in result
            if disease_name.lower() in doc.page_content.lower()
        ]

    return filtered if filtered else [doc.page_content for doc in result]

tools=[disease_analysis_tool,get_treatment_advice_tool]

st.title("🌱 Kelvin's Maize Disease Diagnosis Assistant")
uploaded_image = st.file_uploader("Upload maize leaf image", type=['jpg', 'png', 'jpeg'])
question = st.text_input("Ask your question about treatment advice:")


if uploaded_image and question:
    with open("temp_img.png", "wb") as f:
        f.write(uploaded_image.getbuffer())

    # disease = disease_analysis_tool("temp_img.png")
    # advice = get_treatment_advice_tool(disease)
    agent = create_react_agent(llm=model1, tools=tools, prompt=prompt_template)
    agent_executor = AgentExecutor(agent=agent,
                                    tools=tools,
                                    handle_parsing_errors=True,
                                    verbose=True,
                                    callbacks=[ConsoleCallbackHandler()]



                                    # max_iterations=50,
                                    # max_execution_time=120 
)
# handle_parsing_errors=True)
    # Call agent
    result =asyncio.run(agent_executor.ainvoke({
        "image_path": "temp_img.png",
        "question": question
    }))

    # st.subheader("🩺 Predicted Disease")
    # # st.write(f' the disease is {disease}')
    # st.success(disease)

    # st.subheader("💊 Treatment Advice")
    # # st.info(advice)
    # st.info("\n\n".join(advice))

    st.subheader("🧠 Agent Response")
    st.write(result['output'])
    # output = result['output']
    # if output.startswith("Final Answer:"):
    