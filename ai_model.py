import joblib

model = joblib.load("spoilage_model.pkl")

def predict_spoilage(temp, humidity, gas):
    pred = model.predict([[temp, humidity, gas]])[0]

    if pred == 0:
        return "LOW"
    elif pred == 1:
        return "MEDIUM"
    else:
        return "HIGH"
