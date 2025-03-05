from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    num1 = data.get("num1")
    num2 = data.get("num2")
    
    # Perform calculations
    sum_result = num1 + num2
    product_result = num1 * num2
    
    return jsonify({
        "sum": sum_result,
        "product": product_result
    })

if __name__ == "__main__":
    app.run(debug=True)
