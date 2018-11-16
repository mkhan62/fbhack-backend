"""Instance of db to refactor databse actions."""
import pyrebase


class Firebase:
    """Manage db and client traffic."""

    def __init__(self):
        """Khan."""
        config = {
          "apiKey": "AIzaSyAwqbx-DLKxeY4oO7Z7m5kSxq8kjIpvaQc",
          "authDomain": "fbhack-3f5eb.firebaseapp.com",
          "databaseURL": "https://fbhack-3f5eb.firebaseio.com/",
          "storageBucket": "fbhack-3f5eb.appspot.com",
          "serviceAccount": "cred.json"
        }
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()

    def add_entry(self, data):
        """Add user to db."""
        self.db.child("activity").child(data["userId"]).set(data)
        return {"message": True}

    def read_all(self):
        """Return all entries."""
        return self.db.child("activity").get().val()

    def find_user(self, key):
        """Lookup user."""
        return self.db.child("activity").child(key).get().val()

    def delete_entry(self, key):
        """Delete User."""
        if self.find_user(key):
            self.db.child("activity").child(key).remove()
            return {"message": "Entry successfully deleted"}
        return {"message": "User doesn't exist"}
