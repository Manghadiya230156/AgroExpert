const form = document.getElementById("loginForm");
const email = document.getElementById("email");
const password = document.getElementById("password");

const emailError = document.getElementById("emailError");
const passwordError = document.getElementById("passwordError");

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validateEmail() {
    emailError.textContent = "";
    email.classList.remove("input-error");

    if (email.value.trim() === "") {
        emailError.textContent = "Email is required";
        email.classList.add("input-error");
        return false;
    }

    if (!emailPattern.test(email.value.trim())) {
        emailError.textContent = "Enter valid email";
        email.classList.add("input-error");
        return false;
    }

    return true;
}

function validatePassword() {
    passwordError.textContent = "";
    password.classList.remove("input-error");

    if (password.value.trim() === "") {
        passwordError.textContent = "Password required";
        password.classList.add("input-error");
        return false;
    }

    return true;
}

form.addEventListener("submit", function (e) {

    const validEmail = validateEmail();
    const validPassword = validatePassword();

    // ❌ DO NOT block if valid
    if (!(validEmail && validPassword)) {
        e.preventDefault();
    }

});