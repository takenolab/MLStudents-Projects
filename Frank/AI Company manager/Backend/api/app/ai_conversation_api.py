from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sys, pathlib
import threading

sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
from ai.ai import ai

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from data.data import load_conversation, load_employee, save_employees

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

 
def handle_ai_request(user_text: str):
    try:
        error, response = ai(user_text=user_text.strip().lower())
        if error == False:
      
            socketio.emit("message_response", {"success": True, "response": response})
        else:
            socketio.emit("message_response", {"success": False, "response": "Model failure error occurred. Please try again later."})
    except Exception as e:
        socketio.emit("error", {"success": False, "error": str(e)})

@socketio.on("send_message")
def handle_send_message(data):
    try:
        if not data or "user_text" not in data:
            emit("error", {"error": "Missing 'user_text' in request."})
            return

        user_text = data["user_text"]
 
        socketio.start_background_task(handle_ai_request, user_text)

        updated_conversation = load_conversation()
        emit("conversation_update", {
            "success": True,
            "conversation": updated_conversation,
            "new_message": "Processing your request..."
        }, broadcast=True)

    except Exception as e:
        emit("error", {
            "success": False,
            "error": str(e)
        })
 
@socketio.on("post_new_employee")
def post_new_employee(data):
    import uuid
    try:
        required_fields = ["employee_name", "employee_department", "employee_role", "employee_email", "employee_gender"]
        if not data or not all(field in data for field in required_fields):
            emit("error", {"error": "Missing one or more required fields."})
            return

        employee_list = load_employee()

        # Check for existing employee by email
        if any(emp["employee_email"].lower() == data["employee_email"].lower() for emp in employee_list):
            emit("error", {"error": "An employee with this email already exists."})
            return

        new_employee = {
            "employee_name": data["employee_name"],
            "employee_title": data["employee_title"],
            "employee_gender": data["employee_gender"],
            "employee_department": data["employee_department"],
            "employee_role": data["employee_role"],
            "employee_email": data["employee_email"],
            "employee_id": str(uuid.uuid4().hex)
        }

        employee_list.append(new_employee)
        save_employees(employee_list)

        emit("employee_added", {
            "success": True,
            "employee": new_employee,
            "total_employees": len(employee_list)
        }, broadcast=False)

    except Exception as e:
        emit("error", {
            "success": False,
            "error": str(e)
        })
        raise e

# Handling conversation retrieval
@socketio.on("get_conversation")
def handle_get_conversation():
    try:
        conversation = load_conversation()

        if isinstance(conversation, str):
            emit("conversation_response", {
                "success": False,
                "message": conversation
            })
        else:
            emit("conversation_response", {
                "success": True,
                "conversation": conversation
            })
    except Exception as e:
        emit("error", {
            "success": False,
            "error": str(e)
        })

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8000)
