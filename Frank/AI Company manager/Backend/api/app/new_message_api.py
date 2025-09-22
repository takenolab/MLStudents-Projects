from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import sys, pathlib
import threading
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
import time
from notifications.notifications import check_unread_from_senders 
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from data.data import load_employee_emails


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app) 
 
  

 
def notification_emitter():
    while True:
        time.sleep(3)
        notif_state = check_unread_from_senders(sender_emails=load_employee_emails())
        
 
        socketio.emit(
            'notification',
            {"status": notif_state},
             
        )
        print(notif_state)

 
 


@socketio.on("connect")
def handle_connect():
    print("Client connected")
 
    

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
 


 

 

 

if __name__ == "__main__":
    d = threading.Thread(target=notification_emitter)
    d.daemon = True
    d.start()
    socketio.run(app, debug=True , port=4000)
 