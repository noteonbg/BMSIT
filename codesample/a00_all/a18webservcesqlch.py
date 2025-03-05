#curl -X POST http://127.0.0.1:5000/register -H "Content-Type: application/json" -d '{"username": "newuser", "password": "securepassword"}'

#

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from a17models import Base, User  # Import the User model

# Create a Flask app
app = Flask(__name__)

# Set up SQLAlchemy
DATABASE_URL = "sqlite:///example.db"  # Path to your SQLite database file
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables (if they don't exist already)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Route to register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # Validate inputs
    if not username or not password:
        return jsonify(message="Username and password are required"), 400

    # Check if the username already exists
    existing_user = session.query(User).filter(User.username == username).first()
    if existing_user:
        return jsonify(message="Username already taken"), 400

    # Create a new user
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()

    return jsonify(message="User registered successfully"), 201

# Route to authenticate a user
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # Check if the user exists and the password is correct
    user = session.query(User).filter(User.username == username).first()

    if user and user.password == password:
        return jsonify(message="Login successful"), 200
    else:
        return jsonify(message="Invalid username or password"), 401

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
