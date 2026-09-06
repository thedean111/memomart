// --------------------------------------------------------------
// Map a route to the actual page layout we want to display
// --------------------------------------------------------------
const routes = {
    "/dashboard": {
        page: "/pages/dashboard.html",
        module: () => import("./dashboard.js")
    },

    "/camera": {
        page: "/pages/camera.html",
        module: () => import("./camera.js")
    },

    "/login": {
        page: "/pages/login.html",
        module: () => import("./login.js")
    }
};
let currentPage = null;

// --------------------------------------------------------------
// Map a route to the actual page layout we want to display
// --------------------------------------------------------------
export async function router() {
    let path = window.location.hash.substring(1);

    // default to login page
    if (!path) {
        path = "/login";
    }

    // Get the file location of the page from the route mappings
    const route =  routes[path];

    // Switch the window to the login page if there is no valid route
    if (!route) {
        window.location.hash = "#/login";
        return;
    }

    // Clean up the previous page
    if (currentPage?.destroy) {
        currentPage.destroy();
    }

    const response = await fetch(route.page);

    if (!response.ok) {
        throw new Error(`Failed to load ${route.page}`);
    }

    // Set the HTML
    document.getElementById("app").innerHTML = await response.text();


    // Load the page's JavaScript
    currentPage = await route.module();
    if (currentPage.init) {
        await currentPage.init();
    }
}