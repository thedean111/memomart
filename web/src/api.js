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