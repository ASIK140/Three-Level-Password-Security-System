# auth/level02.py
import random
import smtplib
from email.mime.text import MIMEText
from auth.config import EMAIL_CONFIG
from auth.utils import get_valid_input

def send_verification_email(receiver_email, verification_code):
    """Send email with verification code"""
    message = MIMEText(f'Your verification code is: {verification_code}')
    message['Subject'] = EMAIL_CONFIG['EMAIL_SUBJECT']
    message['From'] = EMAIL_CONFIG['SENDER_EMAIL']
    message['To'] = receiver_email

    try:
        with smtplib.SMTP(
            EMAIL_CONFIG['SMTP_SERVER'],
            EMAIL_CONFIG['SMTP_PORT']
        ) as server:
            server.starttls()
            server.login(
                EMAIL_CONFIG['SENDER_EMAIL'],
                EMAIL_CONFIG['SENDER_PASSWORD']
            )
            server.send_message(message)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def setup_2fa():
    """Setup two-factor authentication during registration"""
    print("\n--- Two-Factor Authentication Setup ---")
    while True:
        email = get_valid_input("Enter email for 2FA: ")
        if '@' in email and '.' in email:  # Basic email validation
            return {"email": email}
        print("Please enter a valid email address.")

def verify_2fa(user_data):
    """Verify two-factor authentication code"""
    print("\n--- Level 2: Two-Factor Authentication ---")
    email = user_data["email"]
    verification_code = str(random.randint(100000, 999999))
    
    # Send actual email
    if not send_verification_email(email, verification_code):
        print("Failed to send verification email. Using fallback method.")
        print(f"[FALLBACK] Your verification code is: {verification_code}")
    
    attempts = 3
    while attempts > 0:
        user_code = input("Enter the 6-digit verification code: ").strip()
        
        if user_code == verification_code:
            return True
        
        attempts -= 1
        if attempts > 0:
            print(f"Incorrect code. {attempts} attempts remaining.")
    
    print("Too many incorrect attempts.")
    return False