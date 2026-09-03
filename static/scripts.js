// SafeGuard AI - Interactive Scripts, Mobile Touch Support & Smooth Orange Grid Canvas

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

    // 🟧 SMOOTH MOBILE & DESKTOP INTERACTIVE ORANGE GRID CANVAS
    initInteractiveGridCanvas();
});

function initInteractiveGridCanvas() {
    const canvas = document.getElementById('interactiveGridCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d', { alpha: true });
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    let mouseX = -1000;
    let mouseY = -1000;
    let targetX = -1000;
    let targetY = -1000;

    const isMobile = window.innerWidth < 768;
    const gridSize = isMobile ? 55 : 42; // Larger grid size on mobile for 4x GPU speedup
    const maxRadius = isMobile ? 140 : 180;

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }, { passive: true });

    // Desktop Mouse listeners
    window.addEventListener('mousemove', (e) => {
        targetX = e.clientX;
        targetY = e.clientY;
    }, { passive: true });

    window.addEventListener('mouseleave', () => {
        targetX = -1000;
        targetY = -1000;
    }, { passive: true });

    // Mobile Touchscreen listeners (iPhone, Android, Tablets)
    window.addEventListener('touchstart', (e) => {
        if (e.touches && e.touches[0]) {
            targetX = e.touches[0].clientX;
            targetY = e.touches[0].clientY;
        }
    }, { passive: true });

    window.addEventListener('touchmove', (e) => {
        if (e.touches && e.touches[0]) {
            targetX = e.touches[0].clientX;
            targetY = e.touches[0].clientY;
        }
    }, { passive: true });

    window.addEventListener('touchend', () => {
        setTimeout(() => {
            targetX = -1000;
            targetY = -1000;
        }, 1200);
    }, { passive: true });

    function drawGrid() {
        // Smooth linear interpolation (lerp) for liquid-smooth animation on mobile touchscreens
        mouseX += (targetX - mouseX) * 0.15;
        mouseY += (targetY - mouseY) * 0.15;

        ctx.clearRect(0, 0, width, height);

        const cols = Math.ceil(width / gridSize);
        const rows = Math.ceil(height / gridSize);

        // Draw ambient subtle grid lines
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

        // Bounded grid highlight rendering (Fast & Smooth performance)
        if (mouseX > -500 && mouseY > -500) {
            const startCol = Math.max(0, Math.floor((mouseX - maxRadius) / gridSize));
            const endCol = Math.min(cols, Math.ceil((mouseX + maxRadius) / gridSize));
            const startRow = Math.max(0, Math.floor((mouseY - maxRadius) / gridSize));
            const endRow = Math.min(rows, Math.ceil((mouseY + maxRadius) / gridSize));

            for (let i = startCol; i < endCol; i++) {
                for (let j = startRow; j < endRow; j++) {
                    const cellX = i * gridSize;
                    const cellY = j * gridSize;
                    const centerX = cellX + gridSize / 2;
                    const centerY = cellY + gridSize / 2;

                    const dist = Math.hypot(mouseX - centerX, mouseY - centerY);

                    if (dist < maxRadius) {
                        const intensity = Math.pow(1 - dist / maxRadius, 2);

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
