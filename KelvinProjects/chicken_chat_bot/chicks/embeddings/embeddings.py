# from langchain_openai import OpenAIEmbeddings
# embeddings=OpenAIEmbeddings(
#     model="embedding-3",
  
#     # api_key="dadc4e4304cd4c169424134357a0a8db.C29f5GShQyrOQdVl",
#     # api_key="39d21d2a55504df58423d1e4f218ec94.OTy73GoacNLqHGuS",
#     # api_key=("e0c7cd5ec96c44b8a88873efda1b61ac.fyJdvSoyTAHFNLkM"),
#     api_key="5dd8688cd8b04521ad49546bf0ef37fb.WxHGfeb5a9Iy1mv8",
#     base_url="https://open.bigmodel.cn/api/paas/v4"
# )

from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
