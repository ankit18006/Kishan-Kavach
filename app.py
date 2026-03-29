import os
import json
import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash

from database import (
    init_db, get_user_by_email, create_user, get_user_by_id,
    get_devices_by_owner, add_device, remove_device, get_all_devices,
    insert_sensor_data, get_latest_sensor_data, get_sensor_history,
    request_access, get_pending_requests, get_approved_farmers,
    update_access_status, revoke_access, get_farmer_approved_devices,
    get_all_owners, get_all_users, delete_user, get_farmer_requests,
    can_send_alert, log_alert, calculate_spoilage, get_device_by_device_id,
    admin_remove_device
)
from auth import login_required, role_required, get_current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'kishan-kavach-secret-key-2024')

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# WhatsApp config
CALLMEBOT_PHONE = os.environ.get('WHATSAPP_PHONE', '')
CALLMEBOT_APIKEY = os.environ.get('WHATSAPP_APIKEY', '')
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')

init_db()


def send_whatsapp_alert(device_id, temperature, humidity, gas, spoilage):
    if not CALLMEBOT_PHONE or not CALLMEBOT_APIKEY:
        print("[ALERT] WhatsApp not configured. Skipping.")
        return False

    if not can_send_alert(device_id, cooldown_minutes=15):
        print(f"[ALERT] Cooldown active for {device_id}. Skipping.")
        return False

    message = (
        f"🚨 *Kishan Kavach Alert* 🚨\n\n"
        f"डिवाइस: {device_id}\n"
        f"🌡 तापमान: {temperature}°C\n"
        f"💧 नमी: {humidity}%\n"
        f"💨 गैस: {gas} PPM\n"
        f"⚠️ खराब होने का जोखिम: *{spoilage}*\n\n"
        f"कृपया तुरंत जांच करें!"
    )

    try:
        url = f"https://api.callmebot.com/whatsapp.php?phone={CALLMEBOT_PHONE}&text={requests.utils.quote(message)}&apikey={CALLMEBOT_APIKEY}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            log_alert(device_id, 'HIGH_SPOILAGE', message)
            print(f"[ALERT] WhatsApp sent for {device_id}")
            return True
    except Exception as e:
        print(f"[ALERT] WhatsApp failed: {e}")
    return False


# ===== ROUTES =====

@app.route('/')
def index():
    if 'user_id' in session:
        user = get_current_user()
        if user:
            return redirect(url_for(f"{user['role']}_dashboard"))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        role = request.form.get('role', 'farmer')
        phone = request.form.get('phone', '').strip()

        if not name or not email or not password:
            flash('सभी फील्ड भरें', 'danger')
            return render_template('register.html')

        if password != confirm:
            flash('पासवर्ड मेल नहीं खाते', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('पासवर्ड कम से कम 6 अक्षर का होना चाहिए', 'danger')
            return render_template('register.html')

        if role not in ('farmer', 'owner'):
            flash('अमान्य भूमिका', 'danger')
            return render_template('register.html')

        password_hash = generate_password_hash(password)
        if create_user(name, email, password_hash, role, phone):
            flash('रजिस्ट्रेशन सफल! कृपया लॉगिन करें', 'success')
            return redirect(url_for('login'))
        else:
            flash('यह ईमेल पहले से रजिस्टर है', 'danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            flash(f'स्वागत है, {user["name"]}!', 'success')
            return redirect(url_for(f"{user['role']}_dashboard"))
        else:
            flash('गलत ईमेल या पासवर्ड', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('आप सफलतापूर्वक लॉगआउट हो गए', 'info')
    return redirect(url_for('index'))


# ===== FARMER DASHBOARD =====

@app.route('/farmer')
@login_required
def farmer_dashboard():
    user = get_current_user()
    if user['role'] != 'farmer':
        return redirect(url_for(f"{user['role']}_dashboard"))

    approved_devices = get_farmer_approved_devices(user['id'])
    owners = get_all_owners()
    my_requests = get_farmer_requests(user['id'])

    device_data = {}
    for dev in approved_devices:
        latest = get_latest_sensor_data(dev['device_id'])
        if latest:
            device_data[dev['device_id']] = latest

    return render_template('farmer.html',
                           user=user,
                           approved_devices=approved_devices,
                           owners=owners,
                           my_requests=my_requests,
                           device_data=device_data)


# ===== OWNER DASHBOARD =====

@app.route('/owner')
@login_required
def owner_dashboard():
    user = get_current_user()
    if user['role'] != 'owner':
        return redirect(url_for(f"{user['role']}_dashboard"))

    devices = get_devices_by_owner(user['id'])
    pending = get_pending_requests(user['id'])
    approved = get_approved_farmers(user['id'])

    device_data = {}
    for dev in devices:
        latest = get_latest_sensor_data(dev['device_id'])
        if latest:
            device_data[dev['device_id']] = latest

    return render_template('owner.html',
                           user=user,
                           devices=devices,
                           pending_requests=pending,
                           approved_farmers=approved,
                           device_data=device_data)


# ===== ADMIN DASHBOARD =====

@app.route('/admin')
@login_required
def admin_dashboard():
    user = get_current_user()
    if user['role'] != 'admin':
        return redirect(url_for(f"{user['role']}_dashboard"))

    all_users = get_all_users()
    all_devices = get_all_devices()

    device_data = {}
    for dev in all_devices:
        latest = get_latest_sensor_data(dev['device_id'])
        if latest:
            device_data[dev['device_id']] = latest

    return render_template('admin.html',
                           user=user,
                           all_users=all_users,
                           all_devices=all_devices,
                           device_data=device_data)


# ===== API ROUTES =====

@app.route('/api/request_access', methods=['POST'])
@login_required
def api_request_access():
    user = get_current_user()
    if user['role'] != 'farmer':
        return jsonify({'error': 'Only farmers can request access'}), 403

    owner_id = request.form.get('owner_id')
    if not owner_id:
        flash('कृपया मालिक चुनें', 'danger')
        return redirect(url_for('farmer_dashboard'))

    if request_access(user['id'], int(owner_id)):
        flash('अनुरोध भेजा गया!', 'success')
    else:
        flash('अनुरोध पहले से मौजूद है', 'warning')

    return redirect(url_for('farmer_dashboard'))


@app.route('/api/approve_access', methods=['POST'])
@login_required
def api_approve_access():
    user = get_current_user()
    if user['role'] != 'owner':
        return jsonify({'error': 'Unauthorized'}), 403

    req_id = request.form.get('request_id')
    action = request.form.get('action')

    if action == 'approve':
        update_access_status(int(req_id), 'approved')
        flash('अनुरोध स्वीकार किया', 'success')
    elif action == 'reject':
        update_access_status(int(req_id), 'rejected')
        flash('अनुरोध अस्वीकार किया', 'info')

    return redirect(url_for('owner_dashboard'))


@app.route('/api/revoke_access', methods=['POST'])
@login_required
def api_revoke_access():
    user = get_current_user()
    if user['role'] != 'owner':
        return jsonify({'error': 'Unauthorized'}), 403

    access_id = request.form.get('access_id')
    revoke_access(int(access_id))
    flash('एक्सेस हटा दिया गया', 'info')
    return redirect(url_for('owner_dashboard'))


@app.route('/api/add_device', methods=['POST'])
@login_required
def api_add_device():
    user = get_current_user()
    if user['role'] != 'owner':
        return jsonify({'error': 'Unauthorized'}), 403

    device_id = request.form.get('device_id', '').strip()
    name = request.form.get('device_name', 'My Device').strip()
    location = request.form.get('location', '').strip()

    if not device_id:
        flash('डिवाइस ID डालें', 'danger')
        return redirect(url_for('owner_dashboard'))

    if add_device(device_id, user['id'], name, location):
        flash('डिवाइस जोड़ा गया!', 'success')
    else:
        flash('यह डिवाइस ID पहले से मौजूद है', 'danger')

    return redirect(url_for('owner_dashboard'))


@app.route('/api/remove_device', methods=['POST'])
@login_required
def api_remove_device():
    user = get_current_user()
    if user['role'] != 'owner':
        return jsonify({'error': 'Unauthorized'}), 403

    device_id = request.form.get('device_id')
    remove_device(device_id, user['id'])
    flash('डिवाइस हटा दिया गया', 'info')
    return redirect(url_for('owner_dashboard'))


@app.route('/api/admin/delete_user', methods=['POST'])
@login_required
def api_admin_delete_user():
    user = get_current_user()
    if user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    uid = request.form.get('user_id')
    if int(uid) == user['id']:
        flash('आप खुद को नहीं हटा सकते', 'danger')
        return redirect(url_for('admin_dashboard'))

    delete_user(int(uid))
    flash('उपयोगकर्ता हटा दिया गया', 'info')
    return redirect(url_for('admin_dashboard'))


@app.route('/api/admin/remove_device', methods=['POST'])
@login_required
def api_admin_remove_device():
    user = get_current_user()
    if user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    device_id = request.form.get('device_id')
    admin_remove_device(device_id)
    flash('डिवाइस हटा दिया गया', 'info')
    return redirect(url_for('admin_dashboard'))


@app.route('/api/sensor_history/<device_id>')
@login_required
def api_sensor_history(device_id):
    user = get_current_user()

    # Check authorization
    if user['role'] == 'admin':
        pass
    elif user['role'] == 'owner':
        devices = get_devices_by_owner(user['id'])
        if not any(d['device_id'] == device_id for d in devices):
            return jsonify({'error': 'Unauthorized'}), 403
    elif user['role'] == 'farmer':
        approved = get_farmer_approved_devices(user['id'])
        if not any(d['device_id'] == device_id for d in approved):
            return jsonify({'error': 'Unauthorized'}), 403

    history = get_sensor_history(device_id, 50)
    history.reverse()
    return jsonify(history)


@app.route('/api/weather')
def api_weather():
    city = request.args.get('city', 'Delhi')
    if not WEATHER_API_KEY:
        return jsonify({
            'city': city,
            'temperature': '--',
            'humidity': '--',
            'description': 'API key not configured',
            'icon': '01d'
        })

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={WEATHER_API_KEY}&units=metric&lang=hi"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get('cod') == 200:
            return jsonify({
                'city': data['name'],
                'temperature': round(data['main']['temp'], 1),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            })
    except Exception as e:
        print(f"Weather API error: {e}")

    return jsonify({
        'city': city,
        'temperature': '--',
        'humidity': '--',
        'description': 'उपलब्ध नहीं',
        'icon': '01d'
    })


@app.route('/api/latest_data/<device_id>')
@login_required
def api_latest_data(device_id):
    latest = get_latest_sensor_data(device_id)
    if latest:
        return jsonify(latest)
    return jsonify({'error': 'No data'}), 404


# ===== SOCKET.IO EVENTS =====

@socketio.on('connect')
def handle_connect():
    print(f"[WS] Client connected")


@socketio.on('disconnect')
def handle_disconnect():
    print(f"[WS] Client disconnected")


@socketio.on('iot_data')
def handle_iot_data(data):
    try:
        device_id = data.get('device_id')
        temperature = float(data.get('temperature', 0))
        humidity = float(data.get('humidity', 0))
        gas = float(data.get('gas', 0))
        battery = float(data.get('battery', 100))

        if not device_id:
            emit('error', {'message': 'device_id required'})
            return

        # Auto-register device if not exists
        device = get_device_by_device_id(device_id)
        if not device:
            print(f"[IOT] Unknown device: {device_id}. Ignoring.")
            emit('error', {'message': 'Device not registered'})
            return

        # Store data
        spoilage = insert_sensor_data(device_id, temperature, humidity, gas, battery)

        payload = {
            'device_id': device_id,
            'temperature': temperature,
            'humidity': humidity,
            'gas': gas,
            'battery': battery,
            'spoilage_level': spoilage,
            'timestamp': datetime.now().isoformat()
        }

        # Broadcast to all clients
        emit('sensor_update', payload, broadcast=True)

        # WhatsApp alert for HIGH spoilage
        if spoilage == 'HIGH':
            send_whatsapp_alert(device_id, temperature, humidity, gas, spoilage)

        print(f"[IOT] {device_id}: T={temperature}, H={humidity}, G={gas}, B={battery}, S={spoilage}")

    except Exception as e:
        print(f"[IOT] Error: {e}")
        emit('error', {'message': str(e)})


# ===== SIMULATE DATA (for testing) =====

@app.route('/api/simulate', methods=['POST'])
def simulate_data():
    data = request.get_json() or {}
    device_id = data.get('device_id', 'ESP32_001')
    temperature = float(data.get('temperature', 28))
    humidity = float(data.get('humidity', 65))
    gas = float(data.get('gas', 300))
    battery = float(data.get('battery', 85))

    device = get_device_by_device_id(device_id)
    if not device:
        return jsonify({'error': 'Device not registered'}), 404

    spoilage = insert_sensor_data(device_id, temperature, humidity, gas, battery)

    payload = {
        'device_id': device_id,
        'temperature': temperature,
        'humidity': humidity,
        'gas': gas,
        'battery': battery,
        'spoilage_level': spoilage,
        'timestamp': datetime.now().isoformat()
    }

    socketio.emit('sensor_update', payload)

    if spoilage == 'HIGH':
        send_whatsapp_alert(device_id, temperature, humidity, gas, spoilage)

    return jsonify({'status': 'ok', 'spoilage': spoilage, 'data': payload})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)
