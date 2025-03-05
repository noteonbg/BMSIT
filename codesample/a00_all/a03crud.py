from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'products.db'

# Utility function to get a database connection
def get_db():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  # To return rows as dictionaries
        return conn
    except sqlite3.Error as e:
        app.logger.error(f"Database connection error: {e}")
        raise

# Error handling for database errors
@app.errorhandler(sqlite3.Error)
def handle_sqlite_error(error):
    app.logger.error(f"SQLite error: {error}")
    return jsonify({"error": "Database error occurred. Please try again later."}), 500

# Error handling for invalid JSON input
@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({"error": "Bad request. Please check your input."}), 400

# Create a product (POST)
@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()

        # Input validation
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')
        quantity = data.get('quantity')

        if not name or not category or not price or not quantity:
            return jsonify({"error": "All fields (name, category, price, quantity) are required!"}), 400

        # Insert product into the database
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO products (name, category, price, quantity)
            VALUES (?, ?, ?, ?)
        ''', (name, category, price, quantity))
        conn.commit()
        conn.close()

        return jsonify({"message": "Product created successfully!"}), 201
    except Exception as e:
        app.logger.error(f"Error creating product: {e}")
        return jsonify({"error": "An error occurred while creating the product."}), 500

# Get all products (GET)
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM products')
        rows = c.fetchall()
        conn.close()

        products = []
        for row in rows:
            products.append({
                "id": row["id"],
                "name": row["name"],
                "category": row["category"],
                "price": row["price"],
                "quantity": row["quantity"]
            })

        return jsonify({"products": products})

    except Exception as e:
        app.logger.error(f"Error retrieving products: {e}")
        return jsonify({"error": "An error occurred while retrieving products."}), 500

# Get a specific product by ID (GET)
@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM products WHERE id = ?', (id,))
        row = c.fetchone()
        conn.close()

        if row:
            product = {
                "id": row["id"],
                "name": row["name"],
                "category": row["category"],
                "price": row["price"],
                "quantity": row["quantity"]
            }
            return jsonify({"product": product})
        else:
            return jsonify({"error": f"Product with ID {id} not found"}), 404

    except Exception as e:
        app.logger.error(f"Error retrieving product by ID {id}: {e}")
        return jsonify({"error": "An error occurred while retrieving the product."}), 500

# Update a product (PUT)
@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    try:
        data = request.get_json()

        # Input validation
        name = data.get('name')
        category = data.get('category')
        price = data.get('price')
        quantity = data.get('quantity')

        if not name or not category or not price or not quantity:
            return jsonify({"error": "All fields (name, category, price, quantity) are required!"}), 400

        # Update the product in the database
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            UPDATE products
            SET name = ?, category = ?, price = ?, quantity = ?
            WHERE id = ?
        ''', (name, category, price, quantity, id))
        conn.commit()

        # Check if any rows were updated (i.e., product exists)
        if c.rowcount == 0:
            return jsonify({"error": f"Product with ID {id} not found"}), 404

        conn.close()
        return jsonify({"message": "Product updated successfully!"})

    except Exception as e:
        app.logger.error(f"Error updating product ID {id}: {e}")
        return jsonify({"error": "An error occurred while updating the product."}), 500

# Delete a product (DELETE)
@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('DELETE FROM products WHERE id = ?', (id,))
        conn.commit()

        # Check if any rows were deleted (i.e., product exists)
        if c.rowcount == 0:
            return jsonify({"error": f"Product with ID {id} not found"}), 404

        conn.close()
        return jsonify({"message": "Product deleted successfully!"})

    except Exception as e:
        app.logger.error(f"Error deleting product ID {id}: {e}")
        return jsonify({"error": "An error occurred while deleting the product."}), 500

# General error handler for unexpected errors
@app.errorhandler(Exception)
def handle_unexpected_error(error):
    app.logger.error(f"Unexpected error: {error}")
    return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)
