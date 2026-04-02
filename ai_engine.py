"""
Kishan Kavach - AI Spoilage Prediction Engine
Rule-based + Smart Logic (Lightweight & Explainable)
"""

from crop_data import get_crop_info, CROP_DATABASE
from datetime import datetime


class AIEngine:
    """
    Multi-factor AI scoring engine for crop spoilage prediction.
    
    Weight System:
    - Temperature: 40%
    - Humidity: 30%
    - Gas Level: 30%
    """

    TEMP_WEIGHT = 0.40
    HUMIDITY_WEIGHT = 0.30
    GAS_WEIGHT = 0.30

    @staticmethod
    def get_spoilage_risk(temperature, humidity, gas):
        """Base spoilage risk classification"""
        if temperature > 30 or humidity > 80 or gas > 400:
            return 'HIGH'
        elif temperature > 25 or humidity > 70 or gas > 300:
            return 'MEDIUM'
        else:
            return 'LOW'

    @staticmethod
    def calculate_temp_score(temp, crop_info):
        """Calculate temperature deviation score (0-100)"""
        if crop_info is None:
            if temp <= 25:
                return 100
            elif temp <= 30:
                return 70
            elif temp <= 35:
                return 40
            else:
                return 10

        ideal_min = crop_info['temp_min']
        ideal_max = crop_info['temp_max']
        ideal_mid = (ideal_min + ideal_max) / 2
        ideal_range = (ideal_max - ideal_min) / 2

        if ideal_min <= temp <= ideal_max:
            return 100
        else:
            deviation = 0
            if temp < ideal_min:
                deviation = ideal_min - temp
            else:
                deviation = temp - ideal_max

            max_tolerable = max(ideal_range * 3, 15)
            score = max(0, 100 - (deviation / max_tolerable) * 100)
            return round(score, 1)

    @staticmethod
    def calculate_humidity_score(humidity, crop_info):
        """Calculate humidity deviation score (0-100)"""
        if crop_info is None:
            if humidity <= 70:
                return 100
            elif humidity <= 80:
                return 70
            elif humidity <= 90:
                return 40
            else:
                return 10

        ideal_min = crop_info['humidity_min']
        ideal_max = crop_info['humidity_max']

        if ideal_min <= humidity <= ideal_max:
            return 100
        else:
            deviation = 0
            if humidity < ideal_min:
                deviation = ideal_min - humidity
            else:
                deviation = humidity - ideal_max

            max_tolerable = 30
            score = max(0, 100 - (deviation / max_tolerable) * 100)
            return round(score, 1)

    @staticmethod
    def calculate_gas_score(gas, crop_info):
        """Calculate gas level score (0-100)"""
        gas_thresholds = {
            'Ethylene': {'safe': 150, 'warning': 300, 'danger': 500},
            'CO2': {'safe': 200, 'warning': 400, 'danger': 600},
            'Ammonia': {'safe': 100, 'warning': 250, 'danger': 400},
            'SO2': {'safe': 50, 'warning': 150, 'danger': 300},
        }

        gas_type = crop_info['harmful_gas'] if crop_info else 'CO2'
        thresholds = gas_thresholds.get(gas_type, gas_thresholds['CO2'])

        if gas <= thresholds['safe']:
            return 100
        elif gas <= thresholds['warning']:
            ratio = (gas - thresholds['safe']) / (thresholds['warning'] - thresholds['safe'])
            return round(100 - ratio * 40, 1)
        elif gas <= thresholds['danger']:
            ratio = (gas - thresholds['warning']) / (thresholds['danger'] - thresholds['warning'])
            return round(60 - ratio * 40, 1)
        else:
            over = gas - thresholds['danger']
            max_over = thresholds['danger']
            score = max(0, 20 - (over / max_over) * 20)
            return round(score, 1)

    @classmethod
    def calculate_health_score(cls, temperature, humidity, gas, crop_key=None):
        """
        Calculate overall health score (0-100) using weighted multi-factor scoring.
        """
        crop_info = get_crop_info(crop_key) if crop_key else None

        temp_score = cls.calculate_temp_score(temperature, crop_info)
        humidity_score = cls.calculate_humidity_score(humidity, crop_info)
        gas_score = cls.calculate_gas_score(gas, crop_info)

        health_score = (
            temp_score * cls.TEMP_WEIGHT +
            humidity_score * cls.HUMIDITY_WEIGHT +
            gas_score * cls.GAS_WEIGHT
        )

        return round(min(100, max(0, health_score)), 1)

    @classmethod
    def calculate_days_remaining(cls, health_score, crop_key=None):
        """
        Estimate days remaining based on health score and shelf life.
        """
        crop_info = get_crop_info(crop_key) if crop_key else None
        base_shelf_life = crop_info['shelf_life'] if crop_info else 30

        quality_factor = health_score / 100.0

        if quality_factor >= 0.9:
            days = base_shelf_life * 1.0
        elif quality_factor >= 0.7:
            days = base_shelf_life * 0.7
        elif quality_factor >= 0.5:
            days = base_shelf_life * 0.4
        elif quality_factor >= 0.3:
            days = base_shelf_life * 0.2
        else:
            days = base_shelf_life * 0.05

        return round(max(0.5, days), 1)

    @staticmethod
    def predict_future_risk(history_data):
        """
        Predict future risk based on trend analysis.
        
        Logic:
        - If temperature is rising → increasing risk
        - If gas is rising → sharp risk increase
        - If stable → maintain current
        """
        if not history_data or len(history_data) < 3:
            return 'LOW', 'stable'

        recent = history_data[:min(10, len(history_data))]
        recent.reverse()

        temps = [r['temperature'] for r in recent if r.get('temperature') is not None]
        gases = [r['gas'] for r in recent if r.get('gas') is not None]

        temp_trend = 'stable'
        gas_trend = 'stable'

        if len(temps) >= 3:
            temp_diffs = [temps[i+1] - temps[i] for i in range(len(temps)-1)]
            avg_temp_diff = sum(temp_diffs) / len(temp_diffs)
            if avg_temp_diff > 0.5:
                temp_trend = 'rising'
            elif avg_temp_diff < -0.5:
                temp_trend = 'falling'

        if len(gases) >= 3:
            gas_diffs = [gases[i+1] - gases[i] for i in range(len(gases)-1)]
            avg_gas_diff = sum(gas_diffs) / len(gas_diffs)
            if avg_gas_diff > 10:
                gas_trend = 'rising'
            elif avg_gas_diff < -10:
                gas_trend = 'falling'

        if temp_trend == 'rising' and gas_trend == 'rising':
            risk = 'HIGH'
            trend = 'deteriorating'
        elif temp_trend == 'rising' or gas_trend == 'rising':
            risk = 'MEDIUM'
            trend = 'declining'
        elif temp_trend == 'falling' and gas_trend == 'falling':
            risk = 'LOW'
            trend = 'improving'
        else:
            risk = 'LOW'
            trend = 'stable'

        return risk, trend

    @staticmethod
    def get_condition(health_score):
        """Get human-readable condition string"""
        if health_score >= 80:
            return 'Safe'
        elif health_score >= 60:
            return 'Good'
        elif health_score >= 40:
            return 'Risky'
        elif health_score >= 20:
            return 'Critical'
        else:
            return 'Spoiled'

    @classmethod
    def get_recommendations(cls, temperature, humidity, gas, crop_key=None):
        """Generate actionable storage recommendations"""
        crop_info = get_crop_info(crop_key) if crop_key else None
        recommendations = []

        if crop_info:
            if temperature > crop_info['temp_max']:
                diff = temperature - crop_info['temp_max']
                recommendations.append(
                    f"🌡 Reduce temperature by {diff:.1f}°C. "
                    f"Ideal: {crop_info['temp_min']}–{crop_info['temp_max']}°C"
                )
            elif temperature < crop_info['temp_min']:
                diff = crop_info['temp_min'] - temperature
                recommendations.append(
                    f"🌡 Increase temperature by {diff:.1f}°C. "
                    f"Ideal: {crop_info['temp_min']}–{crop_info['temp_max']}°C"
                )
            else:
                recommendations.append("🌡 Temperature is within ideal range ✓")

            if humidity > crop_info['humidity_max']:
                recommendations.append(
                    f"💧 Reduce humidity. "
                    f"Ideal: {crop_info['humidity_min']}–{crop_info['humidity_max']}%"
                )
            elif humidity < crop_info['humidity_min']:
                recommendations.append(
                    f"💧 Increase humidity. "
                    f"Ideal: {crop_info['humidity_min']}–{crop_info['humidity_max']}%"
                )
            else:
                recommendations.append("💧 Humidity is within ideal range ✓")
        else:
            if temperature > 25:
                recommendations.append("🌡 Temperature too high. Cool storage recommended.")
            if humidity > 75:
                recommendations.append("💧 Humidity too high. Improve ventilation.")

        if gas > 400:
            recommendations.append("💨 CRITICAL: Gas levels dangerous! Immediate ventilation required.")
        elif gas > 300:
            recommendations.append("💨 WARNING: Gas levels elevated. Improve ventilation.")
        elif gas > 200:
            recommendations.append("💨 Gas levels slightly high. Monitor closely.")
        else:
            recommendations.append("💨 Gas levels normal ✓")

        return recommendations

    @classmethod
    def full_analysis(cls, temperature, humidity, gas, crop_key=None, history=None):
        """
        Complete AI analysis of sensor data.
        Returns comprehensive analysis dictionary.
        """
        health_score = cls.calculate_health_score(temperature, humidity, gas, crop_key)
        spoilage_risk = cls.get_spoilage_risk(temperature, humidity, gas)
        days_remaining = cls.calculate_days_remaining(health_score, crop_key)
        future_risk, trend = cls.predict_future_risk(history or [])
        condition = cls.get_condition(health_score)
        recommendations = cls.get_recommendations(temperature, humidity, gas, crop_key)

        crop_info = get_crop_info(crop_key)

        if crop_info:
            if health_score < 50:
                spoilage_risk = 'HIGH'
            elif health_score < 70:
                spoilage_risk = max(spoilage_risk, 'MEDIUM')

        return {
            'health_score': health_score,
            'spoilage_risk': spoilage_risk,
            'days_remaining': days_remaining,
            'future_risk': future_risk,
            'trend': trend,
            'condition': condition,
            'recommendations': recommendations,
            'crop_info': crop_info,
            'scores': {
                'temperature': cls.calculate_temp_score(temperature, crop_info),
                'humidity': cls.calculate_humidity_score(humidity, crop_info),
                'gas': cls.calculate_gas_score(gas, crop_info)
            }
        }

    @classmethod
    def generate_prediction_data(cls, current_temp, current_humidity, current_gas, 
                                  trend='stable', days=7):
        """
        Generate prediction data points for chart visualization.
        """
        predictions = {
            'labels': [],
            'temperature': [],
            'humidity': [],
            'gas': [],
            'health_score': []
        }

        temp_delta = 0
        gas_delta = 0
        humidity_delta = 0

        if trend == 'deteriorating':
            temp_delta = 1.5
            gas_delta = 25
            humidity_delta = 2
        elif trend == 'declining':
            temp_delta = 0.8
            gas_delta = 15
            humidity_delta = 1
        elif trend == 'improving':
            temp_delta = -0.5
            gas_delta = -10
            humidity_delta = -0.5
        else:
            temp_delta = 0.2
            gas_delta = 5
            humidity_delta = 0.3

        for day in range(days):
            predictions['labels'].append(f'Day {day + 1}')
            pred_temp = current_temp + (temp_delta * (day + 1))
            pred_humidity = min(100, max(0, current_humidity + (humidity_delta * (day + 1))))
            pred_gas = max(0, current_gas + (gas_delta * (day + 1)))

            predictions['temperature'].append(round(pred_temp, 1))
            predictions['humidity'].append(round(pred_humidity, 1))
            predictions['gas'].append(round(pred_gas, 1))

            score = cls.calculate_health_score(pred_temp, pred_humidity, pred_gas)
            predictions['health_score'].append(score)

        return predictions

    @classmethod
    def generate_spoilage_timeline(cls, health_score, days_remaining, crop_key=None):
        """Generate timeline showing spoilage progression"""
        timeline = []
        crop_info = get_crop_info(crop_key)
        shelf_life = crop_info['shelf_life'] if crop_info else 30

        if health_score >= 80:
            timeline.append({'day': 0, 'status': 'Fresh', 'color': '#00ff88'})
            timeline.append({'day': int(days_remaining * 0.3), 'status': 'Good', 'color': '#88ff00'})
            timeline.append({'day': int(days_remaining * 0.6), 'status': 'Aging', 'color': '#ffaa00'})
            timeline.append({'day': int(days_remaining * 0.85), 'status': 'Risky', 'color': '#ff6600'})
            timeline.append({'day': int(days_remaining), 'status': 'Spoiled', 'color': '#ff0000'})
        elif health_score >= 50:
            timeline.append({'day': 0, 'status': 'Aging', 'color': '#ffaa00'})
            timeline.append({'day': int(days_remaining * 0.4), 'status': 'Risky', 'color': '#ff6600'})
            timeline.append({'day': int(days_remaining), 'status': 'Spoiled', 'color': '#ff0000'})
        else:
            timeline.append({'day': 0, 'status': 'Critical', 'color': '#ff3300'})
            timeline.append({'day': int(days_remaining), 'status': 'Spoiled', 'color': '#ff0000'})

        return timeline
