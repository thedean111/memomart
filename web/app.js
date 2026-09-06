import { router } from "./src/router.js";
import "./components/fm-slider.js";

// Run router when the application first loads
window.addEventListener("DOMContentLoaded", router);

// Run router whenever the URL hash changes
window.addEventListener("hashchange", router);