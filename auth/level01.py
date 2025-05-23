from .models import UserData
from .utils import get_valid_input, update_failed_attempts, reset_failed_attempts
import getpass

def register_user():
    print("\n--- Registration ---")
    username = get_valid_input("Enter username: ")
    
    if UserData.user_exists(username):
        print("Username already exists!")
        return False
    
    # Password setup
    while True:
        password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if password == confirm_password:
            break
        print("Passwords don't match!")
    
    hashed_password = UserData.hash_password(password)
    
    return {
        "username": username,
        "password": hashed_password,
        "failed_attempts": 0,
        "locked_until": None
    }

def login_user(username):
    if not UserData.user_exists(username):
        print("User does not exist!")
        return False
    
    user_data = UserData.load_user_data(username)
    
    if UserData.is_account_locked(user_data):
        print(f"Account locked until {user_data['locked_until']}")
        return False
    
    password = getpass.getpass("Enter password: ")
    if not UserData.verify_password(password, user_data["password"]):
        print("Incorrect password!")
        update_failed_attempts(username)
        return False
    
    reset_failed_attempts(username)
    return True