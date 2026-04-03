"""
Kishan Kavach - Database Models
Single Device System - No device_id anywhere
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model - Farmer or Warehouse Owner only"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='farmer')
    # farmer: needs approval | owner: full access
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class AccessRequest(db.Model):
    """Farmer access requests to Warehouse Owner"""
    __tablename__ = 'access_requests'

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    # pending | approved | rejected
    message = db.Column(db.Text, default='')
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime, nullable=True)

    farmer = db.relationship('User', backref='access_requests')


class SensorData(db.Model):
    """
    Real sensor data from ESP32
    NO device_id - Single device system
    """
    __tablename__ = 'sensor_data'

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    gas = db.Column(db.Float, nullable=False)
    battery = db.Column(db.Float, default=0.0)
    crop = db.Column(db.String(100), default='unknown')

    # AI computed fields
    health_score = db.Column(db.Float, default=0.0)
    risk_level = db.Column(db.String(20), default='unknown')
    days_remaining = db.Column(db.Integer, default=0)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'gas': self.gas,
            'battery': self.battery,
            'crop': self.crop,
            'health_score': self.health_score,
            'risk_level': self.risk_level,
            'days_remaining': self.days_remaining,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


class AlertLog(db.Model):
    """Alert history - only for HIGH risk real events"""
    __tablename__ = 'alert_logs'

    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    sensor_data_id = db.Column(db.Integer, db.ForeignKey('sensor_data.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'alert_type': self.alert_type,
            'message': self.message,
            'risk_level': self.risk_level,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
