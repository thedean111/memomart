import {attemptWifiConnection, disconnectWifi} from './api.js';

// --------------------------------------------------------------
// Init the components on the wifi page
// --------------------------------------------------------------
export async function init() {
    const connectButton = document.getElementById("connect-wifi-button");
    connectButton.addEventListener("click", handleConnect);

    const disconnectButton = document.getElementById("disconnect-wifi-button");
    disconnectButton.addEventListener("click", handleDisconnect);
}

async function handleConnect() {
    const ssid = document.getElementById("wifi_ssid").value;
    const pswd = document.getElementById("wifi_password").value;

    // An error will be thrown if credentials are invalid, 
    // so we can catch it and display an error message
    try {
        await attemptWifiConnection({
            "ssid": ssid,
            "password": pswd
        });
    } catch (error) {
        console.log(error.message);
        alert("Login failed: " + error.message);
    }
}

async function handleDisconnect() {
    try {
        await disconnectWifi()
    } catch (error) {
        console.log(error.message);
        alert("Disconnect failed: " + error.message);
    }
}

// --------------------------------------------------------------
// Clean-up components on the dashboard page
// --------------------------------------------------------------
export function destroy() {
}