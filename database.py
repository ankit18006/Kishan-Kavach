import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'kishan_kavach.db')


def get_db():
    """Get database connection - thread safe"""
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'farmer',
        status TEXT NOT NULL DEFAULT 'approved',
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT UNIQUE NOT NULL,
        name TEXT,
        location TEXT,
        crop TEXT DEFAULT 'wheat',
        owner_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_id) REFERENCES users(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT NOT NULL,
        temperature REAL,
        humidity REAL,
        gas REAL,
        battery REAL,
        crop TEXT,
        spoilage_risk TEXT,
        health_score REAL,
        days_remaining REAL,
        future_risk TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS access_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmer_id INTEGER,
        device_id TEXT,
        status TEXT DEFAULT 'pending',
        requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (farmer_id) REFERENCES users(id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        alert_type TEXT,
        message TEXT,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS farmer_device_access (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmer_id INTEGER,
        device_id TEXT,
        granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (farmer_id) REFERENCES users(id)
    )''')

    # Create default admin - APPROVED
    try:
        c.execute(
            "INSERT INTO users (username, password, role, status) VALUES (?, ?, ?, ?)",
            ('admin', 'admin123', 'admin', 'approved')
        )
    except sqlite3.IntegrityError:
        # Already exists - make sure it's approved
        c.execute(
            "UPDATE users SET status = 'approved' WHERE username = 'admin'"
        )

    # Create default owner - APPROVED
    try:
        c.execute(
            "INSERT INTO users (username, password, role, status, phone) VALUES (?, ?, ?, ?, ?)",
            ('owner1', 'owner123', 'owner', 'approved', '+919999999999')
        )
    except sqlite3.IntegrityError:
        # Already exists - make sure it's approved
        c.execute(
            "UPDATE users SET status = 'approved' WHERE username = 'owner1'"
        )

    # Create default devices
    try:
        c.execute(
            "INSERT INTO devices (device_id, name, location, crop, owner_id) VALUES (?, ?, ?, ?, ?)",
            ('ESP32_001', 'Cold Storage Unit 1', 'Warehouse A', 'tomato', 2)
        )
    except sqlite3.IntegrityError:
        pass

    try:
        c.execute(
            "INSERT INTO devices (device_id, name, location, crop, owner_id) VALUES (?, ?, ?, ?, ?)",
            ('ESP32_002', 'Field Sensor 1', 'Farm Block B', 'wheat', 2)
        )
    except sqlite3.IntegrityError:
        pass

    # Fix any existing users stuck in pending
    c.execute("UPDATE users SET status = 'approved' WHERE status = 'pending'")

    conn.commit()
    conn.close()


def insert_sensor_data(data):
    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO sensor_data 
        (device_id, temperature, humidity, gas, battery, crop, 
         spoilage_risk, health_score, days_remaining, future_risk)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (data['device_id'], data['temperature'], data['humidity'],
               data['gas'], data.get('battery', 100), data.get('crop', 'wheat'),
               data.get('spoilage_risk', 'LOW'), data.get('health_score', 100),
               data.get('days_remaining', 30), data.get('future_risk', 'LOW')))
    conn.commit()
    conn.close()


def get_latest_sensor_data(device_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT * FROM sensor_data WHERE device_id = ? 
                 ORDER BY timestamp DESC LIMIT 1''', (device_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def get_sensor_history(device_id, limit=50):
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT * FROM sensor_data WHERE device_id = ? 
                 ORDER BY timestamp DESC LIMIT ?''', (device_id, limit))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_devices(owner_id=None):
    conn = get_db()
    c = conn.cursor()
    if owner_id:
        c.execute('SELECT * FROM devices WHERE owner_id = ?', (owner_id,))
    else:
        c.execute('SELECT * FROM devices')
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user(username):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def create_user(username, password, role, phone=''):
    """Create user - ALL users are auto-approved on registration"""
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO users (username, password, role, status, phone) VALUES (?, ?, ?, ?, ?)',
            (username, password, role, 'approved', phone)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


def get_all_users():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_user_status(user_id, status):
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE users SET status = ? WHERE id = ?', (status, user_id))
    conn.commit()
    conn.close()


def create_access_request(farmer_id, device_id):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        'SELECT * FROM access_requests WHERE farmer_id = ? AND device_id = ? AND status = ?',
        (farmer_id, device_id, 'pending')
    )
    if c.fetchone():
        conn.close()
        return False
    c.execute(
        'INSERT INTO access_requests (farmer_id, device_id) VALUES (?, ?)',
        (farmer_id, device_id)
    )
    conn.commit()
    conn.close()
    return True


def get_access_requests(status='pending'):
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT ar.*, u.username as farmer_name 
                 FROM access_requests ar 
                 JOIN users u ON ar.farmer_id = u.id 
                 WHERE ar.status = ?''', (status,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_access_request(request_id, status):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        'UPDATE access_requests SET status = ? WHERE id = ?',
        (status, request_id)
    )
    if status == 'approved':
        c.execute(
            'SELECT farmer_id, device_id FROM access_requests WHERE id = ?',
            (request_id,)
        )
        row = c.fetchone()
        if row:
            try:
                c.execute(
                    'INSERT INTO farmer_device_access (farmer_id, device_id) VALUES (?, ?)',
                    (row['farmer_id'], row['device_id'])
                )
            except sqlite3.IntegrityError:
                pass
    conn.commit()
    conn.close()


def get_farmer_devices(farmer_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT d.* FROM devices d 
                 JOIN farmer_device_access fda ON d.device_id = fda.device_id 
                 WHERE fda.farmer_id = ?''', (farmer_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_device(device_id, name, location, crop, owner_id):
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO devices (device_id, name, location, crop, owner_id) VALUES (?, ?, ?, ?, ?)',
            (device_id, name, location, crop, owner_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


def update_device_crop(device_id, crop):
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE devices SET crop = ? WHERE device_id = ?', (crop, device_id))
    conn.commit()
    conn.close()


def delete_device(device_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM devices WHERE device_id = ?', (device_id,))
    c.execute('DELETE FROM sensor_data WHERE device_id = ?', (device_id,))
    c.execute('DELETE FROM farmer_device_access WHERE device_id = ?', (device_id,))
    c.execute('DELETE FROM access_requests WHERE device_id = ?', (device_id,))
    conn.commit()
    conn.close()


def delete_user(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    c.execute('DELETE FROM farmer_device_access WHERE farmer_id = ?', (user_id,))
    c.execute('DELETE FROM access_requests WHERE farmer_id = ?', (user_id,))
    conn.commit()
    conn.close()


def get_alert_history(device_id=None, limit=20):
    conn = get_db()
    c = conn.cursor()
    if device_id:
        c.execute(
            'SELECT * FROM alerts WHERE device_id = ? ORDER BY sent_at DESC LIMIT ?',
            (device_id, limit)
        )
    else:
        c.execute('SELECT * FROM alerts ORDER BY sent_at DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def insert_alert(device_id, alert_type, message):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        'INSERT INTO alerts (device_id, alert_type, message) VALUES (?, ?, ?)',
        (device_id, alert_type, message)
    )
    conn.commit()
    conn.close()


def get_system_stats():
    conn = get_db()
    c = conn.cursor()
    stats = {}
    c.execute('SELECT COUNT(*) as count FROM users')
    stats['total_users'] = c.fetchone()['count']
    c.execute('SELECT COUNT(*) as count FROM devices')
    stats['total_devices'] = c.fetchone()['count']
    c.execute('SELECT COUNT(*) as count FROM sensor_data')
    stats['total_readings'] = c.fetchone()['count']
    c.execute('SELECT COUNT(*) as count FROM alerts')
    stats['total_alerts'] = c.fetchone()['count']
    c.execute("SELECT COUNT(*) as count FROM users WHERE status = 'pending'")
    stats['pending_users'] = c.fetchone()['count']
    conn.close()
    return stats
