// --------------------------------------------------------------
// THESE ENDPOINTS SHOULD MAP TO THE BACKEND API ENDPOINTS
// --------------------------------------------------------------
// -- Get all configuration settings -- //
export async function getConfig() {

    const response = await fetch("/api/config");

    if (!response.ok) {
        throw new Error("Failed to load configuration");
    }

    return await response.json();
}

// -- Send new configuration settings to application -- //
export async function updateConfig(changes) {
    console.log("Updating config with changes:", changes);
    const response = await fetch("/api/config", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(changes)
    });

    if (!response.ok) {
        throw new Error("Failed to update configuration");
    }

    return await response.json();
}

// -- Get authentication status -- //
export async function getAuth() {
    const response = await fetch("/api/auth");
    console.log(response);

    if (!response.ok) {
        throw new Error("Failed to get authentication status");
    }

    const data = await response.json();
    console.log("Authenticated:", data.authenticated);
    return data.authenticated;
}

// -- Attempt to login with the credentials -- //
export async function login(credentials) {
    const response = await fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(credentials)
    });

    const data = await response.json();
    console.log(data);
    if (!response.ok) {
        throw new Error(data.error || "Login failed");
    }

    return data;
}

// -- Attempt to connect to the wifi with the credentials -- //
export async function attemptWifiConnection(info) {
    const response = await fetch("/api/wifi/connect", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(info)
    });

    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || " Connection failed");
    }
}

// -- Disconnect from the wifi -- //
export async function disconnectWifi() {
    const response = await fetch("/api/wifi/disconnect", {
        method: "POST"
    });
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || "Failed to disconnect");
    }
    return await response.json();
}