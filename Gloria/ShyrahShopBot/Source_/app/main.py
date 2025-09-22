# from nicegui import ui
# import cv2
# import speech_recognition as sr
# from modules.customer import locate_item, purchase_item
# from modules.admin import authenticate, add_item, update_stock
# import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap')


# # ----- Background Styling -----
# ui.add_body_html("""
# <style>
#   body {
#     background-image: url('/assets/background.jpg');
#     background-size: cover;
#     background-position: center;
#     background-repeat: no-repeat;
#     font-family: 'Roboto', sans-serif;
#     /*...existing styles...*/ 
#     color: white;
#   }
#   .card {
#     background: rgba(0, 0, 0, 0.7);
#     padding: 30px;
#     border-radius: 10px;
#     max-width: 500px;
#     margin: auto;
#   }
# </style>
# """)

# # ----- Routing -----
# def home():
#     ui.label("Welcome to Shyrah ShopBot at Sana!").classes('text-3xl font-bold mt-8')
#     with ui.row().classes('justify-center mt-6'):
#         ui.button("Customer Portal", on_click=lambda: ui.open('/customer'))
#         ui.button("Admin Login", on_click=lambda: ui.open('/admin'))

# @ui.page('/customer')
# def customer_page():
#     with ui.column().classes('card'):
#         ui.label("🛒 Customer Mode").classes('text-2xl font-bold')

#         item_input = ui.input("Enter item name to locate:")
#         qty_input = ui.input("Enter quantity (for purchase):").props('type=number')
#         customer_id_input = ui.input("Enter your customer ID:")
        
#         def locate():
#             ui.notify(locate_item(item_input.value))
        
#         def purchase():
#             result = purchase_item(item_input.value, int(qty_input.value), customer_id_input.value)
#             ui.notify(result)

#         ui.button("Locate Item", on_click=locate).classes('mt-2')
#         ui.button("Buy Item", on_click=purchase).classes('mt-2')
#         ui.button("⬅ Back", on_click=lambda: ui.open('/')).classes('mt-6')

# @ui.page('/admin')
# def admin_page():
#     with ui.column().classes('card'):
#         ui.label("🔐 Admin Portal").classes('text-2xl font-bold')

#         pw_input = ui.input("Enter Admin Password", password=True)
#         item_input = ui.input("Item Name")
#         price_input = ui.input("Price").props('type=number')
#         stock_input = ui.input("Stock").props('type=number')
#         aisle_input = ui.input("Aisle").props('type=number')
#         section_input = ui.input("Section")

#         def handle_add():
#             if authenticate(pw_input.value):
#                 res = add_item(item_input.value, int(aisle_input.value), section_input.value, int(price_input.value), int(stock_input.value))
#                 ui.notify(res)
#             else:
#                 ui.notify("Wrong password", type='negative')

#         def handle_update():
#             if authenticate(pw_input.value):
#                 res = update_stock(item_input.value, int(stock_input.value))
#                 ui.notify(res)
#             else:
#                 ui.notify("Wrong password", type='negative')

#         ui.button("Add Item", on_click=handle_add).classes('mt-2')
#         ui.button("Update Stock", on_click=handle_update).classes('mt-2')
#         ui.button("⬅ Back", on_click=lambda: ui.open('/')).classes('mt-6')

# # @ui.page('/')
# # def main_page():
# #     home()


# ui.run(title="Shyrah ShopBot😉😍 - Sana", port=8080, reload=False)
# ui.page('/', title='Shyrah😍🛒SANA🩵 ShopBot', favicon='favicon.ico')

# @ui.page('/')
# def main_page():
#     ui.image('https://your-image-url.com/logo.png').classes('w-32 h-auto mx-auto mt-4')
#     home()

# # Animated feedback with icon:
# ui.button("Locate Item 🔍", on_click=locate).classes('mt-2')
# ui.notify("Locating item...", type='info')

# # Add a status spinner while tasks run:
# with ui.spinner(text='Processing...'):
#     do_long_task()

# # Add a progress bar:
# bar = ui.progress(value=0)
# bar.value = 50  # or update dynamically during a process


# # Create a video stream UI component
# video = cv2.VideoCapture(0)
# img = ui.image()

# def update_frame():
#     ret, frame = video.read()
#     if ret:
#         _, jpeg = cv2.imencode('.jpg', frame)
#         img.source = jpeg.tobytes()

# ui.timer(0.1, update_frame)  # updates every 0.1 seconds


# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# def update_frame():
#     ret, frame = video.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.1, 4)
#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     _, jpeg = cv2.imencode('.jpg', frame)
#     img.source = jpeg.tobytes()



