"""
Kishan Kavach - AI Spoilage Prediction Engine
Works ONLY on real sensor data — NO fake predictions
"""
from crop_data import get_crop_info


class SpoilageAI:
    """Rule-based AI engine for crop spoilage prediction"""

    @staticmethod
    def analyze(temperature, humidity, gas, crop_key='unknown'):
        """
        Analyze REAL sensor data and return AI insights.
        Returns None if data is invalid.
        """
        # === VALIDATE REAL DATA ===
        if temperature is None or humidity is None or gas is None:
            return None

        if temperature == 0 and humidity == 0 and gas == 0:
            return None  # Likely invalid/disconnected sensor

        # Get crop-specific thresholds
        crop_info = get_crop_info(crop_key) if crop_key != 'unknown' else None

        # === DETERMINE RISK LEVEL ===
        risk_level, risk_score = SpoilageAI._calculate_risk(
            temperature, humidity, gas, crop_info
        )

        # === CALCULATE HEALTH SCORE (0-100) ===
        health_score = SpoilageAI._calculate_health(
            temperature, humidity, gas, crop_info
        )

        # === ESTIMATE DAYS REMAINING ===
        days_remaining = SpoilageAI._estimate_days(
            risk_score, crop_info
        )

        # === FUTURE RISK PREDICTION ===
        future_risk = SpoilageAI._predict_future_risk(
            temperature, humidity, gas, risk_level
        )

        # === GENERATE RECOMMENDATION ===
        recommendation = SpoilageAI._generate_recommendation(
            temperature, humidity, gas, crop_info, risk_level
        )

        # === IDEAL CONDITIONS ===
        ideal_temp = crop_info['ideal_temp'] if crop_info else (15, 25)
        ideal_humidity = crop_info['ideal_humidity'] if crop_info else (55, 70)

        return {
            'health_score': round(health_score, 1),
            'risk_level': risk_level,
            'days_remaining': days_remaining,
            'future_risk': future_risk,
            'recommendation': recommendation,
            'ideal_temp': f"{ideal_temp[0]}°C - {ideal_temp[1]}°C",
            'ideal_humidity': f"{ideal_humidity[0]}% - {ideal_humidity[1]}%",
            'crop_name': crop_info['name'] if crop_info else 'Unknown Crop',
            'shelf_life': crop_info['shelf_life_days'] if crop_info else 0
        }

    @staticmethod
    def _calculate_risk(temp, humidity, gas, crop_info):
        """Calculate risk level based on sensor data and crop thresholds"""
        score = 0

        if crop_info:
            ideal_t = crop_info['ideal_temp']
            ideal_h = crop_info['ideal_humidity']
            gas_threshold = crop_info['gas_risk_threshold']

            # Temperature deviation
            if temp < ideal_t[0]:
                score += min((ideal_t[0] - temp) * 3, 30)
            elif temp > ideal_t[1]:
                score += min((temp - ideal_t[1]) * 4, 40)

            # Humidity deviation
            if humidity < ideal_h[0]:
                score += min((ideal_h[0] - humidity) * 2, 20)
            elif humidity > ideal_h[1]:
                score += min((humidity - ideal_h[1]) * 3, 30)

            # Gas level
            if gas > gas_threshold:
                score += min((gas - gas_threshold) * 0.1, 30)
            elif gas > gas_threshold * 0.7:
                score += 10

        else:
            # Generic thresholds (no crop selected)
            if temp > 35:
                score += 35
            elif temp > 30:
                score += 25
            elif temp > 25:
                score += 15

            if humidity > 85:
                score += 30
            elif humidity > 80:
                score += 20

            if gas > 400:
                score += 35
            elif gas > 300:
                score += 20

        # Determine level
        if score >= 50:
            return 'HIGH', score
        elif score >= 25:
            return 'MEDIUM', score
        else:
            return 'LOW', score

    @staticmethod
    def _calculate_health(temp, humidity, gas, crop_info):
        """Calculate health score 0-100"""
        score = 100.0

        if crop_info:
            ideal_t = crop_info['ideal_temp']
            ideal_h = crop_info['ideal_humidity']
            gas_threshold = crop_info['gas_risk_threshold']

            # Temperature penalty
            mid_t = (ideal_t[0] + ideal_t[1]) / 2
            temp_diff = abs(temp - mid_t)
            score -= min(temp_diff * 2.5, 35)

            # Humidity penalty
            mid_h = (ideal_h[0] + ideal_h[1]) / 2
            hum_diff = abs(humidity - mid_h)
            score -= min(hum_diff * 1.5, 30)

            # Gas penalty
            if gas > gas_threshold:
                score -= min((gas - gas_threshold) * 0.08, 35)
            elif gas > gas_threshold * 0.7:
                score -= 5

        else:
            if temp > 30:
                score -= (temp - 30) * 3
            if humidity > 80:
                score -= (humidity - 80) * 2
            if gas > 300:
                score -= (gas - 300) * 0.1

        return max(0, min(100, score))

    @staticmethod
    def _estimate_days(risk_score, crop_info):
        """Estimate days remaining before spoilage"""
        if crop_info:
            base_days = crop_info['shelf_life_days']
        else:
            base_days = 30  # Generic default

        if risk_score >= 50:
            factor = 0.15
        elif risk_score >= 25:
            factor = 0.5
        else:
            factor = 0.85

        return max(1, int(base_days * factor))

    @staticmethod
    def _predict_future_risk(temp, humidity, gas, current_risk):
        """Predict future risk trend"""
        danger_signals = 0

        if temp > 28:
            danger_signals += 1
        if humidity > 75:
            danger_signals += 1
        if gas > 350:
            danger_signals += 1

        if current_risk == 'HIGH':
            return 'CRITICAL — Immediate action needed'
        elif danger_signals >= 2:
            return 'INCREASING — Conditions deteriorating'
        elif danger_signals == 1:
            return 'MODERATE — Monitor closely'
        else:
            return 'STABLE — Conditions acceptable'

    @staticmethod
    def _generate_recommendation(temp, humidity, gas, crop_info, risk_level):
        """Generate actionable recommendation"""
        recommendations = []

        if crop_info:
            ideal_t = crop_info['ideal_temp']
            ideal_h = crop_info['ideal_humidity']

            if temp > ideal_t[1]:
                recommendations.append(
                    f"🌡️ Temperature too HIGH ({temp}°C). "
                    f"Reduce to {ideal_t[0]}-{ideal_t[1]}°C immediately."
                )
            elif temp < ideal_t[0]:
                recommendations.append(
                    f"🌡️ Temperature too LOW ({temp}°C). "
                    f"Increase to {ideal_t[0]}-{ideal_t[1]}°C."
                )

            if humidity > ideal_h[1]:
                recommendations.append(
                    f"💧 Humidity too HIGH ({humidity}%). "
                    f"Improve ventilation. Target: {ideal_h[0]}-{ideal_h[1]}%."
                )
            elif humidity < ideal_h[0]:
                recommendations.append(
                    f"💧 Humidity too LOW ({humidity}%). "
                    f"Add moisture. Target: {ideal_h[0]}-{ideal_h[1]}%."
                )

            gas_threshold = crop_info['gas_risk_threshold']
            if gas > gas_threshold:
                recommendations.append(
                    f"⚠️ Gas level DANGEROUS ({gas} ppm). "
                    f"Check for spoilage. Max safe: {gas_threshold} ppm."
                )

        else:
            if temp > 30:
                recommendations.append(f"🌡️ High temperature ({temp}°C). Cool the storage.")
            if humidity > 80:
                recommendations.append(f"💧 High humidity ({humidity}%). Improve ventilation.")
            if gas > 400:
                recommendations.append(f"⚠️ High gas ({gas} ppm). Inspect for spoilage.")

        if risk_level == 'HIGH':
            recommendations.insert(0, "🚨 CRITICAL: Take immediate action to prevent crop loss!")

        if not recommendations:
            recommendations.append("✅ All conditions are within safe range. Keep monitoring.")

        return ' | '.join(recommendations)
