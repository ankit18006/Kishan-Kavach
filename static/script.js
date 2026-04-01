// ===== KISHAN KAVACH - MAIN SCRIPT =====

document.addEventListener("DOMContentLoaded", function () {
    const lang = localStorage.getItem("lang") || "hi";
    setLanguage(lang);
});

document.addEventListener('DOMContentLoaded', function() {
    // ===== LANDING PAGE LOGIC =====
    initLandingPage();

    // ===== DASHBOARD LOGIC =====
    initDashboard();
});


const translations = {
    hi: {
        temp: "तापमान",
        humidity: "नमी",
        gas: "गैस स्तर",
        battery: "बैटरी",
        spoilage: "खराब होने का जोखिम",
        dashboard: "डैशबोर्ड",
        devices: "डिवाइस",
        requests: "अनुरोध",
        weather: "मौसम",
        logout: "लॉगआउट"
    },
    en: {
        temp: "Temperature",
        humidity: "Humidity",
        gas: "Gas Level",
        battery: "Battery",
        spoilage: "Spoilage Risk",
        dashboard: "Dashboard",
        devices: "Devices",
        requests: "Requests",
        weather: "Weather",
        logout: "Logout"
    }
};

function setLanguage(lang) {
    localStorage.setItem("lang", lang);

    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });
}

// ===========================
// LANDING PAGE
// ===========================

function initLandingPage() {
    const navbar = document.getElementById('navbar');
    const mobileToggle = document.getElementById('mobileToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    // Scroll effect for navbar
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Mobile menu toggle
    if (mobileToggle && mobileMenu) {
        mobileToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
        });

        // Close mobile menu on link click
        mobileMenu.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                mobileMenu.classList.remove('active');
            });
        });
    }

    // Scroll animations
    initScrollAnimations();
}

function initScrollAnimations() {
    const elements = document.querySelectorAll('.fade-up');

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        elements.forEach(function(el) {
            // Don't pause if in hero (already visible)
            if (!el.closest('.hero')) {
                el.style.animationPlayState = 'paused';
            }
            observer.observe(el);
        });
    }
}

// ===========================
// DASHBOARD
// ===========================

let socket = null;
let sensorChart = null;
let currentDeviceId = null;

function initDashboard() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    const deviceSelector = document.getElementById('deviceSelector');

    // Check if we're on dashboard page
    if (!sidebar) return;

    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    overlay.id = 'sidebarOverlay';
    document.body.appendChild(overlay);

    // Sidebar toggle (mobile)
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        });
    }

    overlay.addEventListener('click', function() {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });

    // Sidebar navigation
    sidebarLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.getAttribute('data-section');
            switchSection(section);

            // Close sidebar on mobile
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
    });

    // Device selector
    if (deviceSelector) {
        deviceSelector.addEventListener('change', function() {
            currentDeviceId = this.value;
            loadDeviceData(currentDeviceId);
            loadChartData(currentDeviceId);
        });

        // Set initial device
        currentDeviceId = deviceSelector.value;
        if (currentDeviceId) {
            loadDeviceData(currentDeviceId);
            loadChartData(currentDeviceId);
        }
    }

    // Initialize Socket.IO
    initSocket();

    // Initialize chart
    initChart();

    // Auto-dismiss flash messages
    setTimeout(function() {
        document.querySelectorAll('.alert').forEach(function(el) {
            el.style.opacity = '0';
            setTimeout(function() { el.remove(); }, 300);
        });
    }, 5000);
}

function switchSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(function(sec) {
        sec.classList.remove('active');
    });

    // Show target section
    const target = document.getElementById('section-' + sectionName);
    if (target) {
        target.classList.add('active');
    }

    // Update sidebar active state
    document.querySelectorAll('.sidebar-link').forEach(function(link) {
        link.classList.remove('active');
        if (link.getAttribute('data-section') === sectionName) {
            link.classList.add('active');
        }
    });
}

// ===========================
// SOCKET.IO
// ===========================
function initSocket() {
    if (typeof io === 'undefined') return;

    socket = io();

    socket.on('connect', function() {
        console.log('[WS] Connected to server');
    });

    socket.on('disconnect', function() {
        console.log('[WS] Disconnected from server');
    });

    socket.on('sensor_update', function(data) {
        console.log('[WS] Sensor update:', data);

        // Only update if this device is currently selected
        if (data.device_id === currentDeviceId) {
            updateSensorCards(data);
            addChartDataPoint(data);
        }
    });

    socket.on('error', function(data) {
        console.error('[WS] Error:', data.message);
    });
}

// ===========================
// SENSOR CARDS
// ===========================
function updateSensorCards(data) {
    const tempEl = document.getElementById('tempValue');
    const humidityEl = document.getElementById('humidityValue');
    const gasEl = document.getElementById('gasValue');
    const batteryEl = document.getElementById('batteryValue');
    const spoilageEl = document.getElementById('spoilageValue');
    const spoilageCard = document.getElementById('card-spoilage');

    if (tempEl) tempEl.textContent = parseFloat(data.temperature).toFixed(1);
    if (humidityEl) humidityEl.textContent = parseFloat(data.humidity).toFixed(1);
    if (gasEl) gasEl.textContent = parseFloat(data.gas).toFixed(0);
    if (batteryEl) batteryEl.textContent = parseFloat(data.battery).toFixed(0);

    if (spoilageEl) {
        const level = data.spoilage_level || 'LOW';
        spoilageEl.textContent = getSpoilageHindi(level);

        // Remove old classes
        spoilageEl.classList.remove('spoilage-low', 'spoilage-medium', 'spoilage-high');
        spoilageEl.classList.add('spoilage-' + level.toLowerCase());
    }

    // Highlight cards based on spoilage level
    if (spoilageCard) {
        spoilageCard.classList.remove('card-highlight-low', 'card-highlight-medium', 'card-highlight-high');
        spoilageCard.classList.add('card-highlight-' + (data.spoilage_level || 'low').toLowerCase());
    }

    // Animate cards
    document.querySelectorAll('.sensor-card').forEach(function(card) {
        card.style.transform = 'scale(1.02)';
        setTimeout(function() { card.style.transform = ''; }, 200);
    });
}

