function validatePasswords() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const errorElement = document.getElementById('passwordError');
    
    if (password.value !== confirmPassword.value) {
        errorElement.textContent = "Passwords do not match";
        password.classList.add('is-invalid');
        confirmPassword.classList.add('is-invalid');
        return false;
    }
    
    if (password.value.length < 8) {
        errorElement.textContent = "Password must be at least 8 characters";
        password.classList.add('is-invalid');
        return false;
    }
    
    return true;
}

document.getElementById('password').addEventListener('input', function() {
    this.classList.remove('is-invalid');
    document.getElementById('passwordError').textContent = '';
});

document.getElementById('confirm_password').addEventListener('input', function() {
    this.classList.remove('is-invalid');
    document.getElementById('passwordError').textContent = '';
});

document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.image-checkbox input[type="checkbox"]');
    const maxSelections = 3;
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const checkedCount = document.querySelectorAll('.image-checkbox input[type="checkbox"]:checked').length;
            
            if (checkedCount > maxSelections) {
                this.checked = false;
                alert(`Please select only ${maxSelections} images`);
            }
        });
    });
});