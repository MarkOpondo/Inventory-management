import requests

# URL of your Flask web backend server
BASE_URL = "http://127.0.0.1:5000/inventory"
INVENTORY_URL = "http://127.0.0.1:5001/product"

while True:
    print("\n--- INVENTORY SYSTEM CLIENT ---")
    print("1. View All Items")
    print("2. Add New Item")
    print("3. Update Item Quantity")
    print("4. Delete An Item")
    print("5. Search Open foods facts")
    print("6. Exit Application")
    
    choice = input("Select an option (1-6): ").strip()

    if choice == "1":
        # GET request to fetch the inventory list
        response = requests.get(BASE_URL)
        items = response.json()
        print("\n--- Current Inventory ---")
        for item in items:
            print(f"ID: {item['id']} | Name: {item['name']} | Qty: {item['quantity']} | Price: ${item['price']}")

    elif choice == "2":
        item_id = input("Enter Item ID: ")
        name = input("Enter Item Name: ")
        qty = int(input("Enter Quantity: "))
        price = float(input("Enter Price: "))
        
        payload = {"id": item_id, "name": name, "quantity": qty, "price": price}
        
        # POST request to create the item
        response = requests.post(BASE_URL, json=payload)
        if response.status_code == 201:
            print("Success: Item added to database file.")
        else:
            print(f"Error: {response.json().get('error')}")

    elif choice == "3":
        item_id = input("Enter the ID of the item to update: ")
        new_qty = int(input("Enter new total quantity: "))
        
        payload = {"quantity": new_qty}
        
        # PATCH request to modify the item
        response = requests.patch(f"{BASE_URL}/{item_id}", json=payload)
        
        if response.status_code == 200:
            print("Success: Quantity updated.")
        else:
            print(f"Error: {response.json().get('error')}")

    elif choice == "4":
        item_id = input("Enter the ID of the item to delete: ")
        
        # DELETE request to remove the item
        response = requests.delete(f"{BASE_URL}/{item_id}")
        
        if response.status_code == 204:
            print("Success: Item erased permanently.")
        else:
            print(f"Error: {response.json().get('error')}")

    elif choice == "5":
        barcode = input("Enter the items barcode: ")
        response = requests.get(F"{INVENTORY_URL}/{barcode}")

        if response.status_code == 200:
            data = response.json()
            print(f"Name : {data["name"]} \n Ingredients : {data["ingredients"]}")

        else:
            print("No such product in our inventory")

    elif choice == "6":
        print("Closing application. Goodbye!")
        break
        
    else:
        print("Invalid choice. Choose a number between 1 and 5.")