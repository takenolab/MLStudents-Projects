from flask import Flask
from flask_socketio import SocketIO, emit , join_room
from flask_cors import CORS
import os, sys, pathlib, json
import threading
from threading import Lock

sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
import time
from ai.ai import ai 
from notifications.notifications import unread_from
from notifications.conversation_body import get_conversation_bodies
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from data.data import load_conversation,load_employee,load_employee_emails,load_employee_name, save_employees


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app) 

def init_ai(user_text: str) -> str:
    error, response = ai(user_text=user_text.strip().lower()) 
    if error == False: 
        return response 
    else:
        return "Model failure error occured. Please try again later."
    
    
  

def employee_conversation() -> list:
    employee_emails = load_employee_emails()
    conv = get_conversation_bodies(sender_emails=employee_emails,sender_name=load_employee_name())
    return conv

@socketio.on("get_employees_conversation")
def handle_get_employees_conversation():
    try:
        conversation = employee_conversation()
        if conversation:
            emit("email_conversation", {
                "success": True,
                "conversation": conversation
            })
        else:
            emit("no_employee_converation", {
                "success": False,
                "message": "No conversation data available."
            })
    except Exception as e:
        emit("employee_list_response", {
            "success": False,
            "message": f"Error loading conversation: {str(e)}"
        })

 

 
user_threads = {}
user_threads_lock = Lock()

def notification_emitter_single_worker(email):
    while True:
        try:
            time.sleep(3)  # check every 10s
            state, count = unread_from(sender_email=email)

            socketio.emit(
                'employee_notification',
                {
                    "email": email,
                    "status": state,
                    "count": count
                },
                room=email  
            )

            print(f"[NOTIFY] {email}: status={state}, count={count}")

        except Exception as e:
            print(f"[ERROR] Worker for {email}: {e}")
            time.sleep(3)
            
@socketio.on('join')
def handle_join(data):
    email = data.get('email')
    if not email:
        return {"success": False, "message": "Email required"}

    join_room(email)
    print(f"[JOIN] {email} joined their room")

    with user_threads_lock:
        if email not in user_threads:
            socketio.start_background_task(notification_emitter_single_worker, email)
            user_threads[email] = True
            print(f"[THREAD] Started notifier for {email}")

    return {"success": True}
       

@socketio.on('join')
def handle_join(data):
    email = data.get('email')
    if not email:
        return {"success": False, "message": "Email is required"}

    join_room(email)
    print(f'User joined room: {email}')  

    with user_threads_lock:
        if email not in user_threads:
            socketio.start_background_task(notification_emitter_single_worker, email)
            user_threads[email] = True
            print(f"Started background task for {email}")

    return {"success": True}

 
 
@socketio.on("get_employees")
def handle_get_employees():
    try:
        employees = load_employee()
        if employees:
            emit("employee_list_response", {
                "success": True,
                "employees": employees
            })
        else:
            emit("employee_list_response", {
                "success": False,
                "message": "No employee data available."
            })
    except Exception as e:
        emit("employee_list_response", {
            "success": False,
            "message": f"Error loading employees: {str(e)}"
        })


@socketio.on("connect")
def handle_connect():
    print("Client connected")
 
    conversation = load_conversation()
    emit("conversation_update", {
        "success": True,
        "conversation": conversation
    })

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

                                                                                                                                                                                                                     


@socketio.on("post_new_employee")
def post_new_employee(data):
    import uuid
    try:
        required_fields = ["employee_name", "employee_department", "employee_role", "employee_email", "employee_gender"] 
        if not data or not all(field in data for field in required_fields):
            emit("error", {"error": "Missing one or more required fields."})
            return

        employee_list = load_employee()

        if any(emp["employee_email"].lower() == data["employee_email"].lower() for emp in employee_list):
            emit("error", {"error": "An employee with this email already exists."})
            return

        new_employee = {
            "employee_name": data["employee_name"],
            "employee_title":data["employee_title"],
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

 

@socketio.on("get_employee_conversation")
def handle_get_employee_conversation(email):
    try:        
        if not email or "employee_email" not in email:
            emit("error", {"error": "Missing 'employee_email' in request."})
            return
        user_email = email["employee_email"] 
        chat=get_conversation_bodies(sender_email=user_email)
        conversation = []
        for msg in chat:
           for body in msg["conversation"]:
               conversation.append(body)
        emit(
            "employee_conversation",
            {
            "success": True,
            "conversation": conversation
            }
        )  
    except Exception as e:
        emit("error", {
            "success": False,
            "error": str(e)
        })

if __name__ == "__main__":
 
    socketio.run(app, debug=True)
 