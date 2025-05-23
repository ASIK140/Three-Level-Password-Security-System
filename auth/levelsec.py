import random
from .utils import get_valid_input

def setup_2fa():
    print("\n--- Two-Factor Authentication Setup ---")
    email = get_valid_input("Enter email for 2FA: ")
    return {"email": email}

def verify_2fa(user_data):
    print("\n--- Level 2: Two-Factor Authentication ---")
    email = user_data["email"]
    verification_code = str(random.randint(100000, 999999))
    
    print(f"A verification code has been sent to {email}")
    print(f"[DEMO] Your verification code is: {verification_code}")
    
    attempts = 3
    while attempts > 0:
        user_code = get_valid_input("Enter the 6-digit verification code: ")
        if user_code == verification_code:
            return True
        attempts -= 1
        print(f"Incorrect code. {attempts} attempts remaining.")
    
    print("Too many incorrect attempts. Login failed.")
    return False