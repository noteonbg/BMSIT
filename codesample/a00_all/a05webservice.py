from flask import Flask, jsonify, request
from a04database import create_table, get_all_products, add_product, update_product, delete_product
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize the database and create the table
#create_table()

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = get_all_products()
        return jsonify({"products": products}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'message': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')
        quantity = data.get('quantity')

        # Insert the product into the database
        add_product(name, category, price, quantity)

        return jsonify({'message': 'Product created successfully!'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product_route(id):
    try:
        data = request.get_json()
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')
        quantity = data.get('quantity')

        # Update the product in the database
        update_product(id, name, category, price, quantity)

        return jsonify({'message': 'Product updated successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product_route(id):
    try:
        # Delete the product from the database
        delete_product(id)

        return jsonify({'message': 'Product deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
