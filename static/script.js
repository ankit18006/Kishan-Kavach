// ===== KISHAN KAVACH - MAIN SCRIPT =====

document.addEventListener("DOMContentLoaded", function () {
    const lang = localStorage.getItem("lang") || "hi";
    updateChartLanguage();
    setLanguage(lang);

    const langSelect = document.querySelector('.lang-select');
    if (langSelect) {
        langSelect.value = lang;
    }

    initLandingPage();
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
        spoilageEl.textContent = getSpoilageText(level);

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

function getSpoilageText(level) {
    const lang = localStorage.getItem("lang") || "hi";

    if (lang === "hi") {
        if (level === "HIGH") return "🔴 उच्च खतरा";
        if (level === "MEDIUM") return "🟡 मध्यम";
        return "🟢 सुरक्षित";
    } else {
        if (level === "HIGH") return "🔴 High Risk";
        if (level === "MEDIUM") return "🟡 Medium";
        return "🟢 Safe";
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

function getChartLabels() {
    const lang = localStorage.getItem("lang") || "hi";

    if (lang === "hi") {
        return {
            temp: "तापमान (°C)",
            humidity: "नमी (%)",
            gas: "गैस (PPM)",
            battery: "बैटरी (%)"
        };
    } else {
        return {
            temp: "Temperature (°C)",
            humidity: "Humidity (%)",
            gas: "Gas (PPM)",
            battery: "Battery (%)"
        };
    }
}

function initChart() {
    const canvas = document.getElementById('sensorChart');
    if (!canvas) return;

    const labelsText = getChartLabels();

    const ctx = canvas.getContext('2d');
    sensorChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: labelsText.temp,
                    data: [],
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: false,
                    pointRadius: 2
                },
                {
                    label: labelsText.humidity,
                    data: [],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: false,
                    pointRadius: 2
                },
                {
                    label: labelsText.gas,
                    data: [],
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: false,
                    pointRadius: 2
                },
                {
                    label: labelsText.battery,
                    data: [],
                    borderColor: '#22c55e',
                    backgroundColor: 'rgba(34, 197, 94, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: false,
                    pointRadius: 2
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
                        color: '#8b949e'
                    }
                }
            }
        }
    });
}

// 🔄 LANGUAGE CHANGE PE CHART UPDATE
function updateChartLanguage() {
    if (!sensorChart) return;

    const labelsText = getChartLabels();

    sensorChart.data.datasets[0].label = labelsText.temp;
    sensorChart.data.datasets[1].label = labelsText.humidity;
    sensorChart.data.datasets[2].label = labelsText.gas;
    sensorChart.data.datasets[3].label = labelsText.battery;

    sensorChart.update();
}

// ===========================
// LOAD DATA
// ===========================

function loadChartData(deviceId) {
    if (!sensorChart) return;

    fetch('/api/sensor_history/' + deviceId)
        .then(res => res.json())
        .then(data => {
            if (!Array.isArray(data)) return;

            let labels = [];
            let temps = [];
            let hums = [];
            let gas = [];
            let bat = [];

            data.forEach(d => {
                let time = (d.timestamp || '').split('T')[1];
                labels.push(time ? time.substring(0,5) : '');

                temps.push(d.temperature);
                hums.push(d.humidity);
                gas.push(d.gas);
                bat.push(d.battery);
            });

            sensorChart.data.labels = labels;
            sensorChart.data.datasets[0].data = temps;
            sensorChart.data.datasets[1].data = hums;
            sensorChart.data.datasets[2].data = gas;
            sensorChart.data.datasets[3].data = bat;

            sensorChart.update();
        });
}

// ===========================
// REALTIME UPDATE
// ===========================

function addChartDataPoint(data) {
    if (!sensorChart) return;

    let time = (data.timestamp || new Date().toISOString()).split('T')[1];
    let label = time ? time.substring(0,5) : '';

    sensorChart.data.labels.push(label);
    sensorChart.data.datasets[0].data.push(data.temperature);
    sensorChart.data.datasets[1].data.push(data.humidity);
    sensorChart.data.datasets[2].data.push(data.gas);
    sensorChart.data.datasets[3].data.push(data.battery);

    if (sensorChart.data.labels.length > 50) {
        sensorChart.data.labels.shift();
        sensorChart.data.datasets.forEach(ds => ds.data.shift());
    }

    sensorChart.update();
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
