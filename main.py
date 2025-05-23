from auth.level01 import register_user, login_user
from auth.level02 import setup_2fa, verify_2fa
from auth.level03 import setup_image_authentication, verify_image_authentication
from auth.models import UserData

def main():
    print("Welcome to the Three-Level Security System")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            user_data = register_user()
            if user_data:
                # Add 2FA setup
                user_data.update(setup_2fa())
                # Add security question
                user_data.update(setup_image_authentication())
                # Save complete user data
                UserData.save_user_data(user_data["username"], user_data)
                print("Registration successful!")
                print("You can now login with your credentials.")
        
        elif choice == "2":
            username = input("Enter username: ")
            if login_user(username):
                user_data = UserData.load_user_data(username)
                try:
                    if verify_2fa(user_data):
                        print("\n✓ Level 2 passed: 2FA code verified")
                        if verify_image_authentication(user_data):
                            print("Image authentication successful!")
                            print("\n=== LOGIN SUCCESSFUL! ===")
                            print("Welcome, " + username + "!")
                            break;
                        else:
                             print("Image authentication failed.")
                    else:
                        print("\n✗ Login failed: Incorrect 2FA code")
                except Exception as e:
                    print(f"\n✗ Login failed: Error in 2FA process - {str(e)}")
            else:
                print("Password authentication failed.")
        
        elif choice == "3":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()