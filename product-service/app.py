
from flask import Flask, jsonify

app = Flask(__name__)

# Sample product data
products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Mobile", "price": 20000}
]

# Home endpoint
@app.route("/")
def home():
    return jsonify({"message": "Welcome to Product Service"})

# Get all products
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

# Get product by ID
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)

    if product:
        return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
