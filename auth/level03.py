import random
from auth.models import UserData
from auth.utils import get_valid_input

# Predefined set of image descriptions
IMAGE_DESCRIPTIONS = {
    1: "Red Apple",
    2: "Blue Car",
    3: "Green Tree",
    4: "Yellow Sun",
    5: "Black Cat",
    6: "White Cloud",
    7: "Orange Ball",
    8: "Purple Flower",
    9: "Brown Dog",
    10: "Gray Mountain"
}

SELECTION_COUNT = 3  # Number of images user must select

def setup_image_authentication():
    """Setup text-based image selection during registration"""
    print("\n--- Level 3: Image Authentication Setup ---")
    print(f"Please select {SELECTION_COUNT} images from the following options:")
    
    # Display available images
    display_image_options()
    
    # Get user selections
    selected_indices = []
    while len(selected_indices) < SELECTION_COUNT:
        try:
            choice = int(input(f"Select image {len(selected_indices)+1} (1-10): "))
            if 1 <= choice <= 10:
                if choice not in selected_indices:
                    selected_indices.append(choice)
                    print(f"Selected: {IMAGE_DESCRIPTIONS[choice]}")
                else:
                    print("You already selected that image.")
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Store the selected image numbers (e.g., [3, 7, 1])
    return {"image_selection": sorted(selected_indices)}

def verify_image_authentication(user_data):
    """Verify image selections during login"""
    print("\n--- Level 3: Image Authentication ---")
    print(f"Please select your {SELECTION_COUNT} previously chosen images:")
    
    # Get correct answers from user data
    correct_selections = user_data.get("image_selection", [])
    if not correct_selections or len(correct_selections) != SELECTION_COUNT:
        print("Error: Image authentication not properly set up.")
        return False
    
    # Display available images in random order
    display_image_options(shuffle=True)
    
    # Get user selections
    selected_indices = []
    while len(selected_indices) < SELECTION_COUNT:
        try:
            choice = int(input(f"Select image {len(selected_indices)+1} (1-10): "))
            if 1 <= choice <= 10:
                if choice not in selected_indices:
                    selected_indices.append(choice)
                    print(f"Selected: {IMAGE_DESCRIPTIONS[choice]}")
                else:
                    print("You already selected that image.")
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Verify selections (order doesn't matter)
    if sorted(selected_indices) == sorted(correct_selections):
        return True
    
    print("Incorrect image selections.")
    return False

def display_image_options(shuffle=False):
    """Display the available image options"""
    print("\nAvailable Images:")
    items = list(IMAGE_DESCRIPTIONS.items())
    
    if shuffle:
        random.shuffle(items)
    
    for num, desc in items:
        print(f"{num}: {desc}")