from crop_data import CROP_DATA
from datetime import datetime, timedelta

def analyze_crop(crop, temp, humidity, gas):

    data = CROP_DATA.get(crop)

    if not data:
        return {"error": "Crop not found"}

    score = 100

    # Temperature check
    if temp < data["temp_min"] or temp > data["temp_max"]:
        score -= 30

    # Humidity check
    if humidity < data["humidity_min"] or humidity > data["humidity_max"]:
        score -= 30

    # Gas effect
    if gas > 400:
        score -= 40

    # Days remaining
    days = int((score / 100) * data["shelf_life_days"])

    return {
        "health_score": score,
        "days_remaining": days,
        "ideal_temp": f"{data['temp_min']} - {data['temp_max']} °C",
        "ideal_humidity": f"{data['humidity_min']} - {data['humidity_max']} %",
        "gas_risk": data["gas"]
    }
