from langchain_openai import ChatOpenAI 
import pathlib 
import dotenv
import os

env = pathlib.Path(__file__).resolve().parents[2] / "utilities" / "secret" / ".env"
dotenv.load_dotenv(dotenv_path=env)
 
llm_model = ChatOpenAI(
        model=os.getenv("MODEL"),
        temperature=0,
        
        api_key=os.getenv("APIKEY"),
        base_url=os.getenv("URL"),
        
        )

   