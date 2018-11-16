"""Backend Mangement for Activty Creator Chatbot."""
from flask import Flask, request, jsonify
import pyrebase
from db import Firebase

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Return all users"""
    result = db.read_all()
    return jsonify(result)


@app.route('/add', methods=['POST'])
def add():
    data = request.data
    result = db.add_entry(data)
    return jsonify(result)


@app.route('/delete', methods=['POST'])
def delete():
    result = db.delete_entry("12234")
    return jsonify(result)


if __name__ == '__main__':
    db = Firebase()
    app.run()
