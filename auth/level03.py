import os
import random
from pathlib import Path

# Available authentication images
AVAILABLE_IMAGES = [
    "cat.jpg", "dog.jpg", "tree.jpg",
    "car.jpg", "house.jpg", "mountain.jpg"
]

def setup_image_authentication(username):
    """Select 3 random images for user authentication"""
    # Ensure images directory exists
    Path('static/auth_images').mkdir(parents=True, exist_ok=True)
    
    # Select 3 unique images
    selected_images = random.sample(AVAILABLE_IMAGES, 3)
    correct_image = random.choice(selected_images)
    
    return {
        "auth_images": selected_images,
        "correct_images": selected_images,  # Store all 3 for verification
        "selected_image": correct_image     # The one they need to select
    }

def verify_image_authentication(user_data, selected_images):
    """Verify user selected the correct images"""
    if not user_data.get('correct_images'):
        return False
    
    # Check if all selected images match the originals
    return set(selected_images) == set(user_data['correct_images'])