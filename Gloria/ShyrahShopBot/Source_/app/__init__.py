# from nicegui import ui

# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# from modules.customer import locate_item, identify_and_purchase
# from modules.admin import authenticate, add_item, update_stock

# def load_json(path):
#     if not os.path.exists(path):
#         return {}
#     with open(path, 'r') as f:
#         return json.load(f)

# def customer_ui():
#     with ui.card():
#         ui.label('Customer Panel')
#         cust_id = ui.input('Customer ID')
#         item = ui.input('Item')
#         qty = ui.input('Quantity').props('type=number')
#         live_id = ui.input('Simulated Face ID')

#         def handle_purchase():
#             result = identify_and_purchase(live_id.value, item.value, int(qty.value), cust_id.value)
#             ui.notify(result)

#         ui.button('Locate Item', on_click=lambda: ui.notify(locate_item(item.value)))
#         ui.button('Buy Item', on_click=handle_purchase)

# def admin_ui():
#     with ui.card():
#         ui.label('Admin Panel')
#         pw = ui.input('Password', password=True)

#         def handle_auth():
#             if authenticate(pw.value):
#                 ui.notify('Authenticated')
#                 item_name = ui.input('Item Name')
#                 aisle = ui.input('Aisle').props('type=number')
#                 section = ui.input('Section')
#                 price = ui.input('Price').props('type=number')
#                 stock = ui.input('Stock').props('type=number')

#                 ui.button('Add Item', on_click=lambda: ui.notify(
#                     add_item(item_name.value, int(aisle.value), section.value, int(price.value), int(stock.value))
#                 ))

#                 ui.button('Update Stock', on_click=lambda: ui.notify(
#                     update_stock(item_name.value, int(stock.value))
#                 ))
#             else:
#                 ui.notify('Authentication failed', type='negative')

#         ui.button('Login', on_click=handle_auth)

# with ui.column():
#     ui.label('Welcome to Shyrah — Sana ShopBot')
#     ui.button('Customer Mode', on_click=customer_ui)
#     ui.button('Admin Mode', on_click=admin_ui)

# ui.run()