# def listen_command():
#     r = sr.Recognizer()
#     with sr.Microphone() as mic:
#         audio = r.listen(mic)
#     try:
#         return r.recognize_google(audio)
#     except sr.UnknownValueError:
#         return ""
#     except sr.RequestError:
#         return ""
# ui.button("Speak Command", on_click=lambda: ui.notify(listen_command()))


# username_input = ui.input("Username")
# pw_input = ui.input("Password", password=True)

# def handle_admin_login():
#     if authenticate_admin(username_input.value, pw_input.value):
#         ui.notify("Welcome, " + username_input.value)
#         ui.open('/admin')
#     else:
#         ui.notify("Access Denied", type='negative')

# ui.button("Login", on_click=handle_admin_login)


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../', "../")))
from nicegui import ui
import cv2
import speech_recognition as sr
import base64
from Source_.modules.customer import locate_item, purchase_item
from Source_.modules.admin import authenticate_admin, add_item, update_stock

# ---- Load Google Fonts and Background Styling ----
ui.add_body_html("""
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
<style>
  body {
    background-image: url('https://picsum.photos/id/1018/1920/1080');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    font-family: 'Roboto', sans-serif;
    color: white;
    margin: 0;
  }
  .card {
    background: rgba(0, 0, 0, 0.75);
    padding: 30px;
    border-radius: 10px;
    max-width: 500px;
    margin: auto;
  }
</style>
""")

# ---- Webcam Setup ----
video = cv2.VideoCapture(0)
img = ui.image()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def update_frame():
    ret, frame = video.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # _, jpeg = cv2.imencode('.jpg', frame)
        _, jpeg = cv2.imencode('.jpg', frame)
        b64 = base64.b64encode(jpeg).decode('utf-8')
        img.source = f'data:image/jpeg;base64,{b64}'

ui.timer(0.1, update_frame)

# ---- Voice Command ----
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as mic:
        audio = r.listen(mic)
    try:
        return r.recognize_google(audio)
    except (sr.UnknownValueError, sr.RequestError):
        return "Could not understand"

# ---- Home Page ----
def home():
    ui.label("Welcome to Shyrah ShopBot at Sana!").classes('text-3xl font-bold mt-8')
    with ui.row().classes('justify-center mt-6'):
        ui.button("🛒 Customer Portal", on_click=lambda: ui.open('/customer')).classes('m-2')
        ui.button("🔐 Admin Login", on_click=lambda: ui.open('/admin')).classes('m-2')
        ui.button("🎙️ Voice Command", on_click=lambda: ui.notify(listen_command())).classes('m-2')

@ui.page('/')
def main_page():
    ui.image('https://your-image-url.com/logo.png').classes('w-32 h-auto mx-auto mt-4')
    home()

# ---- Customer Page ----
@ui.page('/customer')
def customer_page():
    with ui.column().classes('card'):
        ui.label("🛒 Customer Mode").classes('text-2xl font-bold')
        item_input = ui.input("Enter item name to locate:")
        qty_input = ui.input("Enter quantity (for purchase):").props('type=number')
        customer_id_input = ui.input("Enter your customer ID:")

        def locate():
            ui.notify(locate_item(item_input.value))

        def purchase():
            result = purchase_item(item_input.value, int(qty_input.value), customer_id_input.value)
            ui.notify(result)

        ui.button("Locate Item 🔍", on_click=locate).classes('mt-2')
        ui.button("Buy Item 🛍️", on_click=purchase).classes('mt-2')
        ui.button("⬅ Back", on_click=lambda: ui.open('/')).classes('mt-6')

# ---- Admin Page ----
@ui.page('/admin')
def admin_page():
    with ui.column().classes('card'):
        ui.label("🔐 Admin Portal").classes('text-2xl font-bold')
        pw_input = ui.input("Enter Admin Password", password=True)
        item_input = ui.input("Item Name")
        price_input = ui.input("Price").props('type=number')
        stock_input = ui.input("Stock").props('type=number')
        aisle_input = ui.input("Aisle").props('type=number')
        section_input = ui.input("Section")

        def handle_add():
            if authenticate(pw_input.value):
                res = add_item(item_input.value, int(aisle_input.value), section_input.value, int(price_input.value), int(stock_input.value))
                ui.notify(res)
            else:
                ui.notify("Wrong password", type='negative')

        def handle_update():
            if authenticate(pw_input.value):
                res = update_stock(item_input.value, int(stock_input.value))
                ui.notify(res)
            else:
                ui.notify("Wrong password", type='negative')

        ui.button("Add Item ➕", on_click=handle_add).classes('mt-2')
        ui.button("Update Stock 🔄", on_click=handle_update).classes('mt-2')
        ui.button("⬅ Back", on_click=lambda: ui.open('/')).classes('mt-6')

# ---- Run App ----
ui.run(title="Shyrah ShopBot😉😍 - Sana", port=8080, reload=False)
