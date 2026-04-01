// ===== KISHAN KAVACH - MAIN SCRIPT =====
// No dummy data - Only real data from ESP32 / API

document.addEventListener('DOMContentLoaded', function () {
    initLandingPage();
    initDashboard();
});

// ========================
// TRANSLATIONS FOR JS
// ========================
const JS_TRANSLATIONS = {
    en: {
        safe: '🟢 Safe',
        medium: '🟡 Medium Risk',
        high: '🔴 High Danger',
        temperature: 'Temperature (°C)',
        humidity: 'Humidity (%)',
        gas: 'Gas (PPM)',
        battery: 'Battery (%)',
        noData: 'No data received yet. Waiting for ESP32...',
        connected: 'Connected to server',
        disconnected: 'Disconnected from server'
    },
    hi: {
        safe: '🟢 सुरक्षित',
        medium: '🟡 मध्यम जोखिम',
        high: '🔴 उच्च खतरा',
        temperature: 'तापमान (°C)',
        humidity: 'नमी (%)',
        gas: 'गैस (PPM)',
        battery: 'बैटरी (%)',
        noData: 'अभी तक कोई डेटा नहीं मिला। ESP32 की प्रतीक्षा...',
        connected: 'सर्वर से कनेक्टेड',
        disconnected: 'सर्वर से डिस्कनेक्ट'
    }
};

function getLang() {
    return (typeof USER_LANG !== 'undefined') ? USER_LANG : 'en';
}

function jst(key) {
    var lang = getLang();
    var dict = JS_TRANSLATIONS[lang] || JS_TRANSLATIONS['en'];
    return dict[key] || JS_TRANSLATIONS['en'][key] || key;
}

// ========================
// LANDING PAGE
// ========================
function initLandingPage() {
    var navbar = document.getElementById('navbar');
    var mobileToggle = document.getElementById('mobileToggle');
    var mobileMenu = document.getElementById('mobileMenu');

    if (navbar) {
        window.addEventListener('scroll', function () {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        });
    }

    if (mobileToggle && mobileMenu) {
        mobileToggle.addEventListener('click', function () {
            mobileMenu.classList.toggle('active');
        });
        mobileMenu.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                mobileMenu.classList.remove('active');
            });
        });
    }

    // Scroll animations
    var fadeEls = document.querySelectorAll('.fade-up');
    if ('IntersectionObserver' in window && fadeEls.length > 0) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        fadeEls.forEach(function (el) {
            if (!el.closest('.hero')) {
                el.style.animationPlayState = 'paused';
            }
            observer.observe(el);
        });
    }
}

// ========================
// DASHBOARD
// ========================
var socket = null;
var sensorChart = null;
var currentDeviceId = null;

function initDashboard() {
    var sidebarToggle = document.getElementById('sidebarToggle');
    var sidebar = document.getElementById('sidebar');
    var sidebarLinks = document.querySelectorAll('.sidebar-link');
    var deviceSelector = document.getElementById('deviceSelector');

    if (!sidebar) return;

    // Create overlay for mobile
    var overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    overlay.id = 'sidebarOverlay';
    document.body.appendChild(overlay);

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        });
    }

    overlay.addEventListener('click', function () {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });

    // Sidebar nav
    sidebarLinks.forEach(function (link) {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            var section = this.getAttribute('data-section');
            switchSection(section);
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
    });

    // Device selector
    if (deviceSelector) {
        deviceSelector.addEventListener('change', function () {
            currentDeviceId = this.value;
            loadDeviceData(currentDeviceId);
            loadChartData(currentDeviceId);
        });
        currentDeviceId = deviceSelector.value;
        if (currentDeviceId) {
            loadDeviceData(currentDeviceId);
            loadChartData(currentDeviceId);
        }
    }

    // Socket.IO
    initSocket();

    // Chart
    initChart();

    // Auto dismiss flash
    setTimeout(function () {
        document.querySelectorAll('.flash-container .alert').forEach(function (el) {
            el.style.opacity = '0';
            el.style.transition = 'opacity 0.5s';
            setTimeout(function () { el.remove(); }, 500);
        });
    }, 5000);
}

function switchSection(sectionName) {
    document.querySelectorAll('.content-section').forEach(function (sec) {
        sec.classList.remove('active');
    });
    var target = document.getElementById('section-' + sectionName);
    if (target) target.classList.add('active');

    document.querySelectorAll('.sidebar-link').forEach(function (link) {
        link.classList.remove('active');
        if (link.getAttribute('data-section') === sectionName) {
            link.classList.add('active');
        }
    });
}

// ========================
// SOCKET.IO - REAL DATA ONLY
// ========================
function initSocket() {
    if (typeof io === 'undefined') return;

    socket = io();

    socket.on('connect', function () {
        console.log('[WS] ' + jst('connected'));
    });

    socket.on('disconnect', function () {
        console.log('[WS] ' + jst('disconnected'));
    });

    socket.on('sensor_update', function (data) {
        console.log('[WS] Real sensor data:', data);
        if (data.device_id === currentDeviceId) {
            updateSensorCards(data);
            addChartDataPoint(data);
        }
    });

    socket.on('error', function (data) {
        console.error('[WS] Error:', data.message);
    });
}

// ========================
// SENSOR CARDS - REAL DATA
// ========================
function updateSensorCards(data) {
    var tempEl = document.getElementById('tempValue');
    var humidityEl = document.getElementById('humidityValue');
    var gasEl = document.getElementById('gasValue');
    var batteryEl = document.getElementById('batteryValue');
    var spoilageEl = document.getElementById('spoilageValue');
    var spoilageCard = document.getElementById('card-spoilage');

    if (tempEl) tempEl.textContent = parseFloat(data.temperature).toFixed(1);
    if (humidityEl) humidityEl.textContent = parseFloat(data.humidity).toFixed(1);
    if (gasEl) gasEl.textContent = parseFloat(data.gas).toFixed(0);
    if (batteryEl) batteryEl.textContent = parseFloat(data.battery).toFixed(0);

    if (spoilageEl) {
        var level = (data.spoilage_level || 'LOW').toUpperCase();
        spoilageEl.textContent = getSpoilageLabel(level);
        spoilageEl.classList.remove('spoilage-low', 'spoilage-medium', 'spoilage-high');
        spoilageEl.classList.add('spoilage-' + level.toLowerCase());
    }

    if (spoilageCard) {
        spoilageCard.classList.remove('card-highlight-low', 'card-highlight-medium', 'card-highlight-high');
        spoilageCard.classList.add('card-highlight-' + (data.spoilage_level || 'low').toLowerCase());
    }

    // Brief animation
    document.querySelectorAll('.sensor-card').forEach(function (card) {
        card.style.transform = 'scale(1.02)';
        setTimeout(function () { card.style.transform = ''; }, 200);
    });
}

function getSpoilageLabel(level) {
    switch (level) {
        case 'HIGH': return jst('high');
        case 'MEDIUM': return jst('medium');
        case 'LOW': return jst('safe');
        default: return level;
    }
}

function loadDeviceData(deviceId) {
    fetch('/api/latest_data/' + deviceId)
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (!data.error) {
                updateSensorCards(data);
            }
        })
        .catch(function (err) { console.error('Load data error:', err); });
}

// ========================
// CHART - REAL DATA ONLY
// ========================
function initChart() {
    var canvas = document.getElementById('sensorChart');
    if (!canvas) return;

    var ctx = canvas.getContext('2d');
    sensorChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: jst('temperature'),
                    data: [],
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239,68,68,0.1)',
                    borderWidth: 2, tension: 0.4, fill: false,
                    pointRadius: 2, pointHoverRadius: 5
                },
                {
                    label: jst('humidity'),
                    data: [],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59,130,246,0.1)',
                    borderWidth: 2, tension: 0.4, fill: false,
                    pointRadius: 2, pointHoverRadius: 5
                },
                {
                    label: jst('gas'),
                    data: [],
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245,158,11,0.1)',
                    borderWidth: 2, tension: 0.4, fill: false,
                    pointRadius: 2, pointHoverRadius: 5
                },
                {
                    label: jst('battery'),
                    data: [],
                    borderColor: '#22c55e',
                    backgroundColor: 'rgba(34,197,94,0.1)',
                    borderWidth: 2, tension: 0.4, fill: false,
                    pointRadius: 2, pointHoverRadius: 5
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { intersect: false, mode: 'index' },
            plugins: {
                legend: {
                    labels: {
                        color: '#8b949e',
                        font: { family: 'Poppins', size: 12 },
                        padding: 16, usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(22,27,34,0.95)',
                    titleFont: { family: 'Poppins' },
                    bodyFont: { family: 'Poppins' },
                    borderColor: 'rgba(48,54,61,0.6)',
                    borderWidth: 1, cornerRadius: 8, padding: 12
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(48,54,61,0.3)', drawBorder: false },
                    ticks: { color: '#6e7681', font: { family: 'Poppins', size: 10 }, maxTicksLimit: 10 }
                },
                y: {
                    grid: { color: 'rgba(48,54,61,0.3)', drawBorder: false },
                    ticks: { color: '#6e7681', font: { family: 'Poppins', size: 11 } }
                }
            }
        }
    });
}

function loadChartData(deviceId) {
    if (!sensorChart) return;

    fetch('/api/sensor_history/' + deviceId)
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (Array.isArray(data) && data.length > 0) {
                var labels = [], temps = [], hums = [], gases = [], batts = [];
                data.forEach(function (d) {
                    var ts = d.timestamp || '';
                    var time = ts.split('T')[1];
                    labels.push(time ? time.substring(0, 5) : '');
                    temps.push(d.temperature);
                    hums.push(d.humidity);
                    gases.push(d.gas);
                    batts.push(d.battery);
                });
                sensorChart.data.labels = labels;
                sensorChart.data.datasets[0].data = temps;
                sensorChart.data.datasets[1].data = hums;
                sensorChart.data.datasets[2].data = gases;
                sensorChart.data.datasets[3].data = batts;
                sensorChart.update('none');
            }
        })
        .catch(function (err) { console.error('Chart load error:', err); });
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
        sensorChart.data.datasets.forEach(function (ds) { ds.data.shift(); });
    }

    sensorChart.update('none');
}

// ========================
// WEATHER - REAL API DATA
// ========================
function fetchWeather() {
    var cityInput = document.getElementById('weatherCity');
    var weatherCard = document.getElementById('weatherCard');
    if (!cityInput || !weatherCard) return;

    var city = cityInput.value.trim() || 'Delhi';

    fetch('/api/weather?city=' + encodeURIComponent(city))
        .then(function (r) { return r.json(); })
        .then(function (data) {
            document.getElementById('weatherCityName').textContent = data.city || city;
            document.getElementById('weatherDesc').textContent = data.description || '--';
            document.getElementById('weatherTemp').textContent = data.temperature + '°C';
            document.getElementById('weatherHumidity').textContent = data.humidity + '%';
            document.getElementById('weatherIcon').src = 'https://openweathermap.org/img/wn/' + (data.icon || '01d') + '@2x.png';
            weatherCard.style.display = 'block';
        })
        .catch(function (err) { console.error('Weather error:', err); });
}

// ========================
// GLOBAL FUNCTIONS
// ========================
window.switchSection = switchSection;
window.fetchWeather = fetchWeather;
