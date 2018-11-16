"""Instance of db to refactor databse actions."""
import pyrebase


class Firebase:
    """Manage db and client traffic."""

    def __init__(self):
        """Configure data, create instance."""
        config = {
          "apiKey": "AIzaSyAwqbx-DLKxeY4oO7Z7m5kSxq8kjIpvaQc",
          "authDomain": "fbhack-3f5eb.firebaseapp.com",
          "databaseURL": "https://fbhack-3f5eb.firebaseio.com/",
          "storageBucket": "fbhack-3f5eb.appspot.com",
          "serviceAccount": "cred.json"
        }
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()

    def get_num_users(self):
        data = self.db.child('users').get().val()
        if len(data) >= 3:
            return data


    def add_user(self, data):
        """Add user to db."""
        self.db.child("activity").child(data["userId"]).set(data)
        return {"message": True}

    def add_userId(self, id):
        """Add user to db."""
        self.db.child("users").child(id).set(id)
        return {"message": True}

    def add_ready(self, ready_activities):
        """Add ready activities."""
        for event, values in ready_activities.items():
            self.db.child('active').child(event).set(list(values))
        return {"message": True}

    def add_message(self, message):
        """Add message to db."""
        self.db.child('messages').child(message).set(message)
        return {"message": True}

    def find_message(self, message):
        """Lookup message."""
        msgs = self.db.child('messages').get().val()
        if not msgs:
            return {"message": False}
        if message in msgs:
            return {'message': True}
        return {"message": False}

    # def get_impromptu(self, data):
    #     """Lookup impromptu event."""
    #     curr_acts = self.db.child('active').get().val()
    #     key = (data['location'], data['availability'], data['interest'])
    #     return {"message": True, "activity": key, "users": curr_acts[key]} if str(key) in curr_acts else {"message": False}

    def read_all_users(self):
        """Return all entries."""
        return self.db.child("activity").get().val()

    def find_user(self, key):
        """Lookup user."""
        return self.db.child("activity").child(key).get().val()

    def update_user(self, data):
        """Update a user profile."""
        if self.find_user(data['userId']):
            self.db.child(data['userId']).update(data)
            return {"message": "Successfully updated user info!"}
        return {"message": "User does not exist."}

    def delete_user(self, key):
        """Delete User."""
        if self.find_user(key):
            self.db.child("activity").child(key).remove()
            return {"message": "Entry successfully deleted"}
        return {"message": "User doesn't exist"}

    def get_activites(self):
        """Get potential activities which can happend now."""
        pass

    def get_impromptu_activities(self):
        """Spontaneous activity scheduling."""
        pass
