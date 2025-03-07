from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)

# Sample product data
products = [
    {
        "name": "Cement123",
        "category": "Construction Materials",
        "price": 10.99,
        "quantity": 100
    },
    {
        "name": "Steel Rods",
        "category": "Construction Materials",
        "price": 25.50,
        "quantity": 150
    },
    {
        "name": "Welding Machine",
        "category": "Machines",
        "price": 400.00,
        "quantity": 15
    },
    {
        "name": "Hand Tools Set",
        "category": "Tools",
        "price": 60.00,
        "quantity": 50
    }
]

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify({"products": products})

if __name__ == '__main__':
    app.run(debug=True)
