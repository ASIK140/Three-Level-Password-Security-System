# auth/auth_controller.py
from auth.level02 import verify_2fa as auth_verify_2fa
from auth.models import UserData

def handle_2fa_verification(username, code):
    user_data = UserData.load_user_data(username)
    if not user_data:
        return False, "User data not found"
    
    try:
        if auth_verify_2fa(user_data, code):
            # Clear OTP after verification
            user_data.pop('2fa_secret', None)
            user_data.pop('last_otp_sent', None)
            UserData.save_user_data(username, user_data)
            return True, None
        return False, "Invalid verification code"
    except Exception as e:
        return False, str(e)