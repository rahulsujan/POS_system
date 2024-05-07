# Point of Sale System for a Furniture Store
import json
import csv

# Constants for file paths
INVENTORY_FILE = 'inventory.json'
TRANSACTION_LOG = 'transactions.csv'

# Furniture class representing each item in the store
class Furniture:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def update_quantity(self, change):
        self.quantity += change

# Function to load inventory from a JSON file
def load_inventory():
    with open(INVENTORY_FILE, 'r') as f:
        data = json.load(f)
        return {item['name']: Furniture(item['name'], item['price'], item['quantity']) for item in data}

# Function to save inventory to a JSON file
def save_inventory(inventory):
    data = [{'name': item.name, 'price': item.price, 'quantity': item.quantity} for item in inventory.values()]
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Function to display inventory
def display_inventory(inventory):
    print("\nCurrent Inventory:")
    for item in inventory.values():
        print(f"{item.name}: Price - ${item.price}, Quantity - {item.quantity}")

# Function to add an item to the cart
def add_to_cart(cart, inventory, item_name, quantity):
    if item_name in inventory:
        item = inventory[item_name]
        if item.quantity >= quantity:
            item.update_quantity(-quantity)
            if item_name in cart:
                cart[item_name].update_quantity(quantity)
            else:
                cart[item_name] = Furniture(item_name, item.price, quantity)
            print(f"Added {quantity} {item_name}(s) to cart.")
        else:
            print(f"Insufficient stock for {item_name}.")
    else:
        print(f"{item_name} not found in inventory.")

# Function to calculate total price
def calculate_total(cart):
    return sum(item.price * item.quantity for item in cart.values())

# Function to checkout
def checkout(cart):
    total = calculate_total(cart)
    print(f"\nTotal amount to pay: ${total}")
    log_transaction(cart, total)
    cart.clear()
    print("Thank you for shopping with us!")

# Function to log transaction to CSV
def log_transaction(cart, total):
    with open(TRANSACTION_LOG, 'a', newline='') as f:
        writer = csv.writer(f)
        for item in cart.values():
            writer.writerow([item.name, item.price, item.quantity, item.price * item.quantity])
        writer.writerow(['TOTAL', '', '', total])

# Main point of sale loop
def point_of_sale():
    cart = {}
    inventory = load_inventory()
    while True:
        display_inventory(inventory)
        print("\nOptions:")
        print("1. Add item to cart")
        print("2. Checkout")
        print("3. Exit")
        choice = input("Select an option (1/2/3): ")

        if choice == '1':
            item_name = input("Enter the name of the item: ").capitalize()
            try:
                quantity = int(input("Enter the quantity: "))
                add_to_cart(cart, inventory, item_name, quantity)
            except ValueError:
                print("Invalid quantity. Please enter a number.")
        elif choice == '2':
            checkout(cart)
            save_inventory(inventory)
        elif choice == '3':
            print("Exiting point of sale system.")
            save_inventory(inventory)
            break
        else:
            print("Invalid choice. Please select again.")

# Run the point of sale system
point_of_sale()
