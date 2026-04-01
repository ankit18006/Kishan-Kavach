import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kishan_kavach.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('farmer', 'owner', 'admin')),
            phone TEXT DEFAULT '',
            language TEXT DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT UNIQUE NOT NULL,
            owner_id INTEGER NOT NULL,
            name TEXT DEFAULT 'My Device',
            location TEXT DEFAULT '',
            auto_registered INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS access_control (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            owner_id INTEGER NOT NULL,
            device_id INTEGER,
            status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
            requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            responded_at TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            gas REAL NOT NULL,
            battery REAL NOT NULL,
            spoilage_level TEXT DEFAULT 'LOW',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alert_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            message TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sensor_device ON sensor_data(device_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sensor_timestamp ON sensor_data(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_access_farmer ON access_control(farmer_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_access_owner ON access_control(owner_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_devices_owner ON devices(owner_id)')

    # Default admin
    cursor.execute("SELECT id FROM users WHERE role='admin' LIMIT 1")
    if not cursor.fetchone():
        from werkzeug.security import generate_password_hash
        cursor.execute(
            "INSERT INTO users (name, email, password, role, phone) VALUES (?, ?, ?, ?, ?)",
            ('Admin', 'admin@kishankavach.com', generate_password_hash('admin123'), 'admin', '')
        )

    conn.commit()
    conn.close()


def calculate_spoilage(temperature, humidity, gas):
    if temperature > 30 or humidity > 80 or gas > 400:
        return 'HIGH'
    elif temperature > 25:
        return 'MEDIUM'
    else:
        return 'LOW'


# ===== USER FUNCTIONS =====

def get_user_by_email(email):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
    conn.close()
    return dict(user) if user else None


def get_user_by_id(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None


def create_user(name, email, password_hash, role, phone='', language='en'):
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (name, email, password, role, phone, language) VALUES (?, ?, ?, ?, ?, ?)',
            (name, email, password_hash, role, phone, language)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


def update_user_language(user_id, language):
    conn = get_db()
    conn.execute('UPDATE users SET language=? WHERE id=?', (language, user_id))
    conn.commit()
    conn.close()


def get_all_users():
    conn = get_db()
    rows = conn.execute("SELECT id, name, email, role, phone, language, created_at FROM users").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_user(user_id):
    conn = get_db()
    conn.execute('DELETE FROM alert_log WHERE device_id IN (SELECT device_id FROM devices WHERE owner_id=?)', (user_id,))
    conn.execute('DELETE FROM sensor_data WHERE device_id IN (SELECT device_id FROM devices WHERE owner_id=?)', (user_id,))
    conn.execute('DELETE FROM access_control WHERE farmer_id=? OR owner_id=?', (user_id, user_id))
    conn.execute('DELETE FROM devices WHERE owner_id=?', (user_id,))
    conn.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()


# ===== DEVICE FUNCTIONS =====

def get_device_by_device_id(device_id):
    conn = get_db()
    row = conn.execute('SELECT * FROM devices WHERE device_id=?', (device_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_devices_by_owner(owner_id):
    conn = get_db()
    rows = conn.execute('SELECT * FROM devices WHERE owner_id=?', (owner_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_devices():
    conn = get_db()
    rows = conn.execute('''
        SELECT d.*, u.name as owner_name
        FROM devices d JOIN users u ON d.owner_id = u.id
    ''').fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_device(device_id, owner_id, name='My Device', location='', auto_registered=0):
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO devices (device_id, owner_id, name, location, auto_registered) VALUES (?, ?, ?, ?, ?)',
            (device_id, owner_id, name, location, auto_registered)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


def remove_device(device_id, owner_id):
    conn = get_db()
    conn.execute('DELETE FROM sensor_data WHERE device_id=?', (device_id,))
    conn.execute('DELETE FROM alert_log WHERE device_id=?', (device_id,))
    conn.execute('DELETE FROM devices WHERE device_id=? AND owner_id=?', (device_id, owner_id))
    conn.commit()
    conn.close()


def admin_remove_device(device_id_str):
    conn = get_db()
    conn.execute('DELETE FROM sensor_data WHERE device_id=?', (device_id_str,))
    conn.execute('DELETE FROM alert_log WHERE device_id=?', (device_id_str,))
    conn.execute('DELETE FROM devices WHERE device_id=?', (device_id_str,))
    conn.commit()
    conn.close()


# ===== SENSOR DATA FUNCTIONS =====

def insert_sensor_data(device_id, temperature, humidity, gas, battery):
    spoilage = calculate_spoilage(temperature, humidity, gas)
    conn = get_db()
    conn.execute(
        '''INSERT INTO sensor_data (device_id, temperature, humidity, gas, battery, spoilage_level, timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (device_id, temperature, humidity, gas, battery, spoilage, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return spoilage


def get_latest_sensor_data(device_id):
    conn = get_db()
    row = conn.execute(
        'SELECT * FROM sensor_data WHERE device_id=? ORDER BY timestamp DESC LIMIT 1',
        (device_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_sensor_history(device_id, limit=50):
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM sensor_data WHERE device_id=? ORDER BY timestamp DESC LIMIT ?',
        (device_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ===== ACCESS CONTROL FUNCTIONS =====

def request_access(farmer_id, owner_id):
    conn = get_db()
    existing = conn.execute(
        'SELECT id FROM access_control WHERE farmer_id=? AND owner_id=? AND status IN ("pending","approved")',
        (farmer_id, owner_id)
    ).fetchone()
    if existing:
        conn.close()
        return False
    conn.execute(
        'INSERT INTO access_control (farmer_id, owner_id, status) VALUES (?, ?, ?)',
        (farmer_id, owner_id, 'pending')
    )
    conn.commit()
    conn.close()
    return True


def get_pending_requests(owner_id):
    conn = get_db()
    rows = conn.execute('''
        SELECT ac.*, u.name as farmer_name, u.email as farmer_email, u.phone as farmer_phone
        FROM access_control ac
        JOIN users u ON ac.farmer_id = u.id
        WHERE ac.owner_id=? AND ac.status='pending'
    ''', (owner_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_approved_farmers(owner_id):
    conn = get_db()
    rows = conn.execute('''
        SELECT ac.*, u.name as farmer_name, u.email as farmer_email
        FROM access_control ac
        JOIN users u ON ac.farmer_id = u.id
        WHERE ac.owner_id=? AND ac.status='approved'
    ''', (owner_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_access_status(request_id, status):
    conn = get_db()
    conn.execute(
        'UPDATE access_control SET status=?, responded_at=? WHERE id=?',
        (status, datetime.now().isoformat(), request_id)
    )
    conn.commit()
    conn.close()


def revoke_access(access_id):
    conn = get_db()
    conn.execute('DELETE FROM access_control WHERE id=?', (access_id,))
    conn.commit()
    conn.close()


def get_farmer_approved_devices(farmer_id):
    conn = get_db()
    rows = conn.execute('''
        SELECT d.*, u.name as owner_name, ac.id as access_id
        FROM access_control ac
        JOIN users u ON ac.owner_id = u.id
        JOIN devices d ON d.owner_id = ac.owner_id
        WHERE ac.farmer_id=? AND ac.status='approved'
    ''', (farmer_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_farmer_requests(farmer_id):
    conn = get_db()
    rows = conn.execute('''
        SELECT ac.*, u.name as owner_name, u.email as owner_email
        FROM access_control ac
        JOIN users u ON ac.owner_id = u.id
        WHERE ac.farmer_id=?
        ORDER BY ac.requested_at DESC
    ''', (farmer_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_owners():
    conn = get_db()
    rows = conn.execute("SELECT id, name, email FROM users WHERE role='owner'").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ===== ALERT FUNCTIONS =====

def can_send_alert(device_id, cooldown_minutes=15):
    conn = get_db()
    row = conn.execute(
        '''SELECT sent_at FROM alert_log
           WHERE device_id=? AND alert_type='HIGH_SPOILAGE'
           ORDER BY sent_at DESC LIMIT 1''',
        (device_id,)
    ).fetchone()
    conn.close()
    if not row:
        return True
    try:
        last_sent = datetime.fromisoformat(row['sent_at'])
        diff = (datetime.now() - last_sent).total_seconds() / 60
        return diff >= cooldown_minutes
    except Exception:
        return True


def log_alert(device_id, alert_type, message=''):
    conn = get_db()
    conn.execute(
        'INSERT INTO alert_log (device_id, alert_type, message, sent_at) VALUES (?, ?, ?, ?)',
        (device_id, alert_type, message, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_first_owner_id():
    conn = get_db()
    row = conn.execute("SELECT id FROM users WHERE role='owner' ORDER BY id LIMIT 1").fetchone()
    conn.close()
    return row['id'] if row else None
