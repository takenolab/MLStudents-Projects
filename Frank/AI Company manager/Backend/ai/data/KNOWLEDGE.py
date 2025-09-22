import pathlib 
import os 


TXT_KNOWLEDGE_FILE = pathlib.Path(__file__).resolve().parent / "document" / "Goblin_Company_Profile.txt"

def db() ->str:
    if not os.path.exists(str(TXT_KNOWLEDGE_FILE)):
        return "No background knowledge available."
    with open(str(TXT_KNOWLEDGE_FILE), "r", encoding="utf-8") as f:
        return str(f.read())
 