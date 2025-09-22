import pathlib 
import json 
import json


import json
import pathlib

file_path = pathlib.Path(__file__).resolve().parents[2] / "api" / "data" / "server" /"employees.json"

def staff():
    if not file_path.exists() or file_path.stat().st_size == 0:
        return "No employee data found."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data:
            return "Employee list is empty."

        formatted = "\n\n".join(
            f"""
            -------------------------------
            Department: {entry['employee_department']}
            Employee ID: {entry['employee_id']}
            Name: {entry['employee_name']}
            Title: {entry['employee_title']}
            Email: {entry['employee_email']}
            Gender: {entry['employee_gender']}
            -------------------------------
            """ for entry in data
        )

        return formatted

    except (json.JSONDecodeError, KeyError) as e:
        return f"Error loading employee data: {e}"


 