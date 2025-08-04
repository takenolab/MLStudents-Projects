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

@tool

def disease_analysis_tool(image_path:str)->str:
    """
    use the uploaded image path to predict the disease of maize"""

    try:
        image_path = image_path.strip().split("\n")[0].replace('"', '').replace("'", "")
        # image_path=image_path.strip().replace('"', '').split('\n')[0]
        model=tf.keras.models.load_model('maize_diseases.keras')
        img=tf.keras.utils.load_img(image_path,target_size=(128,128))
        img_array=tf.keras.utils.img_to_array(img)
        norm=img_array/255.0
        batch=np.expand_dims(norm,axis=0)
        prediction=model.predict(batch)
        class_names=os.listdir('data')
        output=np.argmax(prediction)
        final_=class_names[output]
        return final_
    except Exception as e:
        return (f'error occured {e}')


@tool
def get_treatment_advice_tool(disease_name:str) ->str:
    """
    use the {disease_name} from the prediction to search for treatment ways in the document base and give to the farmer"""
    
    # disease_name=disease_analysis_tool(image_path)
    pdf=PdfReader('maize disease control.pdf')
    document_base=[
    Document(page_content=page.extract_text())
    for page in pdf.pages
    if page.extract_text()
    ]
    # semantic_chanker_doc=SemanticChunker(embeddings,
    #             breakpoint_threshold_type='percentile',
    #             breakpoint_threshold_amount=95
    #             )
    # text_get=pdf[0].page_content
    # chunks=semantic_chanker_doc.split_text(text_get)
    # final_docs=[Document(page_content=chunk) for chunk in chunks]
    # # return final_docs

    embedding_vector_store=InMemoryVectorStore(embedding)
    vector=embedding_vector_store.add_documents(document_base)

    result=embedding_vector_store.similarity_search(disease_name,k=4)
    filtered = [
            doc.page_content for doc in result
            if disease_name.lower() in doc.page_content.lower()
        ]
    return filtered if filtered else [doc.page_content for doc in result]

    return [doc.page_content for doc in result]




