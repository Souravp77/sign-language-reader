// ===== ALL AUTHENTICATION JAVASCRIPT =====

document.addEventListener('DOMContentLoaded', function() {
    // Initialize based on current page
    if (document.getElementById('loginForm')) {
        initLoginPage();
    } else if (document.getElementById('registerForm')) {
        initRegisterPage();
    }
    
    // Common setup for both pages
    initCommonFeatures();
});

// ===== COMMON FUNCTIONS =====
function initCommonFeatures() {
    // Auto-close flash messages after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.flash-msg').forEach(msg => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300);
        });
    }, 5000);
    
    // Setup password visibility toggle
    document.querySelectorAll('.toggle-password').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.closest('.password-wrapper')
                          .querySelector('.form-input');
            if (input) {
                // Toggle password visibility
                input.type = input.type === 'password' ? 'text' : 'password';
                
                // Toggle eye icon
                const icon = this.querySelector('i');
                if (icon) {
                    icon.classList.toggle('bi-eye');
                    icon.classList.toggle('bi-eye-slash');
                }
            }
        });
    });
    
    // Close flash messages on button click
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('flash-close')) {
            e.target.parentElement.remove();
        }
    });
}

function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showError(input, message) {
    // Clear any existing error first
    clearError(input);
    
    // Add invalid class to input
    input.classList.add('invalid');
    
    // Show error message
    const errorId = input.id + 'Error';
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

function clearError(input) {
    input.classList.remove('invalid');
    const errorId = input.id + 'Error';
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
        errorElement.style.display = 'none';
    }
}

function showLoading(button, text) {
    if (button) {
        button.dataset.originalText = button.innerHTML;
        button.innerHTML = `<i class="bi bi-arrow-repeat spin"></i> ${text}`;
        button.disabled = true;
        
        // Re-enable button after 3 seconds (fallback)
        setTimeout(() => {
            if (button.disabled) {
                button.innerHTML = button.dataset.originalText;
                button.disabled = false;
            }
        }, 3000);
    }
}

// ===== LOGIN PAGE =====
function initLoginPage() {
    const form = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    
    // Clear errors when user types
    [emailInput, passwordInput].forEach(input => {
        input.addEventListener('input', () => clearError(input));
    });
    
    // Form submission
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Validate email
        if (!validateEmail(emailInput.value)) {
            showError(emailInput, 'Please enter a valid email address');
            isValid = false;
        }
        
        // Validate password
        if (passwordInput.value.length < 6) {
            showError(passwordInput, 'Password must be at least 6 characters');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
        } else {
            showLoading(this.querySelector('.btn-primary'), 'Signing in...');
        }
    });
}

// ===== REGISTER PAGE =====
function initRegisterPage() {
    const form = document.getElementById('registerForm');
    const passwordInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirm_password');
    const strengthElement = document.getElementById('passwordStrength');
    
    // Clear errors when user types
    form.querySelectorAll('.form-input').forEach(input => {
        input.addEventListener('input', () => {
            clearError(input);
            
            // Special handling for password strength
            if (input.id === 'password' && strengthElement) {
                updatePasswordStrength(input.value, strengthElement);
            }
            
            // Check password match
            if (input.id === 'password' || input.id === 'confirm_password') {
                checkPasswordMatch(passwordInput, confirmInput);
            }
        });
    });
    
    // Form submission
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Validate username
        const usernameInput = document.getElementById('username');
        if (usernameInput.value.length < 3) {
            showError(usernameInput, 'Username must be at least 3 characters');
            isValid = false;
        }
        
        // Validate email
        const emailInput = document.getElementById('email');
        if (!validateEmail(emailInput.value)) {
            showError(emailInput, 'Please enter a valid email address');
            isValid = false;
        }
        
        // Validate password
        if (passwordInput.value.length < 6) {
            showError(passwordInput, 'Password must be at least 6 characters');
            isValid = false;
        }
        
        // Check password match
        if (!checkPasswordMatch(passwordInput, confirmInput)) {
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
        } else {
            showLoading(this.querySelector('.btn-primary'), 'Creating account...');
        }
    });
}

function updatePasswordStrength(password, element) {
    if (!password) {
        element.style.display = 'none';
        return;
    }
    
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    element.style.display = 'block';
    
    if (strength <= 1) {
        element.textContent = 'Weak password';
        element.className = 'password-strength strength-weak';
    } else if (strength <= 3) {
        element.textContent = 'Medium strength';
        element.className = 'password-strength strength-medium';
    } else {
        element.textContent = 'Strong password';
        element.className = 'password-strength strength-strong';
    }
}

function checkPasswordMatch(passwordInput, confirmInput) {
    const errorElement = document.getElementById('confirmError');
    
    if (!passwordInput || !confirmInput || !errorElement) {
        return true;
    }
    
    if (passwordInput.value !== confirmInput.value && confirmInput.value) {
        confirmInput.classList.add('invalid');
        errorElement.style.display = 'block';
        return false;
    } else {
        confirmInput.classList.remove('invalid');
        errorElement.style.display = 'none';
        return true;
    }
}