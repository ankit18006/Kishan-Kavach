// ===== KISHAN KAVACH - PRODUCTION FRONTEND (Real Data Only) =====

let socket;
let currentRole = 'farmer';
let currentDevice = '';
let sensorChart, predictionChart, healthChart;
let currentLang = 'en';
let allCrops = [];
let deviceOnline = false;
let lastDataTimestamp = null;

// ===== INIT =====
function initApp(role) {
    currentRole = role;
    connectSocket();
    setupNavigation();
    loadDevices();
    loadCrops();
    loadWeather();
    loadAlerts();
    showNoDataState(); // Start with no-data state until real data arrives

    if (role === 'admin') {
        loadUsers();
        loadStats();
        loadAccessRequests();
    }
    if (role === 'owner') {
        loadAccessRequests();
    }

    // Periodic device online check (every 30s)
    setInterval(checkDeviceStatus, 30000);
}

// ===== DATA VALIDATION =====
function isValidSensorData(data) {
    return data &&
        typeof data.temperature === 'number' &&
        typeof data.humidity === 'number' &&
        typeof data.gas === 'number' &&
        !isNaN(data.temperature) &&
        !isNaN(data.humidity) &&
        !isNaN(data.gas);
}

// ===== NO DATA / OFFLINE STATE =====
function showNoDataState() {
    clearDashboard();

    const noDataEl = document.getElementById('noDataMessage');
    if (noDataEl) {
        noDataEl.style.display = 'flex';
        noDataEl.innerHTML = `
            <div class="no-data-container">
                <i class="fas fa-satellite-dish no-data-icon"></i>
                <h3>No live data available</h3>
                <p>Please connect your IoT device to start monitoring</p>
                <span class="device-status-badge offline">
                    <i class="fas fa-circle"></i> Device offline
                </span>
            </div>
        `;
    }

    // Hide dashboard content until real data arrives
    const dashboardContent = document.getElementById('dashboardContent');
    if (dashboardContent) {
        dashboardContent.classList.add('awaiting-data');
    }
}

function hideNoDataState() {
    const noDataEl = document.getElementById('noDataMessage');
    if (noDataEl) {
        noDataEl.style.display = 'none';
    }

    const dashboardContent = document.getElementById('dashboardContent');
    if (dashboardContent) {
        dashboardContent.classList.remove('awaiting-data');
    }
}

function clearDashboard() {
    const fields = ['temperature', 'humidity', 'gasLevel', 'battery',
                    'healthScore', 'daysRemaining', 'condition'];
    fields.forEach(id => setText(id, '--'));

    const futureEl = document.getElementById('futureRisk');
    if (futureEl) {
        futureEl.textContent = '--';
        futureEl.className = 'insight-value';
    }

    const spoilageEl = document.getElementById('spoilageRisk');
    if (spoilageEl) {
        spoilageEl.textContent = 'No data';
        spoilageEl.className = 'sensor-ideal';
    }

    const healthFill = document.getElementById('healthFill');
    if (healthFill) {
        healthFill.style.width = '0%';
        healthFill.style.background = 'var(--glass-border)';
    }

    const recs = document.getElementById('recommendations');
    if (recs) recs.innerHTML = '<p class="empty-state">Waiting for sensor data...</p>';

    const timeline = document.getElementById('spoilageTimeline');
    if (timeline) timeline.innerHTML = '';
}

function showDeviceOffline() {
    deviceOnline = false;
    const statusBadge = document.getElementById('deviceStatusBadge');
    if (statusBadge) {
        statusBadge.innerHTML = '<i class="fas fa-circle"></i> Device offline';
        statusBadge.className = 'device-status-badge offline';
    }
}

function showDeviceOnline() {
    deviceOnline = true;
    const statusBadge = document.getElementById('deviceStatusBadge');
    if (statusBadge) {
        statusBadge.innerHTML = '<i class="fas fa-circle"></i> Device online';
        statusBadge.className = 'device-status-badge online';
    }
}

function checkDeviceStatus() {
    if (!lastDataTimestamp) {
        showDeviceOffline();
        return;
    }
    const elapsed = Date.now() - lastDataTimestamp;
    // Consider device offline if no data for 60 seconds
    if (elapsed > 60000) {
        showDeviceOffline();
    }
}

