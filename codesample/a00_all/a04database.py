import sqlite3
from sqlite3 import Error

# Database file location
DATABASE = 'products.db'

# Function to create a connection to the SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except Error as e:
        print(f"Error: {e}")
    return conn

# Function to create the products table
def create_table():
    conn = create_connection()
    if conn:
        try:
            query = '''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            );
            '''
            conn.execute(query)
            conn.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()

def get_all_products():
    conn = create_connection()
    products = []
    if conn:
        try:
            query = 'SELECT * FROM products'
            cursor = conn.execute(query)
            # Get column names
            column_names = [description[0] for description in cursor.description]
            # Convert each row to a dictionary (row as JSON object)
            for row in cursor.fetchall():
                product = dict(zip(column_names, row))  # Create a dictionary using column names as keys
                products.append(product)
        except Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()
    return products


# Function to fetch all products
def get_all_products1():
    conn = create_connection()
    products = []
    if conn:
        try:
            query = 'SELECT * FROM products'
            cursor = conn.execute(query)
            products = cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()
    return products

# Function to add a product
def add_product(name, category, price, quantity):
    conn = create_connection()
    if conn:
        try:
            query = 'INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)'
            conn.execute(query, (name, category, price, quantity))
            conn.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()

# Function to update a product
def update_product(product_id, name, category, price, quantity):
    conn = create_connection()
    if conn:
        try:
            query = '''
            UPDATE products
            SET name = ?, category = ?, price = ?, quantity = ?
            WHERE id = ?
            '''
            conn.execute(query, (name, category, price, quantity, product_id))
            conn.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()

# Function to delete a product
def delete_product(product_id):
    conn = create_connection()
    if conn:
        try:
            query = 'DELETE FROM products WHERE id = ?'
            conn.execute(query, (product_id,))
            conn.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()
