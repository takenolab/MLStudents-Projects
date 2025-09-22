from langchain_openai import OpenAIEmbeddings 
import pathlib 
import dotenv
import os

env = pathlib.Path(__file__).resolve().parents[1] / "utilities" / "secret" / ".env"
dotenv.load_dotenv(dotenv_path=env)
 
def embedding_model() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=os.getenv("EMBEDDING"),
        api_key=os.getenv("APIKEY"),
        skip_empty=True,
        base_url=os.getenv("URL")
        )
    