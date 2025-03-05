import sqlite3

def init_db():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    # Create the products table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL)''')

    # Insert sample data
    c.executemany('''
        INSERT INTO products (name, category, price, quantity) 
        VALUES (?, ?, ?, ?)
    ''', [
        ("Cement", "Construction Materials", 10.99, 100),
        ("Steel Rods", "Construction Materials", 25.50, 150),
        ("Welding Machine", "Machines", 400.00, 15),
        ("Hand Tools Set", "Tools", 60.00, 50)
    ])

    conn.commit()
    conn.close()
    print("Database and table initialized with sample data.")

if __name__ == '__main__':
    init_db()
