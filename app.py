from flask import Flask, render_template, request, redirect, url_for, session, flash
from auth.level01 import register_user, login_user
from auth.level02 import setup_2fa
from auth.level03 import AVAILABLE_IMAGES,setup_image_authentication
from auth.models import UserData
from datetime import datetime, timedelta
from dateutil.parser import parse  # Add this import
from auth.auth_controller import handle_2fa_verification
from auth.level02 import verify_2fa as auth_verify_2fa
import os,random
from pathlib import Path
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management
# Custom filter to display auth images
@app.template_filter('auth_image')
def auth_image_filter(image_path):
    return url_for('static', filename=f'auth_images/{image_path}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        try:
            if password != confirm_password:
                raise ValueError("Passwords do not match")
                
            # Pass all required arguments correctly
            user_data = register_user(
                username=username,
                email=email,
                password=password
            )
            
            if user_data:
                # user_data.update(setup_2fa(user_data))
                # UserData.save_user_data(username, user_data)
                image_data = setup_image_authentication(username)
                user_data.update(image_data)
                UserData.save_user_data(username, user_data)
                flash('Registration successful! Please login.', 'success')
                return render_template('remember_images.html',
                                username=username,
                                auth_images=user_data['auth_images'])
                # return redirect(url_for('login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            if not login_user(username, password):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
            
            # Always generate and send new OTP
            user_data = UserData.load_user_data(username)
            if not user_data:
                flash('Account not found', 'danger')
                return redirect(url_for('login'))
            
            # Generate and store new OTP
            otp_data = setup_2fa(username)  # This sends the email
            user_data.update(otp_data)
            UserData.save_user_data(username, user_data)
            
            session['username'] = username
            flash('New verification code sent to your email', 'success')
            return redirect(url_for('verify_2fa'))
            return redirect(url_for('verify_image'))
            
        except Exception as e:
            flash(f'Login error: {str(e)}', 'danger')
    
    return render_template('login.html')
@app.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    # Check session first
    if 'username' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

    username = session['username']
    user_data = UserData.load_user_data(username)
    
    # Handle missing user data
    if not user_data:
        flash('User data not found', 'danger')
        return redirect(url_for('login'))

    # POST handling
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        
        if not code:
            flash('Please enter the verification code', 'danger')
        elif not code.isdigit() or len(code) != 6:
            flash('Invalid code format (must be 6 digits)', 'danger')
        else:
            try:
                # Import the auth function with alias to avoid naming conflict
                
                if auth_verify_2fa(user_data, code):
                    # Clear OTP after successful verification
                    user_data.pop('2fa_secret', None)
                    user_data.pop('last_otp_sent', None)
                    UserData.save_user_data(username, user_data)
                    return redirect(url_for('verify_image'))
                else:
                    flash('Invalid verification code', 'danger')
            except Exception as e:
                flash(f'Verification error: {str(e)}', 'danger')
    
    # GET handling or failed POST - must return a response
    last_sent = user_data.get('last_otp_sent')
    expires_in = 0
    
    if last_sent:
        try:
            # Handle both Python 3.7+ and older versions
            if hasattr(datetime, 'fromisoformat'):
                sent_time = datetime.fromisoformat(last_sent)
            else:
                from dateutil.parser import parse
                sent_time = parse(last_sent)
            
            expires_at = sent_time + timedelta(minutes=5)
            expires_in = max(0, (expires_at - datetime.now()).seconds // 60)
        except (ValueError, TypeError):
            expires_in = 0
    
    # This return statement was missing in your original code
    return render_template(
        'verify_2fa.html',
        expires_in=expires_in,
        email=user_data.get('email', '').split('@')[0]
    )

@app.route('/verify-image', methods=['GET', 'POST'])
def verify_image():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_data = UserData.load_user_data(username)
    
    if request.method == 'POST':
        selected_images = request.form.getlist('image_choice')  # Get multiple selections
        
        if len(selected_images) != 3:
            flash('Please select exactly 3 images', 'danger')
        else:
            from auth.level03 import verify_image_authentication
            if verify_image_authentication(user_data, selected_images):
                session['authenticated'] = True
                return redirect(url_for('dashboard'))
            else:
                flash('Incorrect image selection', 'danger')
    
    # Shuffle the images to prevent positional memorization
    all_images = random.sample(AVAILABLE_IMAGES, len(AVAILABLE_IMAGES))
    return render_template('verify_image.html',
                         all_images=all_images,
                         username=username)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/test-images')
def test_images():
    import os
    images = os.listdir(os.path.join(app.static_folder, 'auth_images'))
    return {
        'image_count': len(images),
        'images': images,
        'static_folder': app.static_folder
    }


if __name__ == '__main__':
    app.run(debug=True)