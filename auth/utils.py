import getpass
from .models import UserData

def get_valid_input(prompt, input_type=str):
    while True:
        try:
            user_input = input_type(input(prompt))
            return user_input
        except ValueError:
            print("Invalid input. Please try again.")

def update_failed_attempts(username):
    user_data = UserData.load_user_data(username)
    user_data["failed_attempts"] = user_data.get("failed_attempts", 0) + 1
    
    if user_data["failed_attempts"] >= 3:
        from datetime import datetime, timedelta
        lock_time = datetime.now() + timedelta(minutes=5)
        user_data["locked_until"] = lock_time.strftime("%Y-%m-%d %H:%M:%S")
        print("Too many failed attempts. Account locked for 5 minutes.")
    
    UserData.save_user_data(username, user_data)

def reset_failed_attempts(username):
    user_data = UserData.load_user_data(username)
    user_data["failed_attempts"] = 0
    user_data["locked_until"] = None
    UserData.save_user_data(username, user_data)