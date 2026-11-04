
from flask import Flask, jsonify

app = Flask(__name__)

# Sample order data
orders = [
    {"id": 1, "user_id": 1, "product_id": 1, "quantity": 2},
    {"id": 2, "user_id": 2, "product_id": 2, "quantity": 1}
]

@app.get("/health")
def health():
    return jsonify(service="order-service", status="ok", version="1.0")

# Home endpoint
@app.route("/")
def home():
    return jsonify({"message": "Welcome to Order Service"})

# Get all orders
@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)

# Get order by ID
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = next((o for o in orders if o["id"] == order_id), None)

    if order:
        return jsonify(order)

    return jsonify({"error": "Order not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
