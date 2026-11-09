
from flask import Flask, jsonify

app = Flask(__name__)

# Sample user data
users = [
    {"id": 1, "name": "John", "email": "john@gmail.com"},
    {"id": 2, "name": "David", "email": "david@gmail.com"},
    {"id": 3, "name": "John", "email": "john@gmail.com"}
]


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
    app.run(host="0.0.0.0", port=6001)
