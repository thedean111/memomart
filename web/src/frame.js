import {getConfig, updateConfig} from './api.js';

// --------------------------------------------------------------
// Setup the input elements for camera settings
// --------------------------------------------------------------
export async function init() {
    const framePreview = document.getElementById("frame-preview");
    const config = await getConfig();

    const textConfigs = [
        {id: "event-name", key: "eventDescription"},
        {id: "event-location", key: "eventLocation"},
        {id: "event-date", key: "eventDate"}
    ];
    
    textConfigs.forEach(({ id, key }) => {
    
        const textInput = document.getElementById(id);

    
        if (!textInput) {
            return;
        }

        const input = textInput.querySelector("input");
        if (input && config[key] !== undefined) {
            input.value = config[key];
        }
    
        textInput.addEventListener("input", async (event) => {
    
            await updateConfig({
                [key]: event.target.value
            });

            // When the config is updated, we want to refresh the frame preview to reflect the new settings
            framePreview.src = `/api/preview?t=${Date.now()}`
    
        });
    });
}

// --------------------------------------------------------------
// Camera-specific cleanup goes here
// --------------------------------------------------------------
export function destroy() {
}