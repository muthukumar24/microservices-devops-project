
from flask import Flask, jsonify

app = Flask(__name__)

# Sample user data
users = [
    {"id": 1, "name": "John", "email": "john@gmail.com"},
    {"id": 2, "name": "David", "email": "david@gmail.com"}
]

@app.get("/health")
def health():
    return jsonify(service="user-service", status="ok", version="1.0")

# Home endpoint
@app.route("/")
def home():
    return jsonify({"message": "Welcome to User Service"})

# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

# Get user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)

    if user:
        return jsonify(user)

    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
