from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Secret key for JWT encryption
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
jwt = JWTManager(app)

# In-memory database (for demonstration purposes)
users_db = {
    'admin': generate_password_hash('adminpassword')  # username: admin, password: adminpassword
}

# Route to authenticate and generate JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get the JSON data sent by the client
    username = data.get('username')
    password = data.get('password')

    # Check if user exists in the "database" and if password is correct
    if username in users_db and check_password_hash(users_db[username], password):
        # If authentication is successful, create an access token (JWT)
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid username or password"), 401

# Route to access a protected resource (only for authenticated users)
@app.route('/protected', methods=['GET'])
@jwt_required()  # This decorator ensures that the user must be authenticated with a valid JWT
def protected():
    # Access the current user's identity (username) from the JWT token
    current_user = get_jwt_identity()
    return jsonify(message=f"Hello, {current_user}! This is a protected resource."), 200

# Route to log out (invalidate the token)
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # In this case, we don't need to do anything since JWT is stateless, but this is for example purposes
    return jsonify(message="Successfully logged out."), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
