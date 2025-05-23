import json
import os
import hashlib
from datetime import datetime, timedelta

USER_DATA_FILE = "user_data.json"

class UserData:
    @staticmethod
    def user_exists(username):
        if not os.path.exists(USER_DATA_FILE):
            return False
        with open(USER_DATA_FILE, "r") as f:
            try:
                data = json.load(f)
                return username in data
            except json.JSONDecodeError:
                return False

    @staticmethod
    def save_user_data(username, user_data):
        data = {}
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    pass
        
        data[username] = user_data
        with open(USER_DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_user_data(username):
        with open(USER_DATA_FILE, "r") as f:
            data = json.load(f)
            return data[username]

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    def verify_password(input_password, stored_hash):
        """Verify if the input password matches the stored hash"""
        return UserData.hash_password(input_password) == stored_hash
    @staticmethod
    def is_account_locked(user_data):
        if user_data.get("locked_until"):
            lock_time = datetime.strptime(user_data["locked_until"], "%Y-%m-%d %H:%M:%S")
            if datetime.now() < lock_time:
                return True
            else:
                # Auto-unlock after lock time expires
                user_data["locked_until"] = None
                user_data["failed_attempts"] = 0
                UserData.save_user_data(user_data["username"], user_data)
        return False