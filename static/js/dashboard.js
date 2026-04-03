/**
 * Kishan Kavach - Dashboard JavaScript
 * =====================================
 * REAL DATA ONLY | NO simulation | NO dummy values
 * Single Device System
 */

// ============================================
// SOCKET CONNECTION
// ============================================
const socket = io({
    transports: ['websocket', 'polling'],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: Infinity
});

// ============================================
// CHART INITIALIZATION (EMPTY — Real data only)
// ============================================
const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: { duration: 300 },
    scales: {
        x: {
            display: true,
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: '#888', maxTicksLimit: 10, maxRotation: 0 }
        },
        y: {
            display: true,
            grid: { color: 'rgba(255,255,255,0.08)' },
            ticks: { color: '#888' }
        }
    },
    plugins: {
        legend: { display: false }
    }
};

let tempChart, humidityChart, gasChart;
const MAX_CHART_POINTS = 50;

function initCharts() {
    const tempCtx = document.getElementById('tempChart');
    const humCtx = document.getElementById('humidityChart');
    const gasCtx = document.getElementById('gasChart');

    if (!tempCtx || !humCtx || !gasCtx) return;

    tempChart = new Chart(tempCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperature (°C)',
                data: [],
                borderColor: '#ff6b6b',
                backgroundColor: 'rgba(255,107,107,0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 2
            }]
        },
        options: { ...chartOptions }
    });

    humidityChart = new Chart(humCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Humidity (%)',
                data: [],
                borderColor: '#4ecdc4',
                backgroundColor: 'rgba(78,205,196,0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 2
            }]
        },
        options: { ...chartOptions }
    });

    gasChart = new Chart(gasCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Gas (ppm)',
                data: [],
                backgroundColor: 'rgba(255,165,0,0.6)',
                borderColor: '#ffa500',
                borderWidth: 1
            }]
        },
        options: { ...chartOptions }
    });
}

// ============================================
// LOAD HISTORICAL DATA FROM DB (REAL ONLY)
// ============================================
async function loadHistory() {
    try {
        const resp = await fetch('/api/history?hours=24&limit=50');
        const result = await resp.json();

        if (result.status === 'ok' && result.data.length > 0) {
            result.data.forEach(d => {
                const time = new Date(d.timestamp).toLocaleTimeString('en-IN', {
                    hour: '2-digit', minute: '2-digit'
                });
                addChartPoint(time, d.temperature, d.humidity, d.gas);
            });
        }
        // If no data — charts remain empty (correct behavior)
    } catch (err) {
        console.error('[HISTORY] Load failed:', err);
    }
}

function addChartPoint(label, temp, humidity, gas) {
    if (!tempChart || !humidityChart || !gasChart) return;

    [tempChart, humidityChart, gasChart].forEach(chart => {
        if (chart.data.labels.length >= MAX_CHART_POINTS) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }
    });

    tempChart.data.labels.push(label);
    tempChart.data.datasets[0].data.push(temp);
    tempChart.update('none');

    humidityChart.data.labels.push(label);
    humidityChart.data.datasets[0].data.push(humidity);
    humidityChart.update('none');

    gasChart.data.labels.push(label);
    gasChart.data.datasets[0].data.push(gas);
    gasChart.update('none');
}

// ============================================
// LOAD ALERTS (REAL ONLY)
// ============================================
async function loadAlerts() {
    try {
        const resp = await fetch('/api/alerts');
        const result = await resp.json();

        if (result.status === 'ok' && result.data.length > 0) {
            renderAlerts(result.data);
        }
    } catch (err) {
        console.error('[ALERTS] Load failed:', err);
    }
}

function renderAlerts(alerts) {
    const container = document.getElementById('alertsList');
    if (!container) return;

    if (alerts.length === 0) {
        container.innerHTML = `
            <div class="empty-state small">
                <i class="fas fa-check-circle"></i>
                <p>No alerts yet</p>
            </div>`;
        return;
    }

    container.innerHTML = alerts.map(a => `
        <div class="alert-item ${a.risk_level.toLowerCase()}">
            <div class="alert-icon">
                <i class="fas fa-exclamation-triangle"></i>
            </div>
            <div class="alert-content">
                <span class="alert-type">${a.alert_type}</span>
                <p>${a.message}</p>
                <small>${new Date(a.created_at).toLocaleString('en-IN')}</small>
            </div>
        </div>
    `).join('');
}

// ============================================
// UPDATE DASHBOARD (FROM REAL DATA ONLY)
// ============================================
function updateDashboard(data) {
    // Show dashboard, hide no-data message
    const noDataMsg = document.getElementById('noDataMessage');
    const dashContent = document.getElementById('dashboardContent');
    if (noDataMsg) noDataMsg.classList.add('hidden');
    if (dashContent) dashContent.classList.remove('hidden');

    // Update sensor values
    setText('tempValue', `${data.temperature.toFixed(1)}°C`);
    setText('humidityValue', `${data.humidity.toFixed(1)}%`);
    setText('gasValue', `${Math.round(data.gas)} ppm`);
    setText('batteryValue', `${Math.round(data.battery)}%`);

    // Update sensor bars
    setBarWidth('tempBar', (data.temperature / 50) * 100);
    setBarWidth('humidityBar', data.humidity);
    setBarWidth('gasBar', (data.gas / 1000) * 100);
    setBarWidth('batteryBar', data.battery);

    // Color-code temperature
    const tempCard = document.querySelector('.temp-card');
    if (tempCard) {
        tempCard.classList.remove('danger', 'warning', 'safe');
        if (data.temperature > 35) tempCard.classList.add('danger');
        else if (data.temperature > 28) tempCard.classList.add('warning');
        else tempCard.classList.add('safe');
    }

    // Update AI results
    if (data.ai) {
        updateAI(data.ai);
    }

    // Update chart with new real data point
    const time = new Date().toLocaleTimeString('en-IN', {
        hour: '2-digit', minute: '2-digit', second: '2-digit'
    });
    addChartPoint(time, data.temperature, data.humidity, data.gas);

    // Update last update time
    setText('lastUpdate', `Last: ${time}`);
}

function updateAI(ai) {
    setText('healthScore', ai.health_score);
    setText('daysRemaining', ai.days_remaining);
    setText('futureRisk', ai.future_risk);
    setText('idealTemp', ai.ideal_temp);
    setText('idealHumidity', ai.ideal_humidity);
    setText('recommendation', ai.recommendation);

    // Update risk badge
    const badge = document.getElementById('riskBadge');
    if (badge) {
        badge.textContent = ai.risk_level;
        badge.className = `risk-badge ${ai.risk_level.toLowerCase()}`;
    }

    // Update risk card color
    const card = document.getElementById('riskCard');
    if (card) {
        card.className = `risk-card risk-${ai.risk_level.toLowerCase()}`;
    }
}

// ============================================
// HELPER FUNCTIONS
// ============================================
function setText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
}

function setBarWidth(id, percent) {
    const el = document.getElementById(id);
    if (el) el.style.width = `${Math.min(100, Math.max(0, percent))}%`;
}

function dismissAlert() {
    const banner = document.getElementById('alertBanner');
    if (banner) banner.classList.add('hidden');
}

// ============================================
// CROP SELECTOR
// ============================================
const cropSelect = document.getElementById('cropSelect');
if (cropSelect) {
    cropSelect.addEventListener('change', function () {
        socket.emit('update_crop', { crop: this.value });
    });
}

// Crop search filter
const cropSearch = document.getElementById('cropSearch');
if (cropSearch) {
    cropSearch.addEventListener('input', function () {
        const query = this.value.toLowerCase();
        const options = cropSelect.options;

        for (let i = 1; i < options.length; i++) {
            const text = options[i].text.toLowerCase();
            const val = options[i].value.toLowerCase();
            options[i].style.display =
                (text.includes(query) || val.includes(query)) ? '' : 'none';
        }
    });
}

// ============================================
// SOCKET EVENT HANDLERS (REAL DATA ONLY)
// ============================================
socket.on('connect', () => {
    console.log('[SOCKET] Connected to server');
    const bar = document.getElementById('connectionBar');
    const dot = document.getElementById('connectionDot');
    const text = document.getElementById('connectionText');

    if (bar) bar.className = 'connection-bar online';
    if (dot) dot.className = 'dot online';
    if (text) text.textContent = 'Connected — Waiting for sensor data...';
});

socket.on('disconnect', () => {
    console.log('[SOCKET] Disconnected');
    const bar = document.getElementById('connectionBar');
    const dot = document.getElementById('connectionDot');
    const text = document.getElementById('connectionText');

    if (bar) bar.className = 'connection-bar offline';
    if (dot) dot.className = 'dot offline';
    if (text) text.textContent = 'Device offline — Reconnecting...';
});

// === MAIN DATA HANDLER — ONLY REAL DATA ===
socket.on('sensor_update', (data) => {
    console.log('[SENSOR] Real data received:', data);

    const text = document.getElementById('connectionText');
    if (text) text.textContent = 'Connected — Receiving live data';

    updateDashboard(data);
});

// === ALERT HANDLER ===
socket.on('alert', (data) => {
    console.log('[ALERT]', data);

    const banner = document.getElementById('alertBanner');
    const msg = document.getElementById('alertMessage');

    if (banner && msg) {
        msg.textContent = data.message;
        banner.classList.remove('hidden');
        banner.className = 'alert-banner high';
    }

    // Reload alerts list
    loadAlerts();

    // Auto-dismiss after 30 seconds
    setTimeout(dismissAlert, 30000);
});

socket.on('error', (data) => {
    console.warn('[ERROR]', data.message);
});

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    loadHistory();
    loadAlerts();
});
