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

    // 🟧 BLACKBOX.AI-STYLE INTERACTIVE ORANGE GRID CANVAS ANIMATION
    initInteractiveGridCanvas();
});

function initInteractiveGridCanvas() {
    const canvas = document.getElementById('interactiveGridCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    let mouseX = -1000;
    let mouseY = -1000;

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    window.addEventListener('mouseleave', () => {
        mouseX = -1000;
        mouseY = -1000;
    });

    const gridSize = 45; // 45px square grid cells

    function drawGrid() {
        ctx.clearRect(0, 0, width, height);

        const cols = Math.ceil(width / gridSize);
        const rows = Math.ceil(height / gridSize);

        // Draw ambient subtle grid background lines
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
        ctx.lineWidth = 1;

        for (let i = 0; i <= cols; i++) {
            ctx.beginPath();
            ctx.moveTo(i * gridSize, 0);
            ctx.lineTo(i * gridSize, height);
            ctx.stroke();
        }

        for (let j = 0; j <= rows; j++) {
            ctx.beginPath();
            ctx.moveTo(0, j * gridSize);
            ctx.lineTo(width, j * gridSize);
            ctx.stroke();
        }

        // Draw mouse-following glowing orange square grid highlights
        for (let i = 0; i < cols; i++) {
            for (let j = 0; j < rows; j++) {
                const cellX = i * gridSize;
                const cellY = j * gridSize;
                const centerX = cellX + gridSize / 2;
                const centerY = cellY + gridSize / 2;

                const dist = Math.hypot(mouseX - centerX, mouseY - centerY);
                const maxRadius = 180; // Glowing radius around cursor

                if (dist < maxRadius) {
                    const intensity = Math.pow(1 - dist / maxRadius, 2); // Smooth quadratic fade

                    // Glowing orange square fill
                    ctx.fillStyle = `rgba(249, 115, 22, ${intensity * 0.35})`;
                    ctx.fillRect(cellX + 2, cellY + 2, gridSize - 4, gridSize - 4);

                    // Bright glowing orange border
                    ctx.strokeStyle = `rgba(249, 115, 22, ${intensity * 0.8})`;
                    ctx.lineWidth = 1.5;
                    ctx.strokeRect(cellX + 1, cellY + 1, gridSize - 2, gridSize - 2);
                }
            }
        }

        requestAnimationFrame(drawGrid);
    }

    drawGrid();
}

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
