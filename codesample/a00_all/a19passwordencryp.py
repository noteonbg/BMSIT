import bcrypt

# Function to hash a password
def hash_password(password: str) -> str:
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Function to check if a password matches the stored hash
def check_password(stored_hash: str, password: str) -> bool:
    # Compare the provided password with the stored hash
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

# Example usage

# User's plain-text password
password = "mysecretpassword"

# Step 1: Hash the password (store this hash in the database)
hashed = hash_password(password)
print("Stored Hashed Password:", hashed)

# Step 2: User attempts to log in
login_attempt = "mysecretpassword"  # Correct password
wrong_attempt = "wrongpassword"  # Incorrect password

# Step 3: Verify the password
if check_password(hashed, login_attempt):
    print("Login successful: Password is correct.")
else:
    print("Login failed: Incorrect password.")

# Try with wrong password
if check_password(hashed, wrong_attempt):
    print("Login successful: Password is correct.")
else:
    print("Login failed: Incorrect password.")
