import os,json
import pathlib 
import os
from datetime import datetime

 
 
DATA_DIR =  pathlib.Path(__file__).resolve().parents[2] / "api" / "data" / "server" /"conversation"
TIME = datetime.now().strftime("%B • %d • %Y — %H:%M:%S")


def save_conversation(role: str, content: str):
  
    os.makedirs(str(DATA_DIR), exist_ok=True)
    path =  os.path.join(str(DATA_DIR),"conversation.json")
    
    data = []
    if os.path.exists(path):
        with open(file=path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            
    data.append(
        {
            "time": TIME, 
            "role": role,
            "content": content}
        )
    
    with open(
        file=path,
        mode="w",
        encoding="utf-8"
        ) as f:
        
        json.dump(data, f, indent=2)
        
import os
import json

def load_conversation() -> str:
    os.makedirs(str(DATA_DIR), exist_ok=True)
    path =  os.path.join(str(DATA_DIR),"conversation.json")

    if not os.path.exists(path) or os.stat(path).st_size == 0:
        return " No conversation started yet."

    try:
        with open(file=path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                formatted = []
                for entry in data:
                    role = entry.get("role", "unknown")
                    content = entry.get("content", "")
                    time = entry.get("time", "unknown time")

                    formatted.append(
                        f"{time}\n Role: {role}\n Message: {content}\n" + "-"*40
                    )
                return "\n".join(formatted)
            else:
                return " Invalid conversation format."
    except (json.JSONDecodeError, IOError):
        return " Failed to load conversation history."

