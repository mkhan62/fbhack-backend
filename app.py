"""Backend Mangement for Activty Creator Chatbot."""
from flask import Flask, request, jsonify
from db import Firebase

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Return all users."""
    db = Firebase()
    result = db.read_all_users()
    return jsonify(result)


@app.route('/add', methods=['POST'])
def add():
    """Add a user."""
    db = Firebase()
    data = request.get_json()
    result = db.add_user(data)
    return jsonify(result)


@app.route('/delete', methods=['POST'])
def delete():
    """Delete a user."""
    db = Firebase()
    result = db.delete_entry("12234")
    return jsonify(result)


if __name__ == '__main__':
    app.run()
