import {getConfig, updateConfig} from './api.js';

// --------------------------------------------------------------
// Setup the input elements for camera settings
// --------------------------------------------------------------
export async function init() {

    const config = await getConfig();

    const sliderConfigs = [
        {id: "brightness-slider", key: "brightness"},
        {id: "gain-slider", key: "gain"},
        {id: "exposure-slider", key: "exposure"}
    ];
    
    sliderConfigs.forEach(({ id, key }) => {
    
        const slider = document.getElementById(id);
    
        if (!slider) {
            return;
        }
    
        slider.setAttribute(
            "min",
            config[`min_${key}`]
        );
    
        slider.setAttribute(
            "max",
            config[`max_${key}`]
        );
    
        const input = slider.querySelector("input");
    
        if (input && config[key] !== undefined) {
            input.value = config[key];
        }
    
    
        slider.addEventListener("input", async (event) => {
    
            await updateConfig({
                [key]: Number(event.target.value)
            });
    
        });
    });
}

// --------------------------------------------------------------
// Camera-specific cleanup goes here
// --------------------------------------------------------------
export function destroy() {
}