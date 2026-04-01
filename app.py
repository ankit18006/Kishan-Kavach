import os
import requests as http_requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load .env file
load_dotenv()

from database import (
    init_db, get_user_by_email, create_user, get_user_by_id,
    get_devices_by_owner, add_device, remove_device, get_all_devices,
    insert_sensor_data, get_latest_sensor_data, get_sensor_history,
    request_access, get_pending_requests, get_approved_farmers,
    update_access_status, revoke_access, get_farmer_approved_devices,
    get_all_owners, get_all_users, delete_user, get_farmer_requests,
    can_send_alert, log_alert, get_device_by_device_id,
    admin_remove_device, update_user_language, get_first_owner_id
)
from auth import login_required, role_required, get_current_user, get_user_language
from models import get_translation, get_all_translations, TRANSLATIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'kishan-kavach-prod-secret-2024-xyz')

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# ===== ENVIRONMENT VARIABLES (from .env or system) =====
WHATSAPP_PHONE = os.environ.get('WHATSAPP_PHONE', '')
WHATSAPP_APIKEY = os.environ.get('WHATSAPP_APIKEY', '')
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')
AUTO_REGISTER_DEVICES = os.environ.get('AUTO_REGISTER_DEVICES', 'true').lower() == 'true'

# Initialize database
init_db()

print("=" * 50)
print("  KISHAN KAVACH - Configuration Status")
print("=" * 50)
print(f"  WhatsApp Phone: {'✅ Set' if WHATSAPP_PHONE else '❌ Not set'}")
print(f"  WhatsApp API Key: {'✅ Set' if WHATSAPP_APIKEY else '❌ Not set'}")
print(f"  Weather API Key: {'✅ Set' if WEATHER_API_KEY else '❌ Not set'}")
print(f"  Auto Register Devices: {'✅ Enabled' if AUTO_REGISTER_DEVICES else '❌ Disabled'}")
print(f"  Secret Key: {'✅ Custom' if os.environ.get('SECRET_KEY') else '⚠️ Default (change in production!)'}")
print("=" * 50)


def send_whatsapp_alert(device_id, temperature, humidity, gas, spoilage):
    """Send WhatsApp alert via CallMeBot API - ONLY for HIGH spoilage"""
    if not WHATSAPP_PHONE or not WHATSAPP_APIKEY:
        print(f"[ALERT] WhatsApp not configured. Skipping alert for {device_id}.")
        print(f"[ALERT] Set WHATSAPP_PHONE and WHATSAPP_APIKEY in .env file")
        return False

    if not can_send_alert(device_id, cooldown_minutes=15):
        print(f"[ALERT] Cooldown active for {device_id}. Skipping.")
        return False

    message = (
        f"🚨 *Kishan Kavach Alert* 🚨\n\n"
        f"Device: {device_id}\n"
        f"🌡 Temperature: {temperature}°C\n"
        f"💧 Humidity: {humidity}%\n"
        f"💨 Gas: {gas} PPM\n"
        f"⚠️ Spoilage Risk: *{spoilage}*\n\n"
        f"Please check immediately!"
    )

    try:
        url = (
            f"https://api.callmebot.com/whatsapp.php"
            f"?phone={WHATSAPP_PHONE}"
            f"&text={http_requests.utils.quote(message)}"
            f"&apikey={WHATSAPP_APIKEY}"
        )
        resp = http_requests.get(url, timeout=10)
        if resp.status_code == 200:
            log_alert(device_id, 'HIGH_SPOILAGE', message)
            print(f"[ALERT] ✅ WhatsApp alert sent for {device_id}")
            return True
        else:
            print(f"[ALERT] ❌ WhatsApp API returned status {resp.status_code}")
    except Exception as e:
        print(f"[ALERT] ❌ WhatsApp failed: {e}")
    return False


def t(key):
    """Shortcut for getting translation based on current user language"""
    lang = get_user_language()
    return get_translation(key, lang)


# ===== ROUTES =====

@app.route('/')
def index():
    if 'user_id' in session:
        user = get_current_user()
        if user:
            return redirect(url_for(f"{user['role']}_dashboard"))
    lang = session.get('language', 'en')
    translations = get_all_translations(lang)
    return render_template('index.html', t=translations, lang=lang)


@app.route('/set_language/<lang>')
def set_language(lang):
    if lang not in ('en', 'hi'):
        lang = 'en'
    session['language'] = lang
    if 'user_id' in session:
        update_user_language(session['user_id'], lang)
    referrer = request.referrer or url_for('index')
    return redirect(referrer)


@app.route('/register', methods=['GET', 'POST'])
def register():
    lang = session.get('language', 'en')
    translations = get_all_translations(lang)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        role = request.form.get('role', 'farmer')
        phone = request.form.get('phone', '').strip()
        pref_lang = request.form.get('language', 'en')

        if not name or not email or not password:
            flash(translations['fill_all_fields'], 'danger')
            return render_template('register.html', t=translations, lang=lang)

        if password != confirm:
            flash(translations['password_mismatch'], 'danger')
            return render_template('register.html', t=translations, lang=lang)

        if len(password) < 6:
            flash(translations['password_min'], 'danger')
            return render_template('register.html', t=translations, lang=lang)

        if role not in ('farmer', 'owner'):
            flash(translations['invalid_role'], 'danger')
            return render_template('register.html', t=translations, lang=lang)

        password_hash = generate_password_hash(password)
        if create_user(name, email, password_hash, role, phone, pref_lang):
            session['language'] = pref_lang
            flash(translations['register_success'], 'success')
            return redirect(url_for('login'))
        else:
            flash(translations['email_exists'], 'danger')

    return render_template('register.html', t=translations, lang=lang)


@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = session.get('language', 'en')
    translations = get_all_translations(lang)

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            session['language'] = user.get('language', 'en')
            flash(f"{get_translation('login_success', user.get('language', 'en'))}, {user['name']}!", 'success')
            return redirect(url_for(f"{user['role']}_dashboard"))
        else:
            flash(translations['wrong_credentials'], 'danger')

    return render_template('login.html', t=translations, lang=lang)


@app.route('/logout')
def logout():
    lang = session.get('language', 'en')
    session.clear()
    session['language'] = lang
    flash(get_translation('logout_success', lang), 'info')
    return redirect(url_for('index'))


# ===== FARMER DASHBOARD =====
@app.route('/farmer')
@login_required
def farmer_dashboard():
    user = get_current_user()
    if not user or user['role'] != 'farmer':
        return redirect(url_for('index'))

    lang = user.get('language', 'en')
    translations = get_all_translations(lang)

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
                           device_data=device_data,
                           t=translations,
                           lang=lang)


# ===== OWNER DASHBOARD =====
@app.route('/owner')
@login_required
def owner_dashboard():
    user = get_current_user()
    if not user or user['role'] != 'owner':
        return redirect(url_for('index'))

    lang = user.get('language', 'en')
    translations = get_all_translations(lang)

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
                           device_data=device_data,
                           t=translations,
                           lang=lang)


# ===== ADMIN DASHBOARD =====
@app.route('/admin')
@login_required
def admin_dashboard():
    user = get_current_user()
    if not user or user['role'] != 'admin':
        return redirect(url_for('index'))

    lang = user.get('language', 'en')
    translations = get_all_translations(lang)

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
                           device_data=device_data,
                           t=translations,
                           lang=lang)


# ===== API ROUTES =====

@app.route('/api/request_access', methods=['POST'])
@login_required
def api_request_access():
    user = get_current_user()
    lang = get_user_language()
    if user['role'] != 'farmer':
        return redirect(url_for('index'))

    owner_id = request.form.get('owner_id')
    if not owner_id:
        flash(get_translation('select_owner', lang), 'danger')
        return redirect(url_for('farmer_dashboard'))

    if request_access(user['id'], int(owner_id)):
        flash(get_translation('request_sent', lang), 'success')
    else:
        flash(get_translation('request_exists', lang), 'warning')

    return redirect(url_for('farmer_dashboard'))


@app.route('/api/approve_access', methods=['POST'])
@login_required
def api_approve_access():
    user = get_current_user()
    lang = get_user_language()
    if user['role'] != 'owner':
        return redirect(url_for('index'))

    req_id = request.form.get('request_id')
    action = request.form.get('action')

    if action == 'approve':
        update_access_status(int(req_id), 'approved')
        flash(get_translation('request_approved', lang), 'success')
    elif action == 'reject':
        update_access_status(int(req_id), 'rejected')
        flash(get_translation('request_rejected', lang), 'info')

    return redirect(url_for('owner_dashboard'))


@app.route('/api/revoke_access', methods=['POST'])
@login_required
def api_revoke_access():
    user = get_current_user()
    lang = get_user_language()
    if user['role'] != 'owner':
        return redirect(url_for('index'))

    access_id = request.form.get('access_id')
    revoke_access(int(access_id))
    flash(get_translation('access_revoked', lang), 'info')
    return redirect(url_for('owner_dashboard'))


@app.route('/api/add_device', methods=['POST'])
@login_required
def api_add_device():
    user = get_current_user()
    lang = get_user_language()
    if user['role'] != 'owner':
        return redirect(url_for('index'))

    device_id = request.form.get('device_id', '').strip()
    name = request.form.get('device_name', 'My Device').strip()
    location = request.form.get('location', '').strip()

    if not device_id:
        flash(get_translation('enter_device_id', lang), 'danger')
        return redirect(url_for('owner_dashboard'))

    if add_device(device_id, user['id'], name, location):
        flash(get_translation('device_added', lang), 'success')
    else:
        flash(get_translation('device_exists', lang), 'danger')

    return redirect(url_for('owner_dashboard'))


@app.route('/api/remove_device', methods=['POST'])
@login_required
def api_remove_device():
    user = get_current_user()
    lang = get_user_language()
    if user['role'] != 'owner':
        return redirect(url_for('index'))

    device_id = request.form.get('device_id')
    remove_device(device_id, user['id'])
    flash(get_translation('device_removed', lang), 'info')
    return redirect(url_for('owner_dashboard'))


@app.route('/api/admin/delete_user', methods=['POST'])
@login_required
def api_admin_delete_user():
    user = get_current_user()
    lang = get_user_language()
    if user['role'] != 'admin':
        return redirect(url_for('index'))

    uid = request.form.get('user_id')
    if int(uid) == user['id']:
        flash(get_translation('cannot_delete_self', lang), 'danger')
        return redirect(url_for('admin_dashboard'))

    delete_user(int(uid))
    flash(get_translation('user_removed', lang), 'info')
    return redirect(url_for('admin_dashboard'))


@app.route('/api/admin/remove_device', methods=['POST'])
@login_required
def api_admin_remove_device():
    user = get_current_user()
    lang = get_user_language()
    if user['role'] != 'admin':
        return redirect(url_for('index'))

    device_id = request.form.get('device_id')
    admin_remove_device(device_id)
    flash(get_translation('device_removed', lang), 'info')
    return redirect(url_for('admin_dashboard'))


@app.route('/api/sensor_history/<device_id>')
@login_required
def api_sensor_history(device_id):
    user = get_current_user()

    # Authorization check
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


@app.route('/api/latest_data/<device_id>')
@login_required
def api_latest_data(device_id):
    latest = get_latest_sensor_data(device_id)
    if latest:
        return jsonify(latest)
    return jsonify({'error': 'No data'}), 404


@app.route('/api/weather')
def api_weather():
    city = request.args.get('city', 'Delhi')
    if not WEATHER_API_KEY:
        return jsonify({
            'city': city,
            'temperature': '--',
            'humidity': '--',
            'description': 'API key not configured',
            'icon': '01d',
            'configured': False
        })

    try:
        lang_param = session.get('language', 'en')
        if lang_param == 'hi':
            lang_param = 'hi'
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city},IN&appid={WEATHER_API_KEY}&units=metric&lang={lang_param}"
        )
        resp = http_requests.get(url, timeout=5)
        data = resp.json()
        if data.get('cod') == 200:
            return jsonify({
                'city': data['name'],
                'temperature': round(data['main']['temp'], 1),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'configured': True
            })
    except Exception as e:
        print(f"[WEATHER] API error: {e}")

    return jsonify({
        'city': city,
        'temperature': '--',
        'humidity': '--',
        'description': get_translation('not_available', session.get('language', 'en')),
        'icon': '01d',
        'configured': bool(WEATHER_API_KEY)
    })


# ===== SOCKET.IO EVENTS =====

@socketio.on('connect')
def handle_connect():
    print(f"[WS] Client connected")


@socketio.on('disconnect')
def handle_disconnect():
    print(f"[WS] Client disconnected")


@socketio.on('iot_data')
def handle_iot_data(data):
    """
    Receives IoT data from ESP32 via Socket.IO
    Expected JSON: {device_id, temperature, humidity, gas, battery}
    """
    try:
        device_id = data.get('device_id')
        temperature = float(data.get('temperature', 0))
        humidity = float(data.get('humidity', 0))
        gas = float(data.get('gas', 0))
        battery = float(data.get('battery', 100))

        if not device_id:
            emit('error', {'message': 'device_id required'})
            return

        # Check if device exists
        device = get_device_by_device_id(device_id)

        if not device:
            # AUTO REGISTER: Register device to first owner
            if AUTO_REGISTER_DEVICES:
                first_owner_id = get_first_owner_id()
                if first_owner_id:
                    add_device(device_id, first_owner_id, f'Auto-{device_id}', '', auto_registered=1)
                    print(f"[IOT] ✅ Auto-registered device {device_id} to owner {first_owner_id}")
                else:
                    print(f"[IOT] ❌ No owner exists. Cannot auto-register {device_id}.")
                    emit('error', {'message': 'No owner registered. Create an owner account first.'})
                    return
            else:
                print(f"[IOT] ❌ Unknown device {device_id}. Auto-register disabled.")
                emit('error', {'message': f'Device {device_id} not registered. Register it first.'})
                return

        # Store sensor data
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

        # Broadcast to ALL connected clients
        emit('sensor_update', payload, broadcast=True)

        # WhatsApp alert ONLY for HIGH spoilage
        if spoilage == 'HIGH':
            send_whatsapp_alert(device_id, temperature, humidity, gas, spoilage)

        print(f"[IOT] {device_id}: T={temperature}°C, H={humidity}%, G={gas}PPM, B={battery}%, S={spoilage}")

    except Exception as e:
        print(f"[IOT] ❌ Error processing data: {e}")
        emit('error', {'message': str(e)})


# ===== START =====

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    socketio.run(app, host='0.0.0.0', port=port, debug=debug, allow_unsafe_werkzeug=True)
