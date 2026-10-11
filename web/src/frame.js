import {getConfig, updateConfig, updateBrandImage} from './api.js';

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

    const sliderConfigs = [
        {id: "brand-image-offset-x", key: "brandImageOffsetX"},
        {id: "brand-image-offset-y", key: "brandImageOffsetY"},
        {id: "brand-image-width", key: "brandImageWidth"},
        {id: "brand-image-height", key: "brandImageHeight"},
        {id: "brand-image-opacity", key: "brandImageOpacity"}
    ];
    sliderConfigs.forEach(({ id, key }) => {
    
        const slider = document.getElementById(id);
    
        if (!slider) {
            return;
        }
    
        const input = slider.querySelector("input");
    
        if (input && config[key] !== undefined) {
            input.value = config[key];
        }
    
    
        slider.addEventListener("input", async (event) => {
    
            await updateConfig({
                [key]: Number(event.target.value)
            });

            // When the config is updated, we want to refresh the frame preview to reflect the new settings
            framePreview.src = `/api/preview?t=${Date.now()}`
    
        });
    });

    document.getElementById("upload-image").addEventListener("click", async () => {
        const fileInput = document.getElementById("brand-image");
        const uploadStatus = document.getElementById("upload-status");
        if (!fileInput.files.length) {
            uploadStatus.textContent = "Please select an image to upload.";
            return;
        }
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append("brand-image", file);
        try {
            await updateBrandImage(formData);
            uploadStatus.textContent = "Image uploaded successfully.";
            framePreview.src = `/api/preview?t=${Date.now()}`;
        } catch (error) {
            uploadStatus.textContent = "Error uploading image.";
        }
    });
}

// --------------------------------------------------------------
// Camera-specific cleanup goes here
// --------------------------------------------------------------
export function destroy() {
}