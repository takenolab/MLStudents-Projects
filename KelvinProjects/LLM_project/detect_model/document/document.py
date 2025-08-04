# from PyPDF2 import PdfReader
# from langchain_core.documents import Document
# from langchain_core.vectorstores import InMemoryVectorStore
# from embeddings.embeddings import embedding

# pdf=PdfReader('maize disease control.pdf')
# document_base=[
#     Document(page_content=page.extract_text())
#     for page in pdf.pages
#     if page.extract_text()
# ]
# embedding_vector_store=InMemoryVectorStore(embedding)
# vector=embedding_vector_store.add_documents(document_base)


