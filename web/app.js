document.addEventListener("DOMContentLoaded", async () => {
  try {
    // 1. Fetch the JSON from your endpoint
    const response = await fetch('/api/config');
    if (!response.ok) {
      throw new Error('Failed to load configuration');
    }
    
    const config = await response.json();
    
    // Define the mappings for your sliders
    const sliderConfigs = [
      { id: 'brightness-slider', key: 'brightness' },
      { id: 'gain-slider', key: 'gain' },
      { id: 'exposure-slider', key: 'exposure' }
    ];

    // 2. Map JSON properties and add event listeners
    sliderConfigs.forEach(({ id, key }) => {
      const sliderEl = document.getElementById(id);
      if (!sliderEl) return;

      // Set min and max attributes (triggers attributeChangedCallback -> render())
      sliderEl.setAttribute('min', config[`min_${key}`]);
      sliderEl.setAttribute('max', config[`max_${key}`]);

      // Find the inner range input and set its initial current value
      const input = sliderEl.querySelector('input');
      if (input && config[key] !== undefined) {
        input.value = config[key];
      }

      // 3. Event listener using event bubbling to catch changes from the inner input
      sliderEl.addEventListener('input', async (e) => {
        const newValue = e.target.value;

        try {
          const updateResponse = await fetch('/api/config', {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            // Sends JSON matching what request.get_json() expects on your Flask backend
            body: JSON.stringify({ [key]: Number(newValue) })
          });

          if (!updateResponse.ok) {
            console.error(`Failed to update configuration for ${key}`);
          }
        } catch (err) {
          console.error('Error sending config update:', err);
        }
      });
    });

  } catch (error) {
    console.error('Error loading config:', error);
  }
});    
    
    
class FMSlider extends HTMLElement {
constructor() {
    super();
}

// 1. Tell the browser which attributes to watch for changes
static get observedAttributes() {
    return ['min', 'max', 'step', 'label'];
}

// 2. This runs when the element is first added to the page
connectedCallback() {
    this.render();
}

// 3. This runs whenever one of the observed attributes changes
attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) {
    this.render();
    }
}

// 4. Build the actual HTML inside your custom element
render() {
    // Read the custom attributes (with fallbacks if they are missing)
    const min = this.getAttribute('min') || '0';
    const max = this.getAttribute('max') || '100';
    const step = this.getAttribute('step') || '1';
    const label = this.getAttribute('label') || 'Slider';

    // Inject standard HTML inside your custom tag
    this.innerHTML = `
    <div class="slider-layout">
        <label class="slider-text">${label}</label>
        <input type="range" min="${min}" max="${max}" step="${step}">
    </div>
    `;
}
}

// Register the new element with the browser
customElements.define('fm-slider', FMSlider);