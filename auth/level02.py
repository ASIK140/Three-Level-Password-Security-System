import pyotp
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from auth.config import SMTP_CONFIG
from auth.models import UserData

def setup_2fa(username):
    """Generate and send new OTP without backup codes"""
    # Generate fresh OTP
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=300)  # 5-minute expiry
    current_otp = totp.now()
    
    # Get user email
    user_data = UserData.load_user_data(username)
    if not user_data or not user_data.get('email'):
        raise ValueError("User email not found")
    
    # Send the OTP email
    send_otp_email(
        recipient=user_data['email'],
        otp_code=current_otp
    )
    
    return {
        "2fa_enabled": True,
        "2fa_secret": secret,
        "last_otp_sent": datetime.now().isoformat()
    }

def send_otp_email(recipient, otp_code):
    """Send OTP email without backup codes"""
    message = f"""\
    Your new verification code is: {otp_code}
    Expires in 5 minutes.
    
    This code is valid for one login attempt only.
    """
    
    msg = MIMEText(message)
    msg['Subject'] = "Your Login Verification Code"
    msg['From'] = SMTP_CONFIG['FROM']
    msg['To'] = recipient
    
    try:
        with smtplib.SMTP(SMTP_CONFIG['SERVER'], SMTP_CONFIG['PORT']) as server:
            server.starttls()
            server.login(SMTP_CONFIG['USERNAME'], SMTP_CONFIG['PASSWORD'])
            server.send_message(msg)
    except Exception as e:
        raise RuntimeError(f"Failed to send OTP: {str(e)}")

def verify_2fa(user_data, code):
    """Verify the 2FA code with time window tolerance"""
    if not user_data.get("2fa_enabled", False):
        return False
    
    secret = user_data.get("2fa_secret")
    if not secret:
        return False
    
    # Verify with 1-step window tolerance (current and previous OTP)
    totp = pyotp.TOTP(secret, interval=300)
    return totp.verify(code, valid_window=1) 