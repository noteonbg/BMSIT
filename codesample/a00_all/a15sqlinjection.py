from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from a16models import User  # Assume User is a mapped class

# Create a database engine
engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
session = Session()

# Query using ORM
username = input("Enter username: ")
password = input("Enter password: ")

# ORM query (avoids SQL injection automatically)
user = session.query(User).filter(User.username == username, User.password == password).first()

if user:
    print("Login successful!")
else:
    print("Invalid credentials")

# Close session
session.close()

"""

Parameterized queries: Always use parameterized queries (or prepared statements).
ORMs: Use ORMs like SQLAlchemy or Django ORM, which abstract SQL queries and prevent injection attacks.
Input validation: Sanitize and validate user inputs before using them in queries.
Least privilege: Ensure database accounts only have the privileges necessary for their purpose.


"""