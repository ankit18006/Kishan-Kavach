"""
Kishan Kavach - Main Application
=================================
Single Device | Real Data Only | Production Ready
NO simulation | NO fake data | NO device_id
"""

import os
import time
import requests
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify, session
)
from flask_socketio import SocketIO, emit
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, SensorData, AlertLog, AccessRequest
from ai_engine import SpoilageAI
from crop_data import get_all_crops, get_crop_info, search_crops, get_categories

# ============================================
# APP INITIALIZATION
# ============================================
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Alert cooldown tracker (in-memory)
_last_alert_time = 0


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def owner_required(f):
    """Decorator: only warehouse owner can access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'owner':
            flash('Access denied. Owner only.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def approved_required(f):
    """Decorator: only approved users can access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if current_user.role == 'farmer' and not current_user.is_approved:
            flash('Your access request is pending approval.', 'warning')
            return redirect(url_for('farmer_request'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================
# DATABASE SETUP
# ============================================
with app.app_context():
    db.create_all()
    # Create default owner if not exists
    if not User.query.filter_by(role='owner').first():
        owner = User(
            username='owner',
            email='owner@kishankavach.com',
            password_hash=generate_password_hash('owner123'),
            role='owner',
            is_approved=True
        )
        db.session.add(owner)
        db.session.commit()
        print("[INIT] Default warehouse owner created: owner/owner123")


# ============================================
# AUTH ROUTES
# ============================================
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)

            if user.role == 'farmer' and not user.is_approved:
                return redirect(url_for('farmer_request'))

            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'farmer')

        # Validate
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if role not in ('farmer', 'owner'):
            role = 'farmer'

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            is_approved=(role == 'owner')  # Owners auto-approved
        )
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ============================================
# FARMER ACCESS REQUEST
# ============================================
@app.route('/farmer-request', methods=['GET', 'POST'])
@login_required
def farmer_request():
    if current_user.role != 'farmer':
        return redirect(url_for('dashboard'))

    if current_user.is_approved:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        message = request.form.get('message', '')

        # Check if already has pending request
        existing = AccessRequest.query.filter_by(
            farmer_id=current_user.id, status='pending'
        ).first()

        if existing:
            flash('You already have a pending request.', 'warning')
        else:
            req = AccessRequest(
                farmer_id=current_user.id,
                message=message
            )
            db.session.add(req)
            db.session.commit()
            flash('Access request sent to warehouse owner.', 'success')

    my_requests = AccessRequest.query.filter_by(
        farmer_id=current_user.id
    ).order_by(AccessRequest.requested_at.desc()).all()

    return render_template('farmer_request.html', requests=my_requests)


# ============================================
# OWNER PANEL - MANAGE FARMER REQUESTS
# ============================================
@app.route('/owner-panel')
@login_required
@owner_required
def owner_panel():
    pending = AccessRequest.query.filter_by(status='pending').all()
    all_requests = AccessRequest.query.order_by(
        AccessRequest.requested_at.desc()
    ).all()
    farmers = User.query.filter_by(role='farmer').all()

    return render_template('owner_panel.html',
                           pending=pending,
                           all_requests=all_requests,
                           farmers=farmers)


@app.route('/api/approve-farmer/<int:request_id>', methods=['POST'])
@login_required
@owner_required
def approve_farmer(request_id):
    req = AccessRequest.query.get_or_404(request_id)
    req.status = 'approved'
    req.responded_at = datetime.utcnow()

    farmer = User.query.get(req.farmer_id)
    if farmer:
        farmer.is_approved = True

    db.session.commit()
    flash(f'Farmer {farmer.username} approved.', 'success')
    return redirect(url_for('owner_panel'))


@app.route('/api/reject-farmer/<int:request_id>', methods=['POST'])
@login_required
@owner_required
def reject_farmer(request_id):
    req = AccessRequest.query.get_or_404(request_id)
    req.status = 'rejected'
    req.responded_at = datetime.utcnow()
    db.session.commit()
    flash('Request rejected.', 'info')
    return redirect(url_for('owner_panel'))


# ============================================
# MAIN DASHBOARD
# ============================================
@app.route('/dashboard')
@login_required
@approved_required
def dashboard():
    # Get latest real sensor data
    latest = SensorData.query.order_by(SensorData.timestamp.desc()).first()

    # Get all crops for dropdown
    crops = get_all_crops()
    categories = get_categories()

    # AI analysis (only if real data exists)
    ai_result = None
    if latest:
        ai_result = SpoilageAI.analyze(
            latest.temperature, latest.humidity,
            latest.gas, latest.crop
        )

    return render_template('dashboard.html',
                           latest=latest,
                           ai_result=ai_result,
                           crops=crops,
                           categories=categories)


# ============================================
# API ROUTES (REAL DATA ONLY)
# ============================================
@app.route('/api/latest-data')
@login_required
@approved_required
def api_latest_data():
    """Return latest REAL sensor data"""
    latest = SensorData.query.order_by(SensorData.timestamp.desc()).first()

    if not latest:
        return jsonify({
            'status': 'no_data',
            'message': 'No live data available. Please connect IoT device.'
        })

    ai_result = SpoilageAI.analyze(
        latest.temperature, latest.humidity,
        latest.gas, latest.crop
    )

    return jsonify({
        'status': 'ok',
        'data': latest.to_dict(),
        'ai': ai_result
    })


@app.route('/api/history')
@login_required
@approved_required
def api_history():
    """Return real historical data for graphs"""
    hours = request.args.get('hours', 24, type=int)
    limit = request.args.get('limit', 100, type=int)

    since = datetime.utcnow() - timedelta(hours=hours)
    data = SensorData.query.filter(
        SensorData.timestamp >= since
    ).order_by(SensorData.timestamp.asc()).limit(limit).all()

    if not data:
        return jsonify({
            'status': 'no_data',
            'message': 'No historical data available.',
            'data': []
        })

    return jsonify({
        'status': 'ok',
        'data': [d.to_dict() for d in data]
    })


@app.route('/api/alerts')
@login_required
@approved_required
def api_alerts():
    """Return recent alert logs"""
    alerts = AlertLog.query.order_by(
        AlertLog.created_at.desc()
    ).limit(20).all()

    return jsonify({
        'status': 'ok',
        'data': [a.to_dict() for a in alerts]
    })


@app.route('/api/crop-info/<crop_key>')
@login_required
@approved_required
def api_crop_info(crop_key):
    """Return crop-specific information"""
    info = get_crop_info(crop_key)
    if not info:
        return jsonify({'status': 'error', 'message': 'Crop not found'}), 404

    return jsonify({'status': 'ok', 'data': info})


@app.route('/api/search-crops')
@login_required
@approved_required
def api_search_crops():
    """Search crops by name"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'status': 'ok', 'data': {}})

    results = search_crops(query)
    return jsonify({'status': 'ok', 'data': results})


@app.route('/api/weather')
@login_required
@approved_required
def api_weather():
    """Get real weather data from OpenWeatherMap"""
    api_key = Config.WEATHER_API_KEY
    city = request.args.get('city', Config.WEATHER_CITY)

    if not api_key:
        return jsonify({
            'status': 'no_api_key',
            'message': 'Weather API key not configured.'
        })

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            weather_data = resp.json()
            return jsonify({
                'status': 'ok',
                'data': {
                    'city': weather_data.get('name', city),
                    'temperature': weather_data['main']['temp'],
                    'humidity': weather_data['main']['humidity'],
                    'description': weather_data['weather'][0]['description'],
                    'icon': weather_data['weather'][0]['icon']
                }
            })
        else:
            return jsonify({'status': 'error', 'message': 'Weather API error'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/sensor', methods=['POST'])
def sensor_api():
    data = request.get_json()

    print("ESP32 DATA:", data)

    # सीधे socket event trigger करो
    socketio.emit('sensor_data', data)

    return {"status": "ok"}


# ============================================
# SOCKET.IO — REAL DATA HANDLER (CORE)
# ============================================
def validate_sensor_data(data):
    """Validate incoming sensor data — reject invalid/fake readings"""
    try:
        temp = float(data.get('temperature', 0))
        humidity = float(data.get('humidity', 0))
        gas = float(data.get('gas', 0))
        battery = float(data.get('battery', 0))

        # Reject if all zeros (sensor disconnected)
        if temp == 0 and humidity == 0 and gas == 0:
            return None

        # Reject NaN or out-of-range
        if temp < Config.MIN_VALID_TEMP or temp > Config.MAX_VALID_TEMP:
            return None
        if humidity < Config.MIN_VALID_HUMIDITY or humidity > Config.MAX_VALID_HUMIDITY:
            return None
        if gas < Config.MIN_VALID_GAS or gas > Config.MAX_VALID_GAS:
            return None

        return {
            'temperature': round(temp, 2),
            'humidity': round(humidity, 2),
            'gas': round(gas, 2),
            'battery': round(max(0, min(100, battery)), 1),
            'crop': str(data.get('crop', 'unknown')).strip().lower()
        }
    except (ValueError, TypeError):
        return None


@socketio.on('connect')
def handle_connect():
    print(f"[SOCKET] Client connected: {request.sid}")


@socketio.on('disconnect')
def handle_disconnect():
    print(f"[SOCKET] Client disconnected: {request.sid}")


@socketio.on('sensor_data')
def handle_sensor_data(data):
    """
    MAIN HANDLER — Accepts ONLY real data from ESP32
    NO simulation, NO fake data, NO defaults
    """
    global _last_alert_time

    print(f"[SENSOR] Raw data received: {data}")

    # === VALIDATE ===
    validated = validate_sensor_data(data)
    if validated is None:
        print("[SENSOR] Invalid data rejected.")
        emit('error', {'message': 'Invalid sensor data rejected.'})
        return

    # === AI ANALYSIS ===
    ai_result = SpoilageAI.analyze(
        validated['temperature'],
        validated['humidity'],
        validated['gas'],
        validated['crop']
    )

    # === STORE IN DATABASE ===
    sensor_entry = SensorData(
        temperature=validated['temperature'],
        humidity=validated['humidity'],
        gas=validated['gas'],
        battery=validated['battery'],
        crop=validated['crop'],
        health_score=ai_result['health_score'] if ai_result else 0,
        risk_level=ai_result['risk_level'] if ai_result else 'unknown',
        days_remaining=ai_result['days_remaining'] if ai_result else 0
    )

    db.session.add(sensor_entry)
    db.session.commit()

    # === BUILD BROADCAST PAYLOAD ===
    broadcast_data = {
        **validated,
        'timestamp': sensor_entry.timestamp.isoformat(),
        'ai': ai_result
    }

    # === BROADCAST TO ALL CONNECTED CLIENTS ===
    socketio.emit('sensor_update', broadcast_data, broadcast=True)
    print(f"[BROADCAST] Data sent: temp={validated['temperature']}, "
          f"humidity={validated['humidity']}, gas={validated['gas']}, "
          f"risk={ai_result['risk_level'] if ai_result else 'N/A'}")

    # === ALERT SYSTEM (HIGH risk only, with cooldown) ===
    if ai_result and ai_result['risk_level'] == 'HIGH':
        current_time = time.time()
        if current_time - _last_alert_time > Config.ALERT_COOLDOWN:
            _last_alert_time = current_time

            alert = AlertLog(
                alert_type='spoilage_risk',
                message=ai_result['recommendation'],
                risk_level='HIGH',
                sensor_data_id=sensor_entry.id
            )
            db.session.add(alert)
            db.session.commit()

            socketio.emit('alert', {
                'type': 'HIGH_RISK',
                'message': ai_result['recommendation'],
                'timestamp': datetime.utcnow().isoformat()
            }, broadcast=True)
            print("[ALERT] HIGH risk alert broadcasted!")


@socketio.on('update_crop')
def handle_crop_update(data):
    """Update the crop type for AI analysis"""
    crop = str(data.get('crop', 'unknown')).strip().lower()
    print(f"[CROP] Updated to: {crop}")
    session['selected_crop'] = crop
    emit('crop_updated', {'crop': crop})


# ============================================
# STARTUP
# ============================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(
        app,
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    )
