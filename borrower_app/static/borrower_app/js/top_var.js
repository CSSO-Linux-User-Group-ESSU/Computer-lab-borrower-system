// Get current URL path to set the active state
const currentUrl = window.location.pathname;

// Select all navigation links
const navLinks = document.querySelectorAll('.nav-hover');

// Loop through each link and apply the active class based on the current URL
navLinks.forEach(link => {
    if (link.href.includes(currentUrl)) {
        link.classList.add('nav-active'); // Add 'nav-active' class to the active link
    }
});
