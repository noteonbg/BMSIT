import sqlite3

# Connect to the database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Example of using parameterized queries to avoid SQL injection
username = input("Enter username: ")
password = input("Enter password: ")

# Using placeholders for parameters
cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))

# Fetch results
user = cursor.fetchone()
if user:
    print("Login successful!")
else:
    print("Invalid credentials")

# Close connection
conn.close()

"""
With parameterized queries, user input is treated as data, not as part of the SQL command. 

"""
