import os , sys , pathlib , json


DATA_DIR =  pathlib.Path(__file__).resolve().parent /"server" /"conversation"
EMPLOYEE_FILE =pathlib.Path(__file__).resolve().parent  / "server" /"employees.json"


def load_conversation() -> list:
    os.makedirs(str(DATA_DIR), exist_ok=True)
    path =  os.path.join(str(DATA_DIR),"conversation.json")

    if not os.path.exists(path) or os.stat(path).st_size == 0:
        return " No conversation started yet."

    try:
        with open(file=path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except (json.JSONDecodeError, IOError):
        return " Failed to load conversation history."
    
    



def load_employee_name():
    try:
        path =  EMPLOYEE_FILE
        with open(path, "r", encoding="utf-8") as f:
            employees = json.load(f)
            return [e["employee_name"] for e in employees if "employee_name" in e]
    except Exception as e:
        print(f"Failed to load employees.json: {e}")
        return [] 


def load_employee_emails():
    try:
        path = EMPLOYEE_FILE
        with open(path, "r", encoding="utf-8") as f:
            employees = json.load(f)
            return [e["employee_email"] for e in employees if "employee_email" in e]
    except Exception as e:
        print(f"Failed to load employees.json: {e}")
        return [] 
    


def load_employee():
 
    if os.path.exists(EMPLOYEE_FILE):
        with open(EMPLOYEE_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_employees(data):
 
    with open(EMPLOYEE_FILE, "w") as file:
        json.dump(data, file, indent=4)

 