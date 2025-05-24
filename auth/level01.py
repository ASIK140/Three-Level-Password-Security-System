from .models import UserData
import getpass
def register_user(username, email, password):
    if UserData.user_exists(username):
        raise ValueError("Username already exists")
    if not email or '@' not in email:
        raise ValueError("Invalid email address")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    return {
        "username": username,
        "email": email,
        "password": UserData.hash_password(password),
        "security_level": 1
    }

def login_user(username, password):
    user_data = UserData.load_user_data(username)
    if not user_data:
        return False
    return UserData.verify_password(password,user_data.get("password"))