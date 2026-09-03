// SafeGuard AI - Interactive Scripts & Blackbox.ai-style Orange Grid Animation

// Dynamic UI Theme Switcher & Persistence
function switchTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('userTheme', theme);
}

document.addEventListener('DOMContentLoaded', () => {
    // Load saved theme preference
    const savedTheme = localStorage.getItem('userTheme') || 'cyber';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const themeSel = document.getElementById('themeSelect');
    if (themeSel) themeSel.value = savedTheme;

    // Mobile navigation menu toggle
    const mobileBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.getElementById('navLinks');

    if (mobileBtn && navLinks) {
        mobileBtn.addEventListener('click', () => {
            navLinks.classList.toggle('show');
        });
    }
});

// Auto detect location helper function
function getCurrentLocation(latInputId, lngInputId, statusElementId) {
    const statusEl = statusElementId ? document.getElementById(statusElementId) : null;
    const latInput = document.getElementById(latInputId);
    const lngInput = document.getElementById(lngInputId);

    if (statusEl) {
        statusEl.innerText = "Detecting your location...";
        statusEl.style.color = "#3b82f6";
    }

    if (!navigator.geolocation) {
        if (statusEl) {
            statusEl.innerText = "Geolocation is not supported by your browser.";
            statusEl.style.color = "#ef4444";
        }
        return;
    }

    navigator.geolocation.getCurrentPosition(
        (position) => {
            if (latInput) latInput.value = position.coords.latitude.toFixed(6);
            if (lngInput) lngInput.value = position.coords.longitude.toFixed(6);
            if (statusEl) {
                statusEl.innerText = "Location detected successfully!";
                statusEl.style.color = "#10b981";
            }
        },
        (error) => {
            if (statusEl) {
                statusEl.innerText = "Failed to detect location: " + error.message;
                statusEl.style.color = "#ef4444";
            }
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
}
