from flask import Flask, render_template, request, make_response

app = Flask(__name__)






# Route to render the HTML file (index.html)
@app.route('/')
def index():
    return render_template('index.html')  # Flask automatically looks for 'index.html' in the 'templates' folder.




# Route to set a cookie
@app.route('/set_cookie', methods=['GET', 'POST'])
def set_cookie():
    if request.method == 'POST':
        username = request.form.get('username')
        resp = make_response(render_template('index.html', username=username, message="Cookie has been set!"))
        resp.set_cookie('username', username)  # Set cookie with the name 'username'
        return resp
    return render_template('index.html', message="Please enter your name.")

# Route to get the cookie value
@app.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')  # Retrieve the cookie value
    if username:
        return f"Hello {username}! Welcome back."
    return "No username cookie found. Please set a username first."

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
