from flask import Flask
from routes.inventory_route import inventory

app = Flask(__name__)
app.register_blueprint(inventory)

if __name__ == "__main__":
    app.run(debug=True, port=5000)