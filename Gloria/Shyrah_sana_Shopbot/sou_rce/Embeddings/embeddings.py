import os
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings

# === Load Environment Variables ===
load_dotenv()
API_KEY = os.getenv("BIGMODEL_API_KEY")
BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
EMBEDDING_MODEL = "embedding-3"

# === Directory Config ===
DOCUMENTS_DIR = "embeddings/raw_documents"
INDEX_DIR = "embeddings/faiss_indexes"

# === Embedding Engine ===
def get_embeddings():
    return OpenAIEmbeddings(
        api_key=API_KEY,
        model=EMBEDDING_MODEL,
        base_url=BASE_URL
    )

# === Build FAISS Index ===
def build_vector_index(category: str) -> str:
    """
    Loads documents from a category (e.g. 'Smart_Item_locator'),
    creates a FAISS index and saves it locally.
    """
    file_path = os.path.join(DOCUMENTS_DIR, f"{category}.txt")
    if not os.path.exists(file_path):
        return f"❌ Document file not found: {file_path}"

    print(f"\n📄 Loading documents for category: {category}")
    loader = TextLoader(file_path)
    docs = loader.load()

    print(f"🔁 Generating embeddings for {len(docs)} documents...")
    embeddings = get_embeddings()

    print(f"📦 Building FAISS index for '{category}'...")
    db = FAISS.from_documents(docs, embeddings)

    save_path = os.path.join(INDEX_DIR, category)
    db.save_local(save_path)
    return f"✅ Saved FAISS index to: {save_path}"

# === CLI Entry Point ===
if __name__ == "__main__":
    print("🧠 Embedding Builder — Generating FAISS Indexes")
    categories = ["snacks", "soap", "electronics"]  # Add more as needed

    for cat in categories:
        result = build_vector_index(cat)
        print(result)