import { login } from "./api.js";

export function init() {
    const loginButton = document.getElementById("submit-login-button");
    loginButton.addEventListener("click", handleLogin);
}

async function handleLogin() {
    const username = document.getElementById("in_username").value;
    const password = document.getElementById("in_password").value;

    // An error will be thrown if credentials are invalid, 
    // so we can catch it and display an error message
    try {
        await login({
            "username": username,
            "password": password
        });
        window.location.hash = "#/dashboard";
    } catch (error) {
        console.log(error.message);
        alert("Login failed: " + error.message);
    }
}