"""Backend Mangement for Activty Creator Chatbot."""
from flask import Flask, request, jsonify
from db import Firebase
import requests

app = Flask(__name__)
activities = {}
ready_activities = {}
users = set()


@app.route('/', methods=['GET'])
def index():
    """Return all users."""
    db = Firebase()
    result = db.read_all_users()
    return jsonify(result)


@app.route('/find', methods=['GET'])
def read_user():
    """Read a single user."""
    db = Firebase()
    data = request.args
    result = db.find_user(data['userId'])
    return jsonify(result)


@app.route('/add', methods=['POST'])
def add():
    """Add a user."""
    db = Firebase()
    data = request.get_json()
    result = db.add_user(data)
    check_activities()
    return jsonify(result)


@app.route('/addUser', methods=['POST'])
def add_user():
    """Add user."""
    message = "Hi ya ll, I have arranged you a group and converted this to a group chat! Since you are all interested in hacking and are free on Saturday, I would suggest meeting on facebook headquarters. Btw, this group consists of Mete, Adi and Hamza, have fun! "
    db = Firebase()
    data = request.get_json()
    users.add(data['userId'])
    db.add_userId(data['userId'])
    num = db.get_num_users()
    print(num)
    if num:
        print("gcdjsa")
        for key, val in num.items():
            print(key)
            send_message(key, message)
    return jsonify({'message': True})


@app.route('/deleteAll', methods=['POST'])
def delete_all():
    """Delete all users."""
    users.clear()
    return jsonify({'message': True})


@app.route('/update', methods=['POST'])
def update():
    """Update a user."""
    db = Firebase()
    data = request.get_json()
    result = db.update_user(data)
    return jsonify(result)


@app.route('/delete', methods=['POST'])
def delete():
    """Delete a user."""
    data = request.get_json()
    db = Firebase()
    result = db.delete_user(data['userId'])
    return jsonify(result)


@app.route('/userActive', methods=['GET'])
def active():
    """Check if user is active."""
    data = request.args
    for key, value in ready_activities.items():
        if data['userId'] in value:
            return jsonify({"message": True})
    return jsonify({"message": False, "acts": ready_activities})


@app.route('/usersLeft', methods=['GET'])
def left():
    """Leftover people in chat."""
    res = []
    data = request.args
    db = Firebase()
    d = db.get_all_users()
    for key, value in d.items():
        if data['userId'] != key:
            res.append(key)
    return jsonify({"userIds": res})


def send_message(userId, message):
    realUserId = f'"{userId}"'
    realMessage = f'"{message}"'
    """Send meassage to user."""
    headers = {
        'Content-Type': 'application/json',
    }
    params = (
        ('access_token', 'EAAIKXN8ZAjBsBANToUfJbTPviKjhaQhvCky9jyAOKZArf0V25ensSdZCleC2sIg1Qv2MCa6x9PDRzin1YQCr3X57nWrP494Lfea71sAqTP7b4gQ7SKmJZBeIZAWZAwz6ZBeQu3PrqLZAYn3CGwcqC4TeEMI2KsTgjaRMTuApITEYCAZDZD'),
    )

    recipient = '{ \"recipient\":{'

    id = "\"id\":"

    message = "},\n  \"message\":{\n    \"text\":"


    lastStrin = "\n  }\n}"
    data = '{\n  "recipient":{\n    "id":"1964122107006784"\n  },\n  "message":{\n    "text":"We have an activity, stay tuned! :D"\n  }\n}'

    realData = (recipient + id + realUserId + message + realMessage + lastStrin)

    response = requests.post('https://graph.facebook.com/v2.6/me/messages', headers=headers, params=params, data=realData)
    print(response.text)
    return jsonify({"message": True})

@app.route('/sendMessage', methods=['POST'])
def send():
    """Send meassage to user."""
    d = request.get_json()
    userId = d['userId']
    message = d['message']
    realUserId = f'"{userId}"'
    realMessage = f'"{message}"'
    headers = {
        'Content-Type': 'application/json',
    }
    params = (
        ('access_token', 'EAAIKXN8ZAjBsBANToUfJbTPviKjhaQhvCky9jyAOKZArf0V25ensSdZCleC2sIg1Qv2MCa6x9PDRzin1YQCr3X57nWrP494Lfea71sAqTP7b4gQ7SKmJZBeIZAWZAwz6ZBeQu3PrqLZAYn3CGwcqC4TeEMI2KsTgjaRMTuApITEYCAZDZD'),
    )

    recipient = '{ \"recipient\":{'

    id = "\"id\":"

    message = "},\n  \"message\":{\n    \"text\":"


    lastStrin = "\n  }\n}"
    data = '{\n  "recipient":{\n    "id":"1964122107006784"\n  },\n  "message":{\n    "text":"We have an activity, stay tuned! :D"\n  }\n}'

    realData = (recipient + id + realUserId + message + realMessage + lastStrin)

    response = requests.post('https://graph.facebook.com/v2.6/me/messages', headers=headers, params=params, data=realData)
    db = Firebase()
    db.add_message(message)
    return jsonify({"message": response.text})


@app.route('/findMessage', methods=['GET'])
def foo():
    """Lookup message"""
    # data = request.args
    data = {}
    data["message"] = "jdwkclwcwlxmwx"
    db = Firebase()
    result = db.find_message(data['message'])
    return jsonify(result)


def check_activities():
    """Check ready events."""
    db = Firebase()
    data = db.read_all_users()
    for i, row in data.items():
        for interest in row['interests']:
            key = (row['location'], row['availability'], interest)
            if key in activities:
                activities[key].add(row['userId'])
                if len(activities[key]) >= 2:
                    ready_activities[key] = activities[key]
                    activities.pop(key, None)
            else:
                activities[key] = set([row['userId']])
    db.add_ready(ready_activities)

if __name__ == '__main__':
    app.run()
