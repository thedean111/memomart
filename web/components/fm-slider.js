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