// ===== SOCKET.IO =====
function connectSocket() {
    socket = io();

    socket.on('connect', () => {
        console.log('[Kishan Kavach] Connected to server');
        updateConnectionStatus(true);
    });

    socket.on('disconnect', () => {
        console.log('[Kishan Kavach] Disconnected from server');
        updateConnectionStatus(false);
        showDeviceOffline();
    });

    socket.on('sensor_update', (data) => {
        // ONLY process valid real sensor data
        if (!isValidSensorData(data)) {
            console.warn('[Kishan Kavach] Received invalid sensor data, ignoring');
            return;
        }

        lastDataTimestamp = Date.now();
        showDeviceOnline();
        hideNoDataState();

        if (data.device_id === currentDevice) {
            updateDashboard(data);
        }
        showToast(`📡 New data from ${data.device_id}`, 'success');
    });

    socket.on('device_data', (data) => {
        if (data.latest && isValidSensorData(data.latest)) {
            lastDataTimestamp = Date.now();
            showDeviceOnline();
            hideNoDataState();

            updateDashboard({
                ...data.latest,
                analysis: data.analysis,
                predictions: data.predictions
            });
            updateHistory(data.history);
            if (data.predictions) {
                updatePredictionChart(data.predictions);
            }
        }
    });
}

function updateConnectionStatus(connected) {
    const el = document.getElementById('connectionStatus');
    if (el) {
        el.className = 'connection-status ' + (connected ? 'connected' : 'disconnected');
    }
}

// ===== NAVIGATION =====
function setupNavigation() {
    document.querySelectorAll('.nav-item[data-section]').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const section = item.dataset.section;

            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            item.classList.add('active');

            document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
            const sectionEl = document.getElementById('section-' + section);
            if (sectionEl) sectionEl.classList.add('active');

            // Close mobile sidebar
            document.getElementById('sidebar')?.classList.remove('open');
        });
    });
}

function toggleSidebar() {
    document.getElementById('sidebar')?.classList.toggle('open');
}

// ===== LANGUAGE TOGGLE =====
function toggleLanguage() {
    currentLang = currentLang === 'en' ? 'hi' : 'en';
    const label = document.getElementById('langLabel');
    if (label) label.textContent = currentLang === 'en' ? 'हिंदी' : 'English';

    document.querySelectorAll('[data-en]').forEach(el => {
        const text = el.getAttribute('data-' + currentLang);
        if (text) el.textContent = text;
    });
}

// ===== LOAD DEVICES =====
function loadDevices() {
    fetch('/api/devices')
        .then(r => r.json())
        .then(devices => {
            const selector = document.getElementById('activeDevice');
            if (selector) {
                selector.innerHTML = '<option value="">Select Device</option>';
                devices.forEach(d => {
                    selector.innerHTML += `<option value="${d.device_id}">${d.name || d.device_id} (${d.crop || 'N/A'})</option>`;
                });

                if (devices.length > 0 && !currentDevice) {
                    currentDevice = devices[0].device_id;
                    selector.value = currentDevice;
                    loadDeviceData(currentDevice);
                }
            }

            renderDevicesList(devices);
        })
        .catch(err => console.error('[Kishan Kavach] Error loading devices:', err));
}

function renderDevicesList(devices) {
    const container = document.getElementById('devicesList');
    if (!container) return;

    if (devices.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-microchip" style="font-size:2rem;margin-bottom:10px;opacity:0.5;"></i>
                <p>No devices registered</p>
                <p><small>Add a device and connect your ESP32 to begin</small></p>
            </div>`;
        return;
    }

    container.innerHTML = devices.map(d => `
        <div class="device-card">
            <div class="device-card-header">
                <h3><i class="fas fa-microchip"></i> ${d.name || d.device_id}</h3>
                <span class="status-badge status-approved">Registered</span>
            </div>
            <div class="device-meta">
                <span><i class="fas fa-fingerprint"></i> ${d.device_id}</span>
                <span><i class="fas fa-map-marker-alt"></i> ${d.location || 'N/A'}</span>
                <span><i class="fas fa-seedling"></i> ${d.crop || 'Not set'}</span>
            </div>
            <div class="device-actions">
                <button class="btn-sm btn-approve" onclick="switchDevice('${d.device_id}')">
                    <i class="fas fa-eye"></i> View
                </button>
                ${currentRole !== 'farmer' ? `
                <button class="btn-sm btn-delete" onclick="deleteDevice('${d.device_id}')">
                    <i class="fas fa-trash"></i> Delete
                </button>
                ` : ''}
            </div>
        </div>
    `).join('');
}

function switchDevice(deviceId) {
    if (!deviceId) return;
    currentDevice = deviceId;
    lastDataTimestamp = null; // Reset — we don't know if this device is online yet
    const selector = document.getElementById('activeDevice');
    if (selector) selector.value = deviceId;

    // Reset dashboard while loading
    showNoDataState();
    loadDeviceData(deviceId);

    // Switch to dashboard
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const dashNav = document.querySelector('[data-section="dashboard"]');
    if (dashNav) dashNav.classList.add('active');
    document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
    const dashSection = document.getElementById('section-dashboard');
    if (dashSection) dashSection.classList.add('active');
}

function loadDeviceData(deviceId) {
    fetch(`/api/device/${deviceId}/data`)
        .then(r => r.json())
        .then(data => {
            if (data.latest && isValidSensorData(data.latest)) {
                lastDataTimestamp = Date.now();
                showDeviceOnline();
                hideNoDataState();

                updateDashboard({
                    ...data.latest,
                    analysis: data.analysis,
                    predictions: data.predictions
                });
                updateHistory(data.history);
                if (data.predictions) {
                    updatePredictionChart(data.predictions);
                }
                if (data.timeline) {
                    renderTimeline(data.timeline);
                }
            } else {
                // No real data exists for this device
                showNoDataState();
                clearCharts();
            }
        })
        .catch(err => {
            console.error('[Kishan Kavach] Error loading device data:', err);
            showNoDataState();
        });
}

// ===== UPDATE DASHBOARD (REAL DATA ONLY) =====
function updateDashboard(data) {
    if (!isValidSensorData(data)) {
        showNoDataState();
        return;
    }

    // Sensor values — display only real readings
    setText('temperature', `${data.temperature.toFixed(1)}°C`);
    setText('humidity', `${data.humidity.toFixed(1)}%`);
    setText('gasLevel', `${data.gas.toFixed(0)} ppm`);
    setText('battery', typeof data.battery === 'number' ? `${data.battery.toFixed(0)}%` : '--');

    const analysis = data.analysis || {};
    const cropInfo = analysis.crop_info;

    // AI Insights — only display if analysis ran on real data
    if (analysis && typeof analysis.health_score === 'number') {
        const healthScore = analysis.health_score;
        setText('healthScore', `${healthScore}%`);
        setText('daysRemaining', analysis.days_remaining != null ? `${analysis.days_remaining} days` : '--');
        setText('condition', analysis.condition || '--');

        const futureRisk = analysis.future_risk || '--';
        const futureEl = document.getElementById('futureRisk');
        if (futureEl) {
            futureEl.textContent = futureRisk;
            futureEl.className = futureRisk !== '--'
                ? 'insight-value risk-' + futureRisk.toLowerCase()
                : 'insight-value';
        }

        // Health bar
        const healthFill = document.getElementById('healthFill');
        if (healthFill) {
            healthFill.style.width = healthScore + '%';
            if (healthScore >= 70) healthFill.style.background = 'var(--accent-green)';
            else if (healthScore >= 40) healthFill.style.background = 'var(--accent-orange)';
            else healthFill.style.background = 'var(--accent-red)';
        }

        // Color card by health
        colorCard('healthCard', healthScore >= 70 ? 'green' : healthScore >= 40 ? 'orange' : 'red');
    } else {
        // No AI analysis available
        setText('healthScore', '--');
        setText('daysRemaining', '--');
        setText('condition', '--');
        const futureEl = document.getElementById('futureRisk');
        if (futureEl) {
            futureEl.textContent = '--';
            futureEl.className = 'insight-value';
        }
    }

    // Crop-specific ideals
    if (cropInfo) {
        setText('idealTemp', `Ideal: ${cropInfo.temp_min}–${cropInfo.temp_max}°C`);
        setText('idealHumidity', `Ideal: ${cropInfo.humidity_min}–${cropInfo.humidity_max}%`);
        setText('harmfulGas', `Risk: ${cropInfo.harmful_gas}`);
    }

    // Spoilage risk
    if (analysis.spoilage_risk || data.spoilage_risk) {
        const risk = analysis.spoilage_risk || data.spoilage_risk;
        const riskEl = document.getElementById('spoilageRisk');
        if (riskEl) {
            riskEl.textContent = `Risk: ${risk}`;
            riskEl.className = 'sensor-ideal risk-' + risk.toLowerCase();
        }
    }

    // Recommendations
    if (analysis.recommendations && analysis.recommendations.length > 0) {
        renderRecommendations(analysis.recommendations);
    } else {
        const recs = document.getElementById('recommendations');
        if (recs) recs.innerHTML = '<p class="empty-state">No recommendations yet — monitoring in progress</p>';
    }
}

function colorCard(id, color) {
    const card = document.getElementById(id);
    if (!card) return;
    card.style.borderColor = color === 'green' ? 'rgba(0,255,136,0.3)' :
                             color === 'orange' ? 'rgba(245,158,11,0.3)' :
                             'rgba(239,68,68,0.3)';
}

function setText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
}

function renderRecommendations(recs) {
    const container = document.getElementById('recommendations');
    if (!container) return;
    container.innerHTML = recs.map(r => `
        <div class="recommendation-item">${r}</div>
    `).join('');
}

function renderTimeline(timeline) {
    const container = document.getElementById('spoilageTimeline');
    if (!container) return;

    if (!timeline || timeline.length === 0) {
        container.innerHTML = '<p class="empty-state">No timeline data available</p>';
        return;
    }

    let html = '';
    timeline.forEach((point, i) => {
        html += `
            <div class="timeline-point">
                <div class="timeline-dot" style="background:${point.color}"></div>
                <div class="timeline-label">${point.status}</div>
                <div class="timeline-day">Day ${point.day}</div>
            </div>
        `;
        if (i < timeline.length - 1) {
            html += '<div class="timeline-line"></div>';
        }
    });
    container.innerHTML = html;
}

// ===== CHARTS (REAL DATA ONLY) =====
function clearCharts() {
    if (sensorChart) { sensorChart.destroy(); sensorChart = null; }
    if (healthChart) { healthChart.destroy(); healthChart = null; }
    if (predictionChart) { predictionChart.destroy(); predictionChart = null; }

    const sensorCtx = document.getElementById('sensorChart');
    if (sensorCtx) {
        const parent = sensorCtx.parentElement;
        if (parent && !parent.querySelector('.empty-chart-msg')) {
            const msg = document.createElement('p');
            msg.className = 'empty-chart-msg empty-state';
            msg.textContent = 'No sensor history — waiting for real data';
            parent.appendChild(msg);
        }
    }

    const healthCtx = document.getElementById('healthChart');
    if (healthCtx) {
        const parent = healthCtx.parentElement;
        if (parent && !parent.querySelector('.empty-chart-msg')) {
            const msg = document.createElement('p');
            msg.className = 'empty-chart-msg empty-state';
            msg.textContent = 'No health history — waiting for real data';
            parent.appendChild(msg);
        }
    }

    const predCtx = document.getElementById('predictionChart');
    if (predCtx) {
        const parent = predCtx.parentElement;
        if (parent && !parent.querySelector('.empty-chart-msg')) {
            const msg = document.createElement('p');
            msg.className = 'empty-chart-msg empty-state';
            msg.textContent = 'No predictions available yet';
            parent.appendChild(msg);
        }
    }
}

function removeEmptyChartMessages() {
    document.querySelectorAll('.empty-chart-msg').forEach(el => el.remove());
}

function updateHistory(history) {
    if (!history || history.length === 0) {
        clearCharts();
        return;
    }

    // Filter to only valid data points
    const validHistory = history.filter(h => isValidSensorData(h));
    if (validHistory.length === 0) {
        clearCharts();
        return;
    }

    removeEmptyChartMessages();

    const reversed = [...validHistory].reverse();
    const labels = reversed.map((_, i) => `#${i + 1}`);
    const temps = reversed.map(h => h.temperature);
    const humidities = reversed.map(h => h.humidity);
    const gases = reversed.map(h => h.gas);
    const scores = reversed.map(h => typeof h.health_score === 'number' ? h.health_score : null);

    // Sensor Chart
    const sensorCtx = document.getElementById('sensorChart');
    if (sensorCtx) {
        if (sensorChart) sensorChart.destroy();
        sensorChart = new Chart(sensorCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Temperature (°C)',
                        data: temps,
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239,68,68,0.1)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 2
                    },
                    {
                        label: 'Humidity (%)',
                        data: humidities,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59,130,246,0.1)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 2
                    },
                    {
                        label: 'Gas (ppm)',
                        data: gases,
                        borderColor: '#f59e0b',
                        backgroundColor: 'rgba(245,158,11,0.1)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 2
                    }
                ]
            },
            options: getChartOptions('Sensor Readings Over Time')
        });
    }

    // Health Chart — only if we have valid health scores
    const validScores = scores.filter(s => s !== null);
    const healthCtx = document.getElementById('healthChart');
    if (healthCtx && validScores.length > 0) {
        if (healthChart) healthChart.destroy();
        healthChart = new Chart(healthCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Health Score',
                    data: scores,
                    borderColor: '#00ff88',
                    backgroundColor: 'rgba(0,255,136,0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3,
                    pointBackgroundColor: scores.map(s =>
                        s === null ? '#64748b' :
                        s >= 70 ? '#00ff88' : s >= 40 ? '#f59e0b' : '#ef4444'
                    ),
                    spanGaps: true
                }]
            },
            options: {
                ...getChartOptions('Health Score Trend'),
                scales: {
                    ...getChartOptions('').scales,
                    y: {
                        ...getChartOptions('').scales.y,
                        min: 0,
                        max: 100
                    }
                }
            }
        });
    }
}

function updatePredictionChart(predictions) {
    const predCtx = document.getElementById('predictionChart');
    if (!predCtx) return;

    // Validate predictions have real data
    if (!predictions || !predictions.labels || predictions.labels.length === 0) {
        if (predictionChart) { predictionChart.destroy(); predictionChart = null; }
        const parent = predCtx.parentElement;
        if (parent && !parent.querySelector('.empty-chart-msg')) {
            const msg = document.createElement('p');
            msg.className = 'empty-chart-msg empty-state';
            msg.textContent = 'No AI predictions available — need more real data';
            parent.appendChild(msg);
        }
        return;
    }

    removeEmptyChartMessages();

    if (predictionChart) predictionChart.destroy();
    predictionChart = new Chart(predCtx, {
        type: 'line',
        data: {
            labels: predictions.labels,
            datasets: [
                {
                    label: 'Predicted Temp (°C)',
                    data: predictions.temperature,
                    borderColor: '#ef4444',
                    borderDash: [5, 5],
                    backgroundColor: 'rgba(239,68,68,0.05)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointStyle: 'triangle'
                },
                {
                    label: 'Predicted Gas (ppm)',
                    data: predictions.gas,
                    borderColor: '#f59e0b',
                    borderDash: [5, 5],
                    backgroundColor: 'rgba(245,158,11,0.05)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointStyle: 'triangle'
                },
                {
                    label: 'Predicted Health',
                    data: predictions.health_score,
                    borderColor: '#00ff88',
                    borderDash: [5, 5],
                    backgroundColor: 'rgba(0,255,136,0.05)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointStyle: 'triangle'
                }
            ]
        },
        options: getChartOptions('AI Prediction (Next 7 Days)')
    });
}

function getChartOptions(title) {
    return {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                labels: { color: '#94a3b8', font: { size: 11 } }
            },
            title: {
                display: false,
                text: title,
                color: '#f0f4f8'
            }
        },
        scales: {
            x: {
                ticks: { color: '#64748b', font: { size: 10 } },
                grid: { color: 'rgba(255,255,255,0.05)' }
            },
            y: {
                ticks: { color: '#64748b', font: { size: 10 } },
                grid: { color: 'rgba(255,255,255,0.05)' }
            }
        },
        interaction: { intersect: false, mode: 'index' }
    };
}

// ===== CROPS =====
function loadCrops() {
    fetch('/api/crops/list')
        .then(r => r.json())
        .then(crops => {
            allCrops = crops;
            renderCrops(crops);
            populateCropSelectors(crops);
        })
        .catch(err => console.error('[Kishan Kavach] Error loading crops:', err));
}

function renderCrops(crops) {
    const container = document.getElementById('cropsList');
    if (!container) return;

    if (crops.length === 0) {
        container.innerHTML = '<p class="empty-state">No crops found</p>';
        return;
    }

    container.innerHTML = crops.map(c => `
        <div class="crop-card" onclick="showCropDetail('${c.key}')">
            <div class="crop-card-header">
                <h3>${c.name}</h3>
                <span class="crop-category cat-${c.category}">${c.category}</span>
            </div>
            <div class="crop-info-grid">
                <div class="crop-info-item">
                    <i class="fas fa-temperature-high"></i>
                    ${c.temp_min}–${c.temp_max}°C
                </div>
                <div class="crop-info-item">
                    <i class="fas fa-tint"></i>
                    ${c.humidity_min}–${c.humidity_max}%
                </div>
                <div class="crop-info-item">
                    <i class="fas fa-wind"></i>
                    ${c.harmful_gas}
                </div>
                <div class="crop-info-item">
                    <i class="fas fa-clock"></i>
                    ${c.shelf_life} days
                </div>
            </div>
        </div>
    `).join('');
}

function searchCrops(query) {
    if (!query) {
        renderCrops(allCrops);
        return;
    }
    const filtered = allCrops.filter(c =>
        c.name.toLowerCase().includes(query.toLowerCase()) ||
        c.key.toLowerCase().includes(query.toLowerCase()) ||
        c.category.toLowerCase().includes(query.toLowerCase())
    );
    renderCrops(filtered);
}

function showCropDetail(key) {
    const crop = allCrops.find(c => c.key === key);
    if (!crop) return;
    showToast(
        `🌾 ${crop.name}\n🌡 ${crop.temp_min}–${crop.temp_max}°C | 💧 ${crop.humidity_min}–${crop.humidity_max}% | 💨 ${crop.harmful_gas} | ⏳ ${crop.shelf_life} days`,
        'success', 5000
    );
}

function populateCropSelectors(crops) {
    const selector = document.getElementById('newDeviceCrop');
    if (selector) {
        selector.innerHTML = crops.map(c =>
            `<option value="${c.key}">${c.name}</option>`
        ).join('');
    }
}

// ===== WEATHER =====
function loadWeather() {
    const cityInput = document.getElementById('weatherCity');
    const city = cityInput ? cityInput.value : 'Delhi';

    fetch(`/api/weather?city=${encodeURIComponent(city)}`)
        .then(r => r.json())
        .then(data => {
            const container = document.getElementById('weatherData');
            if (!container) return;

            if (!data || data.error) {
                container.innerHTML = `
                    <div class="empty-state">
                        <i class="fas fa-cloud-sun-rain" style="font-size:2rem;margin-bottom:10px;opacity:0.5;"></i>
                        <p>Weather data unavailable</p>
                        <p><small>${data?.error || 'Please check your connection'}</small></p>
                    </div>`;
                return;
            }

            container.innerHTML = `
                <div class="weather-main glass-card">
                    <div class="weather-icon">
                        <img src="https://openweathermap.org/img/wn/${data.icon || '02d'}@4x.png" 
                             alt="Weather" style="width:100px;height:100px;" 
                             onerror="this.style.display='none'">
                    </div>
                    <div class="weather-temp">${typeof data.temp === 'number' ? data.temp.toFixed(1) + '°C' : '--'}</div>
                    <div class="weather-desc">${data.description || 'N/A'}</div>
                    <h3 style="margin-top:8px;color:var(--accent-cyan)">${data.city || city}</h3>
                    <div class="weather-details">
                        <div class="weather-detail">
                            <i class="fas fa-tint"></i>
                            <div class="weather-detail-value">${typeof data.humidity === 'number' ? data.humidity + '%' : '--'}</div>
                            <div class="weather-detail-label">Humidity</div>
                        </div>
                        <div class="weather-detail">
                            <i class="fas fa-wind"></i>
                            <div class="weather-detail-value">${typeof data.wind === 'number' ? data.wind + ' m/s' : '--'}</div>
                            <div class="weather-detail-label">Wind</div>
                        </div>
                    </div>
                </div>
            `;
        })
        .catch(err => {
            console.error('[Kishan Kavach] Error loading weather:', err);
            const container = document.getElementById('weatherData');
            if (container) {
                container.innerHTML = '<p class="empty-state">Failed to load weather data</p>';
            }
        });
}

// ===== ALERTS =====
function loadAlerts() {
    fetch('/api/alerts?limit=20')
        .then(r => r.json())
        .then(alerts => {
            const container = document.getElementById('alertsList');
            if (!container) return;

            if (!alerts || alerts.length === 0) {
                container.innerHTML = '<p class="empty-state">No alerts yet. Alerts will appear when real sensor data triggers dangerous conditions.</p>';
                return;
            }

            container.innerHTML = alerts.map(a => `
                <div class="alert-item">
                    <div class="alert-icon">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <div class="alert-content">
                        <h4>${a.alert_type} - ${a.device_id}</h4>
                        <p>${a.message}</p>
                        <div class="alert-time">${a.sent_at || 'Just now'}</div>
                    </div>
                </div>
            `).join('');
        })
        .catch(err => console.error('[Kishan Kavach] Error loading alerts:', err));
}

// ===== USERS (ADMIN) =====
function loadUsers() {
    fetch('/api/users')
        .then(r => r.json())
        .then(users => {
            const container = document.getElementById('usersList');
            if (!container) return;

            if (!users || users.length === 0) {
                container.innerHTML = '<p class="empty-state">No users found</p>';
                return;
            }

            container.innerHTML = users.map(u => `
                <div class="user-item">
                    <div class="user-info">
                        <i class="fas fa-user-circle"></i>
                        <div>
                            <h4>${u.username}</h4>
                            <small>${u.role} | ${u.phone || 'No phone'}</small>
                        </div>
                        <span class="status-badge status-${u.status}">${u.status}</span>
                    </div>
                    <div class="user-actions">
                        ${u.status === 'pending' ? `
                            <button class="btn-sm btn-approve" onclick="updateUserStatus(${u.id}, 'approved')">
                                <i class="fas fa-check"></i> Approve
                            </button>
                            <button class="btn-sm btn-reject" onclick="updateUserStatus(${u.id}, 'rejected')">
                                <i class="fas fa-times"></i> Reject
                            </button>
                        ` : ''}
                        ${u.role !== 'admin' ? `
                            <button class="btn-sm btn-delete" onclick="deleteUser(${u.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        ` : ''}
                    </div>
                </div>
            `).join('');
        })
        .catch(err => console.error('[Kishan Kavach] Error loading users:', err));
}

function updateUserStatus(userId, status) {
    fetch(`/api/user/${userId}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
    })
    .then(r => r.json())
    .then(() => {
        showToast(`User ${status}!`, 'success');
        loadUsers();
    });
}

function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user?')) return;
    fetch(`/api/user/${userId}/delete`, { method: 'DELETE' })
        .then(r => r.json())
        .then(() => {
            showToast('User deleted!', 'warning');
            loadUsers();
        });
}

// ===== ACCESS REQUESTS =====
function loadAccessRequests() {
    fetch('/api/access/requests')
        .then(r => r.json())
        .then(requests => {
            const container = document.getElementById('requestsList');
            if (!container) return;

            if (!requests || requests.length === 0) {
                container.innerHTML = '<p class="empty-state">No pending access requests</p>';
                return;
            }

            container.innerHTML = requests.map(r => `
                <div class="request-item">
                    <div class="user-info">
                        <i class="fas fa-user"></i>
                        <div>
                            <h4>${r.farmer_name}</h4>
                            <small>Device: ${r.device_id} | Status: ${r.status}</small>
                        </div>
                    </div>
                    <div class="user-actions">
                        <button class="btn-sm btn-approve" onclick="updateAccess(${r.id}, 'approved')">
                            <i class="fas fa-check"></i> Approve
                        </button>
                        <button class="btn-sm btn-reject" onclick="updateAccess(${r.id}, 'rejected')">
                            <i class="fas fa-times"></i> Reject
                        </button>
                    </div>
                </div>
            `).join('');
        })
        .catch(err => console.error('[Kishan Kavach] Error loading requests:', err));
}

function updateAccess(requestId, status) {
    fetch(`/api/access/${requestId}/update`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
    })
    .then(r => r.json())
    .then(() => {
        showToast(`Access ${status}!`, 'success');
        loadAccessRequests();
    });
}

function requestAccess() {
    const deviceId = document.getElementById('accessDeviceId')?.value?.trim();
    if (!deviceId) {
        showToast('Please enter a device ID', 'error');
        return;
    }

    fetch('/api/access/request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_id: deviceId })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            showToast('Access request sent!', 'success');
            document.getElementById('accessDeviceId').value = '';
        } else {
            showToast(data.error || 'Request already exists', 'warning');
        }
    });
}

// ===== STATS (ADMIN) =====
function loadStats() {
    fetch('/api/stats')
        .then(r => r.json())
        .then(stats => {
            setText('statUsers', stats.total_users || 0);
            setText('statDevices', stats.total_devices || 0);
            setText('statReadings', stats.total_readings || 0);
            setText('statAlerts', stats.total_alerts || 0);

            const detail = document.getElementById('statsDetail');
            if (detail) {
                detail.innerHTML = `
                    <div class="stat-card glass-card">
                        <i class="fas fa-users"></i>
                        <div class="stat-value">${stats.total_users}</div>
                        <div class="stat-label">Total Users</div>
                    </div>
                    <div class="stat-card glass-card">
                        <i class="fas fa-microchip"></i>
                        <div class="stat-value">${stats.total_devices}</div>
                        <div class="stat-label">Total Devices</div>
                    </div>
                    <div class="stat-card glass-card">
                        <i class="fas fa-database"></i>
                        <div class="stat-value">${stats.total_readings}</div>
                        <div class="stat-label">Total Readings</div>
                    </div>
                    <div class="stat-card glass-card">
                        <i class="fas fa-bell"></i>
                        <div class="stat-value">${stats.total_alerts}</div>
                        <div class="stat-label">Total Alerts</div>
                    </div>
                    <div class="stat-card glass-card">
                        <i class="fas fa-clock"></i>
                        <div class="stat-value">${stats.pending_users}</div>
                        <div class="stat-label">Pending Users</div>
                    </div>
                `;
            }
        })
        .catch(err => console.error('[Kishan Kavach] Error loading stats:', err));
}

// ===== DEVICE MANAGEMENT =====
function showAddDevice() {
    const form = document.getElementById('addDeviceForm');
    if (form) form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function addDevice() {
    const deviceId = document.getElementById('newDeviceId')?.value?.trim();
    const name = document.getElementById('newDeviceName')?.value?.trim();
    const location = document.getElementById('newDeviceLocation')?.value?.trim();
    const crop = document.getElementById('newDeviceCrop')?.value;

    if (!deviceId || !name) {
        showToast('Device ID and Name are required!', 'error');
        return;
    }

    fetch('/api/device/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_id: deviceId, name, location, crop })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            showToast('Device added successfully!', 'success');
            document.getElementById('addDeviceForm').style.display = 'none';
            document.getElementById('newDeviceId').value = '';
            document.getElementById('newDeviceName').value = '';
            document.getElementById('newDeviceLocation').value = '';
            loadDevices();
        } else {
            showToast(data.error || 'Failed to add device', 'error');
        }
    });
}

function deleteDevice(deviceId) {
    if (!confirm(`Delete device ${deviceId}?`)) return;
    fetch(`/api/device/${deviceId}/delete`, { method: 'DELETE' })
        .then(r => r.json())
        .then(() => {
            showToast('Device deleted!', 'warning');
            loadDevices();
        });
}

// ===== TOAST NOTIFICATION =====
function showToast(message, type = 'success', duration = 3000) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}
