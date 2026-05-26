const form = document.getElementById("signupForm");

const username = document.getElementById("username");
const fullname = document.getElementById("fullname");
const email = document.getElementById("email");
const phone = document.getElementById("phone");
const password = document.getElementById("password");
const confirmPassword = document.querySelector('input[name="confirm_password"]');
const locationField = document.getElementById("location");

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const phonePattern = /^[0-9]{10}$/;
const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

function setError(input, message) {
    const error = document.getElementById(input.id + "Error");
    if (error) error.textContent = message;
    input.classList.add("input-error");
}

function clearError(input) {
    const error = document.getElementById(input.id + "Error");
    if (error) error.textContent = "";
    input.classList.remove("input-error");
}

function validateField(input, condition, message) {
    if (!condition) {
        setError(input, message);
        return false;
    }
    clearError(input);
    return true;
}

form.addEventListener("submit", function(e){

    let valid = true;

    valid = validateField(username, username.value.trim() !== "", "Username required") && valid;
    valid = validateField(fullname, fullname.value.trim() !== "", "Full name required") && valid;
    valid = validateField(email, emailPattern.test(email.value.trim()), "Valid email required") && valid;
    valid = validateField(phone, phonePattern.test(phone.value.trim()), "Enter 10 digit phone") && valid;
    valid = validateField(password, passwordPattern.test(password.value), "Weak password") && valid;

    if(confirmPassword.value !== password.value){
        valid = false;
        alert("Passwords do not match");
    }

    valid = validateField(locationField, locationField.value.trim() !== "", "Location required") && valid;

    if(!valid){
        e.preventDefault();
    }

});