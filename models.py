"""
Models for Kishan Kavach
Data classes and structures used throughout the application
"""

from datetime import datetime


class SensorReading:
    def __init__(self, device_id, temperature, humidity, gas, battery=100, crop='wheat'):
        self.device_id = device_id
        self.temperature = float(temperature)
        self.humidity = float(humidity)
        self.gas = float(gas)
        self.battery = float(battery)
        self.crop = crop
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            'device_id': self.device_id,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'gas': self.gas,
            'battery': self.battery,
            'crop': self.crop,
            'timestamp': self.timestamp.isoformat()
        }


class AIAnalysis:
    def __init__(self):
        self.health_score = 100
        self.spoilage_risk = 'LOW'
        self.days_remaining = 30
        self.future_risk = 'LOW'
        self.recommendations = []
        self.condition = 'Safe'
        self.trend = 'stable'

    def to_dict(self):
        return {
            'health_score': self.health_score,
            'spoilage_risk': self.spoilage_risk,
            'days_remaining': self.days_remaining,
            'future_risk': self.future_risk,
            'recommendations': self.recommendations,
            'condition': self.condition,
            'trend': self.trend
        }


class CropProfile:
    def __init__(self, name, temp_min, temp_max, humidity_min, humidity_max,
                 harmful_gas, shelf_life, category='vegetable'):
        self.name = name
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.humidity_min = humidity_min
        self.humidity_max = humidity_max
        self.harmful_gas = harmful_gas
        self.shelf_life = shelf_life
        self.category = category

    def to_dict(self):
        return {
            'name': self.name,
            'temp_min': self.temp_min,
            'temp_max': self.temp_max,
            'humidity_min': self.humidity_min,
            'humidity_max': self.humidity_max,
            'harmful_gas': self.harmful_gas,
            'shelf_life': self.shelf_life,
            'category': self.category
        }


"""
=== FUTURE SCOPE: Deep Learning Architecture ===

For future upgrades, an LSTM-based model can be integrated:

Architecture:
- Input: Time series of (temperature, humidity, gas) - last 48 hours
- LSTM Layer 1: 64 units, return_sequences=True
- LSTM Layer 2: 32 units
- Dense Layer: 16 units, ReLU
- Output Layer: 
  - Regression head: predicted values for next 5 days
  - Classification head: spoilage probability

Training:
- Dataset: Historical sensor readings with spoilage labels
- Loss: MSE for regression, Binary Cross-Entropy for classification
- Optimizer: Adam, lr=0.001

Capabilities:
1. Predict next 5 days of temperature, humidity, gas
2. Predict spoilage trend with confidence scores
3. Forecast temperature changes and recommend actions
4. Anomaly detection in sensor readings

Integration:
- Model saved as TensorFlow Lite for edge deployment
- Can run on ESP32 with TFLite Micro
- Server-side inference via Flask endpoint

Note: This is NOT implemented in current version.
Current system uses rule-based AI which is lightweight and explainable.
"""
