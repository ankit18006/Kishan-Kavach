"""
Kishan Kavach - Smart Agriculture IoT Platform
Main Application
"""

import os
import json
import time
import random
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from database import (
    init_db, get_db, insert_sensor_data, get_latest_sensor_data,
    get_sensor_history, get_all_devices, get_user, create_user,
    get_all_users, update_user_status, get_access_requests,
    update_access_request, create_access_request, get_farmer_devices,
    add_device, update_device_crop, delete_device, delete_user,
    get_alert_history, insert_alert, get_system_stats, get_user_by_id
)
from crop_data import get_crop_info, get_all_crops, get_crop_list, search_crops, CROP_DATABASE
from ai_engine import AIEngine
from auth import login_required, role_required, admin_required

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'kishan-kavach-secret-key-2024')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Alert cooldown tracking
alert_cooldowns = {}
ALERT_COOLDOWN_SECONDS = 300  # 5 minutes

# Weather API
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')


def get_weather(city='Delhi'):
    """Get weather data from OpenWeatherMap API"""
    try:
        if WEATHER_API_KEY:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    'city': city,
                    'temp': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'wind': data['wind']['speed']
                }
    except Exception:
        pass
    # Return mock data if API not available
    return {
        'city': city,
        'temp': round(random.uniform(20, 35), 1),
        'humidity': random.randint(40, 80),
        'description': 'partly cloudy',
        'icon': '02d',
        'wind': round(random.uniform(2, 10), 1)
    }


def send_whatsapp_alert(phone, message):
    """Send WhatsApp alert (placeholder - integrate with Twilio/CallMeBot)"""
    try:
        # CallMeBot integration example:
        # url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={message}&apikey=YOUR_KEY"
        # requests.get(url, timeout=10)
        print(f"[WhatsApp Alert] To: {phone} | Message: {message}")
        return True
    except Exception as e:
        print(f"[WhatsApp Error] {e}")
        return False


def check_and_send_alert(device_id, analysis, crop_name):
    """Check if alert should be sent with cooldown protection"""
    global alert_cooldowns
    now = time.time()

    if analysis['spoilage_risk'] == 'HIGH':
        last_alert = alert_cooldowns.get(device_id, 0)
        if now - last_alert > ALERT_COOLDOWN_SECONDS:
            message = (
                f"🚨 KISHAN KAVACH ALERT 🚨\n"
                f"Device: {device_id}\n"
                f"Crop: {crop_name}\n"
                f"Risk: {analysis['spoilage_risk']}\n"
                f"Health: {analysis['health_score']}%\n"
                f"Days Left: {analysis['days_remaining']}\n"
                f"Condition: {analysis['condition']}"
            )

            insert_alert(device_id, 'HIGH_RISK', message)
            alert_cooldowns[device_id] = now

            # Send WhatsApp (would need real phone numbers from device owner)
            send_whatsapp_alert('+919999999999', message)

            return True
    return False


# ======================== ROUTES ========================

@app.route('/')
def index():
    if 'user_id' in session:
        role = session.get('role', 'farmer')
        if role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif role == 'owner':
            return redirect(url_for('owner_dashboard'))
        else:
            return redirect(url_for('farmer_dashboard'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = get_user(username)
        if user and user['password'] == password:
            if user['status'] != 'approved':
                flash('Your account is pending approval.', 'warning')
                return render_template('login.html')

            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user['role'] == 'owner':
                return redirect(url_for('owner_dashboard'))
            else:
                return redirect(url_for('farmer_dashboard'))
        else:
            flash('Invalid credentials!', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'farmer')
        phone = request.form.get('phone', '').strip()

        if not username or not password:
            flash('Username and password required!', 'error')
            return render_template('register.html')

        if create_user(username, password, role, phone):
            flash('Registration successful! Waiting for approval.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists!', 'error')

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ======================== FARMER DASHBOARD ========================

@app.route('/farmer')
@login_required
def farmer_dashboard():
    if session.get('role') not in ['farmer', 'admin']:
        return redirect(url_for('login'))
    return render_template('farmer.html')


# ======================== OWNER DASHBOARD ========================

@app.route('/owner')
@login_required
def owner_dashboard():
    if session.get('role') not in ['owner', 'admin']:
        return redirect(url_for('login'))
    return render_template('owner.html')


# ======================== ADMIN DASHBOARD ========================

@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin.html')


# ======================== API ROUTES ========================

@app.route('/api/crops')
def api_crops():
    """Get all crops with categories"""
    return jsonify(get_all_crops())


@app.route('/api/crops/list')
def api_crops_list():
    return jsonify(get_crop_list())


@app.route('/api/crops/search')
def api_crops_search():
    query = request.args.get('q', '')
    return jsonify(search_crops(query))


@app.route('/api/crop/<crop_key>')
def api_crop_info(crop_key):
    info = get_crop_info(crop_key)
    if info:
        return jsonify(info)
    return jsonify({'error': 'Crop not found'}), 404


@app.route('/api/devices')
@login_required
def api_devices():
    role = session.get('role')
    user_id = session.get('user_id')
    if role == 'admin':
        devices = get_all_devices()
    elif role == 'owner':
        devices = get_all_devices(user_id)
    else:
        devices = get_farmer_devices(user_id)
    return jsonify(devices)


@app.route('/api/device/<device_id>/data')
@login_required
def api_device_data(device_id):
    latest = get_latest_sensor_data(device_id)
    history = get_sensor_history(device_id, 50)
    
    if latest:
        crop_key = latest.get('crop', 'wheat')
        analysis = AIEngine.full_analysis(
            latest['temperature'], latest['humidity'], latest['gas'],
            crop_key, history
        )
        predictions = AIEngine.generate_prediction_data(
            latest['temperature'], latest['humidity'], latest['gas'],
            analysis['trend']
        )
        timeline = AIEngine.generate_spoilage_timeline(
            analysis['health_score'], analysis['days_remaining'], crop_key
        )
    else:
        analysis = {}
        predictions = {}
        timeline = []

    return jsonify({
        'latest': latest,
        'history': history,
        'analysis': analysis,
        'predictions': predictions,
        'timeline': timeline
    })


@app.route('/api/device/add', methods=['POST'])
@login_required
def api_add_device():
    data = request.json
    device_id = data.get('device_id', '').strip()
    name = data.get('name', '').strip()
    location = data.get('location', '').strip()
    crop = data.get('crop', 'wheat').strip()
    owner_id = session.get('user_id')

    if add_device(device_id, name, location, crop, owner_id):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Device ID already exists'}), 400


@app.route('/api/device/<device_id>/crop', methods=['PUT'])
@login_required
def api_update_crop(device_id):
    data = request.json
    crop = data.get('crop', 'wheat')
    update_device_crop(device_id, crop)
    return jsonify({'success': True})


@app.route('/api/device/<device_id>/delete', methods=['DELETE'])
@login_required
def api_delete_device(device_id):
    delete_device(device_id)
    return jsonify({'success': True})


@app.route('/api/users')
@admin_required
def api_users():
    return jsonify(get_all_users())


@app.route('/api/user/<int:user_id>/status', methods=['PUT'])
@login_required
def api_update_user_status(user_id):
    data = request.json
    status = data.get('status', 'pending')
    update_user_status(user_id, status)
    return jsonify({'success': True})


@app.route('/api/user/<int:user_id>/delete', methods=['DELETE'])
@admin_required
def api_delete_user(user_id):
    delete_user(user_id)
    return jsonify({'success': True})


@app.route('/api/access/request', methods=['POST'])
@login_required
def api_access_request():
    data = request.json
    device_id = data.get('device_id', '')
    farmer_id = session.get('user_id')
    if create_access_request(farmer_id, device_id):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Request already exists'}), 400


@app.route('/api/access/requests')
@login_required
def api_access_requests():
    status = request.args.get('status', 'pending')
    return jsonify(get_access_requests(status))


@app.route('/api/access/<int:request_id>/update', methods=['PUT'])
@login_required
def api_update_access(request_id):
    data = request.json
    status = data.get('status', 'pending')
    update_access_request(request_id, status)
    return jsonify({'success': True})


@app.route('/api/alerts')
@login_required
def api_alerts():
    device_id = request.args.get('device_id')
    limit = request.args.get('limit', 20, type=int)
    return jsonify(get_alert_history(device_id, limit))


@app.route('/api/weather')
def api_weather():
    city = request.args.get('city', 'Delhi')
    return jsonify(get_weather(city))


@app.route('/api/stats')
@login_required
def api_stats():
    return jsonify(get_system_stats())


@app.route('/api/simulate', methods=['POST'])
@login_required
def api_simulate():
    """Simulate sensor data for testing"""
    data = request.json or {}
    device_id = data.get('device_id', 'ESP32_001')
    crop = data.get('crop', 'tomato')

    crop_info = get_crop_info(crop)
    if crop_info:
        ideal_temp = (crop_info['temp_min'] + crop_info['temp_max']) / 2
        ideal_hum = (crop_info['humidity_min'] + crop_info['humidity_max']) / 2
        temp = ideal_temp + random.uniform(-8, 15)
        humidity = ideal_hum + random.uniform(-15, 15)
    else:
        temp = random.uniform(15, 40)
        humidity = random.uniform(40, 95)

    sensor_data = {
        'device_id': device_id,
        'temperature': round(temp, 1),
        'humidity': round(min(100, max(0, humidity)), 1),
        'gas': round(random.uniform(100, 600), 1),
        'battery': round(random.uniform(20, 100), 1),
        'crop': crop
    }

    # Process through AI engine
    history = get_sensor_history(device_id, 10)
    analysis = AIEngine.full_analysis(
        sensor_data['temperature'], sensor_data['humidity'],
        sensor_data['gas'], crop, history
    )

    sensor_data.update({
        'spoilage_risk': analysis['spoilage_risk'],
        'health_score': analysis['health_score'],
        'days_remaining': analysis['days_remaining'],
        'future_risk': analysis['future_risk']
    })

    insert_sensor_data(sensor_data)
    check_and_send_alert(device_id, analysis, crop)

    broadcast_data = {**sensor_data, 'analysis': analysis, 'timestamp': datetime.now().isoformat()}
    socketio.emit('sensor_update', broadcast_data)

    return jsonify({'success': True, 'data': broadcast_data})


# ======================== SOCKET.IO EVENTS ========================

@socketio.on('connect')
def handle_connect():
    print(f'[Socket.IO] Client connected: {request.sid}')
    emit('connected', {'status': 'Connected to Kishan Kavach'})


@socketio.on('disconnect')
def handle_disconnect():
    print(f'[Socket.IO] Client disconnected: {request.sid}')


@socketio.on('sensor_data')
def handle_sensor_data(data):
    """Handle incoming sensor data from ESP32"""
    try:
        device_id = data.get('device_id', 'unknown')
        temperature = float(data.get('temperature', 0))
        humidity = float(data.get('humidity', 0))
        gas = float(data.get('gas', 0))
        battery = float(data.get('battery', 100))
        crop = data.get('crop', 'wheat')

        history = get_sensor_history(device_id, 10)
        analysis = AIEngine.full_analysis(temperature, humidity, gas, crop, history)

        sensor_record = {
            'device_id': device_id,
            'temperature': temperature,
            'humidity': humidity,
            'gas': gas,
            'battery': battery,
            'crop': crop,
            'spoilage_risk': analysis['spoilage_risk'],
            'health_score': analysis['health_score'],
            'days_remaining': analysis['days_remaining'],
            'future_risk': analysis['future_risk']
        }

        insert_sensor_data(sensor_record)
        check_and_send_alert(device_id, analysis, crop)

        broadcast_data = {
            **sensor_record,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }

        emit('sensor_update', broadcast_data, broadcast=True)
        emit('data_received', {'status': 'ok', 'device_id': device_id})

        print(f"[Sensor] {device_id} | T:{temperature} H:{humidity} G:{gas} | "
              f"Score:{analysis['health_score']} Risk:{analysis['spoilage_risk']}")

    except Exception as e:
        print(f"[Error] Processing sensor data: {e}")
        emit('error', {'message': str(e)})


@socketio.on('request_data')
def handle_request_data(data):
    """Handle request for specific device data"""
    device_id = data.get('device_id', '')
    latest = get_latest_sensor_data(device_id)
    history = get_sensor_history(device_id, 50)

    if latest:
        analysis = AIEngine.full_analysis(
            latest['temperature'], latest['humidity'], latest['gas'],
            latest.get('crop', 'wheat'), history
        )
        predictions = AIEngine.generate_prediction_data(
            latest['temperature'], latest['humidity'], latest['gas'],
            analysis['trend']
        )
    else:
        analysis = {}
        predictions = {}

    emit('device_data', {
        'device_id': device_id,
        'latest': latest,
        'history': history,
        'analysis': analysis,
        'predictions': predictions
    })


# ======================== INIT ========================

init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
