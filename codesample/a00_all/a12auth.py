from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret key for sessions (must be kept secure)
app.secret_key = 'supersecretkey'

# A simple in-memory "database" to store users (for demo purposes)
users_db = {
    'admin': generate_password_hash('adminpassword')  # username: admin, password: adminpassword
}

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the "database" and if the password matches
        if username in users_db and check_password_hash(users_db[username], password):
            # If login is successful, create a session for the user
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

# Route for the home page (accessible only to authenticated users)
@app.route('/home')
def home():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

# Route to log out
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the user from the session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

"""
Password Hashing:

We're using werkzeug.security to securely store and verify passwords.
generate_password_hash('password'): Hashes the user's password before storing it.
check_password_hash(stored_hash, password): Checks if the entered password matches the hashed password.
Session Management:

Flask's session object is used to store the logged-in user's username.
When the user successfully logs in, their username is stored in the session with session['username'] = username.
If a user tries to access the home route without being logged in (i.e., without a session), they are redirected to the login page.
Flash Messages:

Flask's flash() function is used to display messages to the user (e.g., login success or failure).
Flash messages are typically displayed on the page using get_flashed_messages().
Access Control:

The home route checks if the user is logged in by checking if username exists in the session. If not, the user is redirected to the login page.

"""