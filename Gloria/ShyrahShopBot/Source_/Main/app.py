from modules.customer import locate_item, purchase_item, identify_and_purchase
from modules.admin import authenticate, add_item, update_stock

def main():
    print("Welcome to Shyrah — Sana ShopBot")
    mode = input("Choose mode: (1) Customer  (2) Admin\n> ")

    if mode == '1':
        cust = input("Your customer ID:\n> ")
        action = input("Action: (a) Locate  (b) Buy\n> ")
        if action == 'a':
            item = input("Item to locate:\n> ")
            print(locate_item(item))
        else:
            live = input("Simulate face (enter your customer ID):\n> ")
            item = input("Item to buy:\n> ")
            qty = int(input("Quantity:\n> "))
            print(identify_and_purchase(live, item, qty, cust))
    else:
        pw = input("Admin password:\n> ")
        if authenticate(pw):
            op = input("Admin options: (a) Add item  (b) Update stock\n> ")
            name = input("Item name:\n> ")
            if op == 'a':
                aisle = int(input("Aisle:\n> "))
                sec = input("Section:\n> ")
                price = int(input("Price (MK):\n> "))
                stock = int(input("Stock:\n> "))
                print(add_item(name, aisle, sec, price, stock))
            else:
                stock = int(input("New stock:\n> "))
                print(update_stock(name, stock))
        else:
            print("Authentication failed.")

if __name__ == "__main__":
    main()
