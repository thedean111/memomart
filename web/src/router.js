
import {getAuth} from "./api.js";

// --------------------------------------------------------------
// Map a route to the actual page layout we want to display
// --------------------------------------------------------------
const routes = {
    "/wifi": {
        page: "/pages/wifi.html",
        module: () => import("./wifi.js"),
        navID: "wifi-nav",
        requiresAuth: true
    },

    "/frame": {
        page: "/pages/frame.html",
        module: () => import("./frame.js"),
        navID: "frame-nav",
        requiresAuth: true
    },

    "/camera": {
        page: "/pages/camera.html",
        module: () => import("./camera.js"),
        navID: "camera-nav",
        requiresAuth: true
    },

    "/login": {
        page: "/pages/login.html",
        module: () => import("./login.js"),
        navID: null,
        requiresAuth: false
    }
};

let currentPage = null;
let currentElement = null;

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
        updateSelectedPage(null);
        return;
    }

    // Get authentication status from the backend once
    const authenticated = await getAuth();
    console.log("Authenticated (router):", authenticated);

    // If the desired pages needs authentication, red
    if (route.requiresAuth) {
        if (!authenticated) {
            updateSelectedPage(null);
            window.location.hash = "#/login";
            return;
        }
    }

    // If already logged in, don't show login page
    if (path === "/login") {
        if (authenticated) {
            window.location.hash = "#/frame";
            updateSelectedPage(routes["/frame"].navID);
            return;
        }
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
    updateSelectedPage(route.navID);
    currentPage = await route.module();
    if (currentPage.init) {
        await currentPage.init();
    }
}

function updateSelectedPage(newElement) {
    if (currentElement) {
        document.getElementById(currentElement)?.classList.remove("nav-item-focused");
    }

    if (!newElement) {
        currentElement = null;
        return;
    }

    document.getElementById(newElement)?.classList.add("nav-item-focused");
    currentElement = newElement;
}