class InventoryItem:
    def __init__(self, id , name, quantity, price):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price

    def to_dict(self):
        return{"id": self.id, "name": self.name, "quantity": self.quantity, "price": self.price}