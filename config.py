"""
Kishan Kavach - Configuration
Single Device | Real Data Only | Production Ready
"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'kishan-kavach-secret-key-2024')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///kishan_kavach.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Weather API (OpenWeatherMap)
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')
    WEATHER_CITY = os.environ.get('WEATHER_CITY', 'Delhi')

    # Alert cooldown in seconds
    ALERT_COOLDOWN = 300  # 5 minutes

    # Data validation thresholds
    MIN_VALID_TEMP = -10
    MAX_VALID_TEMP = 80
    MIN_VALID_HUMIDITY = 0
    MAX_VALID_HUMIDITY = 100
    MIN_VALID_GAS = 0
    MAX_VALID_GAS = 10000