function getSpoilageHindi(level) {
    switch(level.toUpperCase()) {
        case 'HIGH': return '🔴 उच्च खतरा';
        case 'MEDIUM': return '🟡 मध्यम';
        case 'LOW': return '🟢 सुरक्षित';
        default: return level;
    }
}

function loadDeviceData(deviceId) {
    fetch('/api/latest_data/' + deviceId)
        .then(function(resp) { return resp.json(); })
        .then(function(data) {
            if (!data.error) {
                updateSensorCards(data);
            }
        })
        .catch(function(err) { console.error('Error loading data:', err); });
}

// ===========================
// CHART
// ===========================
function initChart() {
    const canvas = document.getElementById('sensorChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    sensorChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'तापमान (°C)',
                    data: [],
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: false,
                    pointRadius: 2,
                    pointHoverRadius: 5
                },
                {
                    label: 'नमी (%)',
                    data: [],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: false,
                    pointRadius: 2,
                    pointHoverRadius: 5
                },
                {
                    label: 'गैस (PPM)',
                    data: [],
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: false,
                    pointRadius: 2,
                    pointHoverRadius: 5
                },
                {
                    label: 'बैटरी (%)',
                    data: [],
                    borderColor: '#22c55e',
                    backgroundColor: 'rgba(34, 197, 94, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: false,
                    pointRadius: 2,
                    pointHoverRadius: 5
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#8b949e',
                        font: { family: 'Poppins', size: 12 },
                        padding: 16,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(22, 27, 34, 0.95)',
                    titleFont: { family: 'Poppins' },
                    bodyFont: { family: 'Poppins' },
                    borderColor: 'rgba(48, 54, 61, 0.6)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 12
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(48, 54, 61, 0.3)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6e7681',
                        font: { family: 'Poppins', size: 10 },
                        maxTicksLimit: 10
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(48, 54, 61, 0.3)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6e7681',
                        font: { family: 'Poppins', size: 11 }
                    }
                }
            }
        }
    });
}

function loadChartData(deviceId) {
    if (!sensorChart) return;

    fetch('/api/sensor_history/' + deviceId)
        .then(function(resp) { return resp.json(); })
        .then(function(data) {
            if (Array.isArray(data)) {
                var labels = [];
                var temps = [];
                var humidities = [];
                var gases = [];
                var batteries = [];

                data.forEach(function(d) {
                    var ts = d.timestamp || '';
                    var time = ts.split('T')[1];
                    if (time) {
                        labels.push(time.substring(0, 5));
                    } else {
                        labels.push('');
                    }
                    temps.push(d.temperature);
                    humidities.push(d.humidity);
                    gases.push(d.gas);
                    batteries.push(d.battery);
                });

                sensorChart.data.labels = labels;
                sensorChart.data.datasets[0].data = temps;
                sensorChart.data.datasets[1].data = humidities;
                sensorChart.data.datasets[2].data = gases;
                sensorChart.data.datasets[3].data = batteries;
                sensorChart.update('none');
            }
        })
        .catch(function(err) { console.error('Error loading chart:', err); });
}

function addChartDataPoint(data) {
    if (!sensorChart) return;

    var ts = data.timestamp || new Date().toISOString();
    var time = ts.split('T')[1];
    var label = time ? time.substring(0, 5) : '';

    sensorChart.data.labels.push(label);
    sensorChart.data.datasets[0].data.push(data.temperature);
    sensorChart.data.datasets[1].data.push(data.humidity);
    sensorChart.data.datasets[2].data.push(data.gas);
    sensorChart.data.datasets[3].data.push(data.battery);

    // Keep only last 50
    if (sensorChart.data.labels.length > 50) {
        sensorChart.data.labels.shift();
        sensorChart.data.datasets.forEach(function(ds) {
            ds.data.shift();
        });
    }

    sensorChart.update('none');
}

// ===========================
// WEATHER
// ===========================
function fetchWeather() {
    var cityInput = document.getElementById('weatherCity');
    var weatherCard = document.getElementById('weatherCard');
    if (!cityInput || !weatherCard) return;

    var city = cityInput.value.trim() || 'Delhi';

    fetch('/api/weather?city=' + encodeURIComponent(city))
        .then(function(resp) { return resp.json(); })
        .then(function(data) {
            document.getElementById('weatherCityName').textContent = data.city || city;
            document.getElementById('weatherDesc').textContent = data.description || '--';
            document.getElementById('weatherTemp').textContent = data.temperature + '°C';
            document.getElementById('weatherHumidity').textContent = data.humidity + '%';
            document.getElementById('weatherIcon').src = 'https://openweathermap.org/img/wn/' + (data.icon || '01d') + '@2x.png';
            weatherCard.style.display = 'block';
        })
        .catch(function(err) {
            console.error('Weather error:', err);
        });
}

// ===========================
// UTILITY
// ===========================

// Make switchSection available globally (for inline onclick handlers)
window.switchSection = switchSection;
window.fetchWeather = fetchWeather